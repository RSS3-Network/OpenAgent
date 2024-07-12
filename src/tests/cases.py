import asyncio
import time

from openagent.agent.function_agent import get_agent

question_list = [
    "show some web3 articles?",
    "What is the price of ETH?",
    "What did vitalik.eth do recently?",
    "Send 0.01 eth to vitalik.eth",
    "Swap 1 eth to usdt",
    "What is MODE chain?",
    "Give me the bitcoin price chart",
    "List some popular NFTs?",
    "What's the largest dex with highest trading volume on Solana?",
    "When ETH ETF 19b-4 forms approved?",
    "Who are the main investors of EigenLayer?",
]


async def dummy(_) -> None:
    pass


async def init():
    # vertexai.init(project='openagent-422907')

    # langchain.debug=True
    start = time.time()
    agent = get_agent("11")
    for question in question_list:
        print(f"Question: {question}")

        await agent.ainvoke(
            {"input": question},
            config={
                "metadata": {"agentName": "openagent-backend", "userId": "123"},
            },
        )

        time.sleep(1)

        print("--------------")

    end = time.time()

    print(f"Time elapsed: {end - start}")


if __name__ == "__main__":
    asyncio.run(init())
