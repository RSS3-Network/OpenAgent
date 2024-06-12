from langchain_core.messages import HumanMessage
from workflows.workflow import build_workflow

workflow = build_workflow()
workflow.get_graph().print_ascii()

for s in workflow.stream({"messages": [HumanMessage(content="what's bitcoin price now ?")]}):
    if "__end__" not in s:
        print(s)
        print("----")
