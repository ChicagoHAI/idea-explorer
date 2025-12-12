# GitHub Integration Guide

Idea Explorer now automatically creates GitHub repositories for each research experiment and pushes results when complete. This enables:

- **Transparency**: All research is public by default
- **Collaboration**: Easy sharing and building on prior work
- **Reproducibility**: Complete research artifacts in version control
- **Organization**: Centralized research under ChicagoHAI

## Quick Setup

### 1. Create GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Idea Explorer"
4. Select scopes:
   - ✅ **repo** (Full control of private repositories)
   - ✅ **write:org** (Create repositories in organizations)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

### 2. Configure Environment

**Option A: Using .env file (Recommended)**

```bash
cd idea-explorer
cp .env.example .env
# Edit .env and add your token
nano .env  # or use your preferred editor
```

Add this line:
```
GITHUB_TOKEN=ghp_your_token_here
```

**Option B: Environment Variable**

```bash
export GITHUB_TOKEN=ghp_your_token_here
# Add to your ~/.bashrc or ~/.zshrc to make permanent
```

### 3. Install Dependencies

```bash
uv sync  # Installs all dependencies including PyGithub, GitPython
```

### 4. Test Integration

```bash
# Submit an idea (creates GitHub repo and workspace)
python src/cli/submit.py ideas/examples/ml_regularization_test.yaml

# You should see:
# ✅ GitHub integration enabled (org: ChicagoHAI)
# 📦 Creating GitHub repository...
# ✅ Repository created: https://github.com/ChicagoHAI/...
# ✅ Workspace ready at: workspace/...

# (Optional) Add resources to workspace
cd workspace/<repo-name>
# Add datasets, documents, etc.
git add . && git commit -m "Add resources" && git push
cd ../..

# Run research (uses existing workspace)
python src/core/runner.py <idea_id>
```

## How It Works

### Workflow

**New workspace-first workflow:**

1. **Repository Creation (on submission)**
   - Creates public repo in ChicagoHAI organization when you submit an idea
   - Name based on sanitized idea ID
   - Initialized with README and Python .gitignore

2. **Local Clone (on submission)**
   - Clones repo to `workspace/<repo_name>/` immediately
   - Ready for you to add resources before running

3. **Metadata Initialization (on submission)**
   - Adds `.idea-explorer/idea.yaml` with full specification
   - Creates README.md with research overview
   - Commits: "Initialize research project: {title}"

4. **User Resources (optional, before running)**
   - You can add datasets, documents, code, etc. to workspace
   - Commit and push to GitHub
   - Agent will have access to these resources

5. **Agent Execution (on run)**
   - Pulls latest changes from GitHub (including your resources)
   - AI agent works in the repository directory
   - Creates notebooks, results, etc. directly in repo

6. **Results Publishing (after run)**
   - Commits all changes
   - Pushes to GitHub
   - Message includes research title and status

### Repository Structure

Each research repository contains:

```
repo-name/
├── README.md                    # Research overview
├── .gitignore                   # Python gitignore
├── .idea-explorer/
│   └── idea.yaml                # Full idea specification
├── notebooks/
│   ├── plan_Md.ipynb           # Research plan
│   ├── documentation_Md.ipynb   # Results and analysis
│   └── code_walk_Md.ipynb      # Code walkthrough
├── results/
│   ├── metrics.json            # Quantitative results
│   └── *.png                   # Visualizations
├── artifacts/                   # Models, data, etc.
└── logs/
    ├── research_prompt.txt      # Generated prompt
    └── execution_claude.log     # Execution log
```

## Configuration Options

### Default Organization

Repositories are created in **ChicagoHAI** by default.

To use a different organization:

```bash
python src/core/runner.py <idea_id> --github-org YourOrgName
```

### Public vs Private Repos

Currently creates **public repositories** by default for research transparency.

To change default (requires code modification):

```python
# In src/core/runner.py, line ~133
private=True  # Change to True for private repos
```

### Disable GitHub Integration

Run locally without GitHub:

```bash
python src/core/runner.py <idea_id> --no-github
```

This creates results in `runs/` directory as before.

## Troubleshooting

### "GitHub integration disabled: GITHUB_TOKEN not set"

**Solution**: Set GITHUB_TOKEN environment variable or create .env file

```bash
# Check if token is set
echo $GITHUB_TOKEN

# Set for current session
export GITHUB_TOKEN=ghp_your_token_here

# Or create .env file
cp .env.example .env
# Edit .env and add your token
```

### "Failed to access organization 'ChicagoHAI'"

**Cause**: Your token doesn't have permission to create repos in the organization

**Solutions**:
1. Ask organization admin to invite you
2. Ensure your token has `write:org` scope
3. Use a different organization you have access to:
   ```bash
   python src/core/runner.py <idea_id> --github-org YourUsername
   ```

