"""
Research Runner - Executes research ideas using AI agents

This module orchestrates the execution of research by:
1. Loading idea specifications
2. Creating GitHub repository (optional)
3. Generating prompts
4. Launching agents via scribe
5. Committing and pushing results to GitHub
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
import subprocess
import shlex
from datetime import datetime
import sys
import os
import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.idea_manager import IdeaManager
from templates.prompt_generator import PromptGenerator

try:
    from core.github_manager import GitHubManager
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False


class ResearchRunner:
    """
    Runs research experiments using AI agents.
    Supports optional GitHub integration for automatic repo creation and pushing.
    """

    def __init__(self,
                 project_root: Optional[Path] = None,
                 use_github: bool = True,
                 github_org: str = "ChicagoHAI"):
        """
        Initialize research runner.

        Args:
            project_root: Root directory of project.
                         Defaults to parent of src/
            use_github: Whether to create GitHub repos for experiments (default: True)
            github_org: GitHub organization name (default: ChicagoHAI)
        """
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent

        self.project_root = Path(project_root)
        self.runs_dir = self.project_root / "runs"
        self.runs_dir.mkdir(exist_ok=True)

        self.idea_manager = IdeaManager(self.project_root / "ideas")
        self.prompt_generator = PromptGenerator(self.project_root / "templates")

        # GitHub integration
        self.use_github = use_github
        self.github_manager = None

        if use_github:
            if not GITHUB_AVAILABLE:
                print("⚠️  GitHub integration disabled: GitHubManager not available")
                print("   Install dependencies: pip install PyGithub GitPython")
                self.use_github = False
            elif not os.getenv('GITHUB_TOKEN'):
                print("⚠️  GitHub integration disabled: GITHUB_TOKEN not set")
                print("   Set GITHUB_TOKEN environment variable or create .env file")
                self.use_github = False
            else:
                try:
                    self.github_manager = GitHubManager(org_name=github_org)
                    print(f"✅ GitHub integration enabled (org: {github_org})")
                except Exception as e:
                    print(f"⚠️  GitHub integration failed: {e}")
                    self.use_github = False

    def run_research(self, idea_id: str,
                    provider: str = "claude",
                    timeout: int = 3600) -> Dict[str, Any]:
        """
        Execute research for a given idea.

        If GitHub integration is enabled, creates a GitHub repository,
        clones it, runs research there, and pushes results.

        Args:
            idea_id: Unique identifier of the idea
            provider: AI provider (claude, gemini, codex)
            timeout: Maximum execution time in seconds

        Returns:
            Dictionary with:
            - work_dir: Path where research was conducted
            - github_url: GitHub repo URL (if GitHub enabled)
            - success: Boolean indicating if execution succeeded

        Raises:
            ValueError: If idea not found or invalid
        """
        print(f"🚀 Starting research: {idea_id}")
        print(f"   Provider: {provider}")
        print(f"   GitHub: {'Enabled' if self.use_github else 'Disabled'}")
        print("=" * 80)

        # Load idea
        idea = self.idea_manager.get_idea(idea_id)
        if idea is None:
            raise ValueError(f"Idea not found: {idea_id}")

        idea_spec = idea.get('idea', {})
        title = idea_spec.get('title', 'Untitled Research')

        # Update status
        self.idea_manager.update_status(idea_id, 'in_progress')

        # Setup working directory (GitHub repo or local runs/)
        github_url = None
        github_repo = None

        if self.use_github and self.github_manager:
            # Check if workspace already exists from submission
            # Try to get repo_name from metadata (new method with short names)
            repo_name = idea_spec.get('metadata', {}).get('github_repo_name')
            existing_workspace = self.github_manager.get_workspace_path(idea_id, repo_name)

            if existing_workspace:
                print(f"\n✅ Using existing workspace from submission")
                print(f"   Local: {existing_workspace}")

                # Pull latest changes (in case user added resources)
                try:
                    self.github_manager.pull_latest(existing_workspace)
                except Exception as e:
                    print(f"   ⚠️  Could not pull latest changes: {e}")
                    print(f"   Continuing with local version...")

                work_dir = existing_workspace

                # Get GitHub URL from remote
                try:
                    from git import Repo as GitRepo
                    repo = GitRepo(existing_workspace)
                    github_url = list(repo.remote('origin').urls)[0].replace('.git', '')
                    if 'https://' in github_url and '@' in github_url:
                        # Remove token from URL for display
                        github_url = github_url.split('@')[1]
                        github_url = f"https://{github_url}"
                    print(f"   URL: {github_url}\n")
                except Exception as e:
                    print(f"   ⚠️  Could not get GitHub URL: {e}\n")

            else:
                # Create new GitHub repository (backward compatibility)
                print(f"\n⚠️  No existing workspace found. Creating new GitHub repository...")
                print(f"   (Tip: Use submit.py to create workspace before running)\n")

                try:
                    domain = idea_spec.get('domain', 'research')
                    repo_info = self.github_manager.create_research_repo(
                        idea_id=idea_id,
                        title=title,
                        description=idea_spec.get('hypothesis', ''),
                        private=False,  # Public by default
                        domain=domain
                    )

                    github_url = repo_info['repo_url']
                    github_repo = repo_info['repo_object']

                    # Store repo_name in idea metadata
                    idea['idea']['metadata'] = idea['idea'].get('metadata', {})
                    idea['idea']['metadata']['github_repo_name'] = repo_info['repo_name']
                    idea['idea']['metadata']['github_repo_url'] = github_url

                    # Save updated metadata
                    idea_path = self.idea_manager.ideas_dir / "submitted" / f"{idea_id}.yaml"
                    with open(idea_path, 'w') as f:
                        yaml.dump(idea, f, default_flow_style=False, sort_keys=False)

                    # Clone repository
                    repo = self.github_manager.clone_repo(
                        repo_info['clone_url'],
                        repo_info['local_path']
                    )

                    # Add research metadata
                    self.github_manager.add_research_metadata(
                        repo_info['local_path'],
                        idea
                    )

                    # Commit metadata
                    self.github_manager.commit_and_push(
                        repo_info['local_path'],
                        "Initialize research project with metadata"
                    )

                    work_dir = repo_info['local_path']
                    print(f"\n✅ Working in GitHub repository")
                    print(f"   URL: {github_url}")
                    print(f"   Local: {work_dir}\n")

                except Exception as e:
                    print(f"\n⚠️  GitHub setup failed: {e}")
                    print("   Falling back to local execution\n")
                    self.use_github = False
                    # Fall through to local setup below

        if not self.use_github:
            # Local execution (original behavior)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            run_id = f"{idea_id}_{provider}_{timestamp}"
            work_dir = self.runs_dir / run_id
            work_dir.mkdir(parents=True, exist_ok=True)
            print(f"📁 Working directory: {work_dir}\n")

        # Create subdirectories
        (work_dir / "logs").mkdir(parents=True, exist_ok=True)
        (work_dir / "notebooks").mkdir(parents=True, exist_ok=True)
        (work_dir / "results").mkdir(parents=True, exist_ok=True)
        (work_dir / "artifacts").mkdir(parents=True, exist_ok=True)

        # Generate prompt
        print("📝 Generating research prompt...")
        prompt = self.prompt_generator.generate_research_prompt(
            idea, root_dir=work_dir
        )

        # Save prompt for reference
        prompt_file = work_dir / "logs" / "research_prompt.txt"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)

        print(f"   Prompt saved to: {prompt_file}")
        print(f"   Prompt length: {len(prompt)} characters")
        print()

        # Prepare session instructions
        session_instructions = f"""Start a new session for research execution.

