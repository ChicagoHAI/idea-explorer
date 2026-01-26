# Lab Writing Style Guide

This guide documents our lab's conventions for writing academic papers. Follow these guidelines to ensure consistency across all papers.

---

## 1. Language Style

### 1.1 Introduction Structure

Follow this structure for introductions:

1. **Engaging hook** (1-2 paragraphs)
   - Open with a clear statement about why the problem matters
   - Get to the point quickly - avoid lengthy build-ups

2. **Problem importance** (1 paragraph)
   - Establish the significance of the research area
   - Use specific language: "Given the ability of LLMs to...", "There is growing interest in..."

3. **Gap identification** (1-2 paragraphs)
   - Identify what's missing in existing work
   - Be specific about limitations: "However, it also becomes increasingly challenging to..."
   - Use contrasting structures: "On one hand... On the other hand..."

4. **Your approach** (1-2 paragraphs)
   - Introduce your solution clearly
   - Use confident language: "We propose...", "We hypothesize that..."
   - Reference your method figure: "(see \cref{fig:method})"

5. **Quantitative preview** (1 paragraph)
   - Include specific numbers: "8.97% over few-shot, 15.75% over literature-based alone"
   - Mention key findings concisely

6. **Contribution bullets** (bulleted list)
   - 3-4 specific contributions
   - Start each with an action verb: "We propose...", "We conduct...", "We complement..."
   - Use tight spacing (see LaTeX section)

### 1.2 Writing Voice

**DO:**
- Use active voice: "We propose", "We examine", "We focus on"
- Be direct and confident: "Our main question is...", "We hypothesize that..."
- State things clearly and simply - prefer plain language over jargon
- Use bold questions as organizers: `{\bf what is hypothesis generation?}`
- Include specific quantitative claims throughout
- Use contrasting structures: "Unlike X, we...", "Building on X, we..."

**DON'T:**
- Use passive voice excessively: "It was shown that..." → "We show that..."
- Be vague: "good results" → "8.97% improvement over baselines"
- Use hedging language excessively: "might possibly" → "can"
- Use jargon or fancy wording when simple words work: "utilize" → "use", "facilitate" → "help"
- Overcomplicate sentences - if a sentence is hard to parse, simplify it

### 1.3 Hyperlinks

**Always use `hyperref` package** so readers can click on:
- Citations
- Section references
- Figure references
- Table references
- URLs

```latex
\usepackage[hidelinks]{hyperref}  % hidelinks removes colored boxes
% or with colored links:
\usepackage{hyperref}
\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}
```

### 1.4 Section-Specific Guidelines

**Related Work:**
- Organize by theme (preferred), not chronologically
- Use positioning phrases: "Unlike X, we...", "Building on X, we..."
- End each paragraph by relating back to your work

**Method:**
- Start with problem formulation
- Include algorithm pseudocode for complex methods
- Justify design choices: "We choose X because..."
- Reference implementation details in appendix

**Experiments:**
- Structure: Setup → Main Results → Analysis → Ablations
- Include statistical significance (confidence intervals or p-values)
- Bold best results in tables
- Explain what the numbers mean, not just report them

**Discussion/Limitations:**
- Be honest and specific about limitations
- Discuss failure cases
- Connect to broader implications

---

## 2. LaTeX Structure

### 2.1 Directory Organization

```
paper_draft/
├── main.tex              # Main file with document class and imports
├── references.bib        # BibTeX bibliography
├── commands/
│   ├── math.tex          # Math notation macros
│   ├── general.tex       # General formatting macros
│   └── macros.tex        # Project-specific terms
├── sections/
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── related_work.tex
│   ├── methodology.tex
│   ├── results.tex
│   ├── discussion.tex
│   └── conclusion.tex
├── figures/              # Figure files and .tex for complex figures
├── tables/               # Complex standalone tables
└── appendix/             # Appendix sections
```

### 2.2 Main.tex Structure

