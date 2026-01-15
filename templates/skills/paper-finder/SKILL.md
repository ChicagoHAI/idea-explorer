---
name: paper-finder
description: Find and search for academic papers using the paper-finder service. Use when conducting literature review, searching for related work, finding baseline papers, or looking for methodology references.
---

# Paper Finder

Use this when conducting literature review or searching for academic papers.

## When to Use

- Starting a literature review
- Looking for related work on a topic
- Finding baseline papers for experiments
- Searching for methodology references

## How to Use

Run the helper script from your workspace:

```bash
python scripts/find_papers.py "your research topic"
```

Options:
- `--mode fast` (default): Quick search (~30 seconds)
- `--mode diligent`: Thorough search (~3 minutes)
- `--format json`: Output as JSON instead of text

Example:
```bash
python scripts/find_papers.py "hypothesis generation with large language models" --mode fast
```

## What You Get

Returns relevance-ranked papers with:
- Title, authors, year
- Abstract (already extracted)
- URL for download
- Relevance score (0-3, focus on papers with score >= 2)
- Citation count

## After Finding Papers

1. Download PDFs for papers with relevance >= 2
2. Read abstracts first (already provided in output)
3. Only read full PDFs for most relevant papers
4. Write notes to literature_review.md immediately

## If Paper-Finder Service Not Running

The script will show a fallback message. Use manual search instead:
- arXiv: https://arxiv.org
- Semantic Scholar: https://www.semanticscholar.org
- Papers with Code: https://paperswithcode.com

Manual search works well - paper-finder is just a convenience for faster, more targeted results.
