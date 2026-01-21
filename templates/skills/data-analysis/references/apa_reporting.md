# APA-Style Results Reporting

## General Formatting Rules

### Numbers
- Use numerals for: 10 or higher, measurements, statistics, percentages
- Spell out: numbers below 10 (unless in series with higher numbers)
- Leading zero: Include for values < 1 (e.g., 0.05)
- Exception: No leading zero for values that can't exceed 1 (p = .03, r = .45)

### Decimal Places
| Statistic | Decimal Places |
|-----------|----------------|
| Percentages | 0-1 |
| Means, SDs | 2 |
| Correlations | 2 |
| Proportions | 2-3 |
| p-values | 3 (or < .001) |
| Effect sizes | 2-3 |

### Italics
Italicize:
- Statistical symbols: *t*, *F*, *p*, *N*, *n*, *M*, *SD*, *r*, *d*, η²
- Greek letters: α, β
- Abbreviations of statistics

---

## Test-Specific Reporting

### t-test

**Format**: *t*(df) = X.XX, *p* = .XXX, *d* = X.XX [95% CI: X.XX, X.XX]

**Independent samples**:
```
An independent-samples t-test revealed that the treatment group
(M = 82.5, SD = 8.3) scored significantly higher than the control
group (M = 75.2, SD = 9.1), t(48) = 2.84, p = .007, d = 0.81
[95% CI: 0.23, 1.39].
```

**Paired samples**:
```
A paired-samples t-test indicated that scores significantly increased
from pretest (M = 68.3, SD = 12.4) to posttest (M = 78.9, SD = 10.2),
t(24) = 4.21, p < .001, d = 0.95 [95% CI: 0.46, 1.44].
```

**Non-significant**:
```
An independent-samples t-test revealed no significant difference
between the treatment group (M = 76.2, SD = 8.4) and control group
(M = 74.8, SD = 9.2), t(48) = 0.56, p = .578, d = 0.16 [95% CI:
-0.40, 0.72].
```

### One-way ANOVA

**Format**: *F*(df₁, df₂) = X.XX, *p* = .XXX, η² = .XX

```
A one-way ANOVA revealed a significant effect of treatment condition
on test scores, F(2, 87) = 5.43, p = .006, η² = .111. Post-hoc Tukey
HSD tests indicated that Group A (M = 82.3, SD = 8.4) scored
significantly higher than Group C (M = 72.1, SD = 9.2), p = .004,
d = 1.16. No other pairwise differences were significant.
```

**With follow-up**:
```
Levene's test indicated equal variances, F(2, 87) = 1.23, p = .298.
A one-way ANOVA showed significant differences among groups,
F(2, 87) = 5.43, p = .006, η² = .111.
```

### Repeated Measures ANOVA

**Format**: *F*(df₁, df₂) = X.XX, *p* = .XXX, η²p = .XX

```
Mauchly's test indicated that sphericity was violated, χ²(2) = 8.45,
p = .015, and therefore Greenhouse-Geisser corrected tests are
reported (ε = .78). There was a significant effect of time on
performance, F(1.56, 45.17) = 12.34, p < .001, η²p = .30.
```

### Chi-Square

**Format**: χ²(df, *N* = n) = X.XX, *p* = .XXX

```
A chi-square test of independence revealed a significant association
between treatment condition and outcome, χ²(2, N = 150) = 8.67,
p = .013. Cramer's V = .24, indicating a small to medium effect size.
```

**Fisher's exact** (when expected < 5):
```
Due to low expected cell counts, Fisher's exact test was used,
revealing a significant association between group and outcome,
p = .023, odds ratio = 2.45 [95% CI: 1.15, 5.23].
```

### Correlation

**Format**: *r*(df) = .XX, *p* = .XXX [95% CI: X.XX, X.XX]

**Pearson**:
```
There was a significant positive correlation between study time
and test scores, r(48) = .52, p < .001 [95% CI: .28, .70], indicating
a large effect.
```

**Spearman**:
```
Spearman's correlation revealed a significant positive relationship
between rank in class and satisfaction rating, rs(98) = .38, p < .001.
```

