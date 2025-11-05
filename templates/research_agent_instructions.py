"""
Research Agent Session Instructions Generator

This module generates the session instructions for the AI research agent.
The instructions emphasize initial research, resource gathering, and systematic execution.
"""

def generate_instructions(prompt: str, work_dir: str) -> str:
    """
    Generate comprehensive session instructions for the research agent.

    Args:
        prompt: The research task prompt (from prompt_generator)
        work_dir: Working directory path for the research

    Returns:
        Complete session instructions string
    """
    return f"""Start a new session for research execution.

CRITICAL: Environment Setup
────────────────────────────────────────────────────────────────────────────────
You MUST create a fresh isolated environment for this project. DO NOT use the
idea-explorer environment or any existing environment.

REQUIRED STEPS (in order):

1. Create a fresh virtual environment using uv:
   uv venv

2. Initialize project dependencies file:
   Create pyproject.toml to manage dependencies in THIS workspace only:

   cat > pyproject.toml << 'EOF'
   [project]
   name = "research-workspace"
   version = "0.1.0"
   description = "Research workspace for experiments"
   requires-python = ">=3.10"
   dependencies = []

   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"
   EOF

   CRITICAL: This ensures uv won't search parent directories for pyproject.toml
   and contaminate the idea-explorer environment!

3. Activate the environment:
   source .venv/bin/activate

4. For package installations, use this priority order:

   FIRST CHOICE - uv add (manages pyproject.toml automatically):
   uv add <package-name>

   Examples:
   - uv add numpy pandas matplotlib
   - uv add torch transformers
   - uv add scikit-learn scipy

   SECOND CHOICE - if uv add doesn't work:
   uv pip install <package-name>
   pip freeze > requirements.txt

   LAST RESORT - if uv fails entirely:
   pip install <package-name>
   pip freeze > requirements.txt

   NEVER use conda or conda install!

5. Dependency Management:
   - Using 'uv add' automatically updates pyproject.toml
   - Verify dependencies with: cat pyproject.toml
   - If you used pip, also maintain: pip freeze > requirements.txt
   - This ensures reproducibility of the research environment

WHY: Using an isolated environment ensures:
- No pollution of the idea-explorer environment
- Fast package installation with uv (10-100x faster than pip)
- Automatic dependency tracking with pyproject.toml
- Clean, reproducible research setup

════════════════════════════════════════════════════════════════════════════════

CRITICAL: Initial Research & Resource Gathering Phase
────────────────────────────────────────────────────────────────────────────────
IMPORTANT PHILOSOPHY: This is a fully-automated research system. Your goal is to
run meaningful experiments that test the hypothesis. If the idea specification
lacks details (datasets, methods, baselines), you MUST research to find them.
If research doesn't yield suitable resources, PROPOSE something reasonable and
PROCEED - don't get stuck. The goal is to run SOMETHING that advances knowledge.

PHASE 0: INITIAL ASSESSMENT (Quick evaluation)
───────────────────────────────────────────────────────────────────────────────

First, assess what's provided in the research specification:

1. CHECK PROVIDED RESOURCES:
   - Are datasets specified? If yes, use them
   - Are baselines/methods specified? If yes, use them
   - Are evaluation metrics specified? If yes, use them
   - Are there user-provided files in the workspace? If yes, review them

2. IDENTIFY GAPS:
   - What information is missing?
   - What do you need to research?
   - What can you reasonably infer or propose?

DECISION: If everything is specified → proceed to planning (Phase 1)
         If gaps exist → conduct focused research (steps below)

RESEARCH STEPS (only if needed based on gaps):

1. LITERATURE REVIEW (15-30 minutes max):
   - Search for recent papers on the research topic (use web search, arXiv, etc.)
   - Read abstracts and methodology sections of top 3-5 relevant papers
   - Identify what methods and baselines are commonly used in this area
   - Note what evaluation metrics are standard in the field

   FOR LLM/AI RESEARCH SPECIFICALLY:
   - Search for latest model releases and capabilities (2024-2025)
   - Check current state-of-the-art models (GPT, Claude, Gemini series, and openrouter)
   - Verify model availability and API endpoints
   - Avoid using outdated models (pre-2024) unless for historical baseline

2. DATASET SEARCH (if no dataset specified):
   - Search existing datasets:
     * HuggingFace Datasets (https://huggingface.co/datasets)
     * Papers with Code datasets (https://paperswithcode.com/datasets)
     * Kaggle datasets
     * Academic benchmarks from papers

   - Evaluate for: relevance, size, quality, accessibility
   - Download and inspect promising datasets

   IF NO SUITABLE DATASET FOUND:
   → It's OK to generate synthetic data or create a custom dataset
   → Document your rationale clearly
   → Proceed with execution

3. CODE & BASELINE SEARCH (if no baselines specified):
   - Look for existing implementations on GitHub
   - Check for established libraries/frameworks
   - Identify baseline implementations from papers

   IF NO SUITABLE BASELINES FOUND:
   → Propose simple, reasonable baselines (random, majority class, simple heuristic)
   → Document your choice
   → Proceed with execution

4. RESOURCE DOCUMENTATION:
   Create a brief resources.md file noting:
   - What you searched for and what you found (or didn't find)
   - Why you selected certain resources
   - What you decided to create/propose if nothing suitable existed
   - Justification for your choices

CRITICAL: Don't get stuck in endless research!
- Spend 30-60 minutes maximum on initial research
- If you can't find perfect resources, find good-enough ones
- If nothing exists, CREATE it (synthetic data, simple baselines, etc.)
- ALWAYS PROCEED to execution - the goal is to run experiments

WHY THIS MATTERS:
- Grounds research in existing work when possible
- Ensures comparability with literature when resources exist
- Enables progress even when resources don't exist
- Balances rigor with pragmatism

IMPORTANT: Check for User-Provided Resources
────────────────────────────────────────────────────────────────────────────────
After your initial research, CHECK the workspace directory for resources that
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

════════════════════════════════════════════════════════════════════════════════

EXECUTION WORKFLOW:
────────────────────────────────────────────────────────────────────────────────

Phase 0: Initial Assessment & Research (see above - only if needed)
  ✓ Check what's provided in the specification
  ✓ Identify gaps (datasets, methods, metrics)
  ✓ Conduct focused research to fill gaps (30-60 min max)
  ✓ If resources not found, propose reasonable alternatives
  ✓ Document decisions in resources.md
  ✓ ALWAYS PROCEED - don't get stuck researching

Phase 1: Detailed Planning (do this BEFORE coding!)
  ✓ Create experimental plan based on research findings
  ✓ Design experiments with specific steps
  ✓ Choose baselines and metrics (from research or proposed)
  ✓ Plan timeline and resource allocation
  ✓ Document plan in planning.md or similar

Phase 2: Environment & Data Setup
  ✓ Set up isolated virtual environment (uv venv)
  ✓ Install required packages (uv add)
  ✓ Download and prepare datasets (found or created)
  ✓ Verify data quality and characteristics
  ✓ Run exploratory data analysis

Phase 3: Implementation
  ✓ Use Jupyter notebooks as needed for experiments and analysis
  ✓ Implement baselines first (simpler methods)
  ✓ Implement proposed method
  ✓ Create evaluation harness
  ✓ Write clean, documented code with comments and docstrings
  ✓ Test incrementally

Phase 4: Experimentation
  ✓ Run baseline experiments
  ✓ Run proposed method experiments
  ✓ Collect results systematically (save to results/ directory)
  ✓ Generate visualizations
  ✓ Monitor for issues

Phase 5: Analysis
  ✓ Analyze results statistically
  ✓ Compare against baselines and literature
  ✓ Perform error analysis
  ✓ Create comprehensive visualizations
  ✓ Document findings incrementally

Phase 6: Final Documentation (REQUIRED - see below for details)
  ✓ Create REPORT.md (comprehensive research report)
  ✓ Update README.md (project overview and quick start)
  ✓ Ensure resources.md documents your research process
  ✓ Verify all code has clear comments and docstrings
  ✓ Check reproducibility

Remember:
- You are already in the correct working directory: {work_dir}
- SEARCH and RESEARCH first (but don't get stuck), code later
- Use established datasets and methods from literature when possible
- If nothing suitable exists, CREATE it and document your rationale
- Use Jupyter notebooks for experiments and analysis (name descriptively)
- Use markdown files (.md) for documentation
- Save outputs to organized directories (results/, figures/, etc.)
- Follow the methodology carefully, but adapt based on your research findings

FINAL REQUIRED TASK - After completing all research:
────────────────────────────────────────────────────────────────────────────────
Before finishing, you MUST create two final documentation files:

1. REPORT.md - A comprehensive, easy-to-read research report containing:
   - Executive Summary (2-3 paragraphs)
   - Research Question & Hypothesis
   - Literature Review Summary (key papers and insights)
   - Methodology (what you did, step-by-step)
     * How you selected datasets/baselines based on literature
     * Justification for evaluation metrics
   - Key Findings (main results with supporting data/figures)
   - Discussion & Interpretation
     * How results compare to literature
     * What this means for the research question
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
