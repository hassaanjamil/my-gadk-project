# My GADK Project

Agentic playground that demonstrates how to wire custom tools into the **Google Agent Development Kit (ADK)** and talk to multiple model providers through **LiteLLM**. This repo now hosts a **multi-module agent pack** (`src/agents/*`) so you can serve several specialized agents—e.g., `capital_agent` or `ny_weather_time_planner_agent`—from a single ADK web UI.

---

## 1. What’s in the stack?

| Dependency | Why it’s here |
| --- | --- |
| **Google ADK (`google-adk`)** | CLI + runtime that loads your `root_agent`, provides FastAPI / Web UIs, and manages sessions/evals. |
| **LiteLLM (`litellm`)** | Provider-agnostic client so you can point the agent at OpenAI, Gemini, DeepSeek, Groq, or Ollama with a single model string. |
| **python-dotenv** | Loads `.env` so the ADK process and your tools receive API keys/config without exporting them manually. |
| **Pydantic** | Validates tool inputs/outputs (`CityTime`, `Timezone`) before they’re returned to the model. |
| **CountryInfo · GeoPy · TimezoneFinder** | Utility libs for future geographic features; installed now to keep the environment ready. |
| **Requests** (transitive) | Used inside each agent’s `tools.py` (e.g., `src/agents/capital_agent/tools.py`) to call https://worldtimeapi.org and other APIs. |

Tooling:
* **Python 3.12+**
* **uv** (lockfile-aware package manager; replaces `pip + venv`)

---

## 2. Prerequisites

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (or use pipx).
2. Install Python 3.12 (specified via `.python-version`).
3. **Required for local-first runs**: [Install Ollama](https://ollama.com/download), then run:

```bash
ollama pull llama3.2
ollama run llama3.2  # keeps the model warm; Ctrl+C when done
```

> The multi-agent web runner expects `llama3.2` to be available via Ollama before you start ADK, otherwise LiteLLM will fail to stream responses.

---

## 3. Install dependencies

```bash
git clone <this-repo>
cd my-gadk-project
uv sync          # creates .venv and installs everything from pyproject.toml
# Optionally activate:
source .venv/bin/activate
```

All commands below assume either an activated venv or you prefix them with `uv run`.

### Optional: manual venv setup (without uv)

If you’d rather manage a traditional virtual environment yourself:

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# On Windows (PowerShell):
# .venv\Scripts\Activate.ps1
```

> Once the venv is active, run `uv sync` to mirror the environment.

---

## 4. Configure environment variables

Create `.env` in the project root (same level as `pyproject.toml`). Example template:

```env
# Pick one provider per run; LiteLLM will use the key that matches your model string.
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
DEEPSEEK_API_KEY=sk-...
GROQ_API_KEY=gsk_...

# LiteLLM routing
LITELLM_MODEL=openai/gpt-4o-mini
LLM_MODEL_NAME=ollama_chat/llama3.2   # mirrored inside each agent config (e.g., src/agents/capital_agent/config.py)

# Optional: make LiteLLM talk to a local Ollama server instead of cloud APIs
OLLAMA_BASE_URL=http://localhost:11434
```

### Provider cheat sheet

- **OpenAI**: Create an API key at https://platform.openai.com/account/api-keys.
- **Google (Gemini via Google AI Studio)**: Generate a key at https://aistudio.google.com/app/apikey.
- **DeepSeek**: Keys live at https://platform.deepseek.com/api-keys.
- **Groq**: Use https://console.groq.com/keys.
- **Ollama (local)**: Install Ollama, pull a model (`ollama pull llama3.2`), and keep either `ollama serve` or `ollama run llama3.2` running; no key required, just set `LITELLM_MODEL=ollama_chat/llama3.2`.

> Tip: check the `.env` into `.gitignore` (already set) so secrets never leave your machine.

---

## 5. Running the agents

### 1. Keep Ollama llama3.2 running

```bash
ollama run llama3.2
```

Leave this tab open; LiteLLM streams tokens from the local model while ADK brokers tool calls.

### 2. Serve the multi-agent web workspace

From the repo root:

```bash
source .venv/bin/activate

cd src/agents
uv run adk web --port 8000
# or, with an activated venv:
adk web --port 8000
```

Then visit `http://127.0.0.1:8000`, pick the agent you want to exercise from the dropdown (e.g., `capital_agent` vs `ny_weather_time_planner_agent`), and start chatting. Each agent keeps its own prompt, tools, and model config but shares the same ADK process.

### 3. Direct LiteLLM smoke test

`main.py` demonstrates basic LiteLLM usage:

```bash
uv run python main.py
```

Make sure the referenced provider key is present in `.env` before running the script.

---

## 6. Project anatomy

```
src/
├─ agents/
│  ├─ __init__.py                # registers available agent modules for ADK
│  ├─ capital_agent/
│  │  ├─ agent.py                # exposes root_agent for capital lookups
│  │  ├─ config.py               # LiteLLM model + provider routing
│  │  ├─ instructions.py         # system / developer prompts
│  │  ├─ pydantic.py             # IO schemas for custom tools
│  │  └─ tools.py                # e.g., capital + timezone utilities
│  └─ ny_weather_time_planner_agent/
│     ├─ agent.py
│     ├─ config.py
│     ├─ instructions.py
│     ├─ pydantic.py
│     └─ tools.py
└─ main.py                      # LiteLLM standalone smoke test
```

Every subfolder under `src/agents/` is a self-contained ADK agent module. Add new agents by copying a folder, adjusting its config + toolchain, and importing it inside `src/agents/__init__.py`.

---

## 7. Troubleshooting

- **`ModuleNotFoundError: No module named 'tools'`** — ensure `src/agents/__init__.py` exports each module package and that submodules import tools with relative paths (e.g., `from .tools import ...`).
- **Model errors** — double-check `LITELLM_MODEL` matches the key you’ve supplied (e.g., `openai/gpt-4o-mini`, `google/gemini-2.0-flash`, `groq/llama-3.1-70b-versatile`, `deepseek/deepseek-chat`, or `ollama_chat/llama3.2`).
- **Ollama connection refused** — confirm `ollama serve` is running and `OLLAMA_BASE_URL` points to the same host/port.

Happy hacking! Plug new skills under `src/agents/<agent>/tools.py`, tweak prompts in each `instructions.py`, and let Google ADK handle the orchestration.***
