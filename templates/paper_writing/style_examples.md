# Style Examples

Curated examples showing our lab's paper formatting conventions. Use these as templates.

---

## Example Table (Main Results)

```latex
\begin{table*}[t]
    \centering
    \resizebox{0.92\textwidth}{!}{%
    \begin{tabular}{@{}llrrrr@{}}
        \toprule
                           &                    & \textsc{Dataset}  & \textsc{Dataset} & \textsc{Dataset}   \\
        Models             & Methods            & \textsc{One}      & \textsc{Two}     & \textsc{Three}     \\
        \midrule \midrule
        \roberta (Oracle)  & Train 200          & 100.0             & 84.0             & 49.0               \\
                           & Train 1000         & 100.0             & 91.0             & 60.0               \\
        \midrule
        \gpt               & Zero shot          & 36.0              & 31.0             & 59.0               \\
                           & Few shot           & 75.0              & 51.0             & 60.0               \\
                           & \ours              & {\bf 100.0}       & {\bf 75.3}       & {\bf 61.3}         \\
        \bottomrule
    \end{tabular}
    }
    \caption{
        Prediction accuracies with 200 examples.
        We report the best numbers across all configurations.
        Best results in \textbf{bold}.
    }
    \label{tab:main_results}
\end{table*}
```

---

## Example Table (Multi-column Headers)

```latex
\begin{table}[t]
    \centering
    \resizebox{\textwidth}{!}{%
    \begin{tabular}{lcccccccc}
        \toprule
        \multirow{2}{*}{Method} & \multicolumn{2}{c}{GPT} & \multicolumn{2}{c}{Qwen} & \multicolumn{2}{c}{Llama} \\
        \cmidrule(lr){2-3} \cmidrule(lr){4-5} \cmidrule(lr){6-7}
        & Accuracy & F1 & Accuracy & F1 & Accuracy & F1 \\
        \midrule
        Zero-shot inference & 62.2 & 56.8 & 61.0 & 55.7 & 66.0 & 62.2 \\
        Few-shot inference  & 64.4 & 61.5 & 67.1 & 65.8 & 70.9 & 69.2 \\
        \midrule
        \ours               & \bf 71.9 & \bf 71.3 & \bf 76.0 & \bf 75.7 & \bf 75.2 & \bf 74.3 \\
        \bottomrule
    \end{tabular}%
    }
    \caption{Accuracy and F1 scores across models. Best results in \textbf{bold}.}
    \label{tab:cross_model}
\end{table}
```

---

## Example Table (Qualitative Results)

```latex
\begin{table*}[t]
    \centering
    \renewcommand{\arraystretch}{1.25}
    \resizebox{\textwidth}{!}{%
    \small
    \begin{tabular}{@{}lp{7cm}p{4.25cm}@{}}
    \toprule
    \textbf{Dataset} & \textbf{Finding} & \textbf{Supported/Novel} \\
    \midrule \midrule
    \deceptive & Deceptive reviews contain more emotional terms. & \citet{li2014generalrule} \\
               & Deceptive reviews are more likely to use superlatives. & \citet{ott2011finding} \\
               & Truthful reviews mention reviewer's purpose for staying. & Novel \\
    \midrule
    \headline  & Concreteness helps. & \citet{sadoski2000engaging} \\
               & Humorous headlines are clicked more. & Novel \\
    \bottomrule
    \end{tabular}
    }
    \caption{Summary of generated hypotheses and whether they support existing findings or are novel.}
    \label{tab:hypotheses_analysis}
\end{table*}
```

---

## Example 3-Column Subfigure

```latex
\begin{figure}[t]
  \centering
    \begin{subfigure}[b]{0.32\textwidth}
        \includegraphics[width=\textwidth]{figures/plot_a.pdf}
        \caption{Number of features}
        \label{fig:plot_a}
    \end{subfigure}
    \begin{subfigure}[b]{0.32\textwidth}
        \includegraphics[width=\textwidth]{figures/plot_b.pdf}
        \caption{Compositionality}
        \label{fig:plot_b}
    \end{subfigure}
    \begin{subfigure}[b]{0.32\textwidth}
        \includegraphics[width=\textwidth]{figures/plot_c.pdf}
        \caption{Noise in outcome}
        \label{fig:plot_c}
    \end{subfigure}

  \input{figures/legend}  % Shared legend file

  \caption{F1 scores on synthetic datasets with different task difficulty.}
  \label{fig:controlled_plots}
\end{figure}
```

