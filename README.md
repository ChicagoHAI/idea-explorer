# Idea Explorer: Autonomous Research Framework

**Transform research ideas into comprehensive experiments with AI agents**

Idea Explorer is a generalized autonomous research framework that takes structured research ideas and orchestrates AI agents to design, execute, analyze, and document experiments across diverse domains.

## Quick Start

### Option A: Fetch from IdeaHub

```bash
# 0. Setup (one-time)
uv sync  # Install dependencies with uv
cp .env.example .env
# Edit .env and add your GITHUB_TOKEN and OPENAI_API_KEY

# 1. Fetch an idea from IdeaHub and auto-submit
python src/cli/fetch_from_ideahub.py https://hypogenic.ai/ideahub/idea/HGVv4Z0ALWVHZ9YsstWT --submit

# 2. Run the research
python src/core/runner.py <idea_id>
```

### Option B: Create Your Own Idea

```bash
# 0. Setup (one-time)
uv sync  # Install dependencies with uv
cp .env.example .env
# Edit .env and add your GITHUB_TOKEN

# 1. Submit a research idea (creates GitHub repo & workspace)
python src/cli/submit.py ideas/examples/ml_regularization_test.yaml

# 2. (Optional) Add resources to workspace
cd workspace/<repo-name>
# Add datasets, documents, code, etc.
git add .
git commit -m "Add research resources"
git push

# 3. Run the research
cd ../..  # Back to project root
python src/core/runner.py <idea_id>

# 4. Results automatically pushed to GitHub
# GitHub: https://github.com/ChicagoHAI/<repo-name>
# Local: workspace/<repo-name>/
```

**New Features:**
- **IdeaHub Integration**: Fetch and convert research ideas from IdeaHub automatically
- **Workspace-first workflow**: GitHub repo created on submission, ready for your resources
- **User resources**: Add datasets, documents, and code before running experiments
- **uv package manager**: Fast, modern Python dependency management

## Overview

### What It Does

Idea Explorer automates the entire research workflow:

1. **Submit**: Define research ideas (minimal or detailed) in YAML format
2. **Research**: Agents conduct literature review and resource discovery
3. **Execute**: AI agents design experiments, write code, and run analyses
4. **Document**: Generates comprehensive reports (REPORT.md, README.md)
5. **Evaluate**: (Future) Critic agents assess research quality and reproducibility

### Research-First Philosophy (v1.1)

**You can submit minimal ideas** - agents will research the details:

- ✅ Just provide: title, domain, research question
- 🔍 Agent searches for: datasets, baselines, evaluation methods
- 📚 Grounds in literature when resources exist
- 🛠️ Creates synthetic data/baselines when they don't
- ⚡ Always proceeds to execution - doesn't get stuck

**Example minimal idea:**
```yaml
idea:
  title: "Do LLMs understand causality?"
  domain: artificial_intelligence
  hypothesis: "LLMs can distinguish causal from correlational relationships"
  # That's it! Agent handles the rest
```

### Key Features

- **Flexible Specifications**: Minimal ideas (just research question) or detailed plans
- **Agent-Driven Research**: Literature review, dataset search, baseline identification
- **Pragmatic Execution**: Creates resources when they don't exist, always proceeds
- **Domain-Agnostic**: Works across ML, data science, AI, systems, theory, and more
- **Layered Prompts**: Base methodology + domain-specific best practices
- **Multi-Provider**: Supports Claude, Gemini, and Codex via scribe
- **Smart Documentation**: Notebooks for experiments, markdown for readable docs

## Architecture

```
ideas/
  submitted/      ← New research ideas
  in_progress/    ← Currently executing
  completed/      ← Finished research

templates/
  base/           ← Universal research methodology
  domains/        ← Domain-specific guidelines (ML, data science, etc.)
  evaluation/     ← Critic agent prompts

src/
  core/           ← Idea management, execution orchestration
  templates/      ← Prompt generation engine
  cli/            ← Command-line tools

runs/
  <idea_id>_<timestamp>/
    notebooks/    ← Jupyter notebooks
    results/      ← Metrics, plots, models
    logs/         ← Execution logs
    artifacts/    ← Generated outputs
```

