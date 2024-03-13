import asyncio
import time

from openagent.agent.function_agent import get_agent

question_list = [
    "Hello?",
    "What is the price of ETH?",
    "what did vitalik.eth do recently?",
]


async def dummy(_):
    pass


async def init():
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