```latex
\documentclass[final]{neurips_2025}  % or appropriate style

% Standard packages
\usepackage{times}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[hidelinks]{hyperref}
\usepackage{natbib}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{subcaption}
\usepackage{amsmath,amsfonts}
\usepackage{xspace}
\usepackage{enumitem}

% Import command files
\input{commands/math}
\input{commands/general}
\input{commands/macros}

% Spacing configuration
\captionsetup[subfigure]{aboveskip=4pt,belowskip=4pt}
\captionsetup[table]{aboveskip=4pt,belowskip=4pt}
\captionsetup[figure]{aboveskip=4pt,belowskip=4pt}

\title{Your Paper Title}
\author{...}

\begin{document}
\maketitle

\begin{abstract}
\input{sections/abstract}
\end{abstract}

\input{sections/introduction}
\input{sections/related_work}
\input{sections/methodology}
\input{sections/results}
\input{sections/discussion}
\input{sections/conclusion}

\bibliography{references}
\end{document}
```

---

## 3. Math Notation

### 3.1 Notation Conventions

| Type | Convention | Example |
|------|------------|---------|
| Vectors | Bold lowercase | `\va`, `\vb`, `\vx` → **a**, **b**, **x** |
| Matrices | Bold uppercase | `\mA`, `\mB`, `\mX` → **A**, **B**, **X** |
| Calligraphic | mathcal | `\gA`, `\gD`, `\gL` → 𝒜, 𝒟, ℒ |
| Sets | Blackboard bold | `\sR`, `\sN`, `\sZ` → ℝ, ℕ, ℤ |
| Operators | DeclareMathOperator | `\argmax`, `\argmin` |

### 3.2 Common Macros

```latex
\E           % Expectation: 𝔼
\R           % Real numbers: ℝ
\argmax      % arg max
\argmin      % arg min
\train       % Training set: 𝒟
\test        % Test set: 𝒟_test
```

---

## 4. Reference Macros

### 4.1 Figure References

```latex
\figref{fig:method}      % "figure 1" (lowercase, mid-sentence)
\Figref{fig:method}      % "Figure 1" (capitalized, start of sentence)
\twofigref{fig:a}{fig:b} % "figures 1 and 2"
```

### 4.2 Section References

```latex
\secref{sec:method}      % "section 3"
\Secref{sec:method}      % "Section 3"
```

### 4.3 Using cleveref

For more sophisticated references, use the `cleveref` package:

```latex
\usepackage[noabbrev,capitalize]{cleveref}
\crefname{section}{\S}{\S\S}

% Usage:
\cref{fig:method}        % Auto-formatted based on reference type
\cref{sec:intro,sec:method}  % "Sections 1 and 3"
```

---

## 5. Table Formatting

### 5.1 Basic Structure

```latex
\begin{table}[t]
    \centering
    \resizebox{\textwidth}{!}{%
    \begin{tabular}{@{}llccc@{}}
        \toprule
        \textbf{Method} & \textbf{Dataset} & \textbf{Acc} & \textbf{F1} \\
        \midrule
        Baseline & Dataset-A & 75.2 & 72.1 \\
        \textbf{Ours} & Dataset-A & \textbf{82.1} & \textbf{79.4} \\
        \bottomrule
    \end{tabular}
    }
    \caption{Results on Dataset-A. Best results in \textbf{bold}.}
    \label{tab:results}
\end{table}
```

### 5.2 Key Conventions

- **Always use `booktabs`**: `\toprule`, `\midrule`, `\bottomrule`
- **No vertical lines**: Never use `|` in column specs
- **Remove edge padding**: Use `@{}` at table edges
- **Use `\resizebox`**: `\resizebox{\textwidth}{!}{...}` for wide tables
- **Sub-headers**: Use `\cmidrule(lr){2-4}` for grouping columns
- **Row spacing**: `\renewcommand{\arraystretch}{1.25}` for readability
- **Text columns**: Use `p{Xcm}` for wrapped text
- **Bold best results**: Highlight best numbers with `\textbf{}`
- **Dataset/method names**: Use `\textsc{}` in headers

### 5.3 Multi-column Headers