---

## Example Full-Width Figure

```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/method_overview.pdf}
    \caption{An overview of our method. We curate datasets spanning multiple domains.
    Our evaluation measures both explanatory power and interestingness of generated hypotheses.}
    \label{fig:overview}
\end{figure}
```

---

## Example Introduction Paragraph with \para{}

```latex
To do that, we seek to address three key questions.
First, {\bf what is hypothesis generation?}
The excitement around hypothesis generation is accompanied with the general excitement around AI for science.
Therefore, it is often mixed with studies on research ideation~\cite[e.g.,][]{si2024llmsgeneratenovelresearch}.
A hypothesis is a proposed explanation for a phenomenon~\citep{wikipedia_hypothesis}.
We thus define hypothesis generation as generating natural language theories/explanations about observed phenomena.

Second, {\bf what capabilities need to be benchmarked for hypothesis generation?}
Given our focus on explaining an observed phenomenon, hypothesis generation builds on the following capabilities:
1) inductive and abductive reasoning,
2) abstraction and communication, and optionally
3) synthesis, integrating new observations with existing knowledge.
```

---

## Example Contribution List

```latex
In summary, our main contributions are:
\begin{itemize}[leftmargin=*,itemsep=0pt,topsep=0pt]
    \item We develop a systematic and principled framework for benchmarking hypothesis generation and construct the first benchmark accordingly.
    \item We conduct the first comparison between methods and models for hypothesis generation. In real-world datasets, we find that \litplusdata is the best approach.
    \item We complement our real-world tasks with carefully controlled synthetic datasets at different complexity levels, demonstrating substantial room for improvement.
\end{itemize}
```

---

## Example Quote

```latex
\begin{quote}
``It is the theory that decides what can be observed.''
\hfill ---Albert Einstein
\end{quote}
```

---

## Example Macro Definitions

```latex
% Method names (use \textsc and \xspace)
\newcommand{\ours}{{\bf HypoGeniC}\xspace}
\newcommand{\hypogenic}{\textsc{HypoGeniC}\xspace}
\newcommand{\litplusdata}{\textsc{Literature + Data}\xspace}

% Dataset names
\newcommand{\deceptive}{\textsc{Deceptive Reviews}\xspace}
\newcommand{\headline}{\textsc{Headline Popularity}\xspace}

% Model names
\newcommand{\gpt}{\textsc{GPT-4o-mini}\xspace}
\newcommand{\llama}{\textsc{Llama-3.1-70B}\xspace}
\newcommand{\roberta}{\textsc{RoBERTa}\xspace}

% Result indicators
\newcommand{\increase}{\textcolor{pastelgreen}{\bm{$\uparrow$}}}
\newcommand{\decrease}{\textcolor{red}{\bm{$\downarrow$}}}
```

---

## Example Abstract Structure

```latex
\begin{abstract}
% Context/Problem (1-2 sentences)
Hypothesis generation drives scientific progress, yet it remains understudied in AI research.

% Gap (1 sentence)
While LLMs show promise, existing methods lack systematic evaluation frameworks.

% Approach (1-2 sentences)
We propose \ours, a framework that combines literature-based and data-driven hypothesis generation.

% Results (2-3 sentences)
Experiments on five datasets demonstrate improvements of 8.97\% over few-shot baselines.
Human evaluation shows our hypotheses improve decision-making accuracy by 7.44\%.

% Significance (1 sentence)
Our work provides the first comprehensive benchmark for evaluating hypothesis generation capabilities.
\end{abstract}
```

---

## Caption Spacing Configuration

```latex
% Add to preamble for tight spacing
\usepackage[small]{caption}
\usepackage{subcaption}
\captionsetup[subfigure]{aboveskip=4pt,belowskip=4pt}
\captionsetup[table]{aboveskip=4pt,belowskip=4pt}
\captionsetup[figure]{aboveskip=4pt,belowskip=4pt}
\setlength{\dbltextfloatsep}{11pt}
\setlength{\floatsep}{11pt}
\setlength{\textfloatsep}{11pt}
```
