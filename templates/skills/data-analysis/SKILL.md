---
name: data-analysis
description: Conduct exploratory data analysis and statistical testing with test selection guidance. Use when exploring datasets, selecting statistical tests, performing power analysis, or preparing results for publication.
---

# Data Analysis

Guidance for exploratory data analysis and statistical testing.

## When to Use

- Exploring new datasets
- Selecting appropriate statistical tests
- Performing power analysis
- Reporting results in papers
- Validating experimental results

## Exploratory Data Analysis (EDA)

### EDA Workflow

1. **Load and Inspect**: Basic data structure
2. **Summarize**: Descriptive statistics
3. **Visualize**: Distributions and relationships
4. **Identify Issues**: Missing data, outliers
5. **Document Findings**: Key insights

### Initial Inspection

```python
# Basic checks
df.shape          # Dimensions
df.dtypes         # Data types
df.head()         # First rows
df.describe()     # Summary stats
df.isnull().sum() # Missing values
```

### Key Questions to Answer

| Question | What to Check |
|----------|---------------|
| What's the size? | Rows, columns, data types |
| Any missing data? | Null counts, patterns |
| What's the distribution? | Histograms, descriptive stats |
| Any outliers? | Box plots, z-scores |
| Any relationships? | Correlations, scatter plots |
| Any patterns? | Trends, clusters, groups |

### Visualization Guide

| Data Type | Visualization |
|-----------|---------------|
| Single continuous | Histogram, density plot, box plot |
| Single categorical | Bar chart, pie chart |
| Two continuous | Scatter plot, line plot |
| Two categorical | Grouped bar chart, heatmap |
| Continuous + categorical | Box plot by group, violin plot |
| Time series | Line plot with time axis |

## Statistical Test Selection

### Decision Tree

```
Question: What are you trying to do?
│
├─ Compare groups
│   │
│   ├─ How many groups?
│   │   ├─ 2 groups → See "Two Group Comparisons"
│   │   └─ 3+ groups → See "Multiple Group Comparisons"
│   │
│   └─ Related or independent?
│       ├─ Independent (different subjects)
│       └─ Related (same subjects, before/after)
│
├─ Examine relationships
│   ├─ Two variables → Correlation, regression
│   └─ Multiple variables → Multiple regression
│
└─ Test proportions
    └─ Chi-square test
```

### Two Group Comparisons

| Data Type | Independent Groups | Related Groups |
|-----------|-------------------|----------------|
| **Normal** | Independent t-test | Paired t-test |
| **Non-normal** | Mann-Whitney U | Wilcoxon signed-rank |

### Multiple Group Comparisons

| Data Type | Independent Groups | Related Groups |
|-----------|-------------------|----------------|
| **Normal** | One-way ANOVA | Repeated measures ANOVA |
| **Non-normal** | Kruskal-Wallis | Friedman test |

### Checking Assumptions

**Normality Tests**:
- Shapiro-Wilk (n < 50)
- Kolmogorov-Smirnov (n ≥ 50)
- Visual: Q-Q plot

**Homogeneity of Variance**:
- Levene's test
- Visual: Box plots by group

**Independence**:
- By experimental design
- Durbin-Watson (for residuals)

### When Assumptions Fail

| Violation | Solution |
|-----------|----------|
| Non-normality | Non-parametric test, transformation |
| Unequal variance | Welch's t-test, transformation |
| Non-independence | Mixed-effects model |
| Outliers | Robust methods, removal (with justification) |

## Effect Sizes

### Why Effect Sizes Matter

- p-values tell you if effect exists, not how big
- Effect sizes quantify the magnitude
- Required for power analysis
- Better for meta-analysis

### Common Effect Sizes

| Measure | Context | Interpretation |
|---------|---------|----------------|
| **Cohen's d** | Two means | 0.2=small, 0.5=medium, 0.8=large |
| **Pearson's r** | Correlation | 0.1=small, 0.3=medium, 0.5=large |
| **Eta-squared** | ANOVA | 0.01=small, 0.06=medium, 0.14=large |
| **Odds ratio** | Categorical | 1.5=small, 2.5=medium, 4=large |

### Computing Effect Sizes

```python
# Cohen's d for two groups
import numpy as np

def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std
```

## Power Analysis

### Key Concepts

