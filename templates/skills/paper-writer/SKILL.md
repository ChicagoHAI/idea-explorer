---
name: paper-writer
description: Write academic papers from experiment results using LaTeX. Use when experiments are complete and REPORT.md exists, when asked to write a paper, or when generating publication-ready documents in NeurIPS style.
---

# Paper Writer

Guide for writing academic papers from experiment results using a two-stage process.

## When to Use

- After experiments are complete and REPORT.md exists
- When explicitly asked to write a paper
- When generating publication-ready documents

## Two-Stage Writing Process

### Stage 1: Outline Development

Before writing prose, create a detailed outline:

1. **Skeleton**: Section headers and subsection structure
2. **Key points**: Bullet points for each section (3-5 per section)
3. **Evidence mapping**: Link each claim to supporting data/figures
4. **Citation placeholders**: Note where references are needed
5. **Figure/table planning**: List required visuals

Save outline to `paper/OUTLINE.md` for review before proceeding.

### Stage 2: Prose Writing

Convert outline to full prose:

1. Write section by section (don't jump around)
2. Expand each bullet into 2-4 sentences
3. Add transitions between paragraphs
4. Insert citations as you write
5. Create figures/tables as needed

## Paper Structure (IMRAD Format)

### 1. Title
- Clear, specific, informative
- Conveys main finding or contribution
- No acronyms unless universally known

### 2. Abstract (150-250 words)

Follow this structure:
- **Context/Problem** (1-2 sentences): Why does this matter?
- **Gap/Challenge** (1 sentence): What's missing?
- **Our approach** (1-2 sentences): What did we do?
- **Key results** (2-3 sentences): What did we find?
- **Significance** (1 sentence): Why does it matter?

### 3. Introduction

Structure:
1. **Hook** (1 paragraph): Why does this problem matter?
2. **Background** (1-2 paragraphs): What do readers need to know?
3. **Gap** (1 paragraph): What's missing in existing work?
4. **Contribution** (1 paragraph): What do we provide? Be specific with bullets:
   - Contribution 1
   - Contribution 2
   - Contribution 3
5. **Organization** (optional): Brief roadmap of paper

### 4. Related Work

Organization strategies:
- **By theme**: Group papers by approach/concept
- **By timeline**: Historical development (less preferred)
- **By relationship**: How papers relate to ours

For each group:
- Summarize the approach
- Identify limitations
- Position our work: "Unlike X, we..." or "Building on X, we..."

### 5. Method/Approach

Essential elements:
- Problem formulation (formal if appropriate)
- Method description (clear enough to reproduce)
- Design justifications (why this choice?)
- Algorithm/pseudocode (if complex)
- Complexity analysis (if relevant)

### 6. Experiments

Structure:
1. **Setup**
   - Datasets: source, size, preprocessing
   - Baselines: what and why
   - Metrics: what and why
   - Implementation: hardware, hyperparameters

2. **Main Results**
   - Tables with clear captions
   - Statistical significance (confidence intervals or p-values)
   - Bold best results

3. **Analysis**
   - What do the numbers mean?
   - Why does our method work?
   - Where does it fail?

4. **Ablations**
   - Component contributions
   - Sensitivity analysis
   - Design choice validation

### 7. Discussion

Cover:
- Limitations (be honest and specific)
- Broader implications
- Failure cases and edge cases
- Connections to theory (if applicable)

### 8. Conclusion

Format:
- Summary (1 paragraph): What did we do and find?
- Key takeaway (1 sentence): What should readers remember?
- Future work (2-3 sentences): What comes next?

## LaTeX Template

The NeurIPS 2025 style files are available in the `paper/` directory.

```latex
\documentclass[final]{neurips_2025}

% Essential packages
\usepackage{booktabs}  % Better tables
\usepackage{graphicx}  % Figures
\usepackage{amsmath,amssymb}  % Math
\usepackage{hyperref}  % Links
\usepackage{algorithm2e}  % Algorithms

\title{Clear Title That Conveys Main Contribution}

\author{
  Author One \\
  Affiliation \\
  \texttt{email@example.com}
}

\begin{document}
\maketitle

\begin{abstract}
Your abstract here (150-250 words).
\end{abstract}

\section{Introduction}
...

\section{Related Work}
...

\section{Method}
...

\section{Experiments}
...

\section{Discussion}
...

\section{Conclusion}
...

\bibliography{references}
\bibliographystyle{plainnat}

\end{document}
```

### Table Formatting

```latex
\begin{table}[h]
\centering
\caption{Results comparing methods on [benchmark].
         Higher is better for all metrics.
         Best results in \textbf{bold}.}
\begin{tabular}{lcc}
\toprule
Method & Accuracy (\%) & F1 (\%) \\
\midrule
Baseline 1 & 75.2 {\scriptsize $\pm$ 0.3} & 72.1 {\scriptsize $\pm$ 0.4} \\
Baseline 2 & 78.4 {\scriptsize $\pm$ 0.2} & 75.8 {\scriptsize $\pm$ 0.3} \\
\midrule
Ours & \textbf{82.1} {\scriptsize $\pm$ 0.2} & \textbf{79.4} {\scriptsize $\pm$ 0.3} \\
\bottomrule
\end{tabular}
\label{tab:main_results}
\end{table}
```

### Figure Formatting

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.8\linewidth]{figures/main_result.pdf}
\caption{Caption should be self-contained. Explain what is shown,
         highlight key observations, and note any important details.}
\label{fig:main_result}
\end{figure}
```

## Citation Guidelines

### BibTeX Format

```bibtex
@inproceedings{author2024title,
  title={Full Paper Title},
  author={Last, First and Last2, First2},
  booktitle={Conference Name},
  year={2024}
}
```

### Citation Style

- Use `\cite{key}` for parenthetical: "...as shown previously (Author et al., 2024)"
- Use `\citet{key}` for textual: "Author et al. (2024) showed that..."

## Output

Save to `paper/` directory:
- `main.tex`: Main document
- `references.bib`: BibTeX citations
- `figures/`: Figure files (PDF preferred)

Compile with:
```bash
cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## Quality Checklist

### Content
- [ ] Title reflects main contribution
- [ ] Abstract is self-contained (no citations, no undefined terms)
- [ ] Contributions clearly stated in introduction
- [ ] All claims supported by evidence
- [ ] Limitations honestly discussed
- [ ] Related work positions paper clearly

### Technical
- [ ] Method reproducible from description
- [ ] All experimental details provided
- [ ] Statistical significance reported
- [ ] Ablations validate design choices

### Presentation
- [ ] Figures have informative captions
- [ ] Tables are properly formatted
- [ ] All citations present and correct
- [ ] No placeholder text
- [ ] Consistent notation throughout
- [ ] Proofread for typos

### Ethics
- [ ] Broader impact considered
- [ ] Potential negative uses discussed
- [ ] Data/model limitations noted

## References

See `references/` folder for:
- `writing_guidelines.md`: Section-specific writing advice

See `assets/` folder for:
- `paper_outline_template.md`: Template for Stage 1 outline
