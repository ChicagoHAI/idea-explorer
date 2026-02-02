# Hypothesis Templates

## Template 1: Comparative Study

Use when comparing methods, models, or approaches.

```markdown
# Hypothesis: [Method A] vs [Method B]

## Research Question
Does [Method A] outperform [Method B] on [Task]?

## Hypothesis Statement
[Method A] will achieve higher [Metric] than [Method B] on [Task/Dataset]
because [Reason based on prior work or theory].

## Operationalization
- **Method A**: [Specific implementation details]
- **Method B**: [Specific implementation details]
- **Task**: [Specific task definition]
- **Metric**: [Specific metric(s)]

## Predictions
| Outcome | Metric Difference | Interpretation |
|---------|-------------------|----------------|
| Strong support | >10% improvement | Clear advantage |
| Moderate support | 5-10% improvement | Notable difference |
| Weak support | 1-5% improvement | Minor advantage |
| No support | ≤1% or negative | No advantage |

## Alternative Hypotheses
### H_alt1: Method B is better
[Method B] outperforms [Method A] due to [reason].

### H_null: No difference
There is no significant difference between methods.

## Experimental Design
- **Conditions**: Method A, Method B
- **Datasets**: [List datasets]
- **Runs**: [Number of runs/seeds]
- **Statistical test**: [e.g., paired t-test, Wilcoxon]

## Confounds to Control
- [ ] Same compute budget
- [ ] Same hyperparameter search
- [ ] Same evaluation protocol
- [ ] Same random seeds
```

---

## Template 2: Ablation Study

Use when testing component contributions.

```markdown
# Hypothesis: [Component] Contribution

## Research Question
Does [Component X] contribute to the performance of [Method]?

## Hypothesis Statement
Removing [Component X] from [Method] will decrease [Metric] by
[Expected amount] because [Component X] provides [Specific function].

## Conditions
| Condition | Description |
|-----------|-------------|
| Full model | All components included |
| -Component X | Component X removed |
| -Component Y | Component Y removed |
| -X, -Y | Both removed |

## Predictions
| Condition | Expected Metric | Reason |
|-----------|-----------------|--------|
| Full | Best | All components working |
| -X | Moderate drop | X handles [function] |
| -Y | Small drop | Y handles [function] |
| -X, -Y | Largest drop | Combined effect |

## What Would Falsify This?
- Removing X shows no performance change
- Removing X improves performance
- Effect is much larger/smaller than expected

## Experimental Design
- **Base model**: [Specification]
- **Ablation method**: [How components are removed]
- **Evaluation**: [Metrics and datasets]
```

---

## Template 3: Scaling Hypothesis

Use when testing how performance changes with scale.

```markdown
# Hypothesis: Scaling Behavior

## Research Question
How does [Performance] change with [Scale factor]?

## Hypothesis Statement
[Performance metric] will [increase/decrease] [relationship type]
as [Scale factor] increases, following [expected pattern].

## Scaling Dimensions
| Factor | Range Tested |
|--------|--------------|
| Model size | [e.g., 125M to 175B params] |
| Data size | [e.g., 1M to 1B tokens] |
| Compute | [e.g., GPU hours] |

## Predicted Relationships
| Relationship | Mathematical Form | Expected |
|--------------|-------------------|----------|
| Linear | y = ax + b | [ ] |
| Logarithmic | y = a log(x) + b | [ ] |
| Power law | y = ax^b | [ ] |
| Saturation | y = a(1 - e^(-bx)) | [ ] |

## Predictions at Key Points
| Scale | Predicted Performance |
|-------|----------------------|
| Small (X) | [Value] |
| Medium (Y) | [Value] |
| Large (Z) | [Value] |

## What Would Falsify This?
- Non-monotonic relationship
- Different functional form
- Saturation much earlier/later than expected
```

---

## Template 4: Behavioral Hypothesis

Use when studying model behavior or capabilities.

```markdown
# Hypothesis: [Behavior/Capability]

## Research Question
Does [Model type] exhibit [Behavior X] in [Condition Y]?

## Hypothesis Statement
[Model type] will demonstrate [Behavior X] when [Condition Y],
as evidenced by [Observable measure], because [Mechanism/Reason].

## Behavioral Definition
**Behavior X** is operationally defined as:
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

## Test Conditions
| Condition | Description | Expected Behavior |
|-----------|-------------|-------------------|
| Baseline | [Description] | [Expected] |
| Test | [Description] | [Expected] |
| Control | [Description] | [Expected] |

## Measurement
- **Metric**: [How behavior is quantified]
- **Threshold**: [What counts as exhibiting behavior]
- **Examples**: [Sample inputs/outputs]

## Alternative Explanations
| Explanation | How to rule out |
|-------------|-----------------|
| [Alt 1] | [Control condition] |
| [Alt 2] | [Additional test] |

## Predictions
If hypothesis is true:
- [ ] [Prediction 1]
- [ ] [Prediction 2]
- [ ] [Prediction 3]

If hypothesis is false:
- [ ] [Counter-prediction 1]
- [ ] [Counter-prediction 2]
```

---

## Template 5: Mechanistic Hypothesis

Use when proposing how/why something works.

```markdown
# Hypothesis: [Mechanism]

## Research Question
What mechanism explains [Observed phenomenon]?

## Proposed Mechanism
[Phenomenon] occurs because:
1. [Step 1 of mechanism]
2. [Step 2 of mechanism]
3. [Step 3 of mechanism]

## Hypothesis Statement
[Component A] causes [Effect B] through [Mechanism C],
which we can observe as [Measurable signature D].

## Mechanistic Predictions
If this mechanism is correct, we should observe:

| Test | Prediction | Rationale |
|------|------------|-----------|
| Intervention 1 | [Outcome] | [Why] |
| Intervention 2 | [Outcome] | [Why] |
| Observation 1 | [Pattern] | [Why] |

## Alternative Mechanisms
| Alternative | Key difference | Distinguishing test |
|-------------|----------------|---------------------|
| Mechanism 2 | [Difference] | [Test that distinguishes] |
| Mechanism 3 | [Difference] | [Test that distinguishes] |

## Evidence Requirements
- [ ] Necessary condition: [What must be true]
- [ ] Sufficient condition: [What would prove mechanism]
- [ ] Causal evidence: [Intervention that would confirm]

## What Would Falsify This?
- [Specific outcome that would reject proposed mechanism]
- [Alternative finding that would support different mechanism]
```

---

## Quick Hypothesis Checklist

Use for any hypothesis:

- [ ] **Specific**: Can someone else understand exactly what I'm claiming?
- [ ] **Testable**: Do I have/can I get the data to test this?
- [ ] **Falsifiable**: What outcome would prove me wrong?
- [ ] **Grounded**: Is this based on prior work or theory?
- [ ] **Novel**: Does this add something new?
- [ ] **Operationalized**: Are all terms measurable?
- [ ] **Alternatives considered**: Have I thought about other explanations?
- [ ] **Predictions documented**: Did I write predictions before running experiments?
