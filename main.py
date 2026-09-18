import asyncio
import os
from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from rich.console import Console

os.environ["PYDANTIC_AI_NO_BANNER"] = "1"
MODEL = "qwen3.5:9b"
BASE_URL = "http://localhost:11434/v1"
NOTES_FILE = "notes.txt"

console = Console()

model = OllamaModel(MODEL, provider=OllamaProvider(base_url=BASE_URL))


def get_current_time() -> str:
    """Get the current date and time."""
    return (
        datetime.now(tz=UTC)
        .astimezone(ZoneInfo("Asia/Kolkata"))
        .strftime("%A, %B %d, %Y at %I:%M %p")
    )


def calculate(expression: str) -> str:
    """Evaluate basic math expression."""
    if not set(expression) <= set("0123456789+-*/()."):
        return "Error: only numbers and operators allowed."

    try:
        return str(eval(expression))
    except Exception as error:
        return f"Error: {error}"


def save_note(note: str) -> str:
    """Save a short note."""
    with open(NOTES_FILE, "a", encoding="utf-8") as file:
        file.write(f"- {note}\n")
    return "Note saved."


def read_notes() -> str:
    """Read notes."""
    if not os.path.exists(NOTES_FILE):
        return "Please save a note first."
    with open(NOTES_FILE, encoding="utf-8") as file:
        return file.read()


agent = Agent(
    model,
    tools=[get_current_time, calculate, save_note, read_notes],
    instructions=(
        "You are a helpful ai agent running locally.",
        "Use your tools whenever they can help answer the question.",
        "Keep your answers short and friendly.",
    ),
)


async def main():
    """The main function for the ai agent."""
    console.print(
        "Local agent ready. Type 'quit' or 'exit' to exit.", style="bold green"
    )
    history = []

    while True:
        console.print("\nYour input: ", style="bold yellow", end="")
        user_input = input()

        if user_input.strip().lower() in ("exit", "quit"):
            break

        console.print("\nAgent response: ", end="", style="bold yellow")

        async with agent.run_stream(user_input, message_history=history) as result:
            async for text in result.stream_text(delta=True):
                console.print(text, end="", style="cyan", soft_wrap=True)
            history = result.all_messages()
        console.print("\n")


if __name__ == "__main__":
    asyncio.run(main())
