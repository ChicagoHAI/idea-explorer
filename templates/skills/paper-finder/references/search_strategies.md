# Search Strategies for Academic Papers

## Query Construction Patterns

### Boolean Operators

Most academic search engines support:
- `AND`: Both terms must appear (often implicit)
- `OR`: Either term can appear
- `NOT` or `-`: Exclude term
- `""`: Exact phrase match

Example: `"large language models" AND reasoning NOT "chain of thought"`

### Field-Specific Searches

Different databases support field prefixes:

**Semantic Scholar**:
- `title:` - Search in title only
- `author:` - Search by author name
- `year:` - Filter by publication year

**arXiv**:
- `ti:` - Title
- `au:` - Author
- `abs:` - Abstract
- `cat:` - Category (e.g., `cat:cs.CL`)

**Google Scholar**:
- `intitle:` - In title
- `author:` - By author
- `source:` - Publication venue

### Query Templates by Research Goal

**Finding baselines**:
```
"[task name]" AND ("benchmark" OR "baseline" OR "evaluation")
```

**Finding methods**:
```
"[method name]" AND ("proposed" OR "introduce" OR "novel")
```

**Finding surveys**:
```
"[topic]" AND ("survey" OR "review" OR "overview")
```

**Finding datasets**:
```
"[domain]" AND ("dataset" OR "corpus" OR "benchmark")
```

**Finding recent work**:
```
"[topic]" AND year:2023-2024
```

## Database-Specific Strategies

### arXiv

Best for: Cutting-edge ML/AI research, preprints

Categories to search:
- `cs.CL` - Computation and Language (NLP)
- `cs.LG` - Machine Learning
- `cs.AI` - Artificial Intelligence
- `cs.CV` - Computer Vision
- `stat.ML` - Machine Learning (Statistics)

Tips:
- Check "cross-list" papers that appear in multiple categories
- Use date sorting for recent work
- Look at "related papers" suggestions

### Semantic Scholar

Best for: Citation-aware search, finding influential papers

Features:
- TLDR summaries for quick scanning
- Citation context (how papers cite each other)
- Influential citations filter
- Research topic clusters

Tips:
- Use "Highly Influential Citations" filter
- Check "References" and "Citations" tabs
- Use "Related Papers" for discovery

### Google Scholar

Best for: Broad coverage, finding published versions

Tips:
- Click "Cited by N" to find follow-up work
- Use "Related articles" for similar papers
- Check "All versions" for PDFs
- Set up alerts for topics

### Papers with Code

Best for: Finding implementations, benchmarks

Features:
- Links to official/community code
- Benchmark leaderboards
- Method comparisons

## Search Iteration Strategy

### Round 1: Exploratory (Broad)
- Use general topic terms
- Gather 50-100 initial results
- Goal: Understand landscape

### Round 2: Targeted (Focused)
- Use specific method names from Round 1
- Search for specific authors/labs
- Goal: Find core papers

### Round 3: Citation Network (Deep)
- Check references of key papers
- Find papers citing key papers
- Goal: Complete coverage

### Round 4: Recency Check (Current)
- Filter for last 1-2 years
- Check arXiv for preprints
- Goal: Don't miss new work

## Common Pitfalls

1. **Too narrow too early**: Start broad, then narrow
2. **Ignoring older work**: Seminal papers may be from years ago
3. **Missing synonyms**: Use OR for alternative terms
4. **Only one database**: Cross-reference across sources
5. **Stopping too early**: Check citation networks
