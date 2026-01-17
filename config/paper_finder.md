# Paper Finder Setup (Recommended)

The paper-finder service is **recommended** for quality literature review and proper academic citations. It provides relevance-ranked search results that significantly improve the quality of literature review compared to manual search.

## Why Paper-Finder Matters

For writing academic papers, comprehensive literature review is essential:
- **Relevance ranking**: Finds the most important papers, not just keyword matches
- **Pre-extracted abstracts**: Reduces context window usage when reviewing papers
- **Better citations**: Quality literature review leads to better academic papers
- **Time savings**: Automated search is faster than manual browsing

## How It Works

When running idea-explorer, a helper script (`scripts/find_papers.py`) is copied to the workspace. Agents call this script to search for papers:

```bash
python scripts/find_papers.py "your research topic"
python scripts/find_papers.py "hypothesis generation with LLMs" --mode diligent
```

## Setting Up Paper Finder

### 1. Clone asta-paper-finder

```bash
git clone https://github.com/ChicagoHAI/asta-paper-finder
cd asta-paper-finder/agents/mabool/api
```

### 2. Configure API Keys

Add to your `.env` file (same file used by idea-explorer):

```bash
# Required for paper-finder
S2_API_KEY="your-semantic-scholar-key"
OPENAI_API_KEY="your-openai-key"

# Optional (improves paper reranking)
COHERE_API_KEY="your-cohere-key"
```

### 3. Start the Service

```bash
cd asta-paper-finder/agents/mabool/api
make start-dev
```

The service runs at `http://localhost:8000`.

### 4. Verify

```bash
# Check service is running
curl http://localhost:8000/health

# Test paper search
python templates/scripts/find_papers.py "machine learning calibration"
```

## LLM Configuration

The paper-finder is configured to use OpenAI GPT-4.1 by default in:
`asta-paper-finder/agents/mabool/api/conf/config.toml`

```toml
# All agents use direct model name format: openai:<model-id>
[default.dense_agent]
formulation_model_name = "openai:gpt-4.1-2025-04-14"

[default.relevance_judgement]
relevance_model_name = "openai:gpt-4.1-2025-04-14"

# ... other agents use same model
```

To use a different model, change the model name in the config. The format is `provider:model-id` where the model-id is passed directly to the provider's API.

## Troubleshooting

### Connection Refused
- Ensure asta-paper-finder is running: `curl http://localhost:8000/health`
- Check port 8000 is not in use by another service

### API Key Errors
- Verify environment variables: `echo $S2_API_KEY` and `echo $OPENAI_API_KEY`
- OpenAI API key is required since the default config uses GPT-4.1

### Timeout Errors
- "diligent" mode can take up to 3 minutes
- Use "fast" mode (default) for quicker results (~30 seconds)

### If Paper-Finder Is Unavailable

If paper-finder cannot be set up, agents will fall back to manual search using arXiv, Semantic Scholar, and Papers with Code. However, this produces lower quality results and is more time-consuming. Setting up paper-finder is strongly recommended for serious academic work.

## Future: Docker Integration

We plan to add paper-finder to the idea-explorer docker-compose for easier setup. This will allow starting both services with a single command.