## Creating Research Ideas

### Idea Specification Format

Research ideas are defined in YAML with the following structure:

```yaml
idea:
  title: "Clear, descriptive title"
  domain: machine_learning  # or data_science, systems, etc.

  hypothesis: |
    Specific, testable hypothesis. What do you expect to find?

  background:
    description: "Context and motivation"
    papers:
      - url: "https://arxiv.org/..."
        description: "Why this paper is relevant"
    datasets:
      - name: "Dataset name"
        source: "Where to get it"
        description: "What it contains"

  methodology:
    approach: "High-level strategy"
    steps:
      - "Step 1"
      - "Step 2"
    baselines: ["Baseline 1", "Baseline 2"]
    metrics: ["Metric 1", "Metric 2"]

  constraints:
    compute: gpu_required  # or cpu_only, multi_gpu, tpu
    time_limit: 3600  # seconds
    memory: "16GB"
    dependencies:
      - "numpy"
      - "pandas"

  expected_outputs:
    - type: metrics
      format: json
      fields: [accuracy, f1_score]
    - type: visualization
      format: png
      description: "Comparison plots"

  evaluation_criteria:
    - "Statistical significance (p < 0.05)"
    - "Reproducible across 3 runs"
```

See `ideas/schema.yaml` for the complete specification and `ideas/examples/` for templates.

## Usage

### 1. Submit an Idea

Create a YAML file with your research idea:

```bash
# Validate and submit (creates GitHub repo and workspace)
python src/cli/submit.py my_idea.yaml

# Output:
# ✓ Idea submitted successfully: my_idea_20250103_120000_abc123de
# ✓ Repository created: https://github.com/ChicagoHAI/...
# ✓ Workspace ready at: workspace/...
```

The submission process now creates a GitHub repository and clones it to your local `workspace/` directory.

### 2. Add User Resources (Optional)

Before running the research, you can add datasets, documents, or code to the workspace:

```bash
# Navigate to workspace
cd workspace/<repo-name>

# Add your resources
cp ~/datasets/my_data.csv ./datasets/
cp ~/papers/reference.pdf ./docs/
# Or create files directly
echo "import numpy as np" > utils.py

# Commit and push to GitHub
git add .
git commit -m "Add research resources"
git push

# Return to project root
cd ../..
```

**Why add resources?**
- **Datasets**: Large datasets the agent should analyze
- **Documents**: Papers, documentation, or specifications for context
- **Code**: Helper functions, pre-existing modules, or baseline implementations
- **Configurations**: Model configs, hyperparameter files, etc.

When you run the research, the agent will automatically pull the latest changes and have access to all these resources.

### 3. Run Research

Execute the research with an AI agent:

```bash
python src/core/runner.py my_idea_20250103_120000_abc123de

# Options:
#   --provider claude|gemini|codex  (default: claude)
#   --timeout SECONDS               (default: 3600)
#   --full-permissions              (allow agents to run without permission prompts)
#   --no-github                     (run locally without GitHub integration)
#   --github-org ORG                (specify GitHub organization, default: ChicagoHAI)
```

**Permission Modes:**

By default, agents will prompt for permission before executing sensitive operations. Use `--full-permissions` to allow agents to run autonomously:

```bash
# With permission prompts (default, safer)
python src/core/runner.py my_idea

# Full autonomous mode (faster, no interruptions)
python src/core/runner.py my_idea --provider codex --full-permissions
```

The `--full-permissions` flag translates to provider-specific flags:
- Codex: `codex --yolo`
- Claude: `claude --dangerously-skip-permissions`
- Gemini: (no permission system)


The agent will:
- Generate a comprehensive research plan
- Implement experiments with proper methodology
- Run analyses and generate visualizations
- Create documentation (plan, documentation, code walkthrough)
- Save all outputs in structured directories

### 4. Review Results

Results are organized in `workspace/<repo-name>/`:

