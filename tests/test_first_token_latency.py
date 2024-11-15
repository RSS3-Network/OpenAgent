import time

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


def measure_first_token_latency(model_name: str, num_samples: int = 3) -> float:

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant."),
        ("user", "Tell me a short story about a cat.")
    ])

    model = ChatOpenAI(
        model_name=model_name,
        streaming=True,
        temperature=0
    )

    chain = prompt | model | StrOutputParser()

    latencies = []
    for _ in range(num_samples):
        start_time = time.time()

        for chunk in chain.stream({}):
            first_token_time = time.time()
            latency = (first_token_time - start_time) * 1000
            latencies.append(latency)
            break

        time.sleep(1)

    avg_latency = sum(latencies) / len(latencies)
    return avg_latency


if __name__ == '__main__':
    model_name = "gpt-4o-mini"
    avg_latency = measure_first_token_latency(model_name)
    print(f"Average first token latency for {model_name}: {avg_latency:.2f} ms")