import asyncio
import time

from openagent.agent.function_agent import get_agent

question_list = [
    # "Hello?",
    # "What is the price of ETH?",
    # "What's the ethereum network's gas price now?",
    # "What did vitalik.eth do recently?",
    # "send 0.01 eth to vitalik.eth",
    # "swap 1 eth to usdt",
    "show me some posts about vitalik on Mirror",
]


async def dummy(_):
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
