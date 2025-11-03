# Quick Start Guide

Get your first autonomous research experiment running in 5 minutes!

## Prerequisites

- Python 3.10+
- [Scribe](https://github.com/goodfire-ai/scribe) installed
- Claude API access (or Gemini/Codex)

## Step 1: Install Dependencies

```bash
cd idea-explorer

# Install Python dependencies
pip install pyyaml jinja2

# Install scribe (follow instructions at: https://github.com/goodfire-ai/scribe)
```

## Step 2: Submit Your First Idea

We've provided a working example that tests L2 regularization:

```bash
python src/cli/submit.py ideas/examples/ml_regularization_test.yaml
```

You should see:

```
📄 Loading idea from: ideas/examples/ml_regularization_test.yaml

🔍 Validating idea...
✅ Validation passed!

📤 Submitting idea...
✓ Idea submitted successfully: impact_of_l2_regularization_20250103_143022_abc12345

================================================================================
SUCCESS! Idea submitted.
================================================================================

Idea ID: impact_of_l2_regularization_20250103_143022_abc12345

To run this research:
  python src/core/runner.py impact_of_l2_regularization_20250103_143022_abc12345
```

## Step 3: Run the Research

Copy the idea ID from above and run:

```bash
python src/core/runner.py impact_of_l2_regularization_20250103_143022_abc12345
```

This will:

1. Load your idea specification
2. Generate a comprehensive research prompt (~15KB)
3. Launch Claude via Scribe
4. The agent will:
   - Create a research plan
   - Load and explore the dataset
   - Train baseline and regularized models
   - Run statistical tests
   - Create visualizations
   - Write comprehensive documentation

Expected duration: **15-30 minutes**

## Step 4: Review Results

Results will be in:

```bash
runs/impact_of_l2_regularization_20250103_143022_abc12345_claude_20250103_143045/
```

Open the notebooks:

```bash
# Research plan
jupyter notebook runs/.../notebooks/plan_Md.ipynb

# Results and analysis
jupyter notebook runs/.../notebooks/documentation_Md.ipynb

# Code walkthrough
jupyter notebook runs/.../notebooks/code_walk_Md.ipynb
```

View results files:

```bash
# Metrics
cat runs/.../results/metrics.json

# Plots
open runs/.../results/*.png
```

## What You'll Get

### notebooks/plan_Md.ipynb
- Research question breakdown
- Experimental design
- Methodology justification
- Timeline and milestones

### notebooks/documentation_Md.ipynb
- Executive summary
- Dataset description with examples
- Implementation details
- Results (tables, plots)
- Statistical analysis
- Conclusions and next steps

### notebooks/code_walk_Md.ipynb
- Code structure overview
- Key functions explained
- How to reproduce
- Design decisions

### results/
- `metrics.json`: Quantitative results
- `*.png`: Visualizations (training curves, comparisons)
- `*.pt` or `*.pkl`: Saved models

## Next Steps

### Create Your Own Research Idea

1. Copy the example:
```bash
cp ideas/examples/ml_regularization_test.yaml my_idea.yaml
```

2. Edit `my_idea.yaml`:
```yaml
idea:
  title: "Your Research Title"
  domain: machine_learning  # or data_science, systems, etc.
  hypothesis: "Your testable hypothesis..."
  # ... customize the rest
```

3. Submit and run:
```bash
python src/cli/submit.py my_idea.yaml
python src/core/runner.py <generated_id>
```

### Explore Different Domains

**Data Science Example**:
```yaml
idea:
  title: "Analyze Customer Churn Patterns"
  domain: data_science
  hypothesis: "Usage frequency predicts churn better than demographics"
  # ... rest of specification
```

**Systems Example**:
```yaml
idea:
  title: "Database Index Performance Comparison"
  domain: systems
  hypothesis: "B-trees outperform hash indexes for range queries"
  # ... rest of specification
```

### Try Different AI Providers

```bash
# Use Gemini instead of Claude
python src/core/runner.py <idea_id> --provider gemini

# Use Codex
python src/core/runner.py <idea_id> --provider codex
```

## Common Customizations

### Adjust Time Limit

```bash
# Allow 2 hours instead of default 1 hour
python src/core/runner.py <idea_id> --timeout 7200
```

### Skip Validation (Not Recommended)

```bash
python src/cli/submit.py my_idea.yaml --no-validate
```

### Use Custom Template Directory

```python
from src.templates.prompt_generator import PromptGenerator
from pathlib import Path

generator = PromptGenerator(template_dir=Path("my_templates"))
```

## Troubleshooting

### "Idea not found"
Make sure you copied the full idea ID from the submit command output.

### "scribe: command not found"
Install scribe: https://github.com/goodfire-ai/scribe

### "Validation failed"
Check the error messages - common issues:
- Missing required fields (title, domain, hypothesis, expected_outputs)
- Invalid domain name
- Malformed YAML syntax

### Agent execution hangs
- Check if scribe is properly configured
- Verify API credentials for your AI provider
- Look at logs in `runs/<idea_id>/logs/execution_*.log`

### No notebooks created
- Agent may have encountered errors
- Check execution log
- Verify working directory is set correctly
- Try running with a simpler idea first

## Tips for Success

1. **Start Simple**: Begin with the provided example before creating custom ideas
2. **Be Specific**: Clear, testable hypotheses get better results
3. **Set Reasonable Constraints**: Don't try to do too much in one experiment
4. **Review Logs**: If something goes wrong, check the execution logs
5. **Iterate**: Start with a simple idea, run it, then refine based on results

## Learning Resources

- **Full Documentation**: See `README.md`
- **Design Details**: See `DESIGN.md`
- **Idea Schema**: See `ideas/schema.yaml`
- **Template Examples**: Browse `templates/` directory

## Getting Help

1. Check `README.md` for detailed documentation
2. Review `DESIGN.md` for architecture details
3. Look at example ideas in `ideas/examples/`
4. Open an issue on GitHub

## What's Next?

Once you've successfully run your first experiment:

1. **Try different domains**: ML, data science, systems, theory
2. **Create custom templates**: Add domain-specific guidance
3. **Run critics**: Evaluate research quality automatically
4. **Compare runs**: Execute same idea with different providers
5. **Build knowledge**: Create a library of successful research patterns

---

**You're ready to go! Start with:**

```bash
python src/cli/submit.py ideas/examples/ml_regularization_test.yaml
python src/core/runner.py <generated_id>
```

Happy researching! 🚀
