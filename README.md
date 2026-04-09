# Code Agent CLI

A Claude Code-like CLI tool built for learning purposes — to understand how AI agents work internally.

This project is heavily inspired by [gemini-cli](https://github.com/google-gemini/gemini-cli) and was vibe-coded.

## Setup

1. Install dependencies using [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

2. Configure authentication (choose one):

**Option A: API Key**

```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Option B: Service Account (Vertex AI)**

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

3. Run the CLI:

```bash
uv run code-agent
```
