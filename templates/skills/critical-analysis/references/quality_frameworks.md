# Quality Assessment Frameworks

## Reproducibility Checklist

Based on NeurIPS reproducibility standards.

### For All Papers

- [ ] Model/algorithm clearly described
- [ ] All assumptions clearly stated
- [ ] Theoretical contributions include proofs
- [ ] Datasets clearly described
- [ ] Code/data availability stated

### For Algorithm Papers

- [ ] Pseudocode provided
- [ ] Complexity analysis included
- [ ] All hyperparameters specified
- [ ] Hyperparameter selection method described
- [ ] Training details complete (LR, epochs, etc.)

### For Empirical Papers

- [ ] Computing infrastructure described
- [ ] Average runtime provided
- [ ] Number of parameters reported
- [ ] Statistical significance addressed
- [ ] Multiple runs with variance

### Data Availability

| Level | Description |
|-------|-------------|
| **Full** | Data publicly available |
| **Partial** | Subset or derived data available |
| **Restricted** | Available upon request |
| **None** | Data not available |

### Code Availability

| Level | Description |
|-------|-------------|
| **Complete** | All code for reproduction |
| **Partial** | Core methods only |
| **Pseudo** | Pseudocode only |
| **None** | No code provided |

---

## Internal Validity Assessment

Does the study measure what it claims to measure?

### Threats to Internal Validity

| Threat | Description | How to Detect |
|--------|-------------|---------------|
| **Data leakage** | Test data in training | Check preprocessing pipeline |
| **Confounding** | Other factors explain results | Look for uncontrolled variables |
| **Instrumentation** | Measurement changes | Check evaluation consistency |
| **Selection** | Non-random assignment | Review experimental design |
| **History** | External events affect results | Consider temporal factors |

### Mitigation Strategies

| Threat | Mitigation |
|--------|------------|
| Data leakage | Strict train/test separation |
| Confounding | Control experiments, ablations |
| Instrumentation | Standardized evaluation |
| Selection | Random assignment |
| History | Contemporary controls |

---

## External Validity Assessment

Do results generalize beyond the study?

### Threats to External Validity

| Threat | Description | Check |
|--------|-------------|-------|
| **Population** | Sample ≠ target population | Is data representative? |
| **Ecological** | Lab ≠ real world | Are conditions realistic? |
| **Temporal** | Results may not persist | Has time been a factor? |
| **Setting** | Environment-specific | Multiple settings tested? |

### Generalization Checklist

- [ ] Multiple datasets used
- [ ] Different data distributions tested
- [ ] Real-world vs. benchmark comparison
- [ ] Cross-domain evaluation
- [ ] Different model sizes tested

---

## Claim Strength Assessment

### Claim Categories

| Type | Strength | Requirement |
|------|----------|-------------|
| **Definitive** | "X causes Y" | Controlled experiment, randomization |
| **Correlational** | "X is associated with Y" | Statistical relationship shown |
| **Descriptive** | "X exists/occurs" | Observation documented |
| **Speculative** | "X might..." | Theoretical reasoning |

### Evidence-Claim Match

| Claim Type | Required Evidence |
|------------|-------------------|
| "Better than SOTA" | Direct comparison, same conditions |
| "Generalizes to X" | Evaluation on X |
| "Robust to Y" | Testing under Y conditions |
| "Efficient" | Compute/memory measurements |
| "Novel" | Related work comparison |

---

## Comparison Quality Framework

### Fair Comparison Criteria

| Criterion | Questions |
|-----------|-----------|
| **Same data** | Identical train/test splits? |
| **Same preprocessing** | Same tokenization/normalization? |
| **Same compute** | Equal hyperparameter search? |
| **Same metrics** | Identical evaluation protocol? |
| **Tuned baselines** | Baselines properly optimized? |
| **Contemporary** | Recent baselines included? |

### Comparison Red Flags

- Using outdated baselines
- Different compute budgets
- Non-standard evaluation
- Missing error bars
- Comparing to weakened baselines

---

## Ablation Study Quality

### Components of Good Ablations

1. **Component ablation**: Remove each component
2. **Alternative ablation**: Replace with alternatives
3. **Sensitivity analysis**: Vary hyperparameters
4. **Interaction analysis**: Test component combinations

### Ablation Quality Checklist

- [ ] All major components tested
- [ ] Reasonable alternatives compared
- [ ] Results statistically significant
- [ ] Analysis explains findings
- [ ] Negative results reported

---

## Limitation Assessment

### Limitation Categories

| Category | Examples |
|----------|----------|
| **Scope** | Limited domains, languages, modalities |
| **Scale** | Limited model size, data size |
| **Compute** | High resource requirements |
| **Data** | Data availability, bias |
| **Methodology** | Design assumptions, simplifications |
| **Evaluation** | Benchmark limitations |

### Limitation Disclosure Quality

| Level | Description |
|-------|-------------|
| **Comprehensive** | All significant limitations discussed |
| **Adequate** | Major limitations mentioned |
| **Minimal** | Brief mention of limitations |
| **Missing** | No limitations discussed |

---

## Quick Quality Assessment

### Green Flags (Good Signs)

- [ ] Multiple benchmarks
- [ ] Multiple baselines
- [ ] Statistical significance reported
- [ ] Ablation studies
- [ ] Error analysis
- [ ] Limitations discussed
- [ ] Code/data available
- [ ] Reproducibility details

### Yellow Flags (Caution)

- [ ] Only one dataset
- [ ] No statistical tests
- [ ] Single baseline
- [ ] No ablations
- [ ] Vague methodology

### Red Flags (Serious Concerns)

- [ ] Outdated baselines only
- [ ] Potential data leakage
- [ ] No reproducibility info
- [ ] Extraordinary claims
- [ ] No limitations acknowledged
- [ ] Unfair comparisons

---

## Scoring Rubric Summary

### Overall Quality Score

| Score | Criteria |
|-------|----------|
| **A** | Comprehensive evaluation, fair comparisons, reproducible, limitations acknowledged |
| **B** | Good evaluation with minor gaps, mostly fair comparisons |
| **C** | Adequate evaluation, some methodology concerns |
| **D** | Significant evaluation gaps, multiple concerns |
| **F** | Major flaws, unreliable conclusions |

### Decision Guide

| Score | Recommendation |
|-------|----------------|
| A | Trust findings, cite confidently |
| B | Trust with caveats, cite with context |
| C | Treat as preliminary, verify independently |
| D | Significant skepticism, verify before using |
| F | Do not rely on findings |
