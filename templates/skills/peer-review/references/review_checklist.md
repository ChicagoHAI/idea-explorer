# Detailed Review Checklists

## Checklist by Paper Type

### Empirical ML Paper

#### Claims and Evidence
- [ ] Main claims are clearly stated
- [ ] Each claim is supported by experiments
- [ ] Results support the conclusions drawn
- [ ] Alternative explanations are considered

#### Experimental Design
- [ ] Datasets are appropriate for the task
- [ ] Train/val/test splits are standard or justified
- [ ] Multiple random seeds used
- [ ] Statistical significance is reported
- [ ] Computational resources documented

#### Baselines and Comparisons
- [ ] Baselines are relevant and recent
- [ ] Baselines use same evaluation protocol
- [ ] Hyperparameters are fairly tuned
- [ ] Comparison is apples-to-apples
- [ ] State-of-the-art is included if applicable

#### Reproducibility
- [ ] Model architecture fully specified
- [ ] Training details complete (lr, epochs, batch size, etc.)
- [ ] Data preprocessing described
- [ ] Code availability mentioned
- [ ] Hyperparameter selection method described

### Theoretical Paper

#### Problem Formulation
- [ ] Problem is precisely defined
- [ ] Assumptions are clearly stated
- [ ] Assumptions are reasonable
- [ ] Notation is consistent

#### Proofs and Analysis
- [ ] Theorems are clearly stated
- [ ] Proofs are complete and correct
- [ ] Proof sketches for complex proofs
- [ ] Intuition provided alongside formalism

#### Significance
- [ ] Theoretical contribution is clear
- [ ] Relationship to practice discussed
- [ ] Limitations of theory acknowledged

### Methods Paper

#### Method Description
- [ ] Algorithm is clearly described
- [ ] Pseudocode provided if complex
- [ ] Design choices justified
- [ ] Computational complexity discussed

#### Evaluation
- [ ] Method tested on diverse benchmarks
- [ ] Comparison to strong baselines
- [ ] Ablation studies included
- [ ] Error analysis provided
- [ ] Failure cases discussed

#### Practical Considerations
- [ ] Computational requirements clear
- [ ] Implementation details sufficient
- [ ] Hyperparameter sensitivity explored

### Dataset Paper

#### Dataset Description
- [ ] Data collection process described
- [ ] Data statistics provided
- [ ] Annotation process documented
- [ ] Quality control measures described

#### Analysis
- [ ] Dataset analysis provided
- [ ] Comparison to existing datasets
- [ ] Baseline results included
- [ ] Potential biases discussed

#### Ethics and Access
- [ ] Privacy considerations addressed
- [ ] Consent/licensing documented
- [ ] Access information provided
- [ ] Potential misuse discussed

---

## Common Issues by Section

### Abstract Issues
| Issue | Example | How to Identify |
|-------|---------|-----------------|
| Too vague | "We propose a new method" | No specific contribution |
| Overclaims | "We solve the problem" | Claims not supported |
| Missing results | No quantitative outcomes | No numbers mentioned |
| Too long | >300 words | Word count |

### Introduction Issues
| Issue | How to Identify |
|-------|-----------------|
| Weak motivation | No clear "why this matters" |
| Missing gap | Jump from background to contribution |
| Vague contributions | "We make several contributions" |
| Overclaims | "First to..." without verification |

### Related Work Issues
| Issue | How to Identify |
|-------|-----------------|
| Missing important work | Key papers not cited |
| Only positive comparison | No acknowledgment of prior strengths |
| No positioning | Reader can't see where this fits |
| Straw man | Prior work unfairly characterized |

### Method Issues
| Issue | How to Identify |
|-------|-----------------|
| Insufficient detail | Can't reproduce from description |
| Missing justification | "We use X" with no "because" |
| Inconsistent notation | Symbols change meaning |
| Hidden assumptions | Unstated requirements |

### Experiment Issues
| Issue | How to Identify |
|-------|-----------------|
| Weak baselines | Old or inappropriate comparisons |
| Unfair comparison | Different hyperparameter budgets |
| No error bars | Single run results |
| Cherry-picking | Only favorable results shown |
| Missing ablations | Component contributions unclear |

### Discussion Issues
| Issue | How to Identify |
|-------|-----------------|
| No limitations | Claims paper has no weaknesses |
| Hand-wavy future work | "Future work will address..." |
| Overclaiming | Generalizing beyond evidence |

---

## Scoring Rubrics

### Soundness (1-4)
| Score | Criteria |
|-------|----------|
| 4 | Claims fully supported, methodology rigorous |
| 3 | Minor issues but main claims supported |
| 2 | Significant issues with claims or methods |
| 1 | Major flaws, claims not supported |

### Significance (1-4)
| Score | Criteria |
|-------|----------|
| 4 | Major contribution, high impact |
| 3 | Solid contribution to the field |
| 2 | Incremental contribution |
| 1 | Marginal or unclear contribution |

### Novelty (1-4)
| Score | Criteria |
|-------|----------|
| 4 | Highly novel ideas or approach |
| 3 | Novel combination or extension |
| 2 | Limited novelty |
| 1 | Not novel, straightforward application |

### Presentation (1-4)
| Score | Criteria |
|-------|----------|
| 4 | Excellent writing, clear throughout |
| 3 | Good writing, minor issues |
| 2 | Adequate but could improve |
| 1 | Poor writing, hard to follow |

---

## Red Flags

### Ethical Concerns
- [ ] Dual-use potential not discussed
- [ ] Bias in data/model not addressed
- [ ] Privacy implications not considered
- [ ] Consent issues with human subjects

### Reproducibility Concerns
- [ ] Key implementation details missing
- [ ] Data not available
- [ ] Unusual evaluation protocol
- [ ] Results seem too good

### Scientific Concerns
- [ ] P-hacking indicators
- [ ] Contradictory claims
- [ ] Logical fallacies
- [ ] Circular reasoning
