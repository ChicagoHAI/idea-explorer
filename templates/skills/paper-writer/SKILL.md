---
name: paper-writer
description: Write academic papers from experiment results using LaTeX. Use when experiments are complete and REPORT.md exists, when asked to write a paper, or when generating publication-ready documents in NeurIPS style.
---

# Paper Writer

Guide for writing academic papers from experiment results.

## When to Use

- After experiments are complete and REPORT.md exists
- When explicitly asked to write a paper
- When generating publication-ready documents

## Paper Structure (NeurIPS Style)

### 1. Title
- Clear, specific, informative
- Conveys main finding or contribution

### 2. Abstract (150-250 words)
- Problem statement (1-2 sentences)
- Our approach (1-2 sentences)
- Key results (2-3 sentences)
- Significance (1 sentence)

### 3. Introduction
- Hook: Why does this problem matter?
- Gap: What's missing in existing work?
- Contribution: What do we provide? (Be specific)
- Organization: Brief roadmap

### 4. Related Work
- Organize by theme, not chronologically
- Position our work: "Unlike X, we..."
- Cite papers from literature_review.md

### 5. Method/Approach
- Clear enough to reproduce
- Justify design choices
- Include algorithms/pseudocode if helpful

### 6. Experiments
- Setup: datasets, baselines, metrics
- Results: tables with statistical significance
- Analysis: what do numbers mean?
- Ablations: what matters?

### 7. Discussion
- Limitations (be honest)
- Broader implications
- Failure cases

### 8. Conclusion
- 1 paragraph summary
- Key takeaway
- Future work

## LaTeX Template

The NeurIPS 2025 style files are available in the `paper/` directory after running the paper writer.

```latex
% Document class
\documentclass[final]{neurips_2025}

% Essential packages
\usepackage{booktabs}  % Better tables
\usepackage{graphicx}  % Figures
\usepackage{amsmath}   % Math
\usepackage{hyperref}  % Links

% Tables with proper formatting
\begin{table}[h]
\centering
\caption{Results comparing methods on benchmark.}
\begin{tabular}{lcc}
\toprule
Method & Accuracy & F1 \\
\midrule
Baseline & 0.75 & 0.72 \\
Ours & \textbf{0.82} & \textbf{0.79} \\
\bottomrule
\end{tabular}
\end{table}

% Figures with captions
\begin{figure}[h]
\centering
\includegraphics[width=0.8\linewidth]{figures/main_result.pdf}
\caption{Clear caption explaining what to observe.}
\end{figure}

% Citations
\cite{author2024paper}
```

## Output

Save to `paper/main.tex` with:
- All sections filled (no placeholders)
- Proper citations in BibTeX format (`paper/references.bib`)
- Tables/figures with captions
- Compile with: `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`

## Quality Checklist

- [ ] Title reflects main contribution
- [ ] Abstract is self-contained
- [ ] Claims supported by data
- [ ] Figures have clear captions
- [ ] All citations present
- [ ] No placeholder text
- [ ] Limitations acknowledged
