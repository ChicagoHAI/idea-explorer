# Paper Finder Setup

The paper-finder service provides high-quality literature search with relevance ranking. It significantly improves the quality of literature review compared to manual search.

## Why Paper-Finder Matters

For writing academic papers, comprehensive literature review is essential:
- **Relevance ranking**: Finds the most important papers, not just keyword matches
- **Pre-extracted abstracts**: Reduces context window usage when reviewing papers
- **Better citations**: Quality literature review leads to better academic papers
- **Time savings**: Automated search is faster than manual browsing

## Setup Options

### Option A: Docker (Recommended)

Paper-finder is built into the idea-explorer Docker image. Just add the required API keys to your `.env` file:

```bash
# In your .env file:
S2_API_KEY=your-semantic-scholar-key    # Required for paper-finder
OPENAI_API_KEY=your-openai-key          # Required (used for GPT-4.1)
COHERE_API_KEY=your-cohere-key          # Optional: improves ranking by ~7%
```

When you run `./idea-explorer build` and start the container, paper-finder automatically starts if `S2_API_KEY` and `OPENAI_API_KEY` are configured.

**That's it!** The container handles everything else.

### Option B: Native Installation

For native installations, you need to run paper-finder separately:

```bash
# 1. Install paper-finder dependencies
cd services/paper-finder
make sync-dev

# 2. Start the service (from api subdirectory)
cd agents/mabool/api
make start-dev
```

The service runs at `http://localhost:8000`.

## How It Works

When running idea-explorer, skills are copied to `.claude/skills/` in the workspace. Agents call the helper script to search for papers:

```bash
python .claude/skills/paper-finder/scripts/find_papers.py "your research topic"
python .claude/skills/paper-finder/scripts/find_papers.py "hypothesis generation with LLMs" --mode diligent
```

## API Key Tiers

| Tier | Keys Needed | Features |
|------|-------------|----------|
| **Basic** | 1 AI key (Anthropic/OpenAI/Google) | Full idea-explorer, manual paper search |
| **Standard** | + S2_API_KEY + OPENAI_API_KEY | Paper-finder with 92.5% quality |
| **Full** | + COHERE_API_KEY | Paper-finder with full reranking |

## Getting API Keys

- **S2_API_KEY**: [Semantic Scholar API](https://www.semanticscholar.org/product/api)
- **OPENAI_API_KEY**: [OpenAI Platform](https://platform.openai.com/api-keys)
- **COHERE_API_KEY**: [Cohere Dashboard](https://dashboard.cohere.com/api-keys)

## Troubleshooting

### Connection Refused
- **Docker**: Check container logs with `docker compose logs idea-explorer`
- **Native**: Ensure paper-finder is running: `curl http://localhost:8000/health`

### API Key Errors
- Verify environment variables: `echo $S2_API_KEY` and `echo $OPENAI_API_KEY`
- OpenAI API key is required since paper-finder uses GPT-4.1 for relevance judgment

### Timeout Errors
- "diligent" mode can take up to 3 minutes
- Use "fast" mode (default) for quicker results (~30 seconds)

### If Paper-Finder Is Unavailable

If paper-finder cannot be set up, agents will fall back to manual search using arXiv, Semantic Scholar, and Papers with Code. This produces lower quality results but still works. Setting up paper-finder is strongly recommended for serious academic work.

## LLM Configuration

Paper-finder uses OpenAI GPT-4.1 by default. Configuration is in:
`services/paper-finder/agents/mabool/api/conf/config.toml`

```toml
[default.dense_agent]
formulation_model_name = "openai:gpt-4.1-2025-04-14"

[default.relevance_judgement]
relevance_model_name = "openai:gpt-4.1-2025-04-14"
```

To use a different model, change the model name. Format: `provider:model-id`.
