#!/bin/bash
# =============================================================================
# idea-explorer Container Entrypoint
# Validates environment, configures credentials, and starts the container
# =============================================================================

set -e

# Color output for better visibility
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  idea-explorer Container Starting${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# -----------------------------------------------------------------------------
# Validate environment variables
# -----------------------------------------------------------------------------
validate_env() {
    local has_ai_key=false

    echo -e "${BLUE}Checking API keys...${NC}"

    # Check AI provider keys
    if [ -n "$ANTHROPIC_API_KEY" ]; then
        echo -e "  ${GREEN}[OK]${NC} ANTHROPIC_API_KEY configured (Claude)"
        has_ai_key=true
    fi

    if [ -n "$OPENAI_API_KEY" ]; then
        echo -e "  ${GREEN}[OK]${NC} OPENAI_API_KEY configured (Codex/IdeaHub)"
        has_ai_key=true
    fi

    if [ -n "$GOOGLE_API_KEY" ]; then
        echo -e "  ${GREEN}[OK]${NC} GOOGLE_API_KEY configured (Gemini)"
        has_ai_key=true
    fi

    if [ "$has_ai_key" = false ]; then
        echo -e "${RED}Error: No AI provider API key found${NC}"
        echo ""
        echo "Please provide at least one of the following in your .env file:"
        echo "  - ANTHROPIC_API_KEY (for Claude Code)"
        echo "  - OPENAI_API_KEY (for Codex and IdeaHub)"
        echo "  - GOOGLE_API_KEY (for Gemini)"
        echo ""
        exit 1
    fi

    # Check GitHub token (optional but recommended)
    if [ -n "$GITHUB_TOKEN" ]; then
        echo -e "  ${GREEN}[OK]${NC} GITHUB_TOKEN configured"
    else
        echo -e "  ${YELLOW}[WARN]${NC} GITHUB_TOKEN not set - GitHub integration disabled"
        echo "         Use --no-github flag or set GITHUB_TOKEN for full functionality"
    fi

    echo ""
}

# -----------------------------------------------------------------------------
# Configure git credentials
# -----------------------------------------------------------------------------
setup_git() {
    if [ -n "$GITHUB_TOKEN" ]; then
        echo -e "${BLUE}Configuring Git credentials...${NC}"

        # Configure credential helper
        git config --global credential.helper store

        # Store credentials securely
        echo "https://oauth2:${GITHUB_TOKEN}@github.com" > ~/.git-credentials
        chmod 600 ~/.git-credentials

        # Configure GitHub CLI if available
        if command -v gh &> /dev/null; then
            echo "$GITHUB_TOKEN" | gh auth login --with-token 2>/dev/null || true
        fi

        echo -e "  ${GREEN}[OK]${NC} Git credentials configured"
        echo ""
    fi
}

# -----------------------------------------------------------------------------
# Check GPU availability
# -----------------------------------------------------------------------------
check_gpu() {
    echo -e "${BLUE}GPU Status:${NC}"

    if command -v nvidia-smi &> /dev/null; then
        if nvidia-smi &> /dev/null; then
            nvidia-smi --query-gpu=index,name,memory.total,driver_version --format=csv,noheader | \
                while IFS=',' read -r idx name mem driver; do
                    echo -e "  ${GREEN}[GPU $idx]${NC} $name |$mem | Driver:$driver"
                done
        else
            echo -e "  ${YELLOW}[WARN]${NC} nvidia-smi failed - GPU may not be accessible"
            echo "         Ensure --gpus all (Docker) or --device nvidia.com/gpu=all (Podman) is used"
        fi
    else
        echo -e "  ${YELLOW}[WARN]${NC} nvidia-smi not available"
    fi
    echo ""
}

# -----------------------------------------------------------------------------
# Display available commands
# -----------------------------------------------------------------------------
show_help() {
    echo -e "${BLUE}Available Commands:${NC}"
    echo ""
    echo "  Fetch idea from IdeaHub:"
    echo -e "    ${GREEN}python /app/src/cli/fetch_from_ideahub.py <url> [--submit]${NC}"
    echo ""
    echo "  Submit a research idea:"
    echo -e "    ${GREEN}python /app/src/cli/submit.py <idea.yaml>${NC}"
    echo ""
    echo "  Run research exploration:"
    echo -e "    ${GREEN}python /app/src/core/runner.py <idea_id> [options]${NC}"
    echo ""
    echo "  Options for runner.py:"
    echo "    --provider {claude|codex|gemini}  AI provider (default: claude)"
    echo "    --full-permissions                Skip permission prompts"
    echo "    --no-github                       Run locally without GitHub"
    echo "    --timeout SECONDS                 Execution timeout (default: 3600)"
    echo ""
    echo -e "${BLUE}Workspace:${NC} /workspaces (mounted from host)"
    echo -e "${BLUE}App:${NC} /app"
    echo ""
}

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

# Run all setup steps
validate_env
setup_git
check_gpu

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Container Ready${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

show_help

# Execute the command passed to the container
exec "$@"
