import random

questions = [
    "What's the current BTC price?",
    "What's the ETH block height?",
    "Any latest DeFi news?",
    "What's the current gas fees?",
    "Top NFT projects right now?",
    "Any recent blockchain updates?",
    "Current trends in the crypto market?",
    "Best platforms for staking?",
    "Upcoming ICOs?",
    "Top crypto exchanges?",
    "Any news on smart contracts?",
    "Current crypto regulations?",
    "Best crypto wallets?",
    "Latest DAO projects?",
    "Current yield farming rates?",
    "Top metaverse projects?",
    "Latest crypto airdrops?",
    "Top crypto influencers?",
    "Current DEX volumes?",
    "Latest news on crypto security?",
]


def get_random_questions():
    """
    Randomly select five questions from the list
    """
    return random.sample(questions, 5)
