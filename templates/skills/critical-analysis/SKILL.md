---
name: critical-analysis
description: Evaluate research quality using frameworks like GRADE, bias detection, and logical analysis. Use when assessing paper quality, evaluating claims, or reviewing evidence strength.
---

# Critical Analysis

Frameworks for evaluating research quality and evidence strength.

## When to Use

- Assessing quality of papers during literature review
- Evaluating strength of claims
- Identifying biases in research
- Reviewing your own work critically
- Preparing rebuttals or responses

## GRADE Framework (Adapted for ML)

GRADE (Grading of Recommendations, Assessment, Development and Evaluations) adapted for ML research.

### Evidence Quality Levels

| Level | Definition | ML Example |
|-------|------------|------------|
| **High** | Very confident the true effect is close to estimate | Large-scale, well-designed study with multiple benchmarks, ablations, statistical significance |
| **Moderate** | Moderately confident; true effect likely close to estimate | Good methodology with some limitations in scope or evaluation |
| **Low** | Limited confidence; true effect may be substantially different | Significant methodological concerns or limited evaluation |
| **Very Low** | Very little confidence; true effect likely substantially different | Major flaws or insufficient evidence |

### Factors That Lower Quality

| Factor | Description | Example |
|--------|-------------|---------|
| **Risk of bias** | Methodological flaws | Unfair baseline comparisons, p-hacking |
| **Inconsistency** | Results vary across conditions | Works on one dataset but not others |
| **Indirectness** | Evidence doesn't match question | Tested on different task than claimed |
| **Imprecision** | Wide confidence intervals | Single run, no error bars |
| **Publication bias** | Selective reporting | Only positive results shown |

### Factors That Raise Quality

| Factor | Description | Example |
|--------|-------------|---------|
| **Large effect** | Clear, substantial improvement | >10% improvement over SOTA |
| **Dose-response** | Consistent relationship | Improvement scales with X |
| **Confounds addressed** | Alternative explanations ruled out | Ablations, controls |

### Assessment Template

```markdown
## GRADE Assessment: [Paper]

### Initial Rating
[ ] High (well-designed study)
[ ] Moderate (some limitations)
[ ] Low (significant concerns)
[ ] Very Low (major flaws)

### Downgrade Factors
- [ ] Risk of bias: [Description]
- [ ] Inconsistency: [Description]
- [ ] Indirectness: [Description]
- [ ] Imprecision: [Description]
- [ ] Publication bias: [Description]

### Upgrade Factors
- [ ] Large effect: [Description]
- [ ] Dose-response: [Description]
- [ ] Confounds addressed: [Description]

### Final Rating
[Level] because [reasoning]
```

## Bias Detection

### Types of Bias in ML Research

| Bias Type | Description | How to Detect |
|-----------|-------------|---------------|
| **Selection bias** | Non-representative data/models | Check data sources, model selection criteria |
| **Confirmation bias** | Favoring supporting evidence | Look for missing negative results |
| **Survivorship bias** | Only successful examples shown | Ask about failed attempts |
| **Anchoring bias** | Over-relying on initial results | Check if conclusions change with more data |
| **Availability bias** | Using easily accessible options | Are baselines convenient or appropriate? |

### Experimental Bias Checklist

- [ ] **Data leakage**: Test data seen during training?
- [ ] **Hyperparameter selection**: Tuned on test set?
- [ ] **Baseline fairness**: Same compute budget for baselines?
- [ ] **Cherry-picking**: Best-case results only?
- [ ] **P-hacking**: Multiple tests without correction?
- [ ] **HARKing**: Hypotheses generated after results?

### Reporting Bias Checklist

- [ ] **Selective metrics**: Only favorable metrics shown?
- [ ] **Selective datasets**: Only favorable datasets?
- [ ] **Selective examples**: Only successful cases?
- [ ] **Buried failures**: Limitations minimized?

## Statistical Validity

### Common Statistical Issues

| Issue | Description | Red Flag |
|-------|-------------|----------|
| **No significance testing** | No p-values or confidence intervals | "Method A is better" with no stats |
| **Multiple comparisons** | Many tests without correction | Many experiments, no Bonferroni |
| **Single run** | No variance estimate | Results without ± |
| **Wrong test** | Inappropriate statistical test | Paired test for unpaired data |
| **Misinterpretation** | Conflating significance and importance | "Statistically significant" but tiny effect |

### Statistical Checklist

- [ ] Sample size appropriate
- [ ] Multiple runs with different seeds
- [ ] Error bars or confidence intervals
- [ ] Appropriate statistical test used
- [ ] Multiple comparison correction (if applicable)
- [ ] Effect size reported (not just p-values)

## Logical Fallacy Detection

### Common Fallacies in ML Papers

| Fallacy | Description | Example |
|---------|-------------|---------|
| **Appeal to novelty** | New = better | "Our novel method..." |
| **Appeal to complexity** | Complex = better | More parameters = better |
| **False dichotomy** | Only two options | "Either scale or architecture" |
| **Hasty generalization** | Few examples → general claim | One dataset → "generally better" |
| **Moving goalposts** | Changing success criteria | Switching metrics when losing |
| **Straw man** | Misrepresenting baseline | Weakened baseline comparison |
| **Texas sharpshooter** | Pattern from randomness | Post-hoc metric selection |

### Argument Analysis

For each major claim:
1. **Identify the claim**: What exactly is being stated?
2. **Find the evidence**: What supports it?
3. **Evaluate the link**: Does evidence actually support claim?
4. **Check assumptions**: What's taken for granted?
5. **Consider alternatives**: What else could explain this?

## Critical Questions by Section

### For Claims
- Is this claim clearly stated?
- Is it testable?
- What evidence supports it?
- What would falsify it?
- Are there alternative explanations?

### For Methods
- Could this be reproduced?
- Are assumptions stated?
- Are design choices justified?
- What are the limitations?

### For Experiments
- Are baselines appropriate?
- Is evaluation fair?
- Is variance reported?
- Are ablations thorough?
- Could results be cherry-picked?

### For Results
- Do results support claims?
- Are effects meaningful (not just significant)?
- Do results generalize?
- Are negative results reported?

## Critical Reading Template

```markdown
## Critical Analysis: [Paper Title]

### Main Claims
1. [Claim 1]
2. [Claim 2]
3. [Claim 3]

### Evidence Assessment

| Claim | Evidence | Strength | Issues |
|-------|----------|----------|--------|
| [Claim 1] | [Evidence] | [Strong/Moderate/Weak] | [Issues] |

### Methodology Concerns
- [ ] [Concern 1]
- [ ] [Concern 2]

### Statistical Concerns
- [ ] [Concern 1]
- [ ] [Concern 2]

### Potential Biases
- [ ] [Bias 1]
- [ ] [Bias 2]

### Alternative Explanations
1. [Alternative 1]
2. [Alternative 2]

### Overall Assessment
**Quality**: [High/Moderate/Low/Very Low]
**Confidence in claims**: [High/Medium/Low]
**Key limitation**: [Most important issue]
```

## Quality Checklist

When critically analyzing any work:

- [ ] Claims are clearly identified
- [ ] Evidence for each claim is assessed
- [ ] Methodology is scrutinized
- [ ] Statistics are evaluated
- [ ] Biases are considered
- [ ] Alternative explanations explored
- [ ] Logical reasoning checked
- [ ] Limitations are identified

## References

See `references/` folder for:
- `quality_frameworks.md`: Additional quality assessment frameworks
