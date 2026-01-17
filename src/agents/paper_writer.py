"""
Paper Writer Agent

Generates academic paper drafts from experiment results.
The agent handles LaTeX file creation and compilation.
Style files are copied from templates/paper_styles/ to the workspace.
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

    This is a convenience wrapper that uses PromptGenerator internally.
    The actual prompt template is stored in templates/agents/paper_writer.txt.

    Args:
        work_dir: Workspace directory with experiment results
        style: Paper style (neurips, icml, acl)

    Returns:
        Complete prompt string for paper writing
    """
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from templates.prompt_generator import PromptGenerator

    generator = PromptGenerator()
    return generator.generate_paper_writer_prompt(work_dir, style)


def _copy_style_files(draft_dir: Path, style: str):
    """
    Copy LaTeX style files to paper draft directory.

    The agent runs in a separate workspace without access to idea-explorer's
    templates, so we copy the style files (e.g., neurips_2025.sty) there.

    Args:
        draft_dir: Directory where paper will be written
        style: Paper style (neurips, icml, acl)
    """
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
        print(f"   Agent will need to create paper without template style files")


def run_paper_writer(
    work_dir: Path,
    provider: str = "claude",
    style: str = "neurips",
    timeout: int = 3600,
    full_permissions: bool = True
) -> Dict[str, Any]:
    """
    Run paper writing agent.

    The agent handles all aspects of paper generation:
    - Creating directory structure (paper_draft/sections/, figures/, etc.)
    - Writing LaTeX files
    - Compiling to PDF

    Style files are copied to the workspace before the agent runs.

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

    # Create paper draft directory and copy style files
    draft_dir = work_dir / "paper_draft"
    draft_dir.mkdir(exist_ok=True)
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
            print(f"\n✅ Paper writer agent completed!")
            print(f"   Output directory: {draft_dir}")
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
