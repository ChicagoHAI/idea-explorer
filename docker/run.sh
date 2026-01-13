#!/bin/bash
# =============================================================================
# idea-explorer Docker Runner
# Handles GPU passthrough and credential mounting for containerized execution
# =============================================================================

set -e

# Get script and project directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
IMAGE_NAME="chicagohai/idea-explorer:latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# -----------------------------------------------------------------------------
# Check Docker is available
# -----------------------------------------------------------------------------
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker not found${NC}"
        echo "Please install Docker to use idea-explorer containers."
        exit 1
    fi
}

# -----------------------------------------------------------------------------
# Get user ID flags to match host user (fixes permission issues with mounted volumes)
# -----------------------------------------------------------------------------
get_user_flags() {
    echo "--user $(id -u):$(id -g)"
}

# -----------------------------------------------------------------------------
# Get GPU flags (auto-detects availability)
# -----------------------------------------------------------------------------
get_gpu_flags() {
    if docker info 2>/dev/null | grep -qi nvidia; then
        echo "--gpus all"
    else
        echo -e "${YELLOW}Note: Running without GPU (nvidia-container-toolkit not configured)${NC}" >&2
        echo -e "      To enable GPU: sudo apt install nvidia-container-toolkit && sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker" >&2
        echo ""
    fi
}

# -----------------------------------------------------------------------------
# Get CLI credential mounts (for Claude, Codex, Gemini authentication)
# When running with --user flag, HOME=/tmp, so mount credentials there
# -----------------------------------------------------------------------------
get_cli_credential_mounts() {
    local mounts=""
    local found_any=false

    echo -e "${BLUE}Checking CLI credentials...${NC}" >&2

    # Claude Code credentials (~/.claude/)
    if [ -d "$HOME/.claude" ]; then
        mounts="$mounts -v \"$HOME/.claude:/tmp/.claude\""
        echo -e "  ${GREEN}[OK]${NC} Mounting Claude credentials" >&2
        found_any=true
    fi

    # Codex credentials (~/.codex/)
    if [ -d "$HOME/.codex" ]; then
        mounts="$mounts -v \"$HOME/.codex:/tmp/.codex\""
        echo -e "  ${GREEN}[OK]${NC} Mounting Codex credentials" >&2
        found_any=true
    fi

    # Gemini CLI credentials (~/.gemini/)
    if [ -d "$HOME/.gemini" ]; then
        mounts="$mounts -v \"$HOME/.gemini:/tmp/.gemini\""
        echo -e "  ${GREEN}[OK]${NC} Mounting Gemini credentials" >&2
        found_any=true
    fi

    if [ "$found_any" = false ]; then
        echo -e "  ${YELLOW}[WARN]${NC} No CLI credentials found." >&2
        echo -e "         Run 'claude', 'codex', or 'gemini' on host to login first." >&2
    fi

    echo ""  >&2
    echo "$mounts"
}

# -----------------------------------------------------------------------------
# Ensure directories exist
# -----------------------------------------------------------------------------
ensure_directories() {
    mkdir -p "$PROJECT_ROOT/workspaces"
    mkdir -p "$PROJECT_ROOT/logs"
}

# -----------------------------------------------------------------------------
# Check for .env file
# -----------------------------------------------------------------------------
check_env_file() {
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        echo -e "${YELLOW}Warning: .env file not found${NC}"
        if [ -f "$PROJECT_ROOT/.env.docker.example" ]; then
            echo "Create one from the template:"
            echo "  cp .env.docker.example .env"
            echo "  # Edit .env with your API keys"
        fi
        echo ""
    fi
}

# -----------------------------------------------------------------------------
# Build the container image
# -----------------------------------------------------------------------------
cmd_build() {
    echo -e "${BLUE}Building idea-explorer container image...${NC}"
    cd "$PROJECT_ROOT"
    docker build -t "$IMAGE_NAME" -f docker/Dockerfile .
    echo -e "${GREEN}Build complete!${NC}"
}

