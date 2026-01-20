# Paper Prioritization Guide

## Quick Assessment Framework

When reviewing search results, evaluate each paper on these dimensions:

### Relevance Assessment

**Direct Relevance** (Score 3):
- Addresses your exact research question
- Uses same task/domain/method
- Must read and cite

**Indirect Relevance** (Score 2):
- Related methodology or task
- Applicable insights or techniques
- Should read abstract + methods

**Tangential Relevance** (Score 1):
- Background or context only
- Different task but shared concepts
- Skim for citations

**Not Relevant** (Score 0):
- Different problem entirely
- No applicable insights
- Skip

### Impact Indicators

| Indicator | High Impact | Low Impact |
|-----------|-------------|------------|
| Citations | 100+ in 2 years | <10 total |
| Venue | Tier 1 conference/journal | Workshop/arXiv only |
| Authors | Known researchers in field | Unknown |
| Code | Official repo, many stars | No code |
| Follow-ups | Many citing papers | Few citations |

## Reading Priority Matrix

| Relevance | Citation Impact | Priority | Action |
|-----------|-----------------|----------|--------|
| High | High | 1 (Critical) | Read fully, cite definitely |
| High | Low | 2 (Important) | Read fully, may be recent |
| Medium | High | 3 (Context) | Read abstract + key sections |
| Medium | Low | 4 (Optional) | Skim if time permits |
| Low | Any | 5 (Skip) | Don't read |

## Time-Efficient Reading

### For Priority 1-2 Papers (Full Read)
1. Abstract (2 min)
2. Introduction - last paragraph for contributions (3 min)
3. Method section (10-15 min)
4. Experiments - tables and figures first (10 min)
5. Discussion/Conclusion (3 min)
6. Related Work (skim, 5 min)

### For Priority 3 Papers (Partial Read)
1. Abstract (2 min)
2. Introduction - contributions only (2 min)
3. Method - key equations/algorithms (5 min)
4. Results - main table only (3 min)

### For Priority 4 Papers (Skim)
1. Abstract (1 min)
2. Figures/tables (2 min)
3. Conclusion (1 min)

## Note-Taking Template

For each paper you read:

```markdown
## [Paper Title] ([Year])

**Authors**: [Names]
**Venue**: [Conference/Journal]
**URL**: [Link]

### Key Contribution
[1-2 sentences]

### Method Summary
[2-3 sentences]

### Key Results
- [Result 1]
- [Result 2]

### Relevance to Our Work
[How does this relate to our research?]

### Potential Citations
- [Specific claim we could cite this for]
```

## Red Flags to Watch For

### Quality Concerns
- No peer review (arXiv only, years old)
- Extraordinary claims without strong evidence
- Missing baselines or unfair comparisons
- No code or reproducibility info
- Predatory journal/conference

### Relevance Concerns
- Different domain than appears from title
- Outdated methods (superseded by newer work)
- Specific to narrow application not relevant to us

## Building Citation List

### Must Cite
- Papers you directly extend or compare against
- Foundational methods you use
- Seminal papers defining the problem

### Should Cite
- State-of-the-art approaches
- Related methods in adjacent areas
- Datasets/benchmarks you use

### May Cite
- Background context
- Alternative approaches you considered
- Historical development

### Don't Cite
- Irrelevant work
- Superseded methods
- Poor quality work