| Term | Definition |
|------|------------|
| **Power** | Probability of detecting true effect (1-β) |
| **α (alpha)** | False positive rate (typically 0.05) |
| **β (beta)** | False negative rate (typically 0.20) |
| **Effect size** | Magnitude of effect |
| **Sample size** | Number of observations |

### Power Analysis Uses

1. **A priori**: Before study, determine needed sample size
2. **Post hoc**: After study, calculate achieved power
3. **Sensitivity**: Given n and power, what effect detectable?

### Sample Size Calculation

```python
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()

# Sample size for t-test
n = analysis.solve_power(
    effect_size=0.5,    # Cohen's d
    alpha=0.05,         # Significance level
    power=0.80,         # Desired power
    ratio=1.0,          # n2/n1
    alternative='two-sided'
)
```

### Power Guidelines

| Power | Interpretation |
|-------|----------------|
| < 0.50 | Inadequate |
| 0.50-0.70 | Low |
| 0.70-0.80 | Moderate |
| ≥ 0.80 | Adequate (standard target) |
| ≥ 0.90 | High |

## Multiple Comparisons

### The Problem

- Each test has α chance of false positive
- Multiple tests inflate false positive rate
- Family-wise error rate: 1-(1-α)^n

### Correction Methods

| Method | When to Use | Strictness |
|--------|-------------|------------|
| **Bonferroni** | Few comparisons | Most conservative |
| **Holm** | Few comparisons | Less conservative |
| **Benjamini-Hochberg** | Many comparisons | Controls FDR |
| **Tukey HSD** | Post-hoc ANOVA | Common choice |

### Applying Corrections

```python
from scipy import stats
import numpy as np

# Bonferroni
adjusted_alpha = 0.05 / num_tests

# Holm-Bonferroni
from statsmodels.stats.multitest import multipletests
reject, pvals_corrected, _, _ = multipletests(pvals, method='holm')

# Benjamini-Hochberg (FDR)
reject, pvals_corrected, _, _ = multipletests(pvals, method='fdr_bh')
```

## Reporting Results

### APA Format

**t-test**:
```
t(df) = X.XX, p = .XXX, d = X.XX
```
Example: t(45) = 2.34, p = .023, d = 0.68

**ANOVA**:
```
F(df1, df2) = X.XX, p = .XXX, η² = .XX
```
Example: F(2, 87) = 4.56, p = .013, η² = .095

**Correlation**:
```
r(df) = .XX, p = .XXX
```
Example: r(48) = .42, p = .003

**Chi-square**:
```
χ²(df, N = n) = X.XX, p = .XXX
```
Example: χ²(2, N = 150) = 6.78, p = .034

### Reporting Guidelines

**Do**:
- Report exact p-values (not just < .05)
- Include effect sizes
- Report confidence intervals
- Describe what was tested

**Don't**:
- Say "proved" or "significant difference" alone
- Report only significant results
- Cherry-pick tests
- Over-interpret p = .049 vs p = .051

### Results Table Format

```
Table 1: Comparison of Methods on Benchmark X

Method      Mean (SD)       95% CI          Effect Size
------------------------------------------------------
Baseline    75.2 (3.4)     [73.1, 77.3]    -
Method A    78.9 (2.8)*    [77.2, 80.6]    d = 0.52
Method B    81.4 (3.1)**   [79.5, 83.3]    d = 0.89

Note: * p < .05, ** p < .01 vs Baseline
```

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| P-hacking | Running tests until significant | Pre-register analysis |
| HARKing | Hypothesizing after results known | State hypotheses before |
| Multiple comparisons | Inflated false positives | Apply correction |
| Pseudo-replication | Non-independent samples | Mixed-effects models |
| Ignoring effect sizes | Significant ≠ important | Report effect sizes |

## Quality Checklist

- [ ] Research questions clearly stated
- [ ] Appropriate test selected and justified
- [ ] Assumptions checked
- [ ] Sample size justified (power analysis)
- [ ] Multiple comparisons corrected
- [ ] Effect sizes reported
- [ ] Confidence intervals included
- [ ] Results correctly interpreted
- [ ] Limitations acknowledged

## References

See `references/` folder for:
- `test_selection.md`: Detailed test selection guide
- `apa_reporting.md`: Complete APA reporting templates
