import asyncio
import time

from copilot.agent.function_agent import get_agent

question_list = [
    # "show some active users",  # account query
    # "plz list some hot tokens",  # token query
    # "can you list some hot NFT?",  # NFT query
    # "what is hottest NFT collection?",  # NFT collection query
    # "how many cryptopunks NFT holders are there?",
    # "Tell me the total amount of cryptopunks NFT",
    # "What's the average price of cryptopunks NFT?",
    # "What's the highest offer of cryptopunks NFT?",
    # "what’s the highest price of the cryptopunks NFT?",
    # "what is the trading volume of cryptopunks NFT?",
    # "popular platforms?", # crosschain query
    # "list some hot dapps", # dapp query
    # "list some hot protocols", # dapp query
    # "give me some social projects", # social dapp query
    # "what did vitalik.eth do recently?", # feed query
    # "block height?", # network query -> block height
    # "the gas price", # network query -> gas price
    # "matic price",  # network query -> native token price
    # "what is zkevm polygon?", # general knowledge
    # "what is zkevm?", # general knowledge
    # "what is polygon?", # general knowledge
    # "how can i get some matic?", # general knowledge
    #################################################
    # #for arb copilot
    # "How is the L1 portion of an Arbitrum transaction’s gas fee computed?",
    # "Why does it look like two identical transactions consume a different amount of gas?",
    # "gas price now?",
    # "what is the gas price in arb now?",
    # "what did vitalik.eth do recently?",  # feed query"
    # "what's the price of ARB?",  # native token price
    # "what's the volume of $arb",  # token volume
    # "what are the top tvl projects currently?",  # dapp query
    # "Do I need to pay a tip / Priority fee for my Arbitrum transactions?",  # intent error -> gas price query
    # "How to run a local dev node",  # response need to be improved
    # "Can I run an Arbitrum node in p2p mode?",  # response error
    # "Which method in the Inbox contract should I use to submit a retryable ticket?",  # intent error -> dapp query
    # "What's the difference between Arbitrum Rollup and Arbitrum AnyTrust?",  # lower gas is anytrust core upside
    # "Why was 'one week' chosen for Arbitrum One's dispute window?",  # intent error -> NFT query
    # "Why do I get 'custom tx type' errors when I use hardhat?",  # intent error -> dapp query
    # "What's the state of Arbitrum One's decentralization",  # intent error -> dapp query
    # "Do I need to download any special npm libraries in order to use web3.js or ethers-js on Arbitrum",  # intent error -> dapp query
    # "hey",  # memory error
    # "what can u do?",
    # "what can u do",
    # "what is rss3?",  # emb retrieve error
    # "who are u?",  # emb retrieve error
    # "who build u?",
    # "what is Thetan Arena?",  # intent error -> dapp query
    # "What are some popular social dapps on arb?",
    # "swap 5 eth to arb",
    ###################################################################################
    # #for lens copilot
    # "What is lens?",
    # "Are there developer resources for Windows?",
    # "What did stani do recently?",
    # "what did bradorbradley do recently?",
    # "how many followers do I have?",  # lens follow tool
    # "how many followers do nicolo.lens and bradorbradley.lens have in common?",
    # "how many followers does bradorbradley.lens have?",
    # "show me total revenue of grams.lens",
    # "how many followers do I have?",
    # "what’s my most popular post?",
    # "what’s my most recent post?",
    # "write a post on RSS3 for me",
    # "What is lens?",
    # "what is momoka?",
    # "Show me total revenue of Stani",
    # "who has the most followers in lens?",
    # "What did @iamtherealyakuza do recently?",
    # "show me stani’s total revenue",
    # "is TrustMeBro trending on lens?",
    # "what are the best new apps being built on the lens protocol?",
    # "Which app on lens is the best place to post music?",
    # "which brand new apps that have already been developed are there? what should i try next?",
    # "Why do I need to pay gas when Lenster replies? But some people don't need to pay gas",
    # "Will there be an airdrop for lens?",
    # "How much does it cost to buy a lens now?",
    # "What is the best number of times to post a day to help with my engagement?",
    # "please give me the lens wetsite, i want to click it directly",
    # "I'm looking for Starknet publications on lens. Can you pls show me relevant Starknet content?",
    # "how does someone get access to lens?",
    # "new users each day",
    # "so this copilot much like a spinoff of chatgpt",
    # "momoka update the lens protocol team revealed what it do actually",
    # "when is the v2 of lens coming",
    # "when stani started the development of lens?",
    # "who's popular right now?",
    # "who on the lens feed is popular? ",
    # "what are the most popular post today on lens? ",
    # "who is following @lensvoice.lens? ",
    # "can you show me my post with the most collects?",
    # "does photographers.lens follow levychain.lens? ",
    ###################################################################################
    # #for eth copilot
    # "What is Ethereum?",  # general knowledge
    # "What is the price of ETH?",  # native token price
    # "plz list some hot tokens",  # token query
    # "can you list some hot NFT?",  # NFT query
    # "what did vitalik.eth do recently?",  # feed query ##
    # "block height?",  # network query -> block height
    # "the gas price",  # network query -> gas price
    # "list the most active users on ethereum",  # account query
    # "What's the difference between Arbitrum and Ethereum?",  # general knowledge
    # "how can i get some ETH?",  # general knowledge
    # "hello",  # normal dialogue
    # "what are the top dapps in ethereum?",  # dapp query
    # "list some defi projects having the highest tvl",  # defi query
    # "who are you?",  # normal dialogue
    # "who build you?",  # normal dialogue
    # "what is friend.tech?",  # general knowledge
    # "eth price?",
    # "swap 5 eth to arb",  # swap mutation
    # "Buy me 0.5 ETH.",  # swap mutation
    # "check the current price of RSS3",
    # "send 0.01 ct to birdring.eth",  # transfer mutation
    # "can you edit the transaction amount to 0.0001 ct?",  # transfer mutation
    # "YES",
    # "can you help me transfer 100$rss3 to songkeys.eth?",  # transfer mutation
    # "search the token on ethereum called The Genesis RSS3 Avatar NFT",
    # "Check if ethereum block height is a even numebr; if it is, tell me a joke. Before you check, say hello to me. After you done everything, tell me what's the price of ETH.",
    # "Check if ethereum block height is a even numebr; if it is, tell me a joke. Before you check, say hello to me. After you done everything, say hello again to me.",
    "how many copilot token do i have"
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
