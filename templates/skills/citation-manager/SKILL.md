---
name: citation-manager
description: Manage BibTeX citations including DOI-to-BibTeX conversion, metadata extraction, validation, and deduplication. Use when building reference lists, converting DOIs to citations, or validating existing .bib files.
---

# Citation Manager

Tools and guidance for managing BibTeX citations in research projects.

## When to Use

- Converting DOIs to BibTeX entries
- Building a references.bib file from scratch
- Validating existing citations
- Deduplicating citation files
- Standardizing citation formats

## Tools

### DOI to BibTeX

Convert a DOI to a properly formatted BibTeX entry:

```bash
python .claude/skills/citation-manager/scripts/doi_to_bibtex.py "10.1234/example.doi"
```

Batch conversion from file:
```bash
python .claude/skills/citation-manager/scripts/doi_to_bibtex.py --file dois.txt --output references.bib
```

### Validate Citations

Check a .bib file for common issues:

```bash
python .claude/skills/citation-manager/scripts/validate_citations.py references.bib
```

Checks for:
- Missing required fields
- Invalid DOIs
- Duplicate entries
- Inconsistent formatting

## BibTeX Entry Types

### Conference Paper (@inproceedings)

```bibtex
@inproceedings{author2024keyword,
  title     = {Full Paper Title Here},
  author    = {Last, First and Last2, First2 and Last3, First3},
  booktitle = {Proceedings of the Conference Name},
  year      = {2024},
  pages     = {1--10},
  doi       = {10.1234/example},
}
```

Required: title, author, booktitle, year
Optional: pages, doi, url, volume

### Journal Article (@article)

```bibtex
@article{author2024keyword,
  title   = {Full Article Title Here},
  author  = {Last, First and Last2, First2},
  journal = {Journal Name},
  year    = {2024},
  volume  = {42},
  number  = {3},
  pages   = {100--115},
  doi     = {10.1234/example},
}
```

Required: title, author, journal, year
Optional: volume, number, pages, doi

### arXiv Preprint (@misc)

```bibtex
@misc{author2024keyword,
  title         = {Full Paper Title Here},
  author        = {Last, First and Last2, First2},
  year          = {2024},
  eprint        = {2401.12345},
  archiveprefix = {arXiv},
  primaryclass  = {cs.CL},
}
```

Required: title, author, year, eprint
Optional: archiveprefix, primaryclass

### Book (@book)

```bibtex
@book{author2024keyword,
  title     = {Book Title},
  author    = {Last, First},
  publisher = {Publisher Name},
  year      = {2024},
  address   = {City},
}
```

Required: title, author/editor, publisher, year
Optional: address, edition, volume

## Citation Key Conventions

Format: `authorYEARkeyword`

Examples:
- `vaswani2017attention` - Vaswani et al., 2017, "Attention Is All You Need"
- `brown2020language` - Brown et al., 2020, GPT-3 paper
- `devlin2019bert` - Devlin et al., 2019, BERT paper

Rules:
- Lowercase first author's last name
- Four-digit year
- Meaningful keyword from title (lowercase)
- No spaces, hyphens, or special characters

## Common Venue Abbreviations

### Conferences

| Full Name | Abbreviation |
|-----------|--------------|
| Neural Information Processing Systems | NeurIPS |
| International Conference on Machine Learning | ICML |
| International Conference on Learning Representations | ICLR |
| Association for Computational Linguistics | ACL |
| Empirical Methods in NLP | EMNLP |
| North American Chapter of ACL | NAACL |
| Conference on Computer Vision and Pattern Recognition | CVPR |
| AAAI Conference on Artificial Intelligence | AAAI |

### Journals

| Full Name | Abbreviation |
|-----------|--------------|
| Journal of Machine Learning Research | JMLR |
| Transactions on Machine Learning Research | TMLR |
| Artificial Intelligence | AI |
| Machine Learning | ML |

## Workflow

### Building references.bib

1. **Collect DOIs**: As you read papers, collect DOIs
2. **Convert**: Use doi_to_bibtex.py to convert
3. **Validate**: Run validate_citations.py to check
4. **Organize**: Sort alphabetically by key
5. **Integrate**: Add to paper/references.bib

### Citing in LaTeX

```latex
% Parenthetical citation
Previous work has explored this \cite{author2024keyword}.

% Textual citation (requires natbib)
\citet{author2024keyword} showed that...

% Multiple citations
Several studies \cite{paper1,paper2,paper3} found...
```

## Troubleshooting

### DOI Not Found
- Check DOI is correct (no typos)
- Try CrossRef directly: https://doi.org/[DOI]
- For arXiv, use arXiv ID instead

### Missing Fields
- Check original source for info
- Some fields are optional (add if available)
- Don't leave required fields empty

### Duplicate Keys
- Use more specific keywords
- Add first name initial: `smithj2024keyword`
- Add venue: `smith2024keywordneurips`

## References

See `references/` folder for:
- `citation_styles.md`: Style guide for different formats
