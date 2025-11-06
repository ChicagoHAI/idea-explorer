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

WHAT "FULLY-AUTOMATED" MEANS:
✓ Complete ALL phases (0-6) in a SINGLE CONTINUOUS SESSION
✓ Make reasonable decisions autonomously without waiting for user input
✓ Move immediately from one phase to the next
✓ Document decisions, but keep moving forward
✓ Deliver REPORT.md with actual experimental results at the end

YOU WILL NOT GET ADDITIONAL INSTRUCTIONS between phases.
This prompt contains everything you need. Execute it completely from start to finish.

════════════════════════════════════════════════════════════════════════════════

CRITICAL: For LLM/AI Research - Use Real Models, Not Simulations
────────────────────────────────────────────────────────────────────────────────

IF your research involves LLM behavior, agents, prompting, or AI capabilities:

✓ YOU MUST use REAL LLM APIs:
  - GPT-4.1 or GPT-5, or other real models
  - You can also use openrouter, there is openrouter key in environment variable.
  - Use actual API calls to test behavior
  - Measure real model outputs, not simulated behavior
  - If you are not sure how to prompt and send API calls, search online.

✗ DO NOT create "simulated LLM agents":
  - Don't fake LLM behavior with predefined rules
  - Don't make up confidence scores or calibration behavior
  - Simulated LLMs have NO scientific value for LLM research

WHY THIS MATTERS:
- Real LLMs behave in complex, emergent ways that can't be simulated
- Research on fake agents doesn't generalize to real systems
- API calls are affordable and fast (100s of calls = $5-50)
- You have freedom to use resources needed for quality research

EXAMPLES:

✓ CORRECT: "Test if chain-of-thought improves calibration"
  → Download TruthfulQA dataset
  → Prompt Claude/GPT with and without CoT
  → Measure actual calibration metrics
  → Statistical comparison

✗ WRONG: "Test if chain-of-thought improves calibration"
  → Create simulated agent with confidence = 0.7 + noise
  → Make up 50 questions
  → Run simulation
  → This is NOT research!

If you find yourself about to create "simulated LLM agents," STOP and use real APIs instead.