```latex
\begin{tabular}{lcccccc}
    \toprule
    \multirow{2}{*}{Method} & \multicolumn{2}{c}{GPT} & \multicolumn{2}{c}{Llama} \\
    \cmidrule(lr){2-3} \cmidrule(lr){4-5}
    & Acc & F1 & Acc & F1 \\
    \midrule
    ...
\end{tabular}
```

---

## 6. Figure Formatting

### 6.1 Single Figure

```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/method.pdf}
    \caption{Overview of our method. We first... then... finally...}
    \label{fig:method}
\end{figure}
```

### 6.2 Multi-panel Subfigures (3-column)

```latex
\begin{figure}[t]
    \centering
    \begin{subfigure}[b]{0.32\textwidth}
        \includegraphics[width=\textwidth]{figures/plot_a.pdf}
        \caption{Metric A}
        \label{fig:plot_a}
    \end{subfigure}
    \begin{subfigure}[b]{0.32\textwidth}
        \includegraphics[width=\textwidth]{figures/plot_b.pdf}
        \caption{Metric B}
        \label{fig:plot_b}
    \end{subfigure}
    \begin{subfigure}[b]{0.32\textwidth}
        \includegraphics[width=\textwidth]{figures/plot_c.pdf}
        \caption{Metric C}
        \label{fig:plot_c}
    \end{subfigure}
    \input{figures/legend}  % Shared legend
    \caption{Results across three metrics. \figleft shows...}
    \label{fig:results}
\end{figure}
```

### 6.3 Caption Conventions

- Captions should be self-contained
- Explain what is shown
- Highlight key observations
- Use `\figleft`, `\figright`, `\captiona`, `\captionb` for sub-panel references

---

## 7. Results Presentation

### 7.1 Colored Arrows

```latex
% In tables or text, show improvement/decline
Our method achieves 82.1\% \increase compared to 75.2\% for baseline \decrease
```

### 7.2 Contribution Lists

```latex
\begin{itemize}[leftmargin=*,itemsep=0pt,topsep=0pt]
    \item We propose a novel framework for...
    \item We conduct comprehensive experiments on...
    \item We release our code and data at...
\end{itemize}
```

---

## 8. Algorithm Styling

### 8.1 Basic Algorithm

```latex
\usepackage{algorithm}
\usepackage[noend]{algpseudocode}

\begin{algorithm}[t]
\caption{Our Method}
\label{alg:method}
\begin{algorithmic}[1]
\INPUT Data $\gD$, model $\gM$
\OUTPUT Hypotheses $\gH$
\State Initialize $\gH \gets \emptyset$
\For{each example $x \in \gD$}
    \State $h \gets \gM(x)$ \Comment{Generate hypothesis}
    \State $\gH \gets \gH \cup \{h\}$
\EndFor
\State \Return $\gH$
\end{algorithmic}
\end{algorithm}
```

### 8.2 Comment Style

Use `\triangleright` for inline comments:
```latex
\newcommand{\rightcomment}[1]{\(\triangleright\) {\small \it #1}}
```

---

## 9. Citations

### 9.1 Citation Styles

```latex
\cite{author2024}        % Parenthetical: (Author et al., 2024)
\citet{author2024}       % Textual: Author et al. (2024)
\cite[e.g.,][]{key}      % With prefix: (e.g., Author et al., 2024)
```

### 9.2 BibTeX Entry Format

```bibtex
@inproceedings{zhou2024hypogenic,
    title={Hypothesis Generation with Large Language Models},
    author={Zhou, Yangqiaoyu and Liu, Haokun and Srivastava, Tejes and Mei, Hongyuan and Tan, Chenhao},
    booktitle={Proceedings of ACL},
    year={2024}
}
```

---

## 10. Quick Reference Checklist

Before submitting, verify:

- [ ] Active voice used throughout
- [ ] Specific quantitative claims in introduction
- [ ] Contributions listed with action verbs
- [ ] All tables use `booktabs` (no vertical lines)
- [ ] Best results bolded in tables
- [ ] Figures have self-contained captions
- [ ] References use `\figref`, `\secref` macros
- [ ] Method/dataset names use `\textsc` with `\xspace`
- [ ] Commands directory properly imported
- [ ] No placeholder text remaining
- [ ] Paper compiles without errors
