from dotenv import load_dotenv
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()

members = [
    {
        "name": "Market",
        "description": "a market analyst specialized in Web3. "
        "You provide market information about CEX, DEX, NFTs, inscriptions, and runes.",
    },
    {"name": "Feed", "description": "an expert in web3 social platforms' activities"},
    {
        "name": "Wallet",
        "description": "an expert in web3 wallets, known the asset of a wallet in different chains",
    },
    {
        "name": "Block Stat",
        "description": "an expert in blockchain statistics, known the block height, hash, gas fee etc.",
    },
]

system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers: {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
).format(members=", ".join([f"{member['name']} ({member['description']})" for member in members]))

options = ["FINISH"] + [member["name"] for member in members]
function_def = {
    "name": "route",
    "description": "Select the next role.",
    "parameters": {
        "title": "routeSchema",
        "type": "object",
        "properties": {
            "next": {
                "title": "Next",
                "anyOf": [
                    {"enum": options},
                ],
            }
        },
        "required": ["next"],
    },
}
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Given the conversation above, who should act next?" " Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=str(options), members=", ".join([member["name"] for member in members]))

llm = ChatOpenAI(model="gpt-4o")

supervisor_chain = (
    prompt | llm.bind_functions(functions=[function_def], function_call="route") | JsonOutputFunctionsParser()
)