### "PyGithub not installed"

**Solution**:
```bash
pip install PyGithub GitPython
```

### "Repository already exists"

The system will reuse the existing repository if it already exists.

To force a new repo, change the idea_id or delete the existing repo on GitHub.

### "Failed to push to GitHub"

**Common causes**:
- Token expired → Generate new token
- Network issues → Check internet connection
- Permission issues → Verify token scopes

Results are still saved locally in `workspace/`, you can push manually:

```bash
cd workspace/<repo-name>
git add .
git commit -m "Research results"
git push
```

## Security Best Practices

### Token Security

✅ **DO**:
- Store token in .env file (not tracked by git)
- Use environment variables
- Generate token with minimal required scopes
- Regenerate token periodically

❌ **DON'T**:
- Commit .env file to git
- Share your token
- Use overly permissive scopes
- Hardcode token in code

### .env File Protection

The `.gitignore` file ensures `.env` is never committed:

```bash
# Verify .env is ignored
git status
# Should NOT show .env

# If it does show up:
git rm --cached .env
git commit -m "Remove .env from tracking"
```

## Advanced Usage

### Programmatic Access

```python
from src.core.github_manager import GitHubManager

# Initialize
manager = GitHubManager(org_name="ChicagoHAI")

# Create repository
repo_info = manager.create_research_repo(
    idea_id="my_experiment",
    title="My Research Title",
    description="Research description",
    private=False
)

# Clone it
repo = manager.clone_repo(
    repo_info['clone_url'],
    repo_info['local_path']
)

# Work in the repo...
# ...

# Commit and push
manager.commit_and_push(
    repo_info['local_path'],
    "Add research results"
)
```

### Custom Commit Messages

Modify `src/core/runner.py` around line 309 to customize commit messages.

### Adding Collaborators

```python
from github import Github

g = Github(token)
repo = g.get_repo("ChicagoHAI/repo-name")

# Add collaborator
repo.add_to_collaborators("username", permission="push")
```

### Creating Pull Requests

```python
manager = GitHubManager()

pr_url = manager.create_summary_pr(
    repo_name="repo-name",
    title="Research Results Summary",
    body="Summary of findings...",
    head_branch="results",
    base_branch="main"
)
```

## Benefits of GitHub Integration

### For Researchers

- ✅ Automatic backup of all work
- ✅ Version control for experiments
- ✅ Easy sharing with collaborators
- ✅ Reproducibility guaranteed
- ✅ Professional portfolio of research

### For Organizations

- ✅ Centralized research repository
- ✅ Searchable experiment archive
- ✅ Transparency and accountability
- ✅ Easy code review and collaboration
- ✅ Built-in documentation

### For Science

- ✅ Open by default
- ✅ Complete reproducibility
- ✅ Building on prior work
- ✅ Verifiable results
- ✅ Collaborative improvement

## Examples

### Basic Usage

```bash
# Create and run experiment with GitHub
python src/cli/submit.py my_idea.yaml
python src/core/runner.py my_idea_id

# Results automatically pushed to:
# https://github.com/ChicagoHAI/my-idea-id
```

### Local Development, Later Push

```bash
# Run locally first
python src/core/runner.py my_idea_id --no-github

# Later, manually create repo and push
cd runs/my_idea_id_*/
git init
gh repo create ChicagoHAI/my-experiment --public
git add .
git commit -m "Research results"
git push -u origin main
```

### Collaborative Research

```bash
# Researcher A runs experiment
python src/core/runner.py experiment_001
# Pushed to: github.com/ChicagoHAI/experiment-001

# Researcher B extends the work
git clone https://github.com/ChicagoHAI/experiment-001
cd experiment-001
# Make improvements
git commit -am "Extend analysis with new metrics"
git push
```

## FAQ

**Q: Can I use my personal GitHub account instead of an organization?**

A: Yes! Use `--github-org YourUsername`

**Q: Can I make repositories private?**

A: Currently requires code modification. Edit `src/core/runner.py` line ~133 to set `private=True`.

**Q: What if I don't want to use GitHub?**

A: Use `--no-github` flag. All research will be saved locally in `runs/`.

**Q: Can I push to an existing repository?**

A: Yes, if a repository with the same name exists, it will be reused.

**Q: How do I delete a repository?**

A: Via GitHub web interface or:
```bash
gh repo delete ChicagoHAI/repo-name
```

**Q: Can I change the repository name?**

A: Repository name is derived from idea_id. To change it, modify the idea_id.

## Support

For issues:
1. Check this guide
2. Review logs in `workspace/<repo-name>/logs/`
3. Open issue on main Idea Explorer repo
4. Check GitHub API status: https://www.githubstatus.com/

---

**Last Updated**: 2025-11-03
**Maintained by**: ChicagoHAI
