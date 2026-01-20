---
name: hypothesis-generation
description: Formulate research hypotheses using structured frameworks. Use when developing research questions, designing experiments, or planning studies with testable predictions.
---

# Hypothesis Generation

Structured frameworks for developing research hypotheses and experimental designs.

## When to Use

- Starting a new research project
- Developing research questions
- Planning experiments
- Generating testable predictions
- Exploring competing explanations

## Hypothesis Framework

### Good Hypothesis Characteristics

A strong research hypothesis should be:

1. **Specific**: Clear, precise statement
2. **Testable**: Can be validated with data
3. **Falsifiable**: Can potentially be proven wrong
4. **Grounded**: Based on prior knowledge/theory
5. **Novel**: Adds something new to the field

### Hypothesis Types

| Type | Description | Example |
|------|-------------|---------|
| **Descriptive** | Describes a phenomenon | "LLMs exhibit X behavior on task Y" |
| **Relational** | Proposes relationship | "Factor A correlates with outcome B" |
| **Causal** | Claims causation | "Intervention X causes improvement Y" |
| **Comparative** | Compares conditions | "Method A outperforms method B on task C" |
| **Mechanistic** | Explains how/why | "Effect X occurs because of mechanism Y" |

## Hypothesis Development Process

### Step 1: Identify the Gap

From your literature review, identify:
- What is known
- What is unknown or unclear
- What is contradictory

Document the gap:
```markdown
## Research Gap
**Known**: [What prior work has established]
**Unknown**: [What remains to be discovered]
**Our Focus**: [Which unknown we address]
```

### Step 2: Generate Initial Hypotheses

Use these prompts:
- "If [assumption] is true, then we should observe [prediction]"
- "Based on [theory/observation], we expect [outcome]"
- "Contrary to [current belief], we propose [alternative]"

Generate multiple hypotheses (aim for 3-5 initially).

### Step 3: Develop Competing Hypotheses

For each hypothesis, identify:
- **Alternative explanations**: What else could explain the same observation?
- **Null hypothesis**: What if there's no effect?
- **Opposite hypothesis**: What if the effect is reversed?

### Step 4: Operationalize

Convert abstract hypothesis to concrete, measurable terms:

| Abstract | Operationalized |
|----------|-----------------|
| "LLMs understand X" | "GPT-4 achieves >80% accuracy on benchmark Y" |
| "Method A is better" | "Method A improves F1 by >5% over baseline B" |
| "Training affects X" | "Models trained with X show Y behavior increase" |

### Step 5: Design Tests

For each hypothesis, define:
- **Data**: What data is needed?
- **Method**: How will you test?
- **Metrics**: What measures success/failure?
- **Threshold**: What counts as support/rejection?

## Competing Hypotheses Framework

### Template

```markdown
## Research Question
[Your main question]

### Hypothesis 1: [Name]
**Statement**: [Formal hypothesis]
**Rationale**: [Why this might be true]
**Prediction**: [What we expect to observe]
**Test**: [How to test]

### Hypothesis 2: [Alternative]
**Statement**: [Formal hypothesis]
**Rationale**: [Why this might be true]
**Prediction**: [What we expect to observe]
**Test**: [How to test]

### Hypothesis 3: [Null]
**Statement**: There is no significant effect
**Prediction**: No difference between conditions
**Test**: Statistical significance testing

### Decision Matrix
| Outcome | Supports H1 | Supports H2 | Supports H3 |
|---------|-------------|-------------|-------------|
| [Result A] | Yes | No | No |
| [Result B] | No | Yes | No |
| [Result C] | No | No | Yes |
```

## Experimental Design

### Variables

| Type | Definition | Example |
|------|------------|---------|
| **Independent (IV)** | What you manipulate | Model type, training data |
| **Dependent (DV)** | What you measure | Accuracy, F1, latency |
| **Controlled** | Held constant | Prompt template, temperature |
| **Confounding** | Could affect DV | Data contamination, model size |

### Design Types

**Between-subjects**: Different conditions get different treatments
- Pros: No carryover effects
- Cons: Need more samples, individual differences

**Within-subjects**: Same subject gets all treatments
- Pros: Controls individual differences
- Cons: Order effects, fatigue

**Factorial**: Multiple IVs crossed
- Pros: Tests interactions
- Cons: More conditions needed

### Control Strategies

1. **Baseline comparison**: Compare against known baseline
2. **Ablation study**: Remove components to test necessity
3. **Randomization**: Random assignment to conditions
4. **Counterbalancing**: Vary order across subjects/trials

## Prediction Documentation

### Template for Each Hypothesis

```markdown
## Hypothesis: [Name]

### Formal Statement
[If X, then Y under conditions Z]

### Background
[Why we think this might be true]

### Predictions

#### Primary Prediction
- **Measure**: [What to measure]
- **Expected outcome**: [Specific prediction]
- **Threshold for support**: [Quantitative criterion]

#### Secondary Predictions
1. [Additional prediction 1]
2. [Additional prediction 2]

### Potential Confounds
- [Confound 1]: [How to address]
- [Confound 2]: [How to address]

### What Would Falsify This?
[Specific outcomes that would reject hypothesis]
```

## Common Pitfalls

### Avoid These

1. **Vague hypotheses**: "Method A is good" → "Method A achieves >X on benchmark Y"
2. **Unfalsifiable claims**: "LLMs may sometimes..." → "LLMs will show X in condition Y"
3. **Post-hoc hypothesizing**: Generating hypothesis after seeing data
4. **Confirmation bias**: Only looking for supporting evidence
5. **Missing null hypothesis**: Not considering "no effect" possibility

### Warning Signs

- Hypothesis can explain any outcome
- No clear way to measure
- Based on single observation
- Ignores contradictory evidence
- No alternative hypotheses considered

## Quality Checklist

- [ ] Hypothesis is specific and clear
- [ ] Hypothesis is testable with available resources
- [ ] Hypothesis is falsifiable
- [ ] Hypothesis is grounded in prior work
- [ ] Alternative hypotheses identified
- [ ] Null hypothesis specified
- [ ] Variables operationalized
- [ ] Confounds identified and addressed
- [ ] Success/failure criteria defined
- [ ] Predictions documented before experimentation

## References

See `references/` folder for:
- `hypothesis_templates.md`: Templates for different research types