```
workspace/<repo-name>/
├── notebooks/
│   ├── plan_Md.ipynb           ← Research plan and methodology
│   ├── documentation_Md.ipynb  ← Results, analysis, conclusions
│   └── code_walk_Md.ipynb      ← Code walkthrough and explanations
├── results/
│   ├── metrics.json            ← Performance metrics
│   └── *.png                   ← Visualizations
├── artifacts/
│   └── *.pt / *.pkl            ← Saved models
├── logs/
│   ├── research_prompt.txt     ← Generated prompt
│   └── execution_claude.log    ← Agent execution log
├── datasets/                   ← Your datasets (if added)
├── docs/                       ← Your documents (if added)
└── .idea-explorer/
    └── idea.yaml               ← Original idea specification
```

All results are also available on GitHub at: `https://github.com/ChicagoHAI/<repo-name>`

### 5. Evaluate Quality (Optional)

Run critic agents to assess research quality:

```python
from src.evaluation.critic_runner import CriticRunner

runner = CriticRunner()

# Run all critics
runner.evaluate_research(
    run_dir="runs/my_idea_20250103_120000/",
    critics=["code_quality", "scientific_rigor", "reproducibility"]
)

# Results in run_dir/evaluation/
```

## Supported Domains

- **Artificial Intelligence**: LLM evaluation, prompt engineering, AI agents, benchmarking
- **Machine Learning**: Training, evaluation, hyperparameter tuning
- **Data Science**: EDA, statistical analysis, visualization
- **Systems**: Performance benchmarking, optimization
- **Theory**: Algorithmic analysis, proof verification
- **Scientific Computing**: Simulations, numerical methods
- **NLP**: Language model experiments, text analysis
- **Computer Vision**: Image processing, object detection
- **Reinforcement Learning**: Agent training, policy evaluation

## Examples

### Example 1: AI/LLM Research

```yaml
idea:
  title: "Evaluating Chain-of-Thought Prompting on Mathematical Reasoning"
  domain: artificial_intelligence
  hypothesis: "CoT prompting improves accuracy by 15-30% on multi-step math problems"
  # ... rest of specification
```

See `ideas/examples/ai_chain_of_thought_evaluation.yaml` for complete example.

### Example 2: ML Experiment

```yaml
idea:
  title: "Compare SGD vs Adam on CIFAR-10"
  domain: machine_learning
  hypothesis: "Adam converges faster than SGD but may generalize worse"
  # ... rest of specification
```

### Example 3: Data Science Analysis

```yaml
idea:
  title: "Analyze customer churn predictors"
  domain: data_science
  hypothesis: "Usage frequency is the strongest churn predictor"
  # ... rest of specification
```

### Example 4: Systems Benchmark

```yaml
idea:
  title: "Evaluate database query optimization strategies"
  domain: systems
  hypothesis: "Learned indexes outperform B-trees on skewed distributions"
  # ... rest of specification
```

## Prompt Templates

### Base Researcher Template

The `templates/base/researcher.txt` provides universal research methodology:

- **Phase 1: Planning** - Hypothesis decomposition, experimental design
- **Phase 2: Implementation** - Coding best practices, reproducibility
- **Phase 3: Analysis** - Statistical testing, error analysis
- **Phase 4: Documentation** - Comprehensive reporting standards
- **Phase 5: Validation** - Quality checks before completion

### Domain Templates

Domain-specific templates (`templates/domains/`) add specialized guidance:

- **ML**: Data splitting, model selection, overfitting prevention, metrics
- **Data Science**: EDA, statistical tests, visualization, feature engineering
- **Systems**: Benchmarking, profiling, optimization strategies
- **Theory**: Proof techniques, complexity analysis, formal methods

### Evaluation Templates

Critic templates (`templates/evaluation/`) assess quality:

- **Code Quality**: Runnable %, correctness, redundancy, style
- **Scientific Rigor**: Hypothesis clarity, experimental design, statistical validity
- **Reproducibility**: Environment setup, determinism, result consistency

## Design Principles

