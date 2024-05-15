import asyncio
import time

from openagent.agent.function_agent import get_agent

question_list = [
    # "Hello?",
    # "What is the price of ETH?",
    # "What's the ethereum network's gas price now?",
    # "What did vitalik.eth do recently?",
    # "Send 0.01 eth to vitalik.eth",
    # "Swap 1 eth to usdt",
    # "What is mode chain?",
    # "Give the bitcoin price chart",
    # "Show me some posts about vitalik on Mirror",
    # "most popular nft?"
    "recommend me some articles about web3",
]


async def dummy(_) -> None:
    pass


async def init():
    # langchain.debug=True
    start = time.time()
    agent = get_agent("")
    for question in question_list:
        print(f"Question: {question}")
        await agent.arun(question)
        time.sleep(1)

        print("--------------")

    end = time.time()

    print(f"Time elapsed: {end - start}")


if __name__ == "__main__":
    asyncio.run(init())
