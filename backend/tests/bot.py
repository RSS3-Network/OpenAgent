import asyncio

from openagent.bot.agent import create_agent


async def main():
    agent = await create_agent()

    agent.invoke(
        {
            "input": "any notable nft collaborations in DeFi?",
        },
        config={"configurable": {"session_id": "session_id"}},
    )


if __name__ == "__main__":
    asyncio.run(main())