CRITICAL: Environment Setup
────────────────────────────────────────────────────────────────────────────────
You MUST create a fresh isolated environment for this project. DO NOT use the
idea-explorer environment or any existing environment.

REQUIRED STEPS (in order):

1. Create a fresh virtual environment using uv:
   uv venv

2. Activate the environment:
   source .venv/bin/activate

3. For package installations, use this priority order:

   FIRST CHOICE - uv add (manages pyproject.toml automatically):
   uv add <package-name>

   Examples:
   - uv add numpy pandas matplotlib
   - uv add torch transformers
   - uv add scikit-learn scipy

   SECOND CHOICE - if uv add doesn't work:
   uv pip install <package-name>

   LAST RESORT - if uv fails entirely:
   pip install <package-name>

   NEVER use conda or conda install!

4. Dependency Management:
   - Using 'uv add' automatically creates and maintains pyproject.toml
   - Verify dependencies with: cat pyproject.toml
   - If you used pip, also maintain: pip freeze > requirements.txt
   - This ensures reproducibility of the research environment

WHY: Using an isolated environment ensures:
- No pollution of the idea-explorer environment
- Fast package installation with uv (10-100x faster than pip)
- Automatic dependency tracking with pyproject.toml
- Clean, reproducible research setup

════════════════════════════════════════════════════════════════════════════════

