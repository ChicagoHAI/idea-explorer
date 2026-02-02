# Statistical Test Selection Guide

## Complete Decision Guide

### Step 1: What's Your Research Question?

| Question Type | Direction |
|---------------|-----------|
| Is there a difference between groups? | Comparison tests |
| Is there a relationship between variables? | Correlation/regression |
| Can we predict an outcome? | Regression analysis |
| Is the distribution different from expected? | Goodness-of-fit tests |

### Step 2: What Type of Data?

| Measurement Level | Examples | Tests |
|-------------------|----------|-------|
| **Nominal** | Categories (color, type) | Chi-square, Fisher's exact |
| **Ordinal** | Rankings (1st, 2nd, 3rd) | Non-parametric tests |
| **Interval** | Temperature, dates | Parametric or non-parametric |
| **Ratio** | Height, weight, counts | Parametric or non-parametric |

### Step 3: How Many Variables and Groups?

| Variables | Groups | Test Category |
|-----------|--------|---------------|
| 1 DV, 2 groups | Independent | Two-sample comparison |
| 1 DV, 2 groups | Related | Paired comparison |
| 1 DV, 3+ groups | Independent | One-way ANOVA family |
| 1 DV, 3+ groups | Related | Repeated measures |
| 2+ DVs | Any | Multivariate tests |
| 1 IV → 1 DV | - | Simple regression |
| Multiple IVs → 1 DV | - | Multiple regression |

---

## Comparison Tests

### Two Independent Groups

| Parametric | Non-parametric | Use When |
|------------|----------------|----------|
| Independent t-test | Mann-Whitney U | Two separate groups |
| Welch's t-test | - | Unequal variances |

**Independent t-test assumptions**:
- Normal distribution (or n > 30)
- Homogeneity of variance
- Independent observations

**When to use Mann-Whitney U**:
- Ordinal data
- Non-normal distributions
- Small samples (n < 30)
- Outliers present

### Two Related Groups

| Parametric | Non-parametric | Use When |
|------------|----------------|----------|
| Paired t-test | Wilcoxon signed-rank | Same subjects, two conditions |

**Paired t-test assumptions**:
- Differences are normally distributed
- Observations are paired

**When to use Wilcoxon**:
- Non-normal difference distribution
- Ordinal data
- Small samples

### Three or More Independent Groups

| Parametric | Non-parametric | Use When |
|------------|----------------|----------|
| One-way ANOVA | Kruskal-Wallis | 3+ separate groups |

**ANOVA assumptions**:
- Normality within groups
- Homogeneity of variance
- Independent observations

**Post-hoc tests** (if ANOVA significant):
- Tukey HSD: All pairwise comparisons
- Dunnett's: Compare to control
- Scheffé: Conservative, any comparisons
- Games-Howell: Unequal variances

### Three or More Related Groups

| Parametric | Non-parametric | Use When |
|------------|----------------|----------|
| Repeated measures ANOVA | Friedman test | Same subjects, 3+ conditions |

---

## Correlation Tests

### Two Continuous Variables

| Test | Use When |
|------|----------|
| Pearson's r | Linear relationship, normal data |
| Spearman's ρ | Monotonic relationship, ordinal data |
| Kendall's τ | Small samples, many ties |

### Interpreting Correlations

| r Value | Interpretation |
|---------|----------------|
| 0.00-0.19 | Very weak |
| 0.20-0.39 | Weak |
| 0.40-0.59 | Moderate |
| 0.60-0.79 | Strong |
| 0.80-1.00 | Very strong |

---

## Regression Tests

### Choosing Regression Type

| Outcome Variable | Model |
|------------------|-------|
| Continuous | Linear regression |
| Binary (0/1) | Logistic regression |
| Count | Poisson regression |
| Ordinal | Ordinal regression |
| Multinomial | Multinomial logistic |

### Regression Assumptions

**Linear regression**:
1. Linearity
2. Independence of errors
3. Homoscedasticity (constant variance)
4. Normality of residuals
5. No multicollinearity (multiple regression)

**Logistic regression**:
1. Binary outcome
2. Independence of observations
3. No multicollinearity
4. Large sample size (rule: 10 events per predictor)

---

## Categorical Data Tests

### Single Categorical Variable

| Test | Use When |
|------|----------|
| Chi-square goodness-of-fit | Compare to expected distribution |
| Binomial test | Two categories, compare to probability |

### Two Categorical Variables

| Test | Use When |
|------|----------|
| Chi-square test of independence | Large sample (all expected ≥ 5) |
| Fisher's exact test | Small sample or low expected counts |
| McNemar's test | Paired/matched data |

---

## Assumptions Testing

### Normality Tests

| Test | Best For |
|------|----------|
| Shapiro-Wilk | Small to moderate samples (n < 50) |
| Kolmogorov-Smirnov | Larger samples |
| Anderson-Darling | General purpose |

```python
from scipy import stats

# Shapiro-Wilk
stat, p = stats.shapiro(data)
print(f"Shapiro-Wilk: W={stat:.4f}, p={p:.4f}")
# p > 0.05 suggests normality
```

### Homogeneity of Variance

| Test | Use For |
|------|---------|
| Levene's test | General purpose, robust |
| Bartlett's test | Normal distributions only |

```python
# Levene's test
stat, p = stats.levene(group1, group2, center='median')
print(f"Levene's: W={stat:.4f}, p={p:.4f}")
# p > 0.05 suggests equal variances
```

---

## Sample Size Quick Reference

### Minimum Sample Sizes

| Test | Minimum n per Group |
|------|---------------------|
| t-test | 20-30 |
| ANOVA | 20-30 per group |
| Correlation | 30-50 |
| Regression | 10-20 per predictor |
| Chi-square | Expected ≥ 5 per cell |
| Non-parametric | 10-15 |

### Power Analysis Formulas

For 80% power, α = 0.05:

| Effect Size | Sample Size (per group) |
|-------------|-------------------------|
| Small (d=0.2) | ~400 |
| Medium (d=0.5) | ~65 |
| Large (d=0.8) | ~25 |

---

## Quick Reference Table

| Comparison Type | Normal Data | Non-normal Data |
|-----------------|-------------|-----------------|
| 2 independent groups | Independent t-test | Mann-Whitney U |
| 2 related groups | Paired t-test | Wilcoxon signed-rank |
| 3+ independent groups | One-way ANOVA | Kruskal-Wallis |
| 3+ related groups | Repeated measures ANOVA | Friedman |
| Correlation | Pearson's r | Spearman's ρ |
| 2 categorical variables | Chi-square | Fisher's exact |
