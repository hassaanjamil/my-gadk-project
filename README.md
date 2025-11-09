# My GADK Project

Agentic playground that demonstrates how to wire custom tools into the **Google Agent Development Kit (ADK)** and talk to multiple model providers through **LiteLLM**. The default agent (`src/agent.py`) can fetch world time data through HTTP tools, but you can swap in any LLM endpoint—OpenAI, Google (Gemini), DeepSeek, Groq, or a local Ollama server.

---

## 1. What’s in the stack?

| Dependency | Why it’s here |
| --- | --- |
| **Google ADK (`google-adk`)** | CLI + runtime that loads your `root_agent`, provides FastAPI / Web UIs, and manages sessions/evals. |
| **LiteLLM (`litellm`)** | Provider-agnostic client so you can point the agent at OpenAI, Gemini, DeepSeek, Groq, or Ollama with a single model string. |
| **python-dotenv** | Loads `.env` so the ADK process and your tools receive API keys/config without exporting them manually. |
| **Pydantic** | Validates tool inputs/outputs (`CityTime`, `Timezone`) before they’re returned to the model. |
| **CountryInfo · GeoPy · TimezoneFinder** | Utility libs for future geographic features; installed now to keep the environment ready. |
| **Requests** (transitive) | Used in `src/tools.py` to call https://worldtimeapi.org. |

Tooling:
* **Python 3.12+**
* **uv** (lockfile-aware package manager; replaces `pip + venv`)

---

## 2. Prerequisites

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (or use pipx).
2. Install Python 3.12 (specified via `.python-version`).
3. Optional (local inference): [Install Ollama](https://ollama.com/download) and run `ollama pull llama3.2`.

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
LLM_MODEL_NAME=ollama_chat/llama3.2   # used in src/config.py

# Optional: make LiteLLM talk to a local Ollama server instead of cloud APIs
OLLAMA_BASE_URL=http://localhost:11434
```

### Provider cheat sheet

- **OpenAI**: Create an API key at https://platform.openai.com/account/api-keys.
- **Google (Gemini via Google AI Studio)**: Generate a key at https://aistudio.google.com/app/apikey.
- **DeepSeek**: Keys live at https://platform.deepseek.com/api-keys.
- **Groq**: Use https://console.groq.com/keys.
- **Ollama (local)**: Install Ollama, pull a model (`ollama pull llama3.2`), and keep `ollama serve` running; no key required, just set `LITELLM_MODEL=ollama_chat/llama3.2`.

> Tip: check the `.env` into `.gitignore` (already set) so secrets never leave your machine.

---

## 5. Running the agent

### CLI chat (default)

```bash
uv run adk run src
# or, inside the venv:
adk run src
```

You’ll see `Running agent time_agent, type exit to exit.` and can start chatting. Type `exit` to quit. Use `--save_session` to persist transcripts.

### Web playground

```bash
uv run adk web src
```

This launches the ADK FastAPI server plus a lightweight React UI at `http://127.0.0.1:8000`.

### Direct LiteLLM smoke test

`main.py` demonstrates basic LiteLLM usage:

```bash
uv run python main.py
```

Make sure the referenced provider key is present in `.env` before running the script.

---

## 6. Project anatomy

```
src/
├─ __init__.py              # marks package so `adk` can import src.agent
├─ agent.py                 # defines root_agent that ADK loads
├─ config.py                # holds default LiteLLM model string
├─ instructions.py          # prompt snippets for capital/time agents
├─ tools.py                 # HTTP tools (timezone list + current time lookup)
└─ ...
```

The ADK loader expects `src/agent.py` to expose `root_agent`. Tools are normal Python callables that return JSON-serializable data or Pydantic models.

---

## 7. Troubleshooting

- **`ModuleNotFoundError: No module named 'tools'`** — ensure `src/__init__.py` exists and imports inside `agent.py` use `from .tools import ...`.
- **Model errors** — double-check `LITELLM_MODEL` matches the key you’ve supplied (e.g., `openai/gpt-4o-mini`, `google/gemini-2.0-flash`, `groq/llama-3.1-70b-versatile`, `deepseek/deepseek-chat`, or `ollama_chat/llama3.2`).
- **Ollama connection refused** — confirm `ollama serve` is running and `OLLAMA_BASE_URL` points to the same host/port.

Happy hacking! Plug in new tools under `src/tools.py`, tweak prompts in `src/instructions.py`, and let Google ADK handle the orchestration.***