════════════════════════════════════════════════════════════════════════════════

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

   PRIORITY: Use existing datasets whenever possible!

   - Search and DOWNLOAD from:
     * HuggingFace Datasets (https://huggingface.co/datasets) - use datasets library
     * Papers with Code datasets (https://paperswithcode.com/datasets)
     * GitHub repositories with datasets
     * Kaggle datasets
     * Academic benchmarks from papers

   - Don't just search - ACTUALLY DOWNLOAD and load the data
   - Evaluate for: relevance, size, quality, accessibility
   - Inspect the actual data structure and samples

   FOR LLM/AI RESEARCH:
   Common benchmarks you should check first:
     * TruthfulQA - truthfulness and calibration
     * MMLU - knowledge and reasoning
     * HellaSwag, ARC - commonsense reasoning
     * HumanEval, MBPP - code generation
     * BBQ, WinoBias - bias evaluation

   IF NO SUITABLE DATASET FOUND:
   → First, search more thoroughly (try different keywords)
   → Check if you can adapt an existing dataset
   → ONLY create synthetic data if genuinely nothing exists
   → Document extensive search efforts before creating synthetic data
   → Synthetic data should be last resort, not default choice

3. CODE & BASELINE SEARCH (if no baselines specified):

   PRIORITY: Use and adapt existing implementations!

   - Search GitHub for relevant repositories
   - CLONE or download promising codebases
   - Check official model implementations (HuggingFace, OpenAI repos, etc.)
   - Look for established libraries/frameworks
   - Identify baseline implementations from papers
   - Download and inspect the actual code

   EXAMPLES:
   - For LLM research: Check HuggingFace model cards, official repos
   - For mechanistic interp: TransformerLens, SAELens libraries
   - For multi-agent: Check AutoGen, CrewAI, LangGraph repos

   IF NO SUITABLE BASELINES FOUND:
   → First, search more thoroughly (different terms, check paper citations)
   → Consider: Can you implement a simple version of a paper's method?
   → ONLY create simple baselines (random, majority) if truly nothing exists
   → Document search efforts

4. RESOURCE DOCUMENTATION:
   Create a brief resources.md file noting:
   - What you searched for and what you found (or didn't find)
   - Why you selected certain resources
   - What you decided to create/propose if nothing suitable existed
   - Justification for your choices

CRITICAL: Don't get stuck in endless research!
- Spend 15-30 minutes maximum on initial research
- Keep resources.md brief (1-2 pages) - just key findings
- If you can't find perfect resources, find good-enough ones
- If nothing exists, CREATE it (synthetic data, simple baselines, etc.)
- ALWAYS PROCEED to execution - the goal is to run experiments

BUDGET GUIDANCE FOR PHASE 0:
- Time: 15-30 minutes maximum
- Keep it lightweight - detailed work happens in implementation phases
- Focus on making quick decisions to unblock planning

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

EXECUTION WORKFLOW (FOLLOW THIS SEQUENCE - DO NOT STOP BETWEEN PHASES):
────────────────────────────────────────────────────────────────────────────────

Phase 0: Initial Assessment & Research (15-30 min)
  ✓ Check what's provided in the specification
  ✓ Identify gaps (datasets, methods, metrics)
  ✓ Conduct focused research to fill gaps (30-60 min max)
  ✓ If resources not found, propose reasonable alternatives
  ✓ Document decisions in resources.md (1-2 pages maximum)

  → WHEN COMPLETE: Immediately proceed to Phase 1 (Planning)

Phase 1: Detailed Planning (15-30 min)
  ✓ Create experimental plan based on research findings
  ✓ Design experiments with specific steps
  ✓ Choose baselines and metrics (from research or proposed)
  ✓ Plan timeline and resource allocation
  ✓ Document plan in planning.md (2-3 pages maximum)

  → WHEN COMPLETE: Immediately proceed to Phase 2 (Setup)
  → DO NOT WAIT for user confirmation - this is fully automated!

Phase 2: Environment & Data Setup (10-20 min)
  ✓ Set up isolated virtual environment (uv venv)
  ✓ Install required packages (uv add)
  ✓ Download and prepare datasets (found or created)
  ✓ Verify data quality and characteristics
  ✓ Run exploratory data analysis

  → WHEN COMPLETE: Immediately proceed to Phase 3 (Implementation)

Phase 3: Implementation (60-90 min)
  ✓ Use Jupyter notebooks as needed for experiments and analysis
  ✓ Implement baselines first (simpler methods)
  ✓ Implement proposed method
  ✓ Create evaluation harness
  ✓ Write clean, documented code with comments and docstrings
  ✓ Test incrementally

  → WHEN COMPLETE: Immediately proceed to Phase 4 (Experiments)

Phase 4: Experimentation (60-90 min)
  ✓ Run baseline experiments
  ✓ Run proposed method experiments
  ✓ Collect results systematically (save to results/ directory)
  ✓ Generate visualizations
  ✓ Monitor for issues

  → WHEN COMPLETE: Immediately proceed to Phase 5 (Analysis)

Phase 5: Analysis (30-45 min)
  ✓ Analyze results statistically
  ✓ Compare against baselines and literature
  ✓ Perform error analysis
  ✓ Create comprehensive visualizations
  ✓ Document findings incrementally

  → WHEN COMPLETE: Immediately proceed to Phase 6 (Documentation)

Phase 6: Final Documentation (20-30 min) - MANDATORY BEFORE ENDING SESSION
  ✓ Create REPORT.md with ACTUAL experimental results (not placeholder)
  ✓ Create README.md with project overview and key findings
  ✓ Ensure resources.md documents your research process
  ✓ Verify all code has clear comments and docstrings
  ✓ Check reproducibility

  → WHEN COMPLETE: Session is finished

CRITICAL REMINDERS:
- This is a SINGLE CONTINUOUS SESSION covering all 6 phases
- Never stop between phases waiting for user input
- If you encounter issues, document them and continue
- Even if experiments fail, complete Phase 6 documenting what happened
- REPORT.md is mandatory - it's the primary deliverable

Remember:
- You are already in the correct working directory: {work_dir}
- SEARCH and RESEARCH first (but don't get stuck), code later
- Use established datasets and methods from literature when possible
- If nothing suitable exists, CREATE it and document your rationale
- Use Jupyter notebooks for experiments and analysis (name descriptively)
- Use markdown files (.md) for documentation
- Save outputs to organized directories (results/, figures/, etc.)
- Follow the methodology carefully, but adapt based on your research findings

────────────────────────────────────────────────────────────────────────────────
PHASE 6 REQUIREMENTS - WHAT TO INCLUDE IN FINAL DOCUMENTATION
────────────────────────────────────────────────────────────────────────────────

When you reach Phase 6, create these files with ACTUAL results from your experiments:

1. REPORT.md - Comprehensive research report containing:
   - Executive Summary (2-3 paragraphs summarizing what you found)
   - Research Question & Hypothesis
   - Literature Review Summary (key papers and insights from Phase 0)
   - Methodology (what you actually did, step-by-step)
     * Datasets/baselines you used and why
     * Evaluation metrics and justification
   - Key Findings (ACTUAL results with supporting data/figures from experiments)
   - Discussion & Interpretation
     * How your results compare to expectations
     * What this means for the research question
   - Limitations & Future Work
   - Conclusion
   - References (papers, datasets, tools used)

   Include key visualizations/tables inline (as markdown).

2. README.md - Quick overview containing:
   - Brief project description (2-3 sentences)
   - Key findings summary (bullet points, 3-5 main results from your experiments)
   - How to reproduce (environment setup, run instructions)
   - File structure overview
   - Link to REPORT.md for full details

   Keep this concise and scannable.

IMPORTANT NOTES:
- Do NOT create placeholder/stub reports during planning - wait until Phase 6
- If experiments fail or are incomplete, document what you attempted and what happened
- REPORT.md is the PRIMARY DELIVERABLE - it must contain actual findings
- These documents make your research accessible and understandable

────────────────────────────────────────────────────────────────────────────────
SESSION COMPLETION
────────────────────────────────────────────────────────────────────────────────

The session is COMPLETE when:
✓ All phases (0-6) have been attempted
✓ Experiments were run (even if simple or preliminary)
✓ REPORT.md has been created documenting actual results
✓ README.md has been created with overview
✓ Code is organized with comments
✓ Results are saved to results/ directory

If you reach this point, your research session is finished.
"""
