from dotenv import load_dotenv

load_dotenv()

from graph import graph

if __name__ == "__main__":
    print(graph.get_graph().draw_mermaid())
    with open("graph.png", "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png())

    res = graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Write about AI-Powered SOC / autonomous soc problem domain, list startups that do that and raised capital.",
                }
            ]
        }
    )

    # The model is forced to call a tool, so the answer is in the tool-call args.
    final = res["messages"][-1].tool_calls[0]["args"]
    print(final["answer"])
    print("\nReferences:")
    for ref in final.get("references", []):
        print(f"- {ref}")
