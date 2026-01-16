"""
Paper Writer Agent

Generates academic paper drafts from experiment results.
Uses NeurIPS style by default.
"""

from pathlib import Path
from typing import Dict, Any
import subprocess
import shlex
import os

CLI_COMMANDS = {
    'claude': 'claude -p',
    'codex': 'codex exec',
    'gemini': 'gemini'
}


def generate_paper_writer_prompt(
    work_dir: Path,
    style: str = "neurips"
) -> str:
    """
    Generate prompt for paper writing agent.

    Args:
        work_dir: Workspace directory with experiment results
        style: Paper style (neurips, icml, acl)

    Returns:
        Complete prompt string for paper writing
    """
    # Load experiment results
    report_path = work_dir / "REPORT.md"
    planning_path = work_dir / "planning.md"
    lit_review_path = work_dir / "literature_review.md"

    report_content = report_path.read_text() if report_path.exists() else "No REPORT.md found"
    planning_content = planning_path.read_text() if planning_path.exists() else "No planning.md found"
    lit_review_content = lit_review_path.read_text() if lit_review_path.exists() else "No literature_review.md found"

    return f'''You are an academic paper writer. Generate a complete {style.upper()} style paper
based on the experiment results provided.

════════════════════════════════════════════════════════════════════════════════
                            EXPERIMENT REPORT
════════════════════════════════════════════════════════════════════════════════

{report_content}

════════════════════════════════════════════════════════════════════════════════
                            RESEARCH PLAN
════════════════════════════════════════════════════════════════════════════════

{planning_content}

════════════════════════════════════════════════════════════════════════════════
                          LITERATURE REVIEW
════════════════════════════════════════════════════════════════════════════════

{lit_review_content}

════════════════════════════════════════════════════════════════════════════════
                          PAPER REQUIREMENTS
════════════════════════════════════════════════════════════════════════════════

Generate a complete academic paper with the following structure:

1. TITLE
   - Clear, specific, informative
   - Should convey main finding or contribution

2. ABSTRACT (150-250 words)
   - Problem statement
   - Approach
   - Key results
   - Significance

3. INTRODUCTION
   - Research problem and motivation
   - Gap in existing work
   - Our contribution (be specific)
   - Paper organization

4. RELATED WORK
   - Organized by theme/approach
   - Position our work relative to prior work
   - Cite papers from literature review

5. METHODOLOGY
   - Clear description of approach
   - Experimental setup
   - Datasets used
   - Evaluation metrics
   - Baselines

6. RESULTS
   - Present results with tables and figures
   - Statistical analysis
   - Comparison to baselines
   - Ablation studies (if applicable)

7. DISCUSSION
   - Interpretation of results
   - Limitations
   - Broader implications

8. CONCLUSION
   - Summary of contributions
   - Key findings
   - Future work

9. REFERENCES
   - BibTeX format
   - All cited papers

OUTPUT FORMAT:
- Write in LaTeX format
- Use NeurIPS style (\\documentclass[final]{{neurips_2025}})
- Include all necessary packages
- Save as paper/main.tex
- Save references as paper/references.bib

QUALITY REQUIREMENTS:
- Academic tone throughout
- Claims supported by data
- Proper citations
- Clear figures and tables
- No placeholder text
'''


