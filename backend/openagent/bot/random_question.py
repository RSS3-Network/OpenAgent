import random

questions = [
    "What's the current BTC price?",
    "Any latest DeFi news?",
    "What's the ETH block height?",
    "Gas fees of ethereum now?",
    "Top NFT projects right now?",
    "Any recent blockchain updates?",
    "Current trends in the crypto market?",
    "Best platforms for staking?",
    "Top crypto exchanges?",
    "Any news on smart contracts?",
    "Current crypto regulations?",
    "Best crypto wallets?",
    "Current yield farming rates?",
    "Give the bitcoin price chart",
    "Latest crypto airdrops?",
    "Top crypto influencers?",
]


def get_random_questions():
    """
    Randomly select five questions from the list
    """
    return random.sample(questions, 5)
