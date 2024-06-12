import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph

from openagent.bot.multi_agent.agents.block_stat_agent import block_stat_agent
from openagent.bot.multi_agent.agents.feed_agent import feed_agent
from openagent.bot.multi_agent.agents.market_agent import market_agent
from openagent.bot.multi_agent.agents.wallet_agent import wallet_agent
from openagent.bot.multi_agent.workflows.supervisor_chain import supervisor_chain


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str


def create_node(agent, name):
    def run(state):
        result = agent.invoke(state)
        return {"messages": [HumanMessage(content=result["output"], name=name)]}

    return run


def build_workflow():
    market_node = create_node(market_agent, "Market")
    feed_node = create_node(feed_agent, "Feed")
    wallet_node = create_node(wallet_agent, "Wallet")
    block_stat_node = create_node(block_stat_agent, "Block Stat")

    workflow = StateGraph(AgentState)
    workflow.add_node("Market", market_node)
    workflow.add_node("Feed", feed_node)
    workflow.add_node("Wallet", wallet_node)
    workflow.add_node("Block Stat", block_stat_node)
    workflow.add_node("supervisor", supervisor_chain)

    members = ["Market", "Feed", "Wallet", "Block Stat"]
    for member in members:
        workflow.add_edge(member, "supervisor")

    conditional_map = {k: k for k in members}
    conditional_map["FINISH"] = END
    workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
    workflow.set_entry_point("supervisor")

    return workflow.compile()