def run_paper_writer(
    work_dir: Path,
    provider: str = "claude",
    style: str = "neurips",
    timeout: int = 3600,
    full_permissions: bool = True
) -> Dict[str, Any]:
    """
    Run paper writing agent.

    Args:
        work_dir: Workspace with experiment results
        provider: AI provider (claude, codex, gemini)
        style: Paper style (neurips, icml, acl)
        timeout: Execution timeout in seconds
        full_permissions: Skip permission prompts

    Returns:
        Result dictionary with success status and paths
    """
    print(f"📝 Starting Paper Writer Agent")
    print(f"   Style: {style}")
    print(f"   Provider: {provider}")
    print(f"   Workspace: {work_dir}")

    # Create paper draft directory
    draft_dir = work_dir / "paper_draft"
    draft_dir.mkdir(exist_ok=True)

    # Copy style files
    _copy_style_files(draft_dir, style)

    # Generate prompt
    prompt = generate_paper_writer_prompt(work_dir, style)

    # Save prompt for debugging
    logs_dir = work_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    (logs_dir / "paper_writer_prompt.txt").write_text(prompt)

    # Build command
    cmd = CLI_COMMANDS.get(provider, 'claude -p')
    if full_permissions:
        if provider == "codex":
            cmd += " --yolo"
        elif provider == "claude":
            cmd += " --dangerously-skip-permissions"
        elif provider == "gemini":
            cmd += " --yolo"

    # Add streaming JSON output flags for detailed logging
    if provider == "claude":
        cmd += " --verbose --output-format stream-json"
    elif provider == "codex":
        cmd += " --json"
    elif provider == "gemini":
        cmd += " --output-format stream-json"

    # Execute
    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'

    log_file = logs_dir / f"paper_writer_{provider}.log"

    try:
        with open(log_file, 'w') as log_f:
            process = subprocess.Popen(
                shlex.split(cmd),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
                text=True,
                cwd=str(work_dir)
            )

            process.stdin.write(prompt)
            process.stdin.close()

            for line in iter(process.stdout.readline, ''):
                if line:
                    print(line, end='')
                    log_f.write(line)

            return_code = process.wait(timeout=timeout)

        success = return_code == 0
        if success:
            print(f"\n✅ Paper generated successfully!")
            print(f"   Output: {draft_dir}/main.tex")
        else:
            print(f"\n❌ Paper generation failed with code {return_code}")

        return {
            'success': success,
            'draft_dir': str(draft_dir),
            'log_file': str(log_file),
            'return_code': return_code
        }

    except subprocess.TimeoutExpired:
        process.kill()
        print(f"\n⏰ Paper generation timed out after {timeout}s")
        return {
            'success': False,
            'draft_dir': str(draft_dir),
            'log_file': str(log_file),
            'error': 'timeout'
        }
    except Exception as e:
        print(f"\n❌ Error running paper writer: {e}")
        return {
            'success': False,
            'draft_dir': str(draft_dir),
            'log_file': str(log_file),
            'error': str(e)
        }


def _copy_style_files(draft_dir: Path, style: str):
    """Copy LaTeX style files to paper draft directory."""
    import shutil

    # Style files location - look for Styles subfolder with official files
    styles_dir = Path(__file__).parent.parent.parent / "templates" / "paper_styles"
    style_dir = styles_dir / style / "Styles"

    # Fallback to direct style directory if Styles subfolder doesn't exist
    if not style_dir.exists():
        style_dir = styles_dir / style

    if style_dir.exists():
        for f in style_dir.glob("*"):
            if f.is_file():
                shutil.copy(f, draft_dir)
        print(f"   Copied {style} style files to {draft_dir}")
    else:
        print(f"   Warning: Style directory {style_dir} not found")
        print(f"   Creating minimal template...")
        _create_minimal_template(draft_dir, style)


def _create_minimal_template(draft_dir: Path, style: str):
    """Create minimal LaTeX template if style files not found."""
    template = r"""\documentclass[final]{neurips_2025}

\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{hyperref}
\usepackage{natbib}

\title{Paper Title Here}

\author{
  Author Name \\
  Institution \\
  \texttt{email@example.com}
}

\begin{document}

\maketitle

\begin{abstract}
Abstract goes here.
\end{abstract}

\section{Introduction}
Introduction goes here.

\section{Related Work}
Related work goes here.

\section{Method}
Method goes here.

\section{Experiments}
Experiments go here.

\section{Results}
Results go here.

\section{Conclusion}
Conclusion goes here.

\bibliography{references}
\bibliographystyle{plainnat}

\end{document}
"""
    (draft_dir / "main.tex").write_text(template)
    (draft_dir / "references.bib").write_text("% BibTeX references go here\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate academic paper from experiment results")
    parser.add_argument("work_dir", type=Path, help="Workspace directory with experiment results")
    parser.add_argument("--provider", default="claude", choices=["claude", "codex", "gemini"])
    parser.add_argument("--style", default="neurips", choices=["neurips", "icml", "acl"])
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--no-permissions", action="store_true", help="Require permission prompts")

    args = parser.parse_args()

    result = run_paper_writer(
        work_dir=args.work_dir,
        provider=args.provider,
        style=args.style,
        timeout=args.timeout,
        full_permissions=not args.no_permissions
    )

    exit(0 if result['success'] else 1)
