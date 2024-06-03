import random

questions = [
    "What's the current BTC price?",
    "Any latest DeFi news?",
    "What's the ETH block height?",
    "Gas fees of ethereum now?",
    "Top NFT projects right now?",
    "Current trends in the crypto market?",
    "Top crypto exchanges?",
    "Show some btc price dashboard?",
]


def get_random_questions():
    """
    Randomly select five questions from the list
    """
    return random.sample(questions, 4)
