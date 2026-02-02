# Citation Style Guide

## BibTeX Best Practices

### Entry Key Conventions

**Format**: `authorYYYYkeyword`

| Example Key | Paper |
|-------------|-------|
| `vaswani2017attention` | "Attention Is All You Need" |
| `brown2020language` | "Language Models are Few-Shot Learners" |
| `devlin2019bert` | "BERT: Pre-training of Deep Bidirectional Transformers" |
| `radford2019language` | "Language Models are Unsupervised Multitask Learners" |

**Rules**:
- Use first author's last name (lowercase, no special chars)
- Four-digit year
- Single keyword from title (lowercase)
- For duplicates: add distinguishing letter (`smith2024nlpa`, `smith2024nlpb`)

### Author Formatting

**Single author**:
```bibtex
author = {Last, First}
```

**Multiple authors**:
```bibtex
author = {Last1, First1 and Last2, First2 and Last3, First3}
```

**Corporate author**:
```bibtex
author = {{Google Research} and Smith, John}
```

**With Jr./III**:
```bibtex
author = {King, Jr., Martin Luther}
```

### Title Capitalization

BibTeX lowercases titles. Protect proper nouns and acronyms:

```bibtex
title = {{BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding}
title = {Attention over {Transformer} Architectures}
title = {Learning from {ImageNet}}
```

### Page Ranges

Use double dash for ranges:
```bibtex
pages = {1--10}
pages = {1234--1245}
```

### DOI vs URL

- Prefer DOI when available (more stable)
- Use URL only if no DOI exists
- Don't include both for same resource

```bibtex
% Good
doi = {10.1234/example}

% Also OK (no DOI available)
url = {https://arxiv.org/abs/2001.12345}

% Avoid
doi = {10.1234/example},
url = {https://doi.org/10.1234/example}
```

## Venue-Specific Formats

### NeurIPS

```bibtex
@inproceedings{author2024neurips,
  title     = {Paper Title},
  author    = {Last, First and Last2, First2},
  booktitle = {Advances in Neural Information Processing Systems},
  volume    = {37},
  year      = {2024},
}
```

### ICML

```bibtex
@inproceedings{author2024icml,
  title     = {Paper Title},
  author    = {Last, First and Last2, First2},
  booktitle = {Proceedings of the International Conference on Machine Learning},
  series    = {PMLR},
  volume    = {235},
  year      = {2024},
}
```

### ACL/EMNLP/NAACL

```bibtex
@inproceedings{author2024acl,
  title     = {Paper Title},
  author    = {Last, First and Last2, First2},
  booktitle = {Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics},
  year      = {2024},
  address   = {Bangkok, Thailand},
  publisher = {Association for Computational Linguistics},
}
```

### ICLR

```bibtex
@inproceedings{author2024iclr,
  title     = {Paper Title},
  author    = {Last, First and Last2, First2},
  booktitle = {The Twelfth International Conference on Learning Representations},
  year      = {2024},
}
```

### arXiv Preprints

```bibtex
@misc{author2024arxiv,
  title         = {Paper Title},
  author        = {Last, First and Last2, First2},
  year          = {2024},
  eprint        = {2401.12345},
  archiveprefix = {arXiv},
  primaryclass  = {cs.CL},
}
```

### JMLR

```bibtex
@article{author2024jmlr,
  title   = {Paper Title},
  author  = {Last, First and Last2, First2},
  journal = {Journal of Machine Learning Research},
  volume  = {25},
  number  = {123},
  pages   = {1--50},
  year    = {2024},
}
```

## In-Text Citation Styles

### natbib Commands (LaTeX)

| Command | Output |
|---------|--------|
| `\cite{key}` | (Author et al., 2024) |
| `\citet{key}` | Author et al. (2024) |
| `\citep{key}` | (Author et al., 2024) |
| `\citeauthor{key}` | Author et al. |
| `\citeyear{key}` | 2024 |

### Usage Examples

```latex
% Parenthetical
Recent work has explored this direction \citep{brown2020language}.

% Textual
\citet{vaswani2017attention} introduced the Transformer architecture.

% Multiple citations
Several studies \citep{devlin2019bert,radford2019language,brown2020language} show...

% With page numbers
As shown by \citet[p. 5]{vaswani2017attention}...
```

## Common Issues and Fixes

### Problem: BibTeX lowercases title
**Fix**: Wrap protected text in braces
```bibtex
% Wrong: becomes "Bert: pre-training..."
title = {BERT: Pre-training...}

% Right: preserves "BERT"
title = {{BERT}: Pre-training...}
```

### Problem: Special characters not rendering
**Fix**: Use LaTeX escapes or Unicode
```bibtex
% For German umlaut
author = {M{\"u}ller, Hans}

% For accents
author = {Gonz{\'a}lez, Maria}
```

### Problem: Long author lists
**Fix**: Most styles auto-truncate to "et al."
```bibtex
% List all authors; style will format appropriately
author = {First, A and Second, B and Third, C and Fourth, D and Fifth, E}
```

### Problem: Missing venue/journal
**Fix**: Search DOI on CrossRef or paper on Google Scholar for complete metadata
