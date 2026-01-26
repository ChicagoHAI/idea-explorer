# Paper Screening Guide

## Overview

Screening is the process of systematically evaluating papers to determine which should be included in your review. This guide provides criteria and decision frameworks for each screening stage.

## Stage 1: Title Screening

**Goal**: Quick relevance judgment based on title alone
**Time per paper**: ~5 seconds
**Expected reduction**: ~50%

### Decision Criteria

**Include** if title suggests:
- Same task/problem as your research
- Relevant methodology
- Related dataset or benchmark
- Important background concept

**Exclude** if title indicates:
- Completely different domain
- Unrelated task
- Wrong modality (e.g., images when you need text)
- Tutorial, survey, or workshop report (unless specifically seeking those)

**Maybe** if:
- Unclear from title
- Potentially related
- Need more information

### Common Pitfalls

- Don't exclude papers just because title uses different terminology
- Consider synonyms and related concepts
- When in doubt, mark as "Maybe"

## Stage 2: Abstract Screening

**Goal**: Evaluate relevance based on problem, method, and findings
**Time per paper**: 1-2 minutes
**Expected reduction**: ~50% of remaining

### Decision Framework

Read abstract looking for:

1. **Problem Statement**
   - Is this the same or related problem?
   - Same domain/application area?

2. **Method**
   - Relevant technique or approach?
   - Comparable methodology?

3. **Evaluation**
   - Related datasets/benchmarks?
   - Relevant metrics?

4. **Findings**
   - Insights applicable to your work?
   - Results to compare against?

### Scoring Rubric

| Score | Criteria | Decision |
|-------|----------|----------|
| 3 | Same problem + relevant method | Include |
| 2 | Related problem OR relevant method | Include |
| 1 | Tangentially related | Maybe/Exclude |
| 0 | Not relevant | Exclude |

### Red Flags

- Abstract doesn't mention core concepts
- Different task despite similar keywords
- Preliminary/incomplete work
- Retracted or superseded

## Stage 3: Full-Text Screening

**Goal**: Verify relevance and extract detailed information
**Time per paper**: 10-30 minutes
**Expected reduction**: ~20% of remaining

### Reading Strategy

1. **Quick scan** (2-3 min):
   - Introduction: last paragraph (contributions)
   - Figures and tables
   - Conclusion

2. **Targeted reading** (5-10 min):
   - Method section
   - Experimental setup
   - Key results

3. **Deep reading** (if highly relevant):
   - Full paper
   - Appendices
   - Related work section

### Exclusion Criteria

Exclude if:
- Method doesn't apply to your setting
- Evaluation is fundamentally different
- Quality issues (weak baselines, unfair comparisons)
- Superseded by newer work from same authors

### Information Extraction

For each included paper, record:

| Field | What to Extract |
|-------|-----------------|
| Problem | Formal problem definition |
| Method | Key algorithmic components |
| Data | Datasets, splits, preprocessing |
| Baselines | What they compare against |
| Metrics | Evaluation measures |
| Results | Main quantitative findings |
| Limitations | Acknowledged weaknesses |
| Relevance | Specific connection to your work |

## Quality Assessment

For papers that pass screening, assess quality:

### Methodology Quality

- [ ] Clear problem definition
- [ ] Justified design choices
- [ ] Reproducible description
- [ ] Appropriate baselines

### Experimental Quality

- [ ] Standard benchmarks or justified alternatives
- [ ] Statistical significance reported
- [ ] Multiple runs/seeds
- [ ] Ablation studies

### Presentation Quality

- [ ] Clear writing
- [ ] Informative figures
- [ ] Complete related work
- [ ] Honest limitations

## Decision Tree

```
START
  │
  ▼
[Title relevant?]
  │
  ├─ No ─────────────────────► EXCLUDE
  │
  ├─ Maybe ──┐
  │          │
  ├─ Yes ────┤
             │
             ▼
        [Read abstract]
             │
             ▼
        [Problem related?]
             │
             ├─ No ──────────► EXCLUDE
             │
             ├─ Yes ─────────┐
                             │
                             ▼
                        [Method applicable?]
                             │
                             ├─ No ──────► EXCLUDE
                             │
                             ├─ Maybe ───► Maybe pile
                             │
                             ├─ Yes ──────┐
                                          │
                                          ▼
                                     [Get full text]
                                          │
                                          ▼
                                     [Quality OK?]
                                          │
                                          ├─ No ───► EXCLUDE
                                          │
                                          ├─ Yes ──► INCLUDE
```

## Handling Edge Cases

### Paper is in a different language
- Check for English version or translation
- Include if machine translation is sufficient
- Exclude if quality loss is too great

### Paper is very recent (no citations yet)
- Apply same quality criteria
- May be highly relevant despite no citations
- Note recency in review

### Paper is from predatory venue
- Apply extra scrutiny
- Look for replication by reputable sources
- Consider excluding unless essential

### Multiple versions exist (arXiv + published)
- Use published version if available
- Note differences if significant
- Cite the published version

## Documentation

Track screening decisions for reproducibility:

```markdown
## Screening Log

| Paper ID | Title Screen | Abstract Screen | Full-Text | Reason |
|----------|--------------|-----------------|-----------|--------|
| paper_001 | Include | Include | Include | Key baseline |
| paper_002 | Include | Exclude | - | Different task |
| paper_003 | Exclude | - | - | Wrong domain |
```

## Tips for Efficiency

1. **Batch similar papers**: Screen related papers together
2. **Use keyboard shortcuts**: Quick include/exclude decisions
3. **Time-box**: Don't spend too long on borderline cases
4. **Revisit "maybe"**: Clear the maybe pile after initial pass
5. **Track time**: Monitor screening rate for planning
