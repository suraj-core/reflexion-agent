from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

DEFAULT_MODEL = "google_genai:gemini-3.8-flash"


class LLM:
    """Provider-agnostic chat model wrapper.

    `model` is "<provider>:<model name>", e.g. "google_genai:gemini-3.8-flash",
    "openai:gpt-4o" or "anthropic:claude-sonnet-5-5". Non-Google providers need
    their own langchain package installed and API key set.
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        temperature: float = 0.0,
        max_retries: int = 6,
    ):
        self.model = model
        self.temperature = temperature
        # Retries with backoff cover transient errors such as 503 "high demand".
        self._client = init_chat_model(
            model, temperature=temperature, max_retries=max_retries
        )

    @property
    def client(self):
        return self._client

    def bind_tool(self, tool):
        """Return the model forced to call `tool` (a Pydantic schema)."""
        return self._client.bind_tools(tools=[tool], tool_choice=tool.__name__)
