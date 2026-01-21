---
name: research-brainstorming
description: Creative ideation for research using structured methods like SCAMPER, morphological analysis, and cross-domain analogies. Use when generating research ideas, exploring new directions, or overcoming creative blocks.
---

# Research Brainstorming

Structured methods for creative research ideation.

## When to Use

- Starting a new research direction
- Generating paper ideas
- Exploring extensions of existing work
- Overcoming creative blocks
- Finding novel angles on problems

## Brainstorming Principles

### Diverge, Then Converge

1. **Divergent phase**: Generate many ideas without judgment
2. **Convergent phase**: Evaluate and select best ideas

### Rules for Divergent Phase

- Quantity over quality initially
- No criticism or evaluation
- Build on others' ideas
- Wild ideas are welcome
- Combine and improve ideas

### Rules for Convergent Phase

- Apply evaluation criteria
- Consider feasibility
- Rank by potential impact
- Identify quick wins vs. long-term bets

## SCAMPER Method

SCAMPER is a checklist for transforming existing ideas:

### S - Substitute
*What can be replaced?*

| Prompt | Example |
|--------|---------|
| Different model? | BERT → GPT-4 |
| Different data? | Text → Code |
| Different task? | Classification → Generation |
| Different metric? | Accuracy → Efficiency |

### C - Combine
*What can be merged?*

| Prompt | Example |
|--------|---------|
| Combine methods? | RL + Language Models |
| Combine modalities? | Vision + Language |
| Combine tasks? | Multi-task learning |
| Combine datasets? | Domain adaptation |

### A - Adapt
*What can be borrowed from elsewhere?*

| Prompt | Example |
|--------|---------|
| From another field? | Physics → ML theory |
| From another domain? | Vision → NLP |
| From industry? | Production systems → Research |
| From nature? | Biological systems → Algorithms |

### M - Modify/Magnify/Minimize
*What can be changed in scale or intensity?*

| Prompt | Example |
|--------|---------|
| Make bigger? | Scale up model/data |
| Make smaller? | Efficient/compressed models |
| More extreme? | Harder benchmarks |
| More subtle? | Fine-grained evaluation |

### P - Put to Other Uses
*What else could this be used for?*

| Prompt | Example |
|--------|---------|
| Different application? | Translation → Summarization |
| Different audience? | Researchers → Practitioners |
| Different constraint? | Accuracy → Latency |

### E - Eliminate
*What can be removed?*

| Prompt | Example |
|--------|---------|
| Remove component? | Attention without position |
| Remove assumption? | Without labeled data |
| Remove constraint? | Without domain restriction |

### R - Reverse/Rearrange
*What can be reordered or inverted?*

| Prompt | Example |
|--------|---------|
| Reverse process? | Generation → Understanding |
| Opposite approach? | Top-down → Bottom-up |
| Different order? | Pre-train → Fine-tune vs opposite |

## Morphological Analysis

Systematically explore combinations of dimensions.

### Step 1: Identify Dimensions
List key aspects of your research area:

| Dimension | Options |
|-----------|---------|
| Task | Classification, Generation, Ranking |
| Model | Transformer, RNN, MLP |
| Data | Text, Code, Multi-modal |
| Scale | Small, Medium, Large |
| Supervision | Supervised, Self-supervised, RL |

### Step 2: Generate Combinations
Create a matrix and explore intersections:

```
Task × Model × Data × Scale × Supervision
= Many possible combinations
```

### Step 3: Evaluate Combinations
For each interesting combination:
- [ ] Is it novel?
- [ ] Is it feasible?
- [ ] Is it interesting?
- [ ] Does it address a gap?

### Template

```markdown
## Morphological Analysis: [Topic]

### Dimensions
1. [Dimension 1]: [Option A, Option B, Option C]
2. [Dimension 2]: [Option A, Option B, Option C]
3. [Dimension 3]: [Option A, Option B, Option C]

### Promising Combinations
| D1 | D2 | D3 | Why Interesting |
|----|----|----|-----------------|
| | | | |

### Selected Ideas
1. [Combination]: [Why pursue this]
```

## Cross-Domain Analogies

Find inspiration from analogous problems in other fields.

### Process

1. **Abstract your problem**: What is it fundamentally about?
2. **Find analogies**: What other fields face similar challenges?
3. **Study solutions**: How do they address it?
4. **Transfer insights**: How might their solutions apply?

### Analogy Sources

| Your Problem | Analogous Field | Potential Insight |
|--------------|-----------------|-------------------|
| Scaling | Biology (growth) | Allometric scaling laws |
| Optimization | Physics (annealing) | Simulated annealing |
| Attention | Psychology (cognition) | Selective attention |
| Memory | Neuroscience | Working memory |
| Robustness | Engineering | Fault tolerance |
| Learning | Education | Curriculum learning |

### Template

```markdown
## Cross-Domain Analogy

### Our Problem
[Description of the challenge]

### Analogous Problem
**Field**: [Field name]
**Problem**: [Their version of the challenge]
**Solution**: [How they address it]

### Transfer Opportunity
[How their insight might apply to ML]

### Research Idea
[Concrete research direction]
```

## Assumption Reversal

Challenge fundamental assumptions.

### Process

1. List assumptions in current approaches
2. For each assumption, ask "What if the opposite were true?"
3. Explore implications of reversals

### Template

```markdown
## Assumption Reversal: [Topic]

### Current Assumptions
1. [Assumption 1]
2. [Assumption 2]
3. [Assumption 3]

### Reversals
| Assumption | Reversal | Implication |
|------------|----------|-------------|
| More data is better | Less data could be better | Data efficiency research |
| Bigger models are better | Smaller could be better | Efficient architectures |
| Pre-training helps | Training from scratch | Task-specific models |
```

## Problem Reframing

View the problem from different angles.

### Perspectives

| Perspective | Question |
|-------------|----------|
| **User** | What does the end user actually need? |
| **System** | What are the computational constraints? |
| **Data** | What data is actually available? |
| **Theory** | What would a theoretical analysis reveal? |
| **Ethics** | What are the societal implications? |

### Reframing Prompts

- "Instead of solving X, what if we solved Y?"
- "What problem are we actually trying to solve?"
- "Who else has this problem?"
- "What would make this problem go away?"
- "What would a 10x better solution look like?"

## Idea Evaluation

After generating ideas, evaluate systematically.

### Criteria

| Criterion | Score (1-5) | Notes |
|-----------|-------------|-------|
| Novelty | | Is this new? |
| Impact | | Would this matter? |
| Feasibility | | Can we do this? |
| Clarity | | Is the idea clear? |
| Fit | | Does it match our skills/resources? |

### Quick Feasibility Check

- [ ] Do we have/can we get the data?
- [ ] Do we have the compute?
- [ ] Do we have the expertise?
- [ ] Can we do this in our timeframe?
- [ ] Is there a clear evaluation?

## References

See `references/` folder for:
- `brainstorming_methods.md`: Additional ideation techniques
