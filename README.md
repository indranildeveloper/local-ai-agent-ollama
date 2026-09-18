# Local Agent

A lightweight, fully local AI assistant built with [Pydantic AI](https://ai.pydantic.dev/) and Ollama. It runs a conversation loop in your terminal, streaming responses directly from a local LLM — no cloud, no API keys.

## Features

- **100% local** — uses an Ollama model running on your machine (`localhost:11434`).
- **Streaming responses** — replies appear token-by-token in real time.
- **Built-in tools** the agent can call automatically:
  - `get_current_time` — current date and time in Asia/Kolkata.
  - `calculate` — safe evaluation of basic math expressions.
  - `save_note` / `read_notes` — append to and read `notes.txt`.
- **Conversation memory** — the agent keeps the full message history within a session.
- **Pretty terminal output** — Rich formatting for prompts and responses.

## Requirements

- Python 3.11+
- [Ollama](https://ollama.com/) installed and running locally
- The `qwen3.5:9b` model pulled: `ollama pull qwen3.5:9b`

## Installation

```bash
git clone <your-repo-url>
cd local-agent

uv sync
```

> Make sure `options` are exported in your environment: the OpenAI-compatible API is served at `http://localhost:11434/v1`.

## Usage

```bash
uv run main.py
```

Start typing prompts. Type `exit` or `quit` to leave.

```bash
Local agent ready. Type 'quit' or 'exit' to exit.

Your input: what time is it?

Agent response: It's Friday, September 18, 2026 at 01:23 PM.
```

## Configuration

The key constants live at the top of `main.py`:

| Constant     | Description                           | Default                     |
| ------------ | ------------------------------------- | --------------------------- |
| `MODEL`      | Ollama model name                     | `qwen3.5:9b`                |
| `BASE_URL`   | Ollama OpenAI-compatible API endpoint | `http://localhost:11434/v1` |
| `NOTES_FILE` | Where saved notes are appended        | `notes.txt`                 |

## How It Works

1. An `Agent` is created with the Ollama model and four tools.
2. `main()` starts a REPL loop: read input, stream the agent's response, and store the resulting messages as history for the next turn.
3. The agent decides when to call tools to answer your questions accurately.

### Adding a tool

Define a plain function and add it to the `tools=[...]` list in `main.py`. The docstring is used by the model to understand when to call it.

```python
def say_hello(name: str) -> str:
    """Return a friendly greeting."""
    return f"Hello, {name}!"

agent = Agent(model, tools=[say_hello, ...])
```

## Notes

- Saved notes are plain markdown bullets appended to `notes.txt` in the project directory.
- `calculate` whitelists characters (`0-9`, `+-*/().`) before using `eval`, so only basic math is allowed.
