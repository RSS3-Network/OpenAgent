from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

memory = ConversationBufferMemory(return_messages=True)
memory.chat_memory.add_ai_message("Hello, how can I help you today?")
memory.chat_memory.add_user_message("I would like to know the price of Bitcoin.")
memory.chat_memory.add_ai_message("The price of Bitcoin is $50,000.")

variables = memory.load_memory_variables(inputs={})
print(variables)


model = ChatOpenAI(streaming=True)
