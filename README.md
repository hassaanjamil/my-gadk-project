# Agentic AI Project — Quickstart (with `uv`)

This guide sets up a **Python agentic AI** project using the ultra‑fast `uv` package manager, with a clean structure, modern tooling, and a minimal agent that uses **LiteLLM** for model access.

> Works on macOS/Linux/Windows. Replace `source .venv/bin/activate` with the Windows command shown below if needed.

---

## 1) Create the project

```bash
# Pick a folder name and create it
mkdir agentic-ai && cd agentic-ai

# Initialize a Python project (creates pyproject.toml)
uv init
```

> `uv init` creates a modern Python project with a `pyproject.toml`. You can run everything without manually creating a venv by using `uv run`, but below are common venv commands too.

---

## 2) (Optional) Create/activate a virtual environment

```bash
# Create a .venv in the project
uv venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

# Windows cmd.exe
# .venv\Scripts\activate
```

> You can skip manual activation by prefixing commands with `uv run` (e.g., `uv run python main.py`).

---

## 3) Add runtime dependencies

We’ll use **LiteLLM** (model router) and a few pragmatic libraries for CLI, I/O, and retries.

```bash
uv add litellm==1.79.1-stable python-dotenv typer[all] rich httpx tenacity pydantic
```

- **litellm** — multi‑provider LLM interface (OpenAI, Anthropic, etc.).  
- **python-dotenv** — load environment variables from `.env`.  
- **typer** — ergonomic CLI for your agent.  
- **rich** — pretty terminal output.  
- **httpx** — HTTP client for tool calls.  
- **tenacity** — robust retries.  
- **pydantic** — structured tool I/O.

> If you plan to add graph‑style workflows, consider `uv add langgraph langchain-core` later.

---

## 4) Add dev tools (optional but recommended)

```bash
uv add --dev ruff black pytest mypy
```

- **ruff** — linter/formatter helper  
- **black** — code formatter  
- **pytest** — tests  
- **mypy** — type checking

Convenience scripts (optional) in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100

[tool.black]
line-length = 100
```

---

## 5) Project structure

```text
agentic-ai/
├─ pyproject.toml
├─ .env.example
├─ README.md
└─ src/
   └─ agentic_ai/
      ├─ __init__.py
      ├─ agent.py
      └─ cli.py
```

Create folders:

```bash
mkdir -p src/agentic_ai
touch src/agentic_ai/__init__.py src/agentic_ai/agent.py src/agentic_ai/cli.py
cp .env.example .env 2>/dev/null || true
```

---

## 6) Environment variables

Create `.env.example` with (and copy to `.env`):

```env
# Provider/API credentials
OPENAI_API_KEY=your_openai_key_here

# Default model (LiteLLM model string, e.g., openai/gpt-4o-mini, openai/gpt-4o, etc.)
LITELLM_MODEL=openai/gpt-4o-mini
```

Load it at runtime via `python-dotenv`.

---

## 7) Minimal agent implementation

**`src/agentic_ai/agent.py`**
```python
from __future__ import annotations

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential
from litellm import completion

load_dotenv()

DEFAULT_MODEL = os.getenv("LITELLM_MODEL", "openai/gpt-4o-mini")

SYSTEM_PROMPT = (
    "You are a helpful, cautious agent. Use tools only when needed. "
    "Ask for missing details. Keep answers concise unless asked."
)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def call_llm(messages: List[Dict[str, str]], model: str = DEFAULT_MODEL) -> str:
    resp = completion(
        model=model,
        messages=messages,
        temperature=0.2,
        timeout=60,
    )
    # LiteLLM returns an OpenAI-style response
    return resp["choices"][0]["message"]["content"]

def run_agent(user_input: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]
    return call_llm(messages)
```

**`src/agentic_ai/cli.py`**
```python
from __future__ import annotations

import typer
from rich.console import Console
from .agent import run_agent

app = typer.Typer(help="Agentic AI CLI")

console = Console()

@app.command()
def ask(question: str):
    """Ask the agent a question."""
    console.rule("[bold]Agentic AI[/bold]")
    try:
        answer = run_agent(question)
        console.print(f"[bold green]Answer:[/bold green] {answer}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
```

**Optional**: add an entry point in `pyproject.toml` so you can run `agentic-ai` as a command:

```toml
[project]
name = "agentic-ai"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = []  # managed by `uv add`

[project.scripts]
agentic-ai = "agentic_ai.cli:app"
```

> `uv add` updates `[project.dependencies]` for you; keeping `dependencies = []` here is fine—`uv` will manage actual locks/installs.

---

## 8) Run it

```bash
# Using the venv
python -m agentic_ai.cli ask "Summarize the goal of this project."

# Or without activating venv
uv run python -m agentic_ai.cli ask "Summarize the goal of this project."
```

Expected:
```
Answer: This project scaffolds a minimal agent using LiteLLM...
```

---

## 9) Formatting, linting, tests

```bash
ruff check .
black .
pytest -q
mypy src
```

---

## 10) Next steps

- Add **tools** (e.g., web search, calculators) and route to them based on model output.  
- Persist **short‑term memory** to a lightweight store (SQLite/JSON) if needed.  
- Add **FastAPI** to expose your agent as an HTTP service: `uv add fastapi uvicorn`.

---

## Troubleshooting

- **OpenAI credentials**: ensure `OPENAI_API_KEY` is set in `.env` or your shell env.  
- **Model string**: set `LITELLM_MODEL` to a valid LiteLLM model id (e.g., `openai/gpt-4o-mini`).  
- **Windows execution policy**: If PowerShell blocks venv activation, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.

Happy building! 🎉
