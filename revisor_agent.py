from langgraph.graph import MessagesState

from chain import revisor


def revise_node(state: MessagesState):
    """Revisor: improves the answer using the search results."""
    response = revisor.invoke({"messages": state["messages"]})
    return {"messages": [response]}