IMPORTANT: Check for User-Provided Resources
────────────────────────────────────────────────────────────────────────────────
Before starting your research, CHECK the workspace directory for resources that
may have been added by the user. These could be in directories like:

- papers/ or docs/ - Research papers, documentation (PDFs, markdown)
- datasets/ or data/ - Pre-downloaded datasets, data files
- resources/ - Any other relevant materials
- Root directory - Individual files like papers.txt, data.csv, etc.

If you find relevant resources:
1. List them and briefly describe what you found
2. Review papers or documentation to inform your approach
3. Use provided datasets instead of downloading new ones when applicable
4. Incorporate any constraints or suggestions from these materials

The research specification below may reference some resources, but ALWAYS check
the workspace for additional materials the user may have added!

════════════════════════════════════════════════════════════════════════════════

Execute the following research task:

{prompt}

Remember to:
- You are already in the correct working directory: {work_dir}
- Set up the isolated environment FIRST before installing any packages
- Use 'uv add' for package installation (manages pyproject.toml automatically)
- Create all required notebooks (plan_Md.ipynb, documentation_Md.ipynb, code_walk_Md.ipynb)
- Save all outputs to appropriate directories (notebooks/, outputs/, etc.)
- Follow the methodology carefully
- Document everything thoroughly

FINAL REQUIRED TASK - After completing all research:
────────────────────────────────────────────────────────────────────────────────
Before finishing, you MUST create two final documentation files:

1. REPORT.md - A comprehensive, easy-to-read research report containing:
   - Executive Summary (2-3 paragraphs)
   - Research Question & Hypothesis
   - Methodology (what you did, step-by-step)
   - Key Findings (main results with supporting data/figures)
   - Discussion & Interpretation
   - Limitations & Future Work
   - Conclusion
   - References (papers, datasets, tools used)

   This should be written for a technical audience but be MORE readable than the
   raw notebooks. Include key visualizations/tables inline (as markdown).

2. Update README.md - Add/update the following sections:
   - Brief project description (2-3 sentences)
   - Key findings summary (bullet points, 3-5 main results)
   - How to reproduce (environment setup, run instructions)
   - File structure overview
   - Link to REPORT.md for full details

   Keep README concise and scannable. Think of it as a quick overview someone
   would read to understand what this research accomplished.

These documents are CRITICAL for making your research accessible and understandable!

DO NOT resume the session in the same notebook. Create a new session if continuation is needed.
"""

        # Save session instructions
        session_file = work_dir / "logs" / "session_instructions.txt"
        with open(session_file, 'w', encoding='utf-8') as f:
            f.write(session_instructions)

        print("▶️  Executing research with scribe...")
        print(f"   Using provider: {provider}")
        print(f"   Timeout: {timeout} seconds")
        print()

        # Execute via scribe
        success = False
        try:
            # Set environment variables
            env = os.environ.copy()
            env['SCRIBE_RUN_DIR'] = str(work_dir)
            env['PYTHONUNBUFFERED'] = '1'

            # Prepare command
            log_file = work_dir / "logs" / f"execution_{provider}.log"

            # Run scribe with the prompt
            cmd = f"scribe {provider}"

            print(f"   Command: {cmd}")
            print(f"   Log file: {log_file}")
            print()
            print("=" * 80)
            print("AGENT OUTPUT (streaming)")
            print("=" * 80)
            print()

            with open(log_file, 'w') as log_f:
                # Start process in workspace directory
                process = subprocess.Popen(
                    shlex.split(cmd),
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    env=env,
                    text=True,
                    bufsize=1,
                    cwd=str(work_dir)
                )

                # Send session instructions
                process.stdin.write(session_instructions)
                process.stdin.close()

                # Stream output
                for line in iter(process.stdout.readline, ''):
                    if line:
                        print(line, end='')
                        log_f.write(line)

                # Wait for completion
                return_code = process.wait(timeout=timeout)

            print()
            print("=" * 80)

            if return_code == 0:
                print("✅ Research execution completed successfully!")
                success = True
            else:
                print(f"⚠️  Research execution finished with return code: {return_code}")
                success = False

        except subprocess.TimeoutExpired:
            print(f"\n⏱️  Execution timed out after {timeout} seconds")
            process.kill()
            success = False

        except Exception as e:
            print(f"\n❌ Error during execution: {e}")
            success = False
            raise

        finally:
            # Organize outputs (skip for GitHub repos, files already in place)
            if not self.use_github:
                print()
                print("📦 Organizing outputs...")
                self._organize_outputs(work_dir)

            # Commit and push to GitHub if enabled
            if self.use_github and self.github_manager:
                try:
                    print()
                    print("📤 Pushing results to GitHub...")

                    # Generate commit message
                    status_emoji = "✅" if success else "⚠️"
                    commit_msg = f"""{status_emoji} Research execution completed