### Regression

**Simple linear**:
```
Simple linear regression revealed that study time significantly
predicted test scores, β = 0.56, t(48) = 4.67, p < .001. Study time
explained 31.4% of the variance in test scores, R² = .314,
F(1, 48) = 21.82, p < .001.
```

**Multiple regression**:
```
Multiple regression analysis revealed that the model significantly
predicted test performance, F(3, 96) = 15.67, p < .001, R² = .33,
adjusted R² = .31. Study time (β = .42, p < .001) and prior GPA
(β = .28, p = .008) were significant predictors, while age was not
(β = .08, p = .412).
```

### Mann-Whitney U

**Format**: *U* = X.XX, *p* = .XXX, *r* = .XX

```
A Mann-Whitney U test indicated that the treatment group
(Mdn = 78.0) scored significantly higher than the control group
(Mdn = 71.5), U = 234.5, p = .008, r = .36.
```

### Wilcoxon Signed-Rank

**Format**: *W* = X.XX, *p* = .XXX, *r* = .XX

```
A Wilcoxon signed-rank test indicated that scores were significantly
higher at posttest (Mdn = 82.0) than at pretest (Mdn = 73.0),
W = 186.5, p = .002, r = .48.
```

### Kruskal-Wallis

**Format**: *H*(df) = X.XX, *p* = .XXX

```
A Kruskal-Wallis H test showed a significant effect of treatment
on scores, H(2) = 12.45, p = .002. Pairwise comparisons with
Bonferroni correction revealed that Group A (Mdn = 85.0) scored
significantly higher than Group C (Mdn = 72.0), p = .001.
```

---

## Tables

### Descriptive Statistics Table

```
Table 1
Descriptive Statistics by Condition

Condition       n       M        SD      95% CI
───────────────────────────────────────────────
Control        50     74.2      9.3    [71.6, 76.8]
Treatment A    48     82.5      8.1    [80.1, 84.9]
Treatment B    52     79.8      8.7    [77.4, 82.2]
───────────────────────────────────────────────

Note. CI = confidence interval.
```

### ANOVA Results Table

```
Table 2
Analysis of Variance for Test Scores

Source              df       SS         MS        F        p       η²
─────────────────────────────────────────────────────────────────────
Between groups       2    1234.56    617.28    5.43    .006    .111
Within groups       87    9876.54    113.52
Total               89   11111.10
─────────────────────────────────────────────────────────────────────
```

### Regression Results Table

```
Table 3
Multiple Regression Analysis Predicting Test Performance

Predictor            B       SE       β        t        p
──────────────────────────────────────────────────────────
(Intercept)       24.56    8.23      —      2.98    .004
Study time         3.45    0.72    .42     4.79   <.001
Prior GPA          5.67    2.12    .28     2.67    .008
Age               -0.23    0.28    .08    -0.82    .412
──────────────────────────────────────────────────────────

Note. R² = .33, adjusted R² = .31, F(3, 96) = 15.67, p < .001.
```

### Correlation Matrix

```
Table 4
Correlations Among Study Variables

Variable              1       2       3       4
─────────────────────────────────────────────────
1. Test score        —
2. Study time       .52**    —
3. Prior GPA        .45**   .28*     —
4. Age              .12     .08    -.05      —
─────────────────────────────────────────────────

Note. *p < .05. **p < .001.
```

---

## Confidence Intervals

Always report confidence intervals when possible:

```
The mean difference between groups was 8.3 points, 95% CI [4.2, 12.4].
```

```
The correlation was significant, r = .52, 95% CI [.28, .70].
```

```
The odds ratio indicated increased risk, OR = 2.45, 95% CI [1.15, 5.23].
```

---

## Non-Significant Results

Still report effect sizes and confidence intervals:

```
Although not statistically significant, the treatment group
(M = 76.2, SD = 8.4) scored slightly higher than the control group
(M = 74.8, SD = 9.2), t(48) = 0.56, p = .578, d = 0.16, 95% CI
[-0.40, 0.72]. The effect size was small and the confidence interval
included zero, suggesting no meaningful difference.
```
