from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import ToolMessage
from langgraph.graph import END, START, MessagesState, StateGraph

from actor_agent import draft_node
from revisor_agent import revise_node
from tool_executor import execute_tools

MAX_ITERATIONS = 2


def event_loop(state: MessagesState) -> str:
    """Stop after MAX_ITERATIONS tool runs, otherwise search again."""
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state["messages"])
    if count_tool_visits >= MAX_ITERATIONS:
        return END
    return "execute_tools"


builder = StateGraph(MessagesState)
builder.add_node("draft", draft_node)
builder.add_node("execute_tools", execute_tools)
builder.add_node("revise", revise_node)
builder.add_edge(START, "draft")
builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")
builder.add_conditional_edges("revise", event_loop, ["execute_tools", END])
graph = builder.compile()
