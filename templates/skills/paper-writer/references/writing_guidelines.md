# Academic Writing Guidelines

## General Principles

### Clarity
- Use simple, direct language
- One idea per sentence
- Define terms before using them
- Avoid jargon unless necessary

### Precision
- Be specific, not vague
- Quantify when possible
- Use precise technical terms correctly
- Avoid hedging without reason

### Conciseness
- Remove unnecessary words
- Avoid redundancy
- Get to the point quickly
- Every sentence should add value

## Section-Specific Guidelines

### Abstract

**Do:**
- Write last (after paper is complete)
- Make it self-contained
- Include context, method, results, significance
- Use past tense for completed work

**Don't:**
- Include citations
- Use undefined acronyms
- Leave vague statements
- Promise more than paper delivers

**Template:**
```
[Topic] is important because [reason]. However, existing approaches [limitation].
We propose [method] that [key idea]. Our experiments on [datasets] show that
[key result]. This demonstrates that [significance].
```

### Introduction

**Paragraph 1 - Hook:**
- Start with a compelling problem or observation
- Establish why readers should care
- Use concrete examples if helpful

**Paragraph 2-3 - Background:**
- Provide necessary context
- Define key concepts
- Set up the problem formally if needed

**Paragraph 4 - Gap:**
- Identify what's missing
- Explain why existing solutions fall short
- Be specific about limitations

**Paragraph 5 - Contributions:**
- List contributions explicitly (use bullets)
- Be concrete and specific
- Match paper structure

**Common mistakes:**
- Too much background, too little motivation
- Vague contributions ("we propose a method")
- Not explaining why the problem is hard
- Overselling without evidence

### Related Work

**Organization approaches:**

1. **Thematic** (preferred):
   ```
   Our work relates to three areas: [A], [B], and [C].

   **[Theme A].** Prior work on... [cite]. However...

   **[Theme B].** Another line of research... [cite]. Unlike these, we...

   **[Theme C].** Related to our approach... [cite]. We extend this by...
   ```

2. **Comparative**:
   ```
   Several approaches address [problem]. [Method1] [cite] does X but lacks Y.
   [Method2] [cite] handles Y but not Z. Our method addresses both by...
   ```

**Positioning phrases:**
- "Unlike X, we..."
- "Building on X, we..."
- "While X focuses on..., we address..."
- "Complementary to X, our approach..."

**Don't:**
- Just list papers without analysis
- Be dismissive of prior work
- Miss important references
- Forget to position your work

### Method

**Structure options:**

1. **Problem → Approach → Details:**
   - Define problem formally
   - Describe high-level approach
   - Give algorithmic details

2. **Overview → Components → Integration:**
   - System overview (maybe figure)
   - Each component in detail
   - How components work together

**Writing tips:**
- Start with intuition, then formalize
- Use running examples
- Include algorithm pseudocode
- Justify design choices

**Notation:**
- Define all symbols when first used
- Be consistent throughout paper
- Use a notation table if complex
- Follow field conventions

### Experiments

**Setup section checklist:**
- [ ] Datasets: name, size, source, preprocessing, splits
- [ ] Baselines: what methods, why these, implementation details
- [ ] Metrics: what measures, why appropriate
- [ ] Implementation: framework, hardware, hyperparameters, training details

**Results presentation:**
- Tables for numerical comparisons
- Figures for trends and visualizations
- Bold best results (or use underline for second best)
- Include error bars or confidence intervals

**Analysis questions to answer:**
- Does our method achieve state-of-the-art?
- Under what conditions does it work best/worst?
- What explains the performance difference?
- Are results statistically significant?

**Ablation structure:**
- Component ablation: remove/replace each component
- Hyperparameter sensitivity: vary key parameters
- Design choices: justify architectural decisions

### Discussion

**What to cover:**

1. **Limitations** (be honest):
   - Computational requirements
   - Data requirements
   - Failure modes
   - Scope limitations

2. **Broader implications:**
   - What does this enable?
   - How might it be applied?
   - What does it mean for the field?

3. **Failure cases:**
   - When does the method fail?
   - Show examples if possible
   - Explain why

### Conclusion

**Structure:**
```
In this paper, we [brief summary of contribution]. Our key insight is that
[main idea]. Experiments demonstrate that [main results]. This work opens
directions for [future work].
```

**Don't:**
- Introduce new information
- Repeat abstract verbatim
- Make claims not supported by results
- End with generic "future work" phrases

## Writing Style

### Verb Tense

| Section | Tense | Example |
|---------|-------|---------|
| Abstract | Past | "We proposed... We found..." |
| Introduction | Present | "NLP is important... We propose..." |
| Related Work | Present/Past | "X proposes... Y showed..." |
| Method | Present | "Our method takes... We compute..." |
| Experiments | Past | "We evaluated... Results showed..." |
| Discussion | Present | "This suggests... Limitations include..." |
| Conclusion | Past + Present | "We presented... This enables..." |

### Voice

- Prefer active voice: "We show that X" not "It is shown that X"
- Use passive when agent is unimportant: "The model was trained for 100 epochs"
- Be consistent within sections

### Common Fixes

| Weak | Strong |
|------|--------|
| "very important" | "critical" or remove |
| "it can be seen that" | remove |
| "in order to" | "to" |
| "due to the fact that" | "because" |
| "a number of" | specific number or "several" |
| "utilize" | "use" |
| "methodology" | "method" |

## Figures and Tables

### Figure Guidelines

- Vector format (PDF) when possible
- Legible at printed size
- Consistent style across paper
- Color-blind friendly palettes
- Self-contained captions

### Table Guidelines

- Use booktabs package (no vertical lines)
- Align numbers on decimal point
- Include units in headers
- Caption above table
- Reference in text before table appears

### Caption Writing

**Figures:**
```
Figure 1: [What is shown]. [Key observation]. [Any important details].
```

**Tables:**
```
Table 1: [What is compared] on [benchmark/setting]. [Interpretation guidance].
Best results in bold.
```