1. **Structured Ideas**: YAML schema ensures completeness
2. **Layered Prompts**: Base + domain + task composition
3. **Best Practices**: Enforces scientific and engineering rigor
4. **Reproducibility**: Seeds, versions, documentation requirements
5. **Evaluation**: Automated quality assessment
6. **Extensibility**: Easy to add new domains and templates

## Advanced Features

### Custom Templates

Add domain-specific guidance by creating new templates:

```
templates/domains/my_domain/
  core.txt                 ← Main guidance
  specific_task.txt        ← Task-specific additions
```

### Multi-Run Comparison

Compare results across multiple runs:

```python
from src.core.comparison import compare_runs

compare_runs([
    "runs/idea_001_claude_20250103/",
    "runs/idea_001_gemini_20250103/"
])
```

### Integration with Experiment Trackers

Log metrics to Weights & Biases or MLflow:

```python
# In your idea specification
idea:
  metadata:
    tracking:
      wandb_project: "my-project"
      mlflow_uri: "http://localhost:5000"
```

## Requirements

- Python 3.10+
- [Scribe](https://github.com/goodfire-ai/scribe) for Jupyter integration
- AI provider access (Claude, Gemini, or Codex)
- Standard scientific Python stack (numpy, pandas, scikit-learn, etc.)

## Installation

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone repository
git clone https://github.com/ChicagoHAI/idea-explorer
cd idea-explorer

# 3. Install dependencies with uv
uv sync

# 4. Install scribe
# Follow instructions at: https://github.com/goodfire-ai/scribe

# 5. Configure environment
cp .env.example .env
# Edit .env and add your GITHUB_TOKEN

# 6. Configure AI provider
# Set up API keys for Claude, Gemini, or Codex in .env
```

**Using uv benefits:**
- 10-100x faster than pip for dependency resolution
- Automatic virtual environment management
- Lockfile generation for reproducibility
- Modern, reliable Python package management

## Troubleshooting

### Idea Validation Fails

```bash
# Check validation errors
python src/cli/submit.py my_idea.yaml

# Skip validation (not recommended)
python src/cli/submit.py my_idea.yaml --no-validate
```

### Agent Execution Hangs

- Check timeout settings (default: 1 hour)
- Review logs in `runs/<idea_id>/logs/`
- Verify scribe is properly configured

### Outputs Not Organized

- Ensure notebooks are created in `notebooks/` directory
- Check file patterns in `runner.py`'s `_organize_outputs()`

### Import Errors

Make sure you're running from project root:

```bash
cd /path/to/idea-explorer
python src/core/runner.py <idea_id>
```

## Contributing

Contributions welcome! Areas of interest:

- New domain templates (biology, chemistry, social science, etc.)
- Additional evaluation criteria
- Integration with experiment trackers
- Web interface
- Multi-agent collaboration features

## Documentation

- **[docs/WORKFLOW.md](docs/WORKFLOW.md)**: Complete workflow guide with examples
- **[docs/IDEAHUB_INTEGRATION.md](docs/IDEAHUB_INTEGRATION.md)**: IdeaHub integration guide
- **[DESIGN.md](DESIGN.md)**: Comprehensive design document
- **[GITHUB_INTEGRATION.md](GITHUB_INTEGRATION.md)**: GitHub integration setup and usage
- **[ideas/schema.yaml](ideas/schema.yaml)**: Full specification schema
- **[ideas/examples/](ideas/examples/)**: Example research ideas

## License

MIT License - See LICENSE file

## Acknowledgments

- Built on [Scribe](https://github.com/goodfire-ai/scribe) by Goodfire AI

## Citation

If you use Idea Explorer in research, please cite:

```bibtex
@software{idea_explorer_2025,
  title={Idea Explorer: Autonomous Research Framework},
  author={Haokun Liu},
  year={2025},
  url={https://github.com/ChicagoHAI/idea-explorer}
}
```

---

**Ready to automate your research?** Start by submitting your first idea:

```bash
python src/cli/submit.py ideas/examples/ml_regularization_test.yaml
```

For questions and feedback, please open an issue on GitHub.
