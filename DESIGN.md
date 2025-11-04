# Idea Explorer: Generalized Autonomous Research Framework

## Executive Summary

Idea Explorer is a generalized autonomous research framework that enables AI agents to conduct scientific experiments across diverse domains. Built on the foundation of `mechinterp_playground` and `scribe`, this system accepts research ideas as structured specifications and orchestrates AI agents to design, execute, analyze, and document experiments autonomously.

**Key Innovation**: Transform domain-specific research automation (mechanistic interpretability) into a universal system that works across machine learning, data science, systems programming, theoretical research, and beyond.

---

## Table of Contents

1. [Motivation and Background](#motivation-and-background)
2. [System Architecture](#system-architecture)
3. [Core Components](#core-components)
4. [Idea Specification Format](#idea-specification-format)
5. [Prompt Template System](#prompt-template-system)
6. [Execution Pipeline](#execution-pipeline)
7. [Evaluation Framework](#evaluation-framework)
8. [Implementation Roadmap](#implementation-roadmap)
9. [Example Workflows](#example-workflows)
10. [Future Extensions](#future-extensions)

---

## Motivation and Background

### Origin: mechinterp_playground Analysis

The `mechinterp_playground` repository demonstrates effective patterns for autonomous research:

**Strengths:**
- Concurrent execution of multiple AI agents
- Structured output requirements (plan, documentation, code walkthrough)
- Self-evaluation through critic models
- Automated GitHub PR generation
- Robust process management and result organization

**Limitations:**
- Hardcoded to mechanistic interpretability domain
- Task prompts tightly coupled to neural circuit analysis
- Manual prompt file management
- Limited extensibility to other research domains

### Vision: Universal Research Automation

Create a framework where researchers can:
1. Submit research ideas in a structured format
2. Have AI agents autonomously design and execute experiments
3. Receive comprehensive reports with code, results, and analysis
4. Leverage parallel execution across multiple AI providers
5. Validate results through automated critic systems

**Target Domains:**
- Machine Learning (training, evaluation, hyperparameter tuning)
- Data Science (exploratory analysis, statistical testing, visualization)
- Systems Programming (performance benchmarking, optimization)
- Theoretical Research (proof verification, algorithmic analysis)
- Scientific Computing (numerical simulations, model validation)

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ CLI Tool     │  │ Web Dashboard│  │ API Endpoint │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Orchestration Layer                        │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Idea Manager (validate, store, queue ideas)     │       │
│  └──────────────────────────────────────────────────┘       │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Prompt Generator (templates → prompts)          │       │
│  └──────────────────────────────────────────────────┘       │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Execution Manager (concurrent runs, monitoring) │       │
│  └──────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Template Library                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Base         │  │ Domain       │  │ Evaluation   │      │
│  │ Researcher   │  │ Specific     │  │ Criteria     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Execution Layer                           │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Scribe (Jupyter integration for agents)         │       │
│  └──────────────────────────────────────────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Claude Agent │  │ Gemini Agent │  │ Codex Agent  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Results & Evaluation Layer                  │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Result Collector (organize outputs)             │       │
│  └──────────────────────────────────────────────────┘       │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Critic System (validate & score results)        │       │
│  └──────────────────────────────────────────────────┘       │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Report Generator (compile final outputs)        │       │
│  └──────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
idea-explorer/
├── docs/                          # Documentation
│   ├── DESIGN.md                  # This document
│   ├── API.md                     # API reference
│   └── examples/                  # Example ideas and outputs
├── templates/                     # Prompt templates
│   ├── base/                      # Core research methodology
│   │   ├── researcher.txt         # Base researcher prompt
│   │   ├── planning.txt           # Planning phase guidelines
│   │   ├── implementation.txt     # Implementation best practices
│   │   ├── analysis.txt           # Analysis guidelines
│   │   └── documentation.txt      # Documentation standards
│   ├── domains/                   # Domain-specific templates
│   │   ├── ml/                    # Machine learning
│   │   │   ├── training.txt
│   │   │   ├── evaluation.txt
│   │   │   └── hyperparameter.txt
│   │   ├── data_science/          # Data analysis
│   │   │   ├── exploration.txt
│   │   │   ├── statistics.txt
│   │   │   └── visualization.txt
│   │   ├── systems/               # Systems programming
│   │   └── theory/                # Theoretical research
│   └── evaluation/                # Critic templates
│       ├── code_quality.txt
│       ├── scientific_rigor.txt
│       └── reproducibility.txt
├── ideas/                         # User-submitted ideas
│   ├── schema.yaml                # Idea specification schema
│   ├── submitted/                 # New ideas
│   ├── in_progress/               # Currently executing
│   └── completed/                 # Finished experiments
├── src/                           # Source code
│   ├── core/
│   │   ├── idea_manager.py        # Idea validation & management
│   │   ├── prompt_generator.py    # Template → prompt conversion
│   │   ├── execution_manager.py   # Orchestration logic
│   │   └── result_collector.py    # Output organization
│   ├── templates/
│   │   ├── template_engine.py     # Template rendering
│   │   └── validators.py          # Template validation
│   ├── evaluation/
│   │   ├── critic_runner.py       # Run evaluation agents
│   │   └── metrics.py             # Evaluation metrics
│   └── cli/
│       ├── submit.py              # Submit new ideas
│       ├── run.py                 # Execute research
│       ├── monitor.py             # Monitor progress
│       └── report.py              # Generate reports
├── runs/                          # Execution outputs
│   └── [idea_id]_[timestamp]/
│       ├── logs/                  # Execution logs
│       ├── notebooks/             # Jupyter notebooks
│       ├── results/               # Experiment outputs
│       ├── artifacts/             # Models, data, etc.
│       └── evaluation/            # Critic reports
├── scripts/                       # Utility scripts
│   ├── run_research.sh            # Main execution script
│   ├── run_critic.sh              # Evaluation script
│   └── setup_env.sh               # Environment setup
├── config/                        # Configuration
│   ├── providers.yaml             # AI provider settings
│   ├── execution.yaml             # Execution parameters
│   └── evaluation.yaml            # Evaluation criteria
└── tests/                         # Test suite
    ├── test_idea_validation.py
    ├── test_prompt_generation.py
    └── test_execution.py
```

---

## Core Components

### 1. Idea Manager

**Responsibilities:**
- Validate idea specifications against schema
- Store ideas in appropriate directories
- Track idea status (submitted → in_progress → completed)
- Generate unique idea IDs
- Manage idea metadata

**API:**
```python
class IdeaManager:
    def submit_idea(self, idea_spec: dict) -> str:
        """Submit new idea, returns idea_id"""

    def validate_idea(self, idea_spec: dict) -> ValidationResult:
        """Check if idea meets requirements"""

    def get_idea(self, idea_id: str) -> IdeaSpecification:
        """Retrieve idea by ID"""

    def update_status(self, idea_id: str, status: str) -> None:
        """Update idea execution status"""

    def list_ideas(self, status: str = None) -> List[IdeaSpecification]:
        """List all ideas, optionally filtered by status"""
```

### 2. Prompt Generator

**Responsibilities:**
- Load and parse template files
- Compose templates (base + domain-specific + evaluation)
- Inject idea-specific content
- Validate generated prompts
- Support template variables and conditionals

**API:**
```python
class PromptGenerator:
    def generate_research_prompt(self, idea: IdeaSpecification) -> str:
        """Generate main research prompt from idea"""

    def generate_critic_prompt(self, idea: IdeaSpecification,
                               run_dir: Path) -> str:
        """Generate evaluation prompt"""

    def load_template(self, template_path: str) -> Template:
        """Load and parse template file"""

    def compose_templates(self, templates: List[str]) -> str:
        """Combine multiple templates"""
```

### 3. Execution Manager

**Responsibilities:**
- Manage concurrent agent execution
- Handle process lifecycle (start, monitor, cleanup)
- Implement timeout and retry logic
- Collect execution logs
- Organize output files

**API:**
```python
class ExecutionManager:
    def execute_research(self, idea_id: str,
                        providers: List[str],
                        concurrent_limit: int) -> RunResult:
        """Execute research with specified providers"""

    def monitor_execution(self, run_id: str) -> ExecutionStatus:
        """Check status of running experiment"""

    def cancel_execution(self, run_id: str) -> None:
        """Stop running experiment"""

    def collect_results(self, run_id: str) -> ResultCollection:
        """Gather all outputs from completed run"""
```

### 4. Critic System

**Responsibilities:**
- Run evaluation agents on completed research
- Score results against criteria
- Generate evaluation reports
- Compare multiple runs
- Validate reproducibility

**API:**
```python
class CriticSystem:
    def evaluate_research(self, run_dir: Path,
                         criteria: List[str]) -> EvaluationReport:
        """Run critics on completed research"""

    def generate_report(self, evaluation: EvaluationReport) -> str:
        """Create human-readable evaluation summary"""

    def compare_runs(self, run_ids: List[str]) -> ComparisonReport:
        """Compare multiple executions"""
```

---

## Idea Specification Format

### Philosophy: Research-First, Pragmatic Execution

**Version 1.1 Update (2025-11-04):**

The Idea Explorer follows a "research-first, pragmatic execution" philosophy:

1. **Minimal Specifications Accepted**: Users can submit ideas with just a title, domain, and research question. Detailed experimental design is optional.

2. **Agent-Driven Research**: When details are missing, agents conduct focused literature reviews to identify:
   - Appropriate datasets (HuggingFace, Papers with Code, academic benchmarks)
   - Standard baselines and evaluation methods from related work
   - Best practices and metrics used in the field

3. **Pragmatic Fallbacks**: If research doesn't yield suitable resources:
   - Agents can generate synthetic/custom datasets
   - Simple baselines (random, majority class, heuristics) are acceptable
   - Agents propose reasonable alternatives and document rationale
   - **Critical**: Always proceed to execution - don't get stuck researching

4. **Documentation Requirements**:
   - **Jupyter notebooks**: For experiments, analysis, interactive code
   - **Markdown files**: For documentation meant to be read
   - Required: `resources.md` (research findings), `REPORT.md` (results), `README.md` (overview)

### Schema Definition (YAML)

```yaml
# ideas/schema.yaml (v1.1)
idea:
  type: object
  required: [title, domain, hypothesis]  # expected_outputs now optional
  properties:
    title:
      type: string
      description: "Brief descriptive title for the research"
      example: "Compare fine-tuning vs RAG for domain-specific QA"

    domain:
      type: string
      enum: [machine_learning, data_science, systems, theory, scientific_computing]
      description: "Primary research domain"

    hypothesis:
      type: string
      description: "Research question or hypothesis to test"
      example: "Fine-tuning is more effective than RAG for specialized domains"

    background:
      type: object
      properties:
        description:
          type: string
          description: "Context and motivation"
        papers:
          type: array
          items:
            oneOf:
              - type: object
                properties:
                  path: {type: string}
                  description: {type: string}
              - type: object
                properties:
                  url: {type: string}
                  description: {type: string}
        datasets:
          type: array
          items:
            type: object
            properties:
              name: {type: string}
              source: {type: string}
              description: {type: string}
        code_references:
          type: array
          items:
            type: object
            properties:
              repo: {type: string}
              description: {type: string}

    methodology:
      type: object
      properties:
        approach:
          type: string
          description: "High-level research approach"
        steps:
          type: array
          items:
            type: string
          description: "Key experimental steps"
        baselines:
          type: array
          items:
            type: string
          description: "Baseline methods to compare against"
        metrics:
          type: array
          items:
            type: string
          description: "Evaluation metrics"

    constraints:
      type: object
      properties:
        compute:
          type: string
          enum: [cpu_only, gpu_required, multi_gpu, tpu]
          default: cpu_only
        time_limit:
          type: integer
          description: "Maximum execution time in seconds"
          default: 3600
        memory:
          type: string
          description: "Memory requirements (e.g., '16GB')"
        budget:
          type: number
          description: "API/compute budget in USD"
        dependencies:
          type: array
          items:
            type: string
          description: "Required Python packages or system libraries"

    expected_outputs:
      type: array
      items:
        type: object
        required: [type, format]
        properties:
          type:
            type: string
            enum: [metrics, visualization, model, dataset, report, code]
          format:
            type: string
          fields:
            type: array
            items:
              type: string
          description:
            type: string

    evaluation_criteria:
      type: array
      items:
        type: string
      description: "How to judge success"
      examples:
        - "Statistical significance of results (p < 0.05)"
        - "Reproducibility across 3 runs"
        - "Performance improvement over baseline"
        - "Code quality and documentation"

    metadata:
      type: object
      properties:
        author:
          type: string
        created_at:
          type: string
          format: date-time
        tags:
          type: array
          items:
            type: string
        priority:
          type: string
          enum: [low, medium, high]
          default: medium
```

### Example Idea Specifications

**Example 1: Minimal Specification (v1.1 - Agent researches details)**

```yaml
# ideas/submitted/llm_belief_differentiation_minimal.yaml
idea:
  title: "Do LLMs Differentiate Epistemic Belief from Non-Epistemic Belief?"
  domain: artificial_intelligence

  hypothesis: |
    Large Language Models can distinguish between epistemic beliefs
    (beliefs about what is true) and non-epistemic beliefs (such as
    preferences or commitments) when prompted with scenarios requiring
    such differentiation.

  background:
    description: |
      Humans distinguish multiple kinds of belief in theory of mind tasks.
      As LLMs are used for reasoning and decision-making, it's important
      to assess whether they also differentiate these belief types.

    papers:
      - url: "https://dx.doi.org/10.1037/xge0001765"
        description: |
          Vesga et al. (2025) - Evidence for multiple kinds of belief
          in theory of mind. Provides experimental paradigms.

  constraints:
    compute: cpu_only
    time_limit: 3600
    budget: 100

# Note: No datasets, baselines, or metrics specified!
# Agent will:
# 1. Search for appropriate datasets or create scenarios
# 2. Identify baselines from literature (e.g., majority class, random)
# 3. Select metrics (e.g., accuracy, F1, Cohen's kappa)
# 4. Document choices in resources.md
```

**Example 2: Detailed Specification (traditional approach)**

```yaml
# ideas/submitted/compare_finetuning_vs_rag_001.yaml
idea:
  title: "Fine-tuning vs RAG for Domain-Specific QA"
  domain: machine_learning

  hypothesis: |
    Fine-tuning a language model on domain-specific data will achieve
    better accuracy than RAG for closed-domain question answering,
    but RAG will be more cost-effective and adaptable.

  background:
    description: |
      Recent advances in LLMs enable two approaches for domain adaptation:
      1. Fine-tuning: Update model weights on domain data
      2. RAG: Retrieve relevant context and prompt the base model

      We need empirical comparison on a specialized medical QA dataset.

    papers:
      - url: "https://arxiv.org/abs/2005.11401"
        description: "RAG: Retrieval-Augmented Generation paper"
      - url: "https://arxiv.org/abs/2203.02155"
        description: "Fine-tuning best practices"

    datasets:
      - name: "PubMedQA"
        source: "pubmedqa/pqa_labeled"
        description: "Biomedical question answering dataset"

  methodology:
    approach: "Comparative study with controlled evaluation"
    steps:
      - "Establish baseline with zero-shot GPT-3.5"
      - "Implement RAG pipeline with vector retrieval"
      - "Fine-tune GPT-3.5 on training split"
      - "Evaluate both on held-out test set"
      - "Analyze error cases and cost trade-offs"

    baselines:
      - "Zero-shot GPT-3.5"
      - "BM25 retrieval + GPT-3.5"

    metrics:
      - "Accuracy"
      - "F1 Score"
      - "Inference latency"
      - "Cost per 1000 queries"
      - "Robustness to out-of-distribution queries"

  constraints:
    compute: gpu_required
    time_limit: 7200
    memory: "32GB"
    budget: 50.00
    dependencies:
      - "transformers"
      - "datasets"
      - "faiss-gpu"
      - "openai"

  expected_outputs:
    - type: metrics
      format: json
      fields:
        - accuracy
        - f1_score
        - latency_ms
        - cost_usd
      description: "Performance metrics for each approach"

    - type: visualization
      format: png
      description: "Comparison plots (accuracy vs cost, error analysis)"

    - type: model
      format: pytorch
      description: "Fine-tuned model checkpoint"

    - type: report
      format: markdown
      description: "Comprehensive analysis with recommendations"

  evaluation_criteria:
    - "Statistical significance tested with paired t-test (p < 0.05)"
    - "Reproducible results across 3 independent runs"
    - "Both approaches properly implemented (validated by critic)"
    - "Clear cost-benefit analysis provided"
    - "Error analysis identifies failure modes"

  metadata:
    author: "research_team"
    tags: ["llm", "rag", "fine-tuning", "medical-qa"]
    priority: high
```

**Example 3: Data Science Analysis (detailed)**

```yaml
# ideas/submitted/analyze_customer_churn_002.yaml
idea:
  title: "Customer Churn Prediction with Interpretable Features"
  domain: data_science

  hypothesis: |
    Using interpretable feature engineering with gradient boosting
    will achieve comparable accuracy to deep learning while providing
    actionable insights for business stakeholders.

  background:
    description: |
      Customer retention is critical for SaaS businesses. While
      deep learning achieves high accuracy, business teams need
      interpretable models to understand churn drivers.

    datasets:
      - name: "Telco Customer Churn"
        source: "kaggle:blastchar/telco-customer-churn"
        description: "Customer data with churn labels"

  methodology:
    approach: "Comparative modeling with focus on interpretability"
    steps:
      - "Exploratory data analysis and data quality checks"
      - "Feature engineering (recency, frequency, monetary value)"
      - "Train baseline logistic regression"
      - "Train gradient boosting model (XGBoost/LightGBM)"
      - "Train neural network for comparison"
      - "Generate SHAP explanations for top features"
      - "Create business-friendly visualizations"

    baselines:
      - "Logistic Regression"
      - "Random guess"

    metrics:
      - "AUC-ROC"
      - "Precision at top 10%"
      - "Feature importance scores"

  constraints:
    compute: cpu_only
    time_limit: 1800
    memory: "8GB"
    dependencies:
      - "pandas"
      - "scikit-learn"
      - "xgboost"
      - "shap"
      - "matplotlib"
      - "seaborn"

  expected_outputs:
    - type: metrics
      format: json
      fields: [auc_roc, precision_at_10pct, f1_score]

    - type: visualization
      format: png
      description: "EDA plots, feature importance, SHAP waterfall"

    - type: report
      format: markdown
      description: "Business recommendations based on churn drivers"

  evaluation_criteria:
    - "Model achieves AUC-ROC > 0.75"
    - "Feature importance analysis provided"
    - "Business recommendations are actionable"
    - "Results reproducible with fixed random seed"

  metadata:
    author: "analytics_team"
    tags: ["churn", "classification", "interpretability"]
    priority: medium
```

---

## Prompt Template System

### Template Hierarchy

Templates are composed in layers:

1. **Base Layer**: Universal research methodology
2. **Domain Layer**: Field-specific best practices
3. **Task Layer**: Specific to the research type
4. **Constraint Layer**: Resource and requirement specifications

### Template Variables

Templates support variable substitution using Jinja2 syntax:

```jinja2
{% raw %}
## YOUR RESEARCH TASK

{{ idea.hypothesis }}

## DOMAIN: {{ idea.domain | upper }}

{{ load_domain_template(idea.domain) }}

## BACKGROUND MATERIALS

{% if idea.background.description %}
{{ idea.background.description }}
{% endif %}

{% if idea.background.papers %}
### Relevant Papers:
{% for paper in idea.background.papers %}
- {% if paper.url %}[{{ paper.description }}]({{ paper.url }}){% else %}{{ paper.path }}{% endif %}
{% endfor %}
{% endif %}

## CONSTRAINTS

- Compute: {{ idea.constraints.compute }}
- Time Limit: {{ idea.constraints.time_limit }} seconds
- Memory: {{ idea.constraints.memory }}

## EXPECTED OUTPUTS

{% for output in idea.expected_outputs %}
### {{ output.type | capitalize }}
- Format: {{ output.format }}
{% if output.fields %}
- Fields: {{ output.fields | join(', ') }}
{% endif %}
- Description: {{ output.description }}
{% endfor %}

## EVALUATION CRITERIA

{% for criterion in idea.evaluation_criteria %}
- {{ criterion }}
{% endfor %}
{% endraw %}
```

### Base Researcher Template

Located at `templates/base/researcher.txt`:

```text
You are a senior researcher conducting a systematic scientific investigation.

Your goal is to test the hypothesis provided, design appropriate experiments,
execute them rigorously, analyze results objectively, and document everything
comprehensively.

═══════════════════════════════════════════════════════════════════
                        RESEARCH METHODOLOGY
═══════════════════════════════════════════════════════════════════

PHASE 1: PLANNING
─────────────────────────────────────────────────────────────────

Before writing any code, create a detailed research plan:

1. Decompose the Hypothesis
   - Break down into testable sub-hypotheses
   - Identify independent and dependent variables
   - Define success criteria explicitly

2. Literature Review (if papers provided)
   - Summarize key related work
   - Identify methodology gaps
   - Note relevant techniques

3. Experimental Design
   - Choose appropriate methods and tools
   - Design control conditions
   - Plan sample sizes and statistical tests
   - Identify potential confounds
   - Consider what could go wrong

4. Resource Planning
   - Estimate computational requirements
   - Plan data storage strategy
   - Identify required libraries and tools

5. Timeline
   - Break work into milestones
   - Allocate time for each phase
   - Build in buffer for debugging

DELIVERABLE: notebooks/plan_Md.ipynb
Must include:
- Research question (restated clearly)
- Background and motivation
- Proposed methodology
- Expected outcomes
- Timeline and milestones
- Potential challenges

═══════════════════════════════════════════════════════════════════

PHASE 2: IMPLEMENTATION
─────────────────────────────────────────────────────────────────

Execute your plan systematically and carefully:

1. Environment Setup
   - Install required dependencies
   - Set random seeds for reproducibility
   - Configure logging
   - Verify GPU availability (if needed)

2. Data Preparation
   - Load and validate datasets
   - Perform data quality checks
   - Split data appropriately
   - Document preprocessing steps
   - Save examples for documentation

3. Baseline Establishment
   - Implement simplest possible baseline first
   - Verify it runs correctly
   - Establish performance floor
   - This validates your evaluation pipeline

4. Main Implementation
   - Write modular, well-commented code
   - Implement one component at a time
   - Test each component independently
   - Log intermediate results
   - Save checkpoints frequently

5. Error Handling
   - Use try-except blocks for robustness
   - Log errors with full context
   - Don't ignore warnings
   - Validate assumptions with assertions

6. Version Control Discipline
   - Document what each code cell does
   - Explain non-obvious design choices
   - Note any deviations from the plan
   - Track hyperparameters and configurations

BEST PRACTICES:

✓ Start small - validate on tiny dataset first
✓ Print shapes and statistics frequently
✓ Visualize intermediate results
✓ Save outputs incrementally (don't wait until end)
✓ Make experiments reproducible (random seeds, versions)
✓ Comment complex logic immediately
✓ Use descriptive variable names
✓ Separate data processing, modeling, and evaluation

✗ Don't hardcode paths or magic numbers
✗ Don't skip validation steps
✗ Don't ignore failed assertions or warnings
✗ Don't run long experiments without checkpointing
✗ Don't proceed if results look wrong

═══════════════════════════════════════════════════════════════════

PHASE 3: ANALYSIS
─────────────────────────────────────────────────────────────────

Interpret results rigorously:

1. Descriptive Statistics
   - Compute mean, std, min, max for all metrics
   - Check for outliers
   - Visualize distributions

2. Comparative Analysis
   - Compare against baselines
   - Use appropriate statistical tests
   - Calculate effect sizes
   - Consider practical significance vs statistical significance

3. Hypothesis Testing
   - State null and alternative hypotheses
   - Choose appropriate statistical test
   - Report p-values and confidence intervals
   - Interpret results in context

4. Error Analysis
   - Examine failure cases
   - Look for patterns in errors
   - Identify edge cases
   - Consider confounding factors

5. Robustness Checks
   - Test on out-of-distribution data
   - Vary hyperparameters
   - Check sensitivity to random seed
   - Validate assumptions

6. Limitations
   - Identify threats to validity
   - Note dataset biases
   - Acknowledge methodological limitations
   - Suggest improvements

═══════════════════════════════════════════════════════════════════

PHASE 4: DOCUMENTATION
─────────────────────────────────────────────────────────────────

Create comprehensive documentation that allows others (and your
future self) to understand and reproduce your work.

DELIVERABLE 1: notebooks/documentation_Md.ipynb

Must include these sections:

## 1. Goal
- What hypothesis were you testing?
- What problem does this solve?
- Why is this important?

## 2. Data Construction
- Dataset description (source, size, characteristics)
- Preprocessing steps
- Train/validation/test splits
- Example samples (show 2-3 examples with labels)
- Data quality checks performed

## 3. Experiment Description

### Methodology
- High-level approach and rationale
- Why did you choose this method?
- What alternatives did you consider?

### Implementation Details
- Tools and libraries used (with versions)
- Model architectures or algorithms
- Hyperparameters and how they were chosen
- Training procedure or analysis pipeline

### Experimental Protocol
- Number of runs (for averaging)
- Random seeds used
- Evaluation metrics chosen and why
- Hardware specifications

### Raw Results
- All metric values (tables or JSON)
- Training curves (if applicable)
- Visualizations of key results
- Where outputs are saved

## 4. Result Analysis

### Key Findings
- What do the results show?
- Do they support or refute the hypothesis?
- Statistical significance of findings

### Comparison to Baselines
- How much improvement (if any)?
- Is the improvement meaningful?

### Visualizations
- Plots that illustrate main findings
- Error analysis visualizations
- Feature importance (if applicable)

### Surprises and Insights
- Unexpected results
- Interesting patterns discovered
- Failed approaches (and why)

### Limitations
- What are the caveats?
- What assumptions were made?
- What could invalidate these results?

## 5. Conclusions
- Clear answer to research question
- Practical implications
- Confidence in findings

## 6. Next Steps
- Follow-up experiments suggested
- Alternative approaches to try
- How to extend this work
- Open questions

─────────────────────────────────────────────────────────────────

DELIVERABLE 2: notebooks/code_walk_Md.ipynb

A walkthrough that explains your implementation:

## Code Structure
- Overview of notebook organization
- What each major section does

## Key Functions/Classes
- Explain important functions
- Design rationale
- Example usage

## Data Pipeline
- How data flows through the code
- Transformations applied
- Validation checks

## Experiment Execution
- How to run the experiments
- Expected execution time
- Resource requirements

## Reproducing Results
- Step-by-step instructions
- Required dependencies
- Expected outputs
- How to verify correctness

═══════════════════════════════════════════════════════════════════

PHASE 5: VALIDATION
─────────────────────────────────────────────────────────────────

Before considering the work complete:

✓ Code Validation
  - All cells run without errors
  - Results are reproducible
  - Outputs match what documentation claims

✓ Scientific Validation
  - Statistical tests are appropriate
  - Conclusions are supported by data
  - Limitations are acknowledged
  - No obvious confounds ignored

✓ Documentation Validation
  - All required sections present
  - Explanations are clear
  - Visualizations have labels and captions
  - Code has comments

✓ Output Validation
  - All expected outputs are generated
  - Files are saved in correct locations
  - Results are in specified formats

═══════════════════════════════════════════════════════════════════
                            GENERAL PRINCIPLES
═══════════════════════════════════════════════════════════════════

1. Scientific Rigor
   - Objective analysis, even if results don't match expectations
   - Honest reporting of limitations
   - Appropriate statistical methods
   - No p-hacking or cherry-picking

2. Reproducibility
   - Set random seeds
   - Document all parameters
   - Version dependencies
   - Save raw outputs

3. Clarity
   - Write for an intelligent reader unfamiliar with your work
   - Define terminology
   - Explain reasoning
   - Use visualizations effectively

4. Efficiency
   - Start with smallest viable experiment
   - Cache expensive computations
   - Don't repeat unnecessary work
   - Parallelize when possible

5. Pragmatism
   - Focus on answering the research question
   - Don't over-engineer
   - Document workarounds honestly
   - Know when "good enough" is sufficient

═══════════════════════════════════════════════════════════════════
```

### Domain-Specific Templates

**Machine Learning** (`templates/domains/ml/core.txt`):

```text
═══════════════════════════════════════════════════════════════════
                  MACHINE LEARNING SPECIFIC GUIDELINES
═══════════════════════════════════════════════════════════════════

DATASET HANDLING
─────────────────────────────────────────────────────────────────

1. Data Splitting
   - Use stratified splits for classification
   - Ensure no data leakage between splits
   - Typical splits: 70% train, 15% validation, 15% test
   - Time-series: use temporal splits (train on past, test on future)

2. Data Quality
   - Check for missing values
   - Identify outliers
   - Verify label distributions
   - Look for duplicate examples
   - Validate data types

3. Class Imbalance
   - Report class distribution
   - Consider stratified sampling
   - Use appropriate metrics (F1, AUC-ROC, not just accuracy)
   - Try oversampling/undersampling if severe

4. Data Augmentation (if applicable)
   - Document augmentation strategies
   - Validate augmented samples
   - Ensure augmentation doesn't change semantics

─────────────────────────────────────────────────────────────────

MODEL DEVELOPMENT
─────────────────────────────────────────────────────────────────

1. Baseline Models
   - Start with simplest possible model (logistic regression, etc.)
   - Validate that training pipeline works
   - Establish performance floor

2. Model Selection
   - Choose architecture appropriate for data size
   - Consider computational constraints
   - Reference papers for architectural choices

3. Training Protocol
   - Use proper train/val/test separation
   - Monitor training and validation curves
   - Implement early stopping
   - Save best model checkpoint (not just final)

4. Hyperparameter Tuning
   - Document search space
   - Use validation set (not test set!) for tuning
   - Consider random search or Bayesian optimization
   - Report final hyperparameters

5. Overfitting Prevention
   - Monitor validation loss during training
   - Use regularization techniques
   - Consider data augmentation
   - Visualize training curves

─────────────────────────────────────────────────────────────────

EVALUATION
─────────────────────────────────────────────────────────────────

1. Metrics Selection
   Classification:
   - Accuracy (only if balanced classes)
   - Precision, Recall, F1
   - AUC-ROC, AUC-PR
   - Confusion matrix

   Regression:
   - MSE, RMSE, MAE
   - R² score
   - Residual plots

   Ranking:
   - NDCG, MAP, MRR

2. Statistical Testing
   - Run multiple trials with different random seeds (≥3)
   - Report mean and standard deviation
   - Use paired t-tests for comparing models
   - Report confidence intervals

3. Error Analysis
   - Examine misclassified examples
   - Look for systematic patterns
   - Check performance across subgroups
   - Identify edge cases

4. Robustness Testing
   - Test on out-of-distribution data
   - Evaluate with noisy inputs
   - Check calibration (predicted vs actual probabilities)

5. Efficiency Metrics
   - Training time
   - Inference latency
   - Memory usage
   - Model size

─────────────────────────────────────────────────────────────────

REPRODUCIBILITY
─────────────────────────────────────────────────────────────────

Always set random seeds:
```python
import random
import numpy as np
import torch

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(42)
```

Log environment:
```python
import sys
import torch
print(f"Python: {sys.version}")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA: {torch.version.cuda}")
```

Save model and config together:
```python
torch.save({
    'model_state_dict': model.state_dict(),
    'config': config,
    'metrics': metrics,
    'hyperparameters': hyperparameters
}, 'model_checkpoint.pt')
```

─────────────────────────────────────────────────────────────────

COMMON PITFALLS TO AVOID
─────────────────────────────────────────────────────────────────

✗ Training on test data (even accidentally via normalization)
✗ Tuning hyperparameters on test set
✗ Not setting random seeds
✗ Ignoring class imbalance
✗ Using accuracy for imbalanced classification
✗ Not checking for data leakage
✗ Training until convergence on small validation set (overfitting)
✗ Comparing single runs instead of averaging
✗ Not saving the best model (only the last)
✗ Forgetting to call model.eval() during inference

═══════════════════════════════════════════════════════════════════
```

**Data Science** (`templates/domains/data_science/core.txt`):

```text
═══════════════════════════════════════════════════════════════════
                   DATA SCIENCE SPECIFIC GUIDELINES
═══════════════════════════════════════════════════════════════════

EXPLORATORY DATA ANALYSIS (EDA)
─────────────────────────────────────────────────────────────────

1. Initial Inspection
   - Shape and size of data
   - Column names and types
   - First/last rows
   - Memory usage

2. Descriptive Statistics
   For numerical columns:
   - Mean, median, mode
   - Standard deviation, IQR
   - Min, max, range
   - Percentiles

   For categorical columns:
   - Value counts
   - Number of unique values
   - Most/least common categories

3. Missing Data Analysis
   - Percentage missing per column
   - Patterns in missingness (MCAR, MAR, MNAR)
   - Visualize with heatmap
   - Decide on handling strategy

4. Distribution Analysis
   - Histograms for numerical features
   - Bar plots for categorical features
   - Check for skewness
   - Identify outliers

5. Correlation Analysis
   - Correlation matrix for numerical features
   - Visualize with heatmap
   - Check for multicollinearity
   - Relationship with target variable

6. Temporal Patterns (if time-series)
   - Time-based trends
   - Seasonality
   - Autocorrelation

─────────────────────────────────────────────────────────────────

VISUALIZATION BEST PRACTICES
─────────────────────────────────────────────────────────────────

1. Essential Elements
   - Clear, descriptive titles
   - Labeled axes with units
   - Legend when needed
   - Appropriate scale (linear vs log)
   - Readable font sizes

2. Choosing the Right Plot
   - Distribution: histogram, KDE, box plot
   - Comparison: bar chart, grouped bar chart
   - Relationship: scatter plot, line plot
   - Composition: pie chart, stacked bar
   - Time series: line plot with confidence bands

3. Color Usage
   - Use colorblind-friendly palettes
   - Consistent color scheme across plots
   - Highlight key findings with color
   - Don't overuse colors

4. Sample Visualization Code
```python
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.figure(figsize=(10, 6))
# ... plotting code ...
plt.title("Clear Descriptive Title", fontsize=14)
plt.xlabel("X-axis Label [units]", fontsize=12)
plt.ylabel("Y-axis Label [units]", fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig("results/plot_name.png", dpi=300, bbox_inches='tight')
plt.show()
```

─────────────────────────────────────────────────────────────────

STATISTICAL ANALYSIS
─────────────────────────────────────────────────────────────────

1. Hypothesis Testing

   A. Formulate Hypotheses
   - Null hypothesis (H0)
   - Alternative hypothesis (H1)
   - Significance level (α, typically 0.05)

   B. Choose Appropriate Test
   - t-test: Compare two groups (normally distributed)
   - Mann-Whitney U: Compare two groups (non-parametric)
   - ANOVA: Compare multiple groups
   - Chi-square: Test independence (categorical)
   - Correlation tests: Pearson, Spearman

   C. Check Assumptions
   - Normality (Shapiro-Wilk test, Q-Q plot)
   - Equal variance (Levene's test)
   - Independence of observations

   D. Interpret Results
   - p-value and statistical significance
   - Effect size (Cohen's d, etc.)
   - Confidence intervals
   - Practical significance

2. Handling Multiple Comparisons
   - Use Bonferroni correction or FDR
   - Report both raw and corrected p-values

3. Reporting Statistical Results
   ```
   Example: "Group A (M=50.2, SD=5.1) showed significantly higher
   scores than Group B (M=45.3, SD=4.8), t(98)=4.52, p<0.001,
   Cohen's d=0.91."
   ```

─────────────────────────────────────────────────────────────────

FEATURE ENGINEERING
─────────────────────────────────────────────────────────────────

1. Handling Missing Data
   - Deletion: if <5% missing and MCAR
   - Mean/median imputation: for MCAR
   - Mode imputation: for categorical
   - Predictive imputation: model-based
   - Add "missingness" indicator feature

2. Encoding Categorical Variables
   - One-hot encoding: nominal categories
   - Label encoding: ordinal categories
   - Target encoding: high cardinality
   - Frequency encoding: capture rarity

3. Scaling Numerical Features
   - Standardization: (x - μ) / σ
   - Min-max scaling: (x - min) / (max - min)
   - Robust scaling: using IQR (for outliers)

4. Creating New Features
   - Domain-specific transformations
   - Polynomial features
   - Interaction terms
   - Binning continuous variables
   - Date/time decomposition

5. Feature Selection
   - Remove low-variance features
   - Remove highly correlated features
   - Use domain knowledge
   - Forward/backward selection
   - L1 regularization

─────────────────────────────────────────────────────────────────

DATA QUALITY CHECKS
─────────────────────────────────────────────────────────────────

Run these checks systematically:

```python
import pandas as pd
import numpy as np

def data_quality_report(df):
    """Generate comprehensive data quality report"""

    report = {
        'shape': df.shape,
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'duplicates': df.duplicated().sum(),
        'missing_values': df.isnull().sum(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).round(2),
        'dtypes': df.dtypes,
    }

    # Check for outliers in numerical columns
    numerical = df.select_dtypes(include=[np.number]).columns
    outliers = {}
    for col in numerical:
        Q1, Q3 = df[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        outliers[col] = ((df[col] < Q1 - 1.5*IQR) |
                         (df[col] > Q3 + 1.5*IQR)).sum()
    report['outliers'] = outliers

    return report
```

─────────────────────────────────────────────────────────────────

BUSINESS RECOMMENDATIONS
─────────────────────────────────────────────────────────────────

Your analysis should lead to actionable insights:

1. Executive Summary
   - Key findings in 2-3 bullet points
   - Bottom-line impact
   - Recommended actions

2. Actionable Recommendations
   - Specific, implementable suggestions
   - Prioritized by impact
   - Include expected outcomes
   - Note required resources

3. Risk and Limitations
   - Uncertainty in estimates
   - Assumptions made
   - Data quality caveats
   - When to revisit analysis

═══════════════════════════════════════════════════════════════════
```

---

## Execution Pipeline

### Workflow Diagram

```
┌─────────────────┐
│  User submits   │
│  idea (YAML)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validate idea   │
│ against schema  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate unique │
│ idea_id         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Load templates  │
│ (base + domain) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate prompt │
│ with variables  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Create run dir  │
│ with timestamp  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ Launch agent(s) via scribe  │
│ (concurrent if multiple)    │
└──────────┬──────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Agent executes research:     │
│ 1. Planning phase            │
│ 2. Implementation            │
│ 3. Analysis                  │
│ 4. Documentation             │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Collect outputs:             │
│ - Notebooks (plan, doc, code)│
│ - Results (JSON, plots)      │
│ - Artifacts (models, data)   │
│ - Logs                       │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Launch critic agents to:     │
│ - Validate code quality      │
│ - Check reproducibility      │
│ - Verify scientific rigor    │
│ - Score against criteria     │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Generate final report:       │
│ - Research summary           │
│ - Key findings               │
│ - Evaluation scores          │
│ - Artifacts inventory        │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Optional: Create GitHub PR   │
│ with results                 │
└──────────────────────────────┘
```

### Main Execution Script (`run_research.sh`)

Key improvements over `mechinterp_playground`:

1. **Dynamic Prompt Generation**: Instead of hardcoded prompt files
2. **Idea-based Organization**: Runs organized by idea_id, not generic names
3. **Richer Metadata**: Track idea context, author, timestamps
4. **Better Error Handling**: Validate outputs match expected formats
5. **Progress Tracking**: Real-time status updates

---

## Evaluation Framework

### Multi-Level Evaluation

**Level 1: Code Quality**
- Runnable percentage
- Correctness
- Style and readability
- Redundancy
- Modularity

**Level 2: Scientific Rigor**
- Hypothesis clarity
- Experimental design appropriateness
- Statistical validity
- Baseline comparisons
- Error analysis depth

**Level 3: Reproducibility**
- Random seed setting
- Dependency documentation
- Result consistency across runs
- Clear execution instructions

**Level 4: Documentation Quality**
- Completeness
- Clarity
- Visual aids
- Code walkthrough usefulness

**Level 5: Outputs Validation**
- Expected outputs present
- Correct formats
- Results match documentation claims

### Critic Prompts

**Code Quality Critic** (`templates/evaluation/code_quality.txt`):

```text
You are a code quality critic evaluating a research implementation.

TASK: Analyze the code_walk notebook and run the code to assess quality.

EVALUATION CRITERIA:

1. RUNNABLE PERCENTAGE
   - Re-execute every code block
   - Count how many run without errors
   - Report: X% of code blocks are runnable

2. CORRECTNESS
   - Check implementations against described methodology
   - Verify calculations are correct
   - Look for logical errors
   - Report: X% of code blocks have correctness issues

3. CORRECTION RATE
   - Identify code blocks that were initially wrong but fixed later
   - Report: X% of blocks show self-correction

4. REDUNDANCY
   - Find code blocks that duplicate functionality
   - Identify repeated measurements of the same property
   - Report: X% of code blocks are redundant

5. IRRELEVANCE
   - Identify code blocks unnecessary for the research goal
   - Look for tangential explorations
   - Report: X% of code blocks are irrelevant

6. CODE STYLE
   - Assess readability
   - Check for comments and documentation
   - Evaluate naming conventions
   - Grade: A/B/C/D/F

OUTPUT: Create notebooks/code_quality_evaluation.ipynb with:
- Summary statistics for each criterion
- Examples of good and bad code
- Specific improvement recommendations
- Overall code quality score (0-100)
```

**Scientific Rigor Critic** (`templates/evaluation/scientific_rigor.txt`):

```text
You are a scientific reviewer assessing research rigor.

TASK: Read the documentation notebook and evaluate scientific quality.

EVALUATION CRITERIA:

1. HYPOTHESIS CLARITY
   - Is the research question well-defined?
   - Are variables clearly identified?
   - Grade: Clear / Somewhat Clear / Unclear

2. EXPERIMENTAL DESIGN
   - Are methods appropriate for the question?
   - Are controls properly designed?
   - Is sample size justified?
   - Grade: Strong / Adequate / Weak

3. STATISTICAL VALIDITY
   - Are statistical tests appropriate?
   - Are assumptions checked?
   - Are effect sizes reported?
   - Is multiple testing corrected?
   - Grade: Rigorous / Adequate / Insufficient

4. BASELINE COMPARISONS
   - Are baselines appropriate?
   - Are comparisons fair?
   - Grade: Strong / Adequate / Missing

5. ERROR ANALYSIS
   - Are failure cases examined?
   - Are limitations acknowledged?
   - Grade: Thorough / Basic / Absent

6. REPRODUCIBILITY
   - Can results be reproduced from documentation?
   - Are all parameters documented?
   - Grade: Fully / Partially / Not Reproducible

7. CONCLUSION VALIDITY
   - Do conclusions follow from results?
   - Are claims appropriately hedged?
   - Grade: Strong / Adequate / Overstated

OUTPUT: Create notebooks/scientific_rigor_evaluation.ipynb with:
- Grades for each criterion
- Specific strengths and weaknesses
- Suggestions for improvement
- Overall scientific quality score (0-100)
```

**Reproducibility Critic** (`templates/evaluation/reproducibility.txt`):

```text
You are a reproducibility validator.

TASK: Attempt to reproduce the research results from scratch.

PROCEDURE:

1. Start with a clean environment
2. Follow the documentation step-by-step
3. Re-run all code from the code_walk notebook
4. Compare your results to the reported results

EVALUATION CRITERIA:

1. ENVIRONMENT SETUP
   - Are dependencies clearly listed?
   - Do they install successfully?
   - Grade: Easy / Moderate / Difficult

2. CODE EXECUTION
   - Does code run without errors?
   - Are file paths portable?
   - Grade: Runs Perfectly / Minor Issues / Major Issues

3. RESULT CONSISTENCY
   - Do reproduced metrics match original? (within tolerance)
   - For each metric, compute: |reproduced - original| / original
   - Grade: Exact Match / Close Match / Mismatch

4. RANDOM SEED CONTROL
   - Are random seeds set?
   - Do results match when using same seed?
   - Grade: Deterministic / Mostly Deterministic / Stochastic

5. DOCUMENTATION SUFFICIENCY
   - Can a new researcher reproduce without asking questions?
   - Grade: Self-Sufficient / Minor Clarifications Needed / Insufficient

OUTPUT: Create notebooks/reproducibility_evaluation.ipynb with:
- Step-by-step reproduction log
- Comparison table (original vs reproduced metrics)
- Issues encountered and how they were resolved
- Overall reproducibility score (0-100)
```

### Scoring System

Each evaluation dimension receives a score 0-100.

**Overall Research Quality Score:**
```
Overall = 0.25 * CodeQuality +
          0.35 * ScientificRigor +
          0.25 * Reproducibility +
          0.15 * DocumentationQuality
```

**Interpretation:**
- 90-100: Excellent, publication-ready
- 80-89: Good, minor improvements needed
- 70-79: Adequate, significant improvements recommended
- 60-69: Weak, major revisions required
- <60: Insufficient, restart with different approach

---

## Implementation Roadmap

### Phase 1: Core Infrastructure (Week 1)

**Goals:**
- Working end-to-end pipeline for single domain (ML)
- Idea submission and validation
- Basic prompt generation
- Single-agent execution

**Deliverables:**
1. `src/core/idea_manager.py` - Idea validation and storage
2. `src/core/prompt_generator.py` - Template rendering
3. `ideas/schema.yaml` - Idea specification schema
4. `templates/base/researcher.txt` - Base template
5. `templates/domains/ml/core.txt` - ML template
6. `scripts/run_research.sh` - Main execution script
7. `scripts/submit_idea.py` - CLI for idea submission

**Success Criteria:**
- Submit ML idea via CLI
- Generate prompt successfully
- Execute research with Claude
- Collect outputs in structured directory

### Phase 2: Multi-Domain Support (Week 2)

**Goals:**
- Support data science, systems, theory domains
- Template composition system
- Domain-specific best practices

**Deliverables:**
1. `templates/domains/data_science/core.txt`
2. `templates/domains/systems/core.txt`
3. `templates/domains/theory/core.txt`
4. Enhanced prompt generator with template composition
5. Domain detection and validation

**Success Criteria:**
- Successfully execute ideas from 3+ different domains
- Templates provide relevant domain guidance
- Generated prompts are coherent and comprehensive

### Phase 3: Evaluation System (Week 3)

**Goals:**
- Automated result validation
- Critic agents for quality assessment
- Scoring and reporting

**Deliverables:**
1. `templates/evaluation/code_quality.txt`
2. `templates/evaluation/scientific_rigor.txt`
3. `templates/evaluation/reproducibility.txt`
4. `src/evaluation/critic_runner.py`
5. `src/evaluation/metrics.py`
6. `scripts/run_critic.sh`

**Success Criteria:**
- Critics successfully evaluate completed research
- Scores are informative and actionable
- Evaluation reports identify specific issues

### Phase 4: Usability & Polish (Week 4)

**Goals:**
- Improved CLI with rich output
- Progress monitoring
- Result browsing and comparison
- Documentation and examples

**Deliverables:**
1. `src/cli/monitor.py` - Real-time progress tracking
2. `src/cli/report.py` - Result summarization
3. `docs/examples/` - Example ideas and outputs
4. `docs/API.md` - API documentation
5. Integration tests

**Success Criteria:**
- Smooth user experience from idea submission to results
- Clear progress visibility
- Easy result browsing and comparison

### Phase 5: Advanced Features (Future)

**Goals:**
- Web dashboard
- Experiment tracking integration (W&B, MLflow)
- Multi-run comparison and meta-analysis
- Automated hypothesis generation
- Knowledge base of completed research

---

## Example Workflows

### Example 1: Quick ML Experiment

```bash
# 1. Create idea file
cat > ideas/submitted/quick_ml_test.yaml << EOF
idea:
  title: "Test regularization impact on overfitting"
  domain: machine_learning
  hypothesis: "L2 regularization reduces overfitting on small datasets"
  constraints:
    compute: gpu_required
    time_limit: 1800
  expected_outputs:
    - type: metrics
      format: json
      fields: [train_acc, val_acc, test_acc]
    - type: visualization
      format: png
EOF

# 2. Submit and run
./scripts/submit_idea.sh ideas/submitted/quick_ml_test.yaml
./scripts/run_research.sh quick_ml_test_001 --provider claude

# 3. Monitor progress
./scripts/monitor.sh quick_ml_test_001

# 4. When complete, review results
./scripts/report.sh quick_ml_test_001

# 5. Run critics
./scripts/run_critic.sh quick_ml_test_001

# 6. View final evaluation
cat runs/quick_ml_test_001_*/evaluation/summary.md
```

### Example 2: Multi-Provider Comparison

```bash
# Run same idea with multiple providers to compare approaches
./scripts/run_research.sh complex_idea_005 \
    --providers claude,gemini,codex \
    --concurrent 3

# Compare results across providers
./scripts/compare_runs.sh \
    runs/complex_idea_005_claude_* \
    runs/complex_idea_005_gemini_* \
    runs/complex_idea_005_codex_*
```

### Example 3: Iterative Refinement

```bash
# Initial attempt
./scripts/run_research.sh hypothesis_xyz_001 --provider claude

# Review results, refine idea based on findings
./scripts/report.sh hypothesis_xyz_001
# ... edit ideas/submitted/hypothesis_xyz_002.yaml ...

# Run refined version
./scripts/run_research.sh hypothesis_xyz_002 --provider claude

# Compare iterations
./scripts/compare_runs.sh \
    runs/hypothesis_xyz_001_* \
    runs/hypothesis_xyz_002_*
```

---

## Future Extensions

### Short Term (3-6 months)

1. **Web Dashboard**
   - Visual idea submission form
   - Real-time execution monitoring
   - Interactive result exploration
   - Run comparison interface

2. **Experiment Tracking Integration**
   - W&B integration for ML experiments
   - MLflow integration for model versioning
   - Automatic metric logging

3. **Enhanced Templates**
   - More domain templates (NLP, CV, RL, etc.)
   - Task-specific templates (hyperparameter tuning, ablation studies)
   - Industry-specific templates (finance, healthcare, etc.)

4. **Collaborative Features**
   - Share ideas and results
   - Comment on research outputs
   - Fork and extend existing research

### Medium Term (6-12 months)

1. **Automated Hypothesis Generation**
   - Analyze completed research to suggest follow-ups
   - Identify research gaps
   - Generate promising research directions

2. **Meta-Analysis**
   - Aggregate results across multiple studies
   - Identify robust findings vs flukes
   - Build knowledge graphs of related research

3. **Active Learning**
   - System suggests most informative experiments
   - Optimizes exploration-exploitation tradeoff
   - Reduces number of experiments needed

4. **Multi-Agent Collaboration**
   - Multiple agents work together on complex research
   - Specialization (one for data prep, one for modeling, etc.)
   - Peer review between agents

### Long Term (1-2 years)

1. **Autonomous Research Lab**
   - System proposes novel hypotheses
   - Designs experiments to test them
   - Publishes findings automatically
   - Minimal human supervision

2. **Transfer Learning Across Domains**
   - Apply insights from one domain to another
   - Cross-pollination of techniques
   - Analogical reasoning

3. **Human-AI Research Teams**
   - Seamless collaboration between researchers and AI
   - AI handles routine analysis, human provides intuition
   - Natural language interaction for steering research

4. **Scientific Paper Generation**
   - Auto-generate draft papers from research outputs
   - Follow publication standards (e.g., ICML format)
   - Submit to preprint servers

---

## Conclusion

Idea Explorer transforms autonomous research from domain-specific automation to a universal framework. By separating research methodology (templates) from research content (ideas), we create a flexible system that scales across disciplines while maintaining rigor and reproducibility.

**Key Innovations:**

1. **Structured Idea Specification**: Research ideas as declarative YAML documents
2. **Composable Templates**: Layered prompts (base + domain + task)
3. **Multi-Agent Orchestration**: Parallel execution with multiple providers
4. **Automated Evaluation**: Critic agents ensure quality
5. **Comprehensive Documentation**: Every experiment produces publication-ready docs

**Next Steps:**

Implement Phase 1 (Core Infrastructure) to validate the design with a working prototype.

---

**Document Version**: 1.0
**Last Updated**: 2025-11-03
**Authors**: Design based on analysis of mechinterp_playground and scribe