Research: {title}
Provider: {provider}
Status: {"Success" if success else "Completed with issues"}

Generated by Idea Explorer
https://github.com/ChicagoHAI/idea-explorer
"""

                    # Commit and push
                    self.github_manager.commit_and_push(
                        work_dir,
                        commit_msg
                    )

                    print(f"\n🎉 Results published to GitHub!")
                    print(f"   {github_url}")

                except Exception as e:
                    print(f"\n⚠️  Failed to push to GitHub: {e}")
                    print("   Results are available locally")

            # Update idea status
            self.idea_manager.update_status(idea_id, 'completed')

            print()
            print(f"✅ Research completed!")
            print(f"   Location: {work_dir}")
            if github_url:
                print(f"   GitHub: {github_url}")

        # Return result info
        return {
            'work_dir': work_dir,
            'github_url': github_url,
            'success': success
        }

    def _organize_outputs(self, run_dir: Path):
        """
        Organize research outputs into appropriate directories.

        Args:
            run_dir: Run directory path
        """
        # Move notebooks from main notebooks/ directory to run
        main_notebooks_dir = self.project_root / "notebooks"
        if main_notebooks_dir.exists():
            # Find notebooks created during this run
            # (Simple approach: move all recent notebooks)
            for notebook in main_notebooks_dir.glob("*.ipynb"):
                dest = run_dir / "notebooks" / notebook.name
                if not dest.exists():
                    notebook.rename(dest)
                    print(f"   Moved: {notebook.name}")

        # Move results files
        results_patterns = [
            "*.json", "*.csv", "*.png", "*.jpg", "*.pdf"
        ]
        for pattern in results_patterns:
            for result_file in self.project_root.glob(pattern):
                if "runs" not in str(result_file) and "venv" not in str(result_file):
                    dest = run_dir / "results" / result_file.name
                    if not dest.exists():
                        try:
                            result_file.rename(dest)
                            print(f"   Moved: {result_file.name}")
                        except:
                            pass  # File might be in use

        print("   ✓ Outputs organized")


def main():
    """CLI entry point for runner."""
    import argparse

    # Load .env file if it exists
    try:
        from dotenv import load_dotenv
        env_file = Path(__file__).parent.parent.parent / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            print("✓ Loaded environment from .env file")
    except ImportError:
        # python-dotenv not installed, that's okay
        pass

    parser = argparse.ArgumentParser(
        description="Run research experiments with AI agents (with GitHub integration)"
    )
    parser.add_argument(
        "idea_id",
        help="ID of the idea to run"
    )
    parser.add_argument(
        "--provider",
        default="claude",
        choices=["claude", "gemini", "codex"],
        help="AI provider to use (default: claude)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=3600,
        help="Timeout in seconds (default: 3600)"
    )
    parser.add_argument(
        "--no-github",
        action="store_true",
        help="Disable GitHub integration (run locally only)"
    )
    parser.add_argument(
        "--github-org",
        default="ChicagoHAI",
        help="GitHub organization name (default: ChicagoHAI)"
    )

    args = parser.parse_args()

    runner = ResearchRunner(
        use_github=not args.no_github,
        github_org=args.github_org
    )

    try:
        result = runner.run_research(
            idea_id=args.idea_id,
            provider=args.provider,
            timeout=args.timeout
        )

        print()
        print("=" * 80)
        print("SUCCESS! Research execution completed.")
        print(f"Location: {result['work_dir']}")
        if result.get('github_url'):
            print(f"GitHub: {result['github_url']}")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
