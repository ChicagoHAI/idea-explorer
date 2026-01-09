#!/bin/bash
# =============================================================================
# idea-explorer Docker/Podman Runner
# Unified script that auto-detects container runtime and handles GPU passthrough
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
# Detect container runtime (Docker or Podman)
# -----------------------------------------------------------------------------
detect_runtime() {
    if command -v podman &> /dev/null; then
        RUNTIME="podman"
        # Check if podman-compose or podman compose is available
        if command -v podman-compose &> /dev/null; then
            COMPOSE_CMD="podman-compose"
        elif podman compose version &> /dev/null 2>&1; then
            COMPOSE_CMD="podman compose"
        else
            COMPOSE_CMD=""
        fi
    elif command -v docker &> /dev/null; then
        RUNTIME="docker"
        if docker compose version &> /dev/null 2>&1; then
            COMPOSE_CMD="docker compose"
        elif command -v docker-compose &> /dev/null; then
            COMPOSE_CMD="docker-compose"
        else
            COMPOSE_CMD=""
        fi
    else
        echo -e "${RED}Error: Neither docker nor podman found${NC}"
        echo "Please install Docker or Podman to use idea-explorer containers."
        exit 1
    fi

    echo -e "${BLUE}Using container runtime:${NC} $RUNTIME"
}

# -----------------------------------------------------------------------------
# Get user ID flags to match host user (fixes permission issues with mounted volumes)
# -----------------------------------------------------------------------------
get_user_flags() {
    echo "--user $(id -u):$(id -g)"
}

# -----------------------------------------------------------------------------
# Check if GPU support is available
# -----------------------------------------------------------------------------
check_gpu_available() {
    if [ "$RUNTIME" = "podman" ]; then
        # Podman: Check if CDI spec exists
        [ -f /etc/cdi/nvidia.yaml ] || [ -f /var/run/cdi/nvidia.yaml ]
    else
        # Docker: Check if nvidia runtime is configured
        docker info 2>/dev/null | grep -qi nvidia
    fi
}

# -----------------------------------------------------------------------------
# Get GPU flags based on runtime (auto-detects availability)
# -----------------------------------------------------------------------------
get_gpu_flags() {
    if [ "$RUNTIME" = "podman" ]; then
        # Podman uses CDI (Container Device Interface) for GPU access
        if [ -f /etc/cdi/nvidia.yaml ] || [ -f /var/run/cdi/nvidia.yaml ]; then
            echo "--device nvidia.com/gpu=all --security-opt label=disable"
        else
            echo -e "${YELLOW}Note: Running without GPU (NVIDIA CDI spec not found)${NC}" >&2
            echo -e "      To enable GPU: sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml" >&2
            echo "--security-opt label=disable"
        fi
    else
        # Docker uses --gpus flag
        if check_gpu_available; then
            echo "--gpus all"
        else
            echo -e "${YELLOW}Note: Running without GPU (nvidia-container-toolkit not configured)${NC}" >&2
            echo -e "      To enable GPU: sudo apt install nvidia-container-toolkit && sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker" >&2
            echo ""
        fi
    fi
}

