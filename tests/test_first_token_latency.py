import time

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


def measure_model_metrics(model_name: str, num_samples: int = 3) -> tuple[float, float]:
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
    token_rates = []

    for _ in range(num_samples):
        start_time = time.time()
        first_token_received = False
        token_count = 0

        for chunk in chain.stream({}):
            current_time = time.time()
            if not first_token_received:
                latency = (current_time - start_time) * 1000
                latencies.append(latency)
                first_token_received = True
                first_token_time = current_time

            token_count += 1

        total_time = time.time() - first_token_time
        if total_time > 0:
            tokens_per_second = token_count / total_time
            token_rates.append(tokens_per_second)

        time.sleep(1)

    avg_latency = sum(latencies) / len(latencies)
    avg_token_rate = sum(token_rates) / len(token_rates)
    return avg_latency, avg_token_rate


def measure_first_token_latency(model_name: str, num_samples: int = 3) -> float:
    latency, _ = measure_model_metrics(model_name, num_samples)
    return latency


if __name__ == '__main__':
    model_name = "gpt-4o-mini"
    avg_latency, avg_token_rate = measure_model_metrics(model_name)
    print(f"Average first token latency for {model_name}: {avg_latency:.2f} ms")
    print(f"Average token output rate for {model_name}: {avg_token_rate:.2f} tokens/sec")