# -----------------------------------------------------------------------------
# Run interactive shell
# -----------------------------------------------------------------------------
cmd_shell() {
    ensure_directories
    check_env_file

    local gpu_flags=$(get_gpu_flags)
    local user_flags=$(get_user_flags)
    local credential_mounts=$(get_cli_credential_mounts)

    echo -e "${BLUE}Starting interactive shell...${NC}"

    eval "docker run -it --rm \
        $gpu_flags \
        $user_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$PROJECT_ROOT/workspaces:/workspaces\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas\" \
        -v \"$PROJECT_ROOT/logs:/app/logs\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro\" \
        $credential_mounts \
        -w /workspaces \
        \"$IMAGE_NAME\" \
        bash"
}

# -----------------------------------------------------------------------------
# Fetch from IdeaHub
# -----------------------------------------------------------------------------
cmd_fetch() {
    if [ -z "$1" ]; then
        echo -e "${RED}Usage: $0 fetch <ideahub_url> [--submit]${NC}"
        exit 1
    fi

    ensure_directories
    check_env_file

    local gpu_flags=$(get_gpu_flags)
    local user_flags=$(get_user_flags)
    local credential_mounts=$(get_cli_credential_mounts)

    echo -e "${BLUE}Fetching from IdeaHub...${NC}"

    eval "docker run -it --rm \
        $gpu_flags \
        $user_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$PROJECT_ROOT/workspaces:/workspaces\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas\" \
        -v \"$PROJECT_ROOT/logs:/app/logs\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro\" \
        $credential_mounts \
        -w /app \
        \"$IMAGE_NAME\" \
        python /app/src/cli/fetch_from_ideahub.py $@"
}