# -----------------------------------------------------------------------------
# Get volume flags based on runtime
# -----------------------------------------------------------------------------
get_volume_flags() {
    if [ "$RUNTIME" = "podman" ]; then
        # Podman: Use :Z for SELinux relabeling
        echo "-v \"$PROJECT_ROOT/workspaces:/workspaces:Z\" \
              -v \"$PROJECT_ROOT/ideas:/app/ideas:Z\" \
              -v \"$PROJECT_ROOT/logs:/app/logs:Z\" \
              -v \"$PROJECT_ROOT/config:/app/config:ro,Z\""
    else
        # Docker: Standard volume mounts
        echo "-v \"$PROJECT_ROOT/workspaces:/workspaces\" \
              -v \"$PROJECT_ROOT/ideas:/app/ideas\" \
              -v \"$PROJECT_ROOT/logs:/app/logs\" \
              -v \"$PROJECT_ROOT/config:/app/config:ro\""
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
        mounts="$mounts -v \"$HOME/.claude:/tmp/.claude${RUNTIME_VOL_SUFFIX}\""
        echo -e "  ${GREEN}[OK]${NC} Mounting Claude credentials" >&2
        found_any=true
    fi

    # Codex credentials (~/.codex/)
    if [ -d "$HOME/.codex" ]; then
        mounts="$mounts -v \"$HOME/.codex:/tmp/.codex${RUNTIME_VOL_SUFFIX}\""
        echo -e "  ${GREEN}[OK]${NC} Mounting Codex credentials" >&2
        found_any=true
    fi

    # Gemini CLI credentials (~/.config/gemini/)
    if [ -d "$HOME/.config/gemini" ]; then
        # Also need to create the parent .config directory structure
        mounts="$mounts -v \"$HOME/.config/gemini:/tmp/.config/gemini${RUNTIME_VOL_SUFFIX}\""
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
    $RUNTIME build -t "$IMAGE_NAME" -f docker/Dockerfile .
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

    eval "$RUNTIME run -it --rm \
        $gpu_flags \
        $user_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$PROJECT_ROOT/workspaces:/workspaces${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/workspaces:/data/hypogenicai/workspaces${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/logs:/app/logs${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro${RUNTIME_VOL_SUFFIX}\" \
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

    eval "$RUNTIME run -it --rm \
        $gpu_flags \
        $user_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$PROJECT_ROOT/workspaces:/workspaces${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/workspaces:/data/hypogenicai/workspaces${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/logs:/app/logs${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro${RUNTIME_VOL_SUFFIX}\" \
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
        local mount_flag="-v \"$idea_dir:/input:ro${RUNTIME_VOL_SUFFIX}\""
        local idea_path="/input/$idea_name"
    else
        # Relative path - assume it's in ideas/ directory
        local idea_path="/app/$idea_file"
        local mount_flag=""
    fi

    echo -e "${BLUE}Submitting research idea...${NC}"

    eval "$RUNTIME run -it --rm \
        $gpu_flags \
        $user_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$PROJECT_ROOT/workspaces:/workspaces${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/workspaces:/data/hypogenicai/workspaces${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/logs:/app/logs${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro${RUNTIME_VOL_SUFFIX}\" \
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

    eval "$RUNTIME run -it --rm \
        $gpu_flags \
        $user_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$PROJECT_ROOT/workspaces:/workspaces${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/workspaces:/data/hypogenicai/workspaces${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/logs:/app/logs${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro${RUNTIME_VOL_SUFFIX}\" \
        $credential_mounts \
        -w /app \
        \"$IMAGE_NAME\" \
        python /app/src/core/runner.py $@"
}

# -----------------------------------------------------------------------------
# Docker Compose operations
# -----------------------------------------------------------------------------
cmd_up() {
    if [ -z "$COMPOSE_CMD" ]; then
        echo -e "${RED}Error: No compose command available${NC}"
        echo "Install docker-compose or podman-compose"
        exit 1
    fi

    check_env_file
    cd "$PROJECT_ROOT"
    $COMPOSE_CMD up -d
    echo -e "${GREEN}Container started in background${NC}"
}

cmd_down() {
    if [ -z "$COMPOSE_CMD" ]; then
        echo -e "${RED}Error: No compose command available${NC}"
        exit 1
    fi

    cd "$PROJECT_ROOT"
    $COMPOSE_CMD down
    echo -e "${GREEN}Container stopped${NC}"
}

cmd_logs() {
    if [ -z "$COMPOSE_CMD" ]; then
        echo -e "${RED}Error: No compose command available${NC}"
        exit 1
    fi

    cd "$PROJECT_ROOT"
    $COMPOSE_CMD logs -f
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
    mkdir -p "$HOME/.claude" "$HOME/.codex" "$HOME/.config/gemini"

    local gpu_flags=$(get_gpu_flags)

    # Note: No --user flag for login - we run as the container user to write credentials
    # But we mount with :rw so credentials persist to host
    eval "$RUNTIME run -it --rm \
        $gpu_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$HOME/.claude:/tmp/.claude${RUNTIME_VOL_SUFFIX}\" \
        -v \"$HOME/.codex:/tmp/.codex${RUNTIME_VOL_SUFFIX}\" \
        -v \"$HOME/.config/gemini:/tmp/.config/gemini${RUNTIME_VOL_SUFFIX}\" \
        -w /tmp \
        \"$IMAGE_NAME\" \
        bash"
}

# -----------------------------------------------------------------------------
# Show help
# -----------------------------------------------------------------------------
cmd_help() {
    echo ""
    echo -e "${BLUE}idea-explorer Container Runner${NC}"
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

# Detect runtime first
detect_runtime

# Set volume suffix for SELinux (Podman only)
if [ "$RUNTIME" = "podman" ]; then
    RUNTIME_VOL_SUFFIX=":Z"
else
    RUNTIME_VOL_SUFFIX=""
fi

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
