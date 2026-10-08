from langgraph.graph import MessagesState

from chain import first_responder


def draft_node(state: MessagesState):
    """Actor: writes the first answer plus a self-critique and search queries."""
    response = first_responder.invoke({"messages": state["messages"]})
    return {"messages": [response]}
