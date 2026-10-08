from dotenv import load_dotenv

load_dotenv()
import datetime

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from schema import AnswerQuestion, ReviseAnswer
from llm import LLM

# Each role can use a different model/provider.
actor_llm = LLM("google_genai:gemini-3.8-flash")
revisor_llm = LLM("google_genai:gemini-3.8-flash")

actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. Recommend search queries to research information and improve your answer.""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer the user's question above using the required format."),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)


first_responder = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer."
) | actor_llm.bind_tool(AnswerQuestion)


revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""


revisor = actor_prompt_template.partial(
    first_instruction=revise_instructions
) | revisor_llm.bind_tool(ReviseAnswer)
