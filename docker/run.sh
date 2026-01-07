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
# Get GPU flags based on runtime
# -----------------------------------------------------------------------------
get_gpu_flags() {
    if [ "$RUNTIME" = "podman" ]; then
        # Podman uses CDI (Container Device Interface) for GPU access
        # Check if CDI spec exists
        if [ -f /etc/cdi/nvidia.yaml ] || [ -f /var/run/cdi/nvidia.yaml ]; then
            echo "--device nvidia.com/gpu=all --security-opt label=disable"
        else
            echo -e "${YELLOW}Warning: NVIDIA CDI spec not found${NC}" >&2
            echo "Run: sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml" >&2
            echo "--security-opt label=disable"
        fi
    else
        # Docker uses --gpus flag
        echo "--gpus all"
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

    echo -e "${BLUE}Starting interactive shell...${NC}"

    eval "$RUNTIME run -it --rm \
        $gpu_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$PROJECT_ROOT/workspaces:/workspaces${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/logs:/app/logs${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro${RUNTIME_VOL_SUFFIX}\" \
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

    echo -e "${BLUE}Fetching from IdeaHub...${NC}"

    eval "$RUNTIME run -it --rm \
        $gpu_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$PROJECT_ROOT/workspaces:/workspaces${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/logs:/app/logs${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro${RUNTIME_VOL_SUFFIX}\" \
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
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$PROJECT_ROOT/workspaces:/workspaces${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/logs:/app/logs${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro${RUNTIME_VOL_SUFFIX}\" \
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

    echo -e "${BLUE}Running research exploration...${NC}"

    eval "$RUNTIME run -it --rm \
        $gpu_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -v \"$PROJECT_ROOT/workspaces:/workspaces${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/logs:/app/logs${RUNTIME_VOL_SUFFIX}\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro${RUNTIME_VOL_SUFFIX}\" \
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
    echo "  shell                     Start an interactive shell"
    echo "  fetch <url> [--submit]    Fetch idea from IdeaHub"
    echo "  submit <idea.yaml>        Submit a research idea"
    echo "  run <id> [options]        Run research exploration"
    echo "  up                        Start container in background (compose)"
    echo "  down                      Stop background container (compose)"
    echo "  logs                      View container logs (compose)"
    echo "  help                      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 fetch https://ideahub.example.com/idea/123 --submit"
    echo "  $0 submit ideas/examples/ml_regularization_test.yaml"
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
