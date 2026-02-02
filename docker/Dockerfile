# syntax=docker/dockerfile:1.5
# idea-explorer Docker Image
# Multi-stage build with NVIDIA CUDA for GPU-accelerated ML experiments

ARG CUDA_VERSION=12.6.3
ARG UBUNTU_VERSION=22.04
ARG UV_VERSION=0.5.11

# =============================================================================
# Stage 1: Builder - Install all dependencies
# =============================================================================
FROM nvidia/cuda:${CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION} AS builder

# Metadata
LABEL org.opencontainers.image.title="idea-explorer"
LABEL org.opencontainers.image.description="Autonomous research framework with AI agents"
LABEL org.opencontainers.image.source="https://github.com/ChicagoHAI/idea-explorer"
LABEL maintainer="ChicagoHAI"

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Essential build tools
    build-essential \
    curl \
    wget \
    git \
    ca-certificates \
    gnupg \
    # Python build dependencies
    libssl-dev \
    libffi-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    liblzma-dev \
    zlib1g-dev \
    # Git for GitHub operations
    git-lfs \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 22 (required for Codex CLI which needs Node 22+)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && rm -rf /var/lib/apt/lists/*

# Copy uv from official image (best practice)
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /usr/local/bin/uv

# uv environment settings
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed

# Install Python via uv (same as local: uv python install 3.12)
RUN uv python install 3.12

# Install AI CLI tools globally via npm
RUN npm install -g @anthropic-ai/claude-code \
    && npm install -g @openai/codex \
    && npm install -g @google/gemini-cli

# Create app directory and copy dependency files first (for better layer caching)
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./

# Create minimal src directory structure for hatchling
RUN mkdir -p src

# Create virtual environment and install Python dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv /app/.venv \
    && uv sync --frozen --no-dev

# =============================================================================
# Stage 2: Runtime - Production image with uv available for agents
# =============================================================================
FROM nvidia/cuda:${CUDA_VERSION}-runtime-ubuntu${UBUNTU_VERSION} AS runtime

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    git-lfs \
    openssh-client \
    ca-certificates \
    # For nvidia-smi and CUDA runtime
    libcudnn8 \
    && rm -rf /var/lib/apt/lists/*

# Install LaTeX for paper compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-science \
    texlive-bibtex-extra \
    biber \
    latexmk \
    && rm -rf /var/lib/apt/lists/*

# Copy Node.js from builder
COPY --from=builder /usr/bin/node /usr/bin/
COPY --from=builder /usr/lib/node_modules /usr/lib/node_modules
RUN ln -sf /usr/lib/node_modules/npm/bin/npm-cli.js /usr/bin/npm \
    && ln -sf /usr/lib/node_modules/npm/bin/npx-cli.js /usr/bin/npx

# Copy CLI tool binaries (npm creates these during global install)
COPY --from=builder /usr/bin/claude /usr/bin/claude
COPY --from=builder /usr/bin/codex /usr/bin/codex
COPY --from=builder /usr/bin/gemini /usr/bin/gemini

# Copy uv for agents to use (they need to manage their own environments)
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /usr/local/bin/uv

# Copy Python installation from builder (installed by uv)
COPY --from=builder /python /python

# Copy Python virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Set up paths - IMPORTANT: this makes python and uv available
ENV PATH="/app/.venv/bin:/python/bin:/usr/local/bin:${PATH}"
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed
ENV VIRTUAL_ENV="/app/.venv"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
# Add /app to PYTHONPATH so 'templates' and 'src' modules can be imported
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Create non-root user for security (with configurable UID/GID)
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} researcher \
    && useradd -u ${UID} -g researcher -m -s /bin/bash researcher

# Create workspace directory (will be mounted from host)
RUN mkdir -p /workspaces && chown researcher:researcher /workspaces

# Copy application code
WORKDIR /app
COPY --chown=researcher:researcher . .

# Create necessary directories
RUN mkdir -p /app/ideas/submitted /app/ideas/in_progress /app/ideas/completed \
    /app/logs /app/runs \
    && chown -R researcher:researcher /app

# Fix permissions for running as any user (needed when using --user flag)
# Make all directories and files readable/executable by everyone
RUN chmod -R a+rX /app

# Switch to non-root user
USER researcher

# Configure git for the researcher user
RUN git config --global user.email "researcher@idea-explorer" \
    && git config --global user.name "Idea Explorer" \
    && git config --global init.defaultBranch main

# Create CLI tool configuration directories and uv cache
RUN mkdir -p ~/.config/claude ~/.config/codex ~/.config/gemini ~/.cache/uv

# Set environment variable for workspace location
ENV IDEA_EXPLORER_WORKSPACE=/workspaces

# Declare volume mount point
VOLUME ["/workspaces"]

# Default working directory for research
WORKDIR /workspaces

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Entrypoint
ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["bash"]
