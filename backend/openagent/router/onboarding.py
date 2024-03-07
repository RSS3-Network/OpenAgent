import json
import uuid
import re

from fastapi import APIRouter
from loguru import logger
from sse_starlette import EventSourceResponse

from openagent.dto.chat_req import ChatReq
from openagent.dto.chat_resp import ChatResp

onboarding_router = APIRouter(tags=["Onboarding"])

introduction_text = """\
Hey there, digital explorer! 🚀 I'm OpenAgent, your trusty sidekick in the vast and vibrant universe of web3! 🌐✨

What can I do, you ask? Well, buckle up because I'm here to navigate you through the cosmic maze of blockchain networks, tokens, NFTs, and decentralized applications (dApps). Whether you're looking to trade some tokens, transfer some crypto to your buddy, or just curious about the latest NFT craze, I've got your back!

Here's a quick rundown of my superpowers:

- **Token Transfer**: Need to send some USDC to a friend? I'll guide your transaction to its destination faster than a shooting star! 🌠💸
- **Blockchain Intel**: Curious about the gas prices on Ethereum or the block height on Binance Smart Chain? I'll fetch that info like a space hound chasing a comet! 🐕🌠
- **NFT Insights**: Wondering what's hot in the NFT universe? I'll bring you market caps, floor prices, and the most popular NFTs out there! 🖼️📈
- **DApp Discovery**: Looking for the next DeFi gem or a social dApp to connect with fellow spacefarers? I'll be your guide to the decentralized cosmos! 🌌🔍
- **Crypto Queries**: Got questions about token prices or market caps? I'm like a crypto-encyclopedia with the latest data! 📚💹

So, if you're ready to embark on a web3 adventure, just hit me up and let's make some interstellar magic happen! And remember, I'm here to keep things fun and lively, so don't be surprised if I drop a pun or two along the way! 🎉👾
"""  # noqa: E501

suggested_questions = [
    "What's the current gas price on Ethereum?",
    "Can you show me the latest transactions for vitalik.eth?",
    "What's the floor price of the Bored Ape Yacht Club NFT collection?",
    "How much is 1 ETH in USDT right now?",
    "Tell me about the defi project with the highest TVL.",
    "Who are the popular users on Uniswap?",
    "Can you help me transfer 0.1 $ETH to vitalik.eth?",
]


def generate_stream():
    unique_message_id = str(uuid.uuid4())

    tokens = re.findall(r"\S+\s*", introduction_text)

    for token in tokens:
        yield f'{{"message_id":"{unique_message_id}","block_id":null,"type":"natural_language","body":{json.dumps(token)}}}'  # noqa: E501

    questions_json = json.dumps(suggested_questions)
    yield f'{{"message_id":"{unique_message_id}","block_id":null,"type":"suggested_questions","body":{questions_json}}}'  # noqa: E501


@onboarding_router.post("/onboarding/", response_model=ChatResp)
async def onboarding(req: ChatReq):
    logger.info(f"Received request: req={req}")
    return EventSourceResponse(generate_stream())
