from langchain_core.messages import HumanMessage
from workflows.workflow import build_workflow

if __name__ == "__main__":
    workflow = build_workflow()
    workflow.get_graph().print_ascii()

    for s in workflow.stream({"messages": [HumanMessage(content="top market cap coins?")]}):
        if "__end__" not in s:
            print(s)
            print("----")
