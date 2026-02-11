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
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# -----------------------------------------------------------------------------
# ASCII Art Banner
# -----------------------------------------------------------------------------
show_banner() {
    echo -e "${BLUE}${BOLD}"
    echo '  ___    _                _____            _                       '
    echo ' |_ _|__| | ___  __ _   | ____|_  ___ __ | | ___  _ __ ___ _ __  '
    echo '  | |/ _` |/ _ \/ _` |  |  _| \ \/ / '"'"'_ \| |/ _ \| '"'"'__/ _ \ '"'"'__|'
    echo '  | | (_| |  __/ (_| |  | |___ >  <| |_) | | (_) | | |  __/ |   '
    echo ' |___\__,_|\___|\__,_|  |_____/_/\_\ .__/|_|\___/|_|  \___|_|   '
    echo '                                    |_|                           '
    echo -e "${NC}"
    echo -e "  ${DIM}Autonomous Research Framework${NC}  ${CYAN}github.com/ChicagoHAI/idea-explorer${NC}"
    echo ""
}

# -----------------------------------------------------------------------------
# Status dashboard
# -----------------------------------------------------------------------------
show_status() {
    echo -e "  ${BOLD}Status:${NC}"

    # Docker
    if command -v docker &> /dev/null; then
        echo -e "    Docker .............. ${GREEN}[OK]${NC}"
    else
        echo -e "    Docker .............. ${RED}[MISSING]${NC} install docker first"
    fi

    # Docker image
    if docker image inspect "$IMAGE_NAME" &> /dev/null; then
        echo -e "    Docker image ........ ${GREEN}[OK]${NC} $IMAGE_NAME"
    else
        echo -e "    Docker image ........ ${YELLOW}[MISSING]${NC} run: ./idea-explorer setup"
    fi

    # GPU
    if docker info 2>/dev/null | grep -qi nvidia; then
        echo -e "    GPU ................. ${GREEN}[OK]${NC} nvidia-container-toolkit"
    else
        echo -e "    GPU ................. ${YELLOW}[WARN]${NC} nvidia-container-toolkit not found"
    fi

    # .env
    if [ -f "$PROJECT_ROOT/.env" ]; then
        echo -e "    .env ................ ${GREEN}[OK]${NC} configured"
    else
        echo -e "    .env ................ ${YELLOW}[MISSING]${NC} run: ./idea-explorer setup"
    fi

    # Claude credentials
    if [ -d "$HOME/.claude" ]; then
        echo -e "    Claude credentials .. ${GREEN}[OK]${NC} ~/.claude found"
    else
        echo -e "    Claude credentials .. ${DIM}[--]${NC} not configured"
    fi

    # Codex credentials
    if [ -d "$HOME/.codex" ]; then
        echo -e "    Codex credentials ... ${GREEN}[OK]${NC} ~/.codex found"
    fi

    # Gemini credentials
    if [ -d "$HOME/.gemini" ]; then
        echo -e "    Gemini credentials .. ${GREEN}[OK]${NC} ~/.gemini found"
    fi

    echo ""
}

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
# Get workspace directory from config
# Reads workspace.yaml (or falls back to workspace.yaml.example)
# -----------------------------------------------------------------------------
get_workspace_dir() {
    local config_file="$PROJECT_ROOT/config/workspace.yaml"
    local template_file="$PROJECT_ROOT/config/workspace.yaml.example"
    local parent_dir=""

    # Try user config first, then template
    if [ -f "$config_file" ]; then
        parent_dir=$(grep -E '^\s*parent_dir:' "$config_file" | sed 's/.*parent_dir:\s*["'\'']\?\([^"'\'']*\)["'\'']\?.*/\1/' | tr -d ' ')
    elif [ -f "$template_file" ]; then
        parent_dir=$(grep -E '^\s*parent_dir:' "$template_file" | sed 's/.*parent_dir:\s*["'\'']\?\([^"'\'']*\)["'\'']\?.*/\1/' | tr -d ' ')
    fi

    # Default to ./workspaces if not found or empty
    if [ -z "$parent_dir" ]; then
        parent_dir="$PROJECT_ROOT/workspaces"
    # Handle relative paths (make them relative to project root)
    elif [[ "$parent_dir" != /* ]]; then
        parent_dir="$PROJECT_ROOT/$parent_dir"
    fi

    echo "$parent_dir"
}

# -----------------------------------------------------------------------------
# Ensure directories exist
# -----------------------------------------------------------------------------
ensure_directories() {
    local workspace_dir=$(get_workspace_dir)
    mkdir -p "$workspace_dir"
    mkdir -p "$PROJECT_ROOT/logs"
}

# -----------------------------------------------------------------------------
# Check for .env file
# -----------------------------------------------------------------------------
check_env_file() {
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        echo -e "${YELLOW}Warning: .env file not found${NC}"
        if [ -f "$PROJECT_ROOT/.env.example" ]; then
            echo "Create one from the template:"
            echo "  cp .env.example .env"
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
    local workspace_dir=$(get_workspace_dir)

    echo -e "${BLUE}Starting interactive shell...${NC}"
    echo -e "${BLUE}Workspace:${NC} $workspace_dir -> /workspaces"

    eval "docker run -it --rm \
        $gpu_flags \
        $user_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -e IDEA_EXPLORER_WORKSPACE=/workspaces \
        -v \"$workspace_dir:/workspaces\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas\" \
        -v \"$PROJECT_ROOT/logs:/app/logs\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro\" \
        -v \"$PROJECT_ROOT/templates:/app/templates:ro\" \
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
    local workspace_dir=$(get_workspace_dir)

    echo -e "${BLUE}Fetching from IdeaHub...${NC}"
    echo -e "${BLUE}Workspace:${NC} $workspace_dir -> /workspaces"

    eval "docker run -it --rm \
        $gpu_flags \
        $user_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -e IDEA_EXPLORER_WORKSPACE=/workspaces \
        -v \"$workspace_dir:/workspaces\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas\" \
        -v \"$PROJECT_ROOT/logs:/app/logs\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro\" \
        -v \"$PROJECT_ROOT/templates:/app/templates:ro\" \
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

    local workspace_dir=$(get_workspace_dir)

    echo -e "${BLUE}Submitting research idea...${NC}"
    echo -e "${BLUE}Workspace:${NC} $workspace_dir -> /workspaces"

    eval "docker run -it --rm \
        $gpu_flags \
        $user_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -e IDEA_EXPLORER_WORKSPACE=/workspaces \
        -v \"$workspace_dir:/workspaces\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas\" \
        -v \"$PROJECT_ROOT/logs:/app/logs\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro\" \
        -v \"$PROJECT_ROOT/templates:/app/templates:ro\" \
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
    local workspace_dir=$(get_workspace_dir)

    echo -e "${BLUE}Running research exploration...${NC}"
    echo -e "${BLUE}Workspace:${NC} $workspace_dir -> /workspaces"

    eval "docker run -it --rm \
        $gpu_flags \
        $user_flags \
        --env-file \"$PROJECT_ROOT/.env\" \
        -e IDEA_EXPLORER_WORKSPACE=/workspaces \
        -v \"$workspace_dir:/workspaces\" \
        -v \"$PROJECT_ROOT/ideas:/app/ideas\" \
        -v \"$PROJECT_ROOT/logs:/app/logs\" \
        -v \"$PROJECT_ROOT/config:/app/config:ro\" \
        -v \"$PROJECT_ROOT/templates:/app/templates:ro\" \
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
# Setup wizard helpers
# -----------------------------------------------------------------------------

# Check prerequisites: verify required tools are installed
check_prerequisites() {
    echo -e "  ${BOLD}Step 1/5: Checking prerequisites${NC}"

    local all_ok=true

    if command -v git &> /dev/null; then
        echo -e "    ${GREEN}[OK]${NC} git found"
    else
        echo -e "    ${RED}[MISSING]${NC} git not found — install git first"
        all_ok=false
    fi

    if command -v docker &> /dev/null; then
        echo -e "    ${GREEN}[OK]${NC} docker found"
    else
        echo -e "    ${RED}[MISSING]${NC} docker not found — install Docker first"
        all_ok=false
    fi

    if command -v curl &> /dev/null; then
        echo -e "    ${GREEN}[OK]${NC} curl found"
    else
        echo -e "    ${YELLOW}[WARN]${NC} curl not found (optional, used for IdeaHub)"
    fi

    if docker info 2>/dev/null | grep -qi nvidia; then
        echo -e "    ${GREEN}[OK]${NC} nvidia-container-toolkit (GPU support)"
    else
        echo -e "    ${YELLOW}[WARN]${NC} nvidia-container-toolkit not found (GPU support optional)"
    fi

    echo ""

    if [ "$all_ok" = false ]; then
        echo -e "  ${RED}Missing required tools. Please install them and re-run setup.${NC}"
        exit 1
    fi
}

# Check Docker image: pull if needed
check_image() {
    echo -e "  ${BOLD}Step 2/5: Docker image${NC}"

    if docker image inspect "$IMAGE_NAME" &> /dev/null; then
        echo -e "    ${GREEN}[OK]${NC} Image already present: $IMAGE_NAME"
        echo ""
        return
    fi

    echo -e "    Pulling ghcr.io/chicagohai/idea-explorer:latest..."
    if docker pull ghcr.io/chicagohai/idea-explorer:latest; then
        docker tag ghcr.io/chicagohai/idea-explorer:latest "$IMAGE_NAME"
        echo -e "    ${GREEN}[OK]${NC} Image ready (tagged as $IMAGE_NAME)"
    else
        echo -e "    ${YELLOW}[WARN]${NC} Pull failed — you can build locally with: ./idea-explorer build"
    fi
    echo ""
}

# Read a secret value from user input (hidden)
# Usage: prompt_secret "Label" "ENV_VAR" "required|optional" "validation_prefix"
prompt_secret() {
    local label="$1"
    local env_var="$2"
    local required="$3"
    local prefix="$4"

    if [ "$required" = "required" ]; then
        echo -e "    ${BOLD}$label${NC} (recommended)"
    else
        echo -e "    ${BOLD}$label${NC} (optional)"
    fi

    if [ -n "$5" ]; then
        echo -e "    ${DIM}$5${NC}"
    fi

    local value=""
    if [ "$required" = "optional" ]; then
        echo -ne "    > ${DIM}[Enter to skip]${NC} "
        read -s value
        echo ""
    else
        echo -ne "    > "
        read -s value
        echo ""
    fi

    if [ -z "$value" ]; then
        echo -e "    ${DIM}[SKIP]${NC} $label skipped"
        return 1
    fi

    # Validate prefix if provided (GitHub tokens can be ghp_ or github_pat_)
    if [ -n "$prefix" ] && [[ ! "$value" == $prefix* ]]; then
        if [ "$env_var" = "GITHUB_TOKEN" ] && [[ "$value" == github_pat_* ]]; then
            : # github_pat_ is also valid
        else
            echo -e "    ${YELLOW}[WARN]${NC} Expected value starting with '$prefix' — saving anyway"
        fi
    fi

    # Write to .env
    if grep -q "^${env_var}=" "$PROJECT_ROOT/.env" 2>/dev/null; then
        sed -i "s|^${env_var}=.*|${env_var}=${value}|" "$PROJECT_ROOT/.env"
    elif grep -q "^# *${env_var}=" "$PROJECT_ROOT/.env" 2>/dev/null; then
        sed -i "s|^# *${env_var}=.*|${env_var}=${value}|" "$PROJECT_ROOT/.env"
    else
        echo "${env_var}=${value}" >> "$PROJECT_ROOT/.env"
    fi

    echo -e "    ${GREEN}[OK]${NC} $env_var saved"
    return 0
}

# Display a numbered menu and return the selection number
# Usage: prompt_choice "Header" "option1" "option2" ...
# Returns: selected number (1-based) in $REPLY
prompt_choice() {
    local header="$1"
    shift
    local options=("$@")

    echo -e "    ${BOLD}$header${NC}"
    local i=1
    for opt in "${options[@]}"; do
        echo "      [$i] $opt"
        ((i++))
    done

    local selection=""
    while true; do
        echo -ne "    > "
        read selection
        if [[ "$selection" =~ ^[0-9]+$ ]] && [ "$selection" -ge 1 ] && [ "$selection" -le "${#options[@]}" ]; then
            REPLY="$selection"
            return
        fi
        echo -e "    ${YELLOW}Please enter a number between 1 and ${#options[@]}${NC}"
    done
}

# -----------------------------------------------------------------------------
# Interactive setup wizard
# -----------------------------------------------------------------------------
cmd_setup() {
    show_banner

    echo -e "${BOLD}  Welcome to Idea Explorer!${NC}"
    echo -e "  ${DIM}This wizard will get you set up in a few minutes.${NC}"
    echo ""

    # ── Step 1: Prerequisites ──
    check_prerequisites

    # ── Step 2: Docker image ──
    check_image

    # ── Step 3: Configuration (.env) ──
    echo -e "  ${BOLD}Step 3/5: Configuration (.env)${NC}"

    if [ -f "$PROJECT_ROOT/.env" ]; then
        echo -e "    ${GREEN}[OK]${NC} .env file already exists"
        echo -ne "    Reconfigure? [y/N] "
        read reconfigure
        if [[ ! "$reconfigure" =~ ^[Yy] ]]; then
            echo -e "    ${DIM}Keeping existing configuration${NC}"
            echo ""
        else
            echo ""
            setup_env_interactive
        fi
    else
        # Create from template
        if [ -f "$PROJECT_ROOT/.env.example" ]; then
            cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
        else
            touch "$PROJECT_ROOT/.env"
        fi
        setup_env_interactive
    fi

    # ── Step 4: AI CLI Login ──
    echo -e "  ${BOLD}Step 4/5: AI CLI Login${NC}"

    prompt_choice "Which provider will you use?" \
        "Claude (recommended)" \
        "Codex" \
        "Gemini" \
        "Skip for now"

    local provider_choice="$REPLY"

    case "$provider_choice" in
        1)
            echo -e "    Opening Claude login in Docker container..."
            echo -e "    ${DIM}Run 'claude' inside, complete login, then type 'exit'${NC}"
            echo ""
            mkdir -p "$HOME/.claude"
            local gpu_flags=$(get_gpu_flags 2>/dev/null)
            eval "docker run -it --rm \
                $gpu_flags \
                --env-file \"$PROJECT_ROOT/.env\" \
                -v \"$HOME/.claude:/tmp/.claude\" \
                -w /tmp \
                \"$IMAGE_NAME\" \
                bash" 2>/dev/null || true
            if [ -d "$HOME/.claude" ] && [ "$(ls -A "$HOME/.claude" 2>/dev/null)" ]; then
                echo -e "    ${GREEN}[OK]${NC} Claude credentials saved"
            else
                echo -e "    ${YELLOW}[WARN]${NC} No Claude credentials detected — you can login later with: ./idea-explorer login"
            fi
            ;;
        2)
            echo -e "    Opening Codex login in Docker container..."
            echo -e "    ${DIM}Run 'codex' inside, complete login, then type 'exit'${NC}"
            echo ""
            mkdir -p "$HOME/.codex"
            local gpu_flags=$(get_gpu_flags 2>/dev/null)
            eval "docker run -it --rm \
                $gpu_flags \
                --env-file \"$PROJECT_ROOT/.env\" \
                -v \"$HOME/.codex:/tmp/.codex\" \
                -w /tmp \
                \"$IMAGE_NAME\" \
                bash" 2>/dev/null || true
            if [ -d "$HOME/.codex" ] && [ "$(ls -A "$HOME/.codex" 2>/dev/null)" ]; then
                echo -e "    ${GREEN}[OK]${NC} Codex credentials saved"
            else
                echo -e "    ${YELLOW}[WARN]${NC} No Codex credentials detected — you can login later with: ./idea-explorer login"
            fi
            ;;
        3)
            echo -e "    Opening Gemini login in Docker container..."
            echo -e "    ${DIM}Run 'gemini' inside, complete login, then type 'exit'${NC}"
            echo ""
            mkdir -p "$HOME/.gemini"
            local gpu_flags=$(get_gpu_flags 2>/dev/null)
            eval "docker run -it --rm \
                $gpu_flags \
                --env-file \"$PROJECT_ROOT/.env\" \
                -v \"$HOME/.gemini:/tmp/.gemini\" \
                -w /tmp \
                \"$IMAGE_NAME\" \
                bash" 2>/dev/null || true
            if [ -d "$HOME/.gemini" ] && [ "$(ls -A "$HOME/.gemini" 2>/dev/null)" ]; then
                echo -e "    ${GREEN}[OK]${NC} Gemini credentials saved"
            else
                echo -e "    ${YELLOW}[WARN]${NC} No Gemini credentials detected — you can login later with: ./idea-explorer login"
            fi
            ;;
        4)
            echo -e "    ${DIM}[SKIP]${NC} You can login later with: ./idea-explorer login"
            ;;
    esac
    echo ""

    # ── Step 5: Run your first idea ──
    echo -e "  ${BOLD}Step 5/5: Run your first idea (optional)${NC}"

    prompt_choice "How would you like to provide your research idea?" \
        "IdeaHub URL (paste a link from hypogenic.ai/ideahub)" \
        "YAML file (local file path)" \
        "Try an example idea (built-in)" \
        "Skip — I'll run later"

    local idea_choice="$REPLY"

    # Determine provider flag from step 4
    local provider_flag="claude"
    case "$provider_choice" in
        2) provider_flag="codex" ;;
        3) provider_flag="gemini" ;;
    esac

    case "$idea_choice" in
        1)
            echo -ne "    Paste your IdeaHub URL: "
            read ideahub_url
            if [ -z "$ideahub_url" ]; then
                echo -e "    ${YELLOW}[SKIP]${NC} No URL provided"
            else
                echo ""
                echo -e "    ${DIM}Provider: $provider_flag | Full permissions: yes (safe in Docker)${NC}"
                echo -e "    Starting: ./idea-explorer fetch $ideahub_url --submit --run --provider $provider_flag --full-permissions"
                echo ""
                # Re-exec via the wrapper to run fetch
                exec "$PROJECT_ROOT/idea-explorer" fetch "$ideahub_url" --submit --run --provider "$provider_flag" --full-permissions
            fi
            ;;
        2)
            echo -ne "    Path to YAML file: "
            read yaml_path
            if [ -z "$yaml_path" ] || [ ! -f "$yaml_path" ]; then
                echo -e "    ${YELLOW}[SKIP]${NC} File not found or no path provided"
            else
                echo ""
                echo -e "    ${DIM}Provider: $provider_flag | Full permissions: yes (safe in Docker)${NC}"
                echo -e "    Starting: ./idea-explorer submit $yaml_path then run"
                echo ""
                # Submit then run — let user handle the run step since they need the idea ID
                exec "$PROJECT_ROOT/idea-explorer" submit "$yaml_path" --run --provider "$provider_flag" --full-permissions
            fi
            ;;
        3)
            local example_file="ideas/examples/ml_regularization_test.yaml"
            echo -e "    Using built-in example: $example_file"
            echo ""
            echo -e "    ${DIM}Provider: $provider_flag | Full permissions: yes (safe in Docker)${NC}"
            echo -e "    Starting: ./idea-explorer submit $example_file then run"
            echo ""
            exec "$PROJECT_ROOT/idea-explorer" submit "$example_file" --run --provider "$provider_flag" --full-permissions
            ;;
        4)
            echo ""
            echo -e "  ${GREEN}Setup complete!${NC} You're ready to go."
            echo ""
            echo "  Next steps:"
            echo "    ./idea-explorer fetch <ideahub_url> --submit --run --provider claude --full-permissions"
            echo "    ./idea-explorer help"
            echo ""
            ;;
    esac
}

# Helper: interactive .env configuration
setup_env_interactive() {
    prompt_secret "GitHub Token" "GITHUB_TOKEN" "required" "ghp_" \
        "Get one at: https://github.com/settings/tokens (repo scope)"
    echo ""

    prompt_secret "OpenAI API Key" "OPENAI_API_KEY" "optional" "sk-" \
        "Enables IdeaHub + LLM repo naming"
    echo ""

    prompt_secret "Semantic Scholar API Key" "S2_API_KEY" "optional" "" \
        "Enables paper-finder literature search (https://www.semanticscholar.org/product/api)"
    echo ""

    echo -e "    ${GREEN}[OK]${NC} .env file configured"
    echo ""
}

# -----------------------------------------------------------------------------
# Show help
# -----------------------------------------------------------------------------
cmd_help() {
    show_banner
    show_status

    echo "Usage: $0 <command> [arguments]"
    echo ""
    echo "Commands:"
    echo "  setup                     Interactive setup wizard (start here!)"
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
    echo "  $0 setup                  # Interactive wizard (recommended)"
    echo ""
    echo "Daily usage:"
    echo "  $0 fetch https://ideahub.example.com/idea/123 --submit --run --provider claude --full-permissions"
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
    setup)
        cmd_setup
        ;;
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