# -----------------------------------------------------------------------------
# Submit a research idea
# -----------------------------------------------------------------------------
cmd_submit() {
    if [ -z "$1" ]; then
        echo -e "${RED}Usage: $0 submit <idea.yaml> [options]${NC}"
        exit 1
    fi

    ensure_directories
    check_env_file

    local gpu_flags=$(get_gpu_flags)
    local user_flags=$(get_user_flags)
    local credential_mounts=$(get_cli_credential_mounts)
    local idea_file="$1"
    shift

    # Handle relative vs absolute paths for idea file
    if [[ "$idea_file" = /* ]]; then
        # Absolute path - mount the parent directory
        local idea_dir=$(dirname "$idea_file")
        local idea_name=$(basename "$idea_file")
        local mount_flag="-v \"$idea_dir:/input:ro\""
        local idea_path="/input/$idea_name"
    else
        # Relative path - assume it's in ideas/ directory
        local idea_path="/app/$idea_file"
        local mount_flag=""
    fi

    echo -e "${BLUE}Submitting research idea...${NC}"

    eval "docker run -it --rm \
        $gpu_flags \
        $user_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$PROJECT_ROOT/workspaces:/workspaces\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas\" \
        -v \"$PROJECT_ROOT/logs:/app/logs\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro\" \
        $credential_mounts \
        $mount_flag \
        -w /app \
        \"$IMAGE_NAME\" \
        python /app/src/cli/submit.py \"$idea_path\" $@"
}

# -----------------------------------------------------------------------------
# Run research exploration
# -----------------------------------------------------------------------------
cmd_run() {
    if [ -z "$1" ]; then
        echo -e "${RED}Usage: $0 run <idea_id> [--provider claude|codex|gemini] [options]${NC}"
        exit 1
    fi

    ensure_directories
    check_env_file

    local gpu_flags=$(get_gpu_flags)
    local user_flags=$(get_user_flags)
    local credential_mounts=$(get_cli_credential_mounts)

    echo -e "${BLUE}Running research exploration...${NC}"

    eval "docker run -it --rm \
        $gpu_flags \
        $user_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$PROJECT_ROOT/workspaces:/workspaces\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas\" \
        -v \"$PROJECT_ROOT/logs:/app/logs\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro\" \
        $credential_mounts \
        -w /app \
        \"$IMAGE_NAME\" \
        python /app/src/core/runner.py $@"
}

# -----------------------------------------------------------------------------
# Docker Compose operations
# -----------------------------------------------------------------------------
cmd_up() {
    check_env_file
    cd "$PROJECT_ROOT"
    docker compose up -d
    echo -e "${GREEN}Container started in background${NC}"
}

cmd_down() {
    cd "$PROJECT_ROOT"
    docker compose down
    echo -e "${GREEN}Container stopped${NC}"
}

cmd_logs() {
    cd "$PROJECT_ROOT"
    docker compose logs -f
}

# -----------------------------------------------------------------------------
# Login to CLI tools (interactive shell for authentication)
# -----------------------------------------------------------------------------
cmd_login() {
    local provider="${1:-claude}"

    ensure_directories

    echo -e "${BLUE}Starting login shell for $provider...${NC}"
    echo ""
    echo "Run one of these commands inside the container:"
    echo "  claude   # Login to Claude Code"
    echo "  codex    # Login to Codex"
    echo "  gemini   # Login to Gemini CLI"
    echo ""
    echo "After logging in, exit the shell. Your credentials will be saved."
    echo ""

    # For login, we need write access to credential directories
    # Create them on host if they don't exist
    mkdir -p "$HOME/.claude" "$HOME/.codex" "$HOME/.gemini"

    local gpu_flags=$(get_gpu_flags)

    # Note: No --user flag for login - we run as the container user to write credentials
    eval "docker run -it --rm \
        $gpu_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$HOME/.claude:/tmp/.claude\" \
        -v \"$HOME/.codex:/tmp/.codex\" \
        -v \"$HOME/.gemini:/tmp/.gemini\" \
        -w /tmp \
        \"$IMAGE_NAME\" \
        bash"
}

# -----------------------------------------------------------------------------
# Show help
# -----------------------------------------------------------------------------
cmd_help() {
    echo ""
    echo -e "${BLUE}idea-explorer Docker Runner${NC}"
    echo ""
    echo "Usage: $0 <command> [arguments]"
    echo ""
    echo "Commands:"
    echo "  build                     Build the container image"
    echo "  login [provider]          Login to CLI tools (claude/codex/gemini)"
    echo "  shell                     Start an interactive shell"
    echo "  fetch <url> [--submit]    Fetch idea from IdeaHub"
    echo "  submit <idea.yaml>        Submit a research idea"
    echo "  run <id> [options]        Run research exploration"
    echo "  up                        Start container in background (compose)"
    echo "  down                      Stop background container (compose)"
    echo "  logs                      View container logs (compose)"
    echo "  help                      Show this help message"
    echo ""
    echo "First-time setup:"
    echo "  1. $0 build               # Build the container"
    echo "  2. $0 login               # Login to Claude/Codex/Gemini"
    echo ""
    echo "Daily usage:"
    echo "  $0 fetch https://ideahub.example.com/idea/123 --submit"
    echo "  $0 run my-idea-id --provider claude --full-permissions"
    echo "  $0 shell"
    echo ""
}

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

# Check Docker is available
check_docker

# Parse command
ACTION="${1:-help}"
shift 2>/dev/null || true

case "$ACTION" in
    build)
        cmd_build
        ;;
    login)
        cmd_login "$@"
        ;;
    shell)
        cmd_shell
        ;;
    fetch)
        cmd_fetch "$@"
        ;;
    submit)
        cmd_submit "$@"
        ;;
    run)
        cmd_run "$@"
        ;;
    up)
        cmd_up
        ;;
    down)
        cmd_down
        ;;
    logs)
        cmd_logs
        ;;
    help|--help|-h)
        cmd_help
        ;;
    *)
        echo -e "${RED}Unknown command: $ACTION${NC}"
        cmd_help
        exit 1
        ;;
esac
