"""
Research Agent Session Instructions Generator

This module generates the session instructions for the AI research agent.
The actual template is stored in templates/agents/session_instructions.txt.

This file provides backward-compatible wrapper functions that use PromptGenerator internally.

TEMPLATE LOCATION: templates/agents/session_instructions.txt
To customize the experiment runner workflow (phases 1-6), edit that template file.
"""

from pathlib import Path
import sys

# Add parent src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def extract_user_instructions(prompt: str) -> str:
    """
    Extract user-provided instructions from the prompt.

    This is a convenience wrapper that uses PromptGenerator internally.

    Args:
        prompt: The research task prompt

    Returns:
        Extracted user instructions, or empty string if none found
    """
    from templates.prompt_generator import PromptGenerator
    generator = PromptGenerator()
    return generator._extract_user_instructions(prompt)


def generate_instructions(prompt: str, work_dir: str, use_scribe: bool = False) -> str:
    """
    Generate comprehensive session instructions for the research agent.

    This is a convenience wrapper that uses PromptGenerator internally.
    The actual template is stored in templates/agents/session_instructions.txt.

    Args:
        prompt: The research task prompt (from prompt_generator)
        work_dir: Working directory path for the research
        use_scribe: If True, include notebook instructions; if False, use Python scripts

    Returns:
        Complete session instructions string
    """
    from templates.prompt_generator import PromptGenerator
    generator = PromptGenerator()
    return generator.generate_session_instructions(prompt, work_dir, use_scribe)
