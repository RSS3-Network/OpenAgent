import os
import sys

import pytest
from jinja2 import Environment, FileSystemLoader
from loguru import logger

# Global model configurations
PROPRIETARY_MODELS = [
    {"name": "gpt-4o-mini", "function_call_support": True},
    {"name": "gpt-4o", "function_call_support": True},
    {"name": "gemini-1.5-flash", "function_call_support": True},
    {"name": "gemini-1.5-pro", "function_call_support": True},
]

OPENSOURCE_MODELS = [
    {"name": "qwen2", "function_call_support": True},
    {"name": "mistral", "function_call_support": True},
    {"name": "qwen2.5", "function_call_support": True},
    {"name": "llama3.1", "function_call_support": True},
    {"name": "llama3.2", "function_call_support": True},
    {"name": "mistral-nemo", "function_call_support": True},
]

from gen_benchmark_html_report import measure_proprietary_models_metrics, measure_opensource_models_metrics


class TestStats:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.errors = 0

    def pytest_runtest_logreport(self, report):
        if report.when == 'call':
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1
            elif report.skipped:
                self.skipped += 1
        elif report.when == 'setup' and report.outcome == 'error':
            self.errors += 1

    def calculate_model_score(self):
        total_tests = self.passed + self.failed
        if total_tests == 0:
            return 0
        score = (self.passed / total_tests) * 100
        return round(score)

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Skipped: {self.skipped}")
        print(f"Errors: {self.errors}")


def run_model_tests(model_name):
    print(f"\nTesting model: {model_name}")
    stats = TestStats()
    test_files = ["supervisor_chain.py"] \
        # + glob.glob("agent_trajectory/*.py")
    pytest.main(["--count=1", "-n", "11"] + test_files + [f"--model={model_name}"] + sys.argv[1:], plugins=[stats])
    return stats.calculate_model_score()


def bool_to_emoji(value):
    return "✅" if value else "❌"


def generate_benchmark_report(proprietary_results, opensource_results):
    """Generate HTML benchmark report for model performance results.

    Args:
        proprietary_results (dict): Results for proprietary models containing tuples of (score, first_token_latency, token_rate)
        opensource_results (dict): Results for open source models containing tuples of (score, first_token_latency, token_rate)
    """
    # Convert results format and sort by score
    proprietary_models = []
    for model in PROPRIETARY_MODELS:
        if model['name'] in proprietary_results:
            score, latency, token_rate = proprietary_results[model['name']]
            proprietary_models.append({
                'name': model['name'],
                'score': score,
                'first_token_latency': f"{latency:.2f}ms",
                'token_rate': f"{token_rate:.1f} tokens/sec",
                'function_call_support': bool_to_emoji(model['function_call_support'])
            })
    proprietary_models.sort(key=lambda x: x['score'], reverse=True)

    open_source_models = []
    for model in OPENSOURCE_MODELS:
        if model['name'] in opensource_results:
            score, latency, token_rate = opensource_results[model['name']]
            open_source_models.append({
                'name': model['name'],
                'score': score,
                'first_token_latency': f"{latency:.2f}ms",
                'token_rate': f"{token_rate:.1f} tokens/sec",
                'function_call_support': bool_to_emoji(model['function_call_support'])
            })
    open_source_models.sort(key=lambda x: x['score'], reverse=True)

    # Set up template environment
    env = Environment(loader=FileSystemLoader('templates'))

    # Generate HTML benchmark report
    html_template = env.get_template('benchmark.html.j2')
    html_output = html_template.render(
        open_source_models=open_source_models,
        proprietary_models=proprietary_models
    )

    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)

    # Save HTML report
    with open('reports/benchmark.html', 'w') as f:
        f.write(html_output)


def main():
    proprietary_results = {}
    opensource_results = {}

    for model in PROPRIETARY_MODELS:
        score = run_model_tests(model['name'])
        latency, token_rate = measure_proprietary_models_metrics(model['name'])
        logger.info(f"First token latency for {model['name']}: {latency:.2f}ms")
        logger.info(f"Token output rate for {model['name']}: {token_rate:.1f} tokens/sec")
        proprietary_results[model['name']] = (score, latency, token_rate)

    for model in OPENSOURCE_MODELS:
        score = run_model_tests(model['name'])
        latency, token_rate = measure_opensource_models_metrics(model['name'])
        logger.info(f"First token latency for {model['name']}: {latency:.2f}ms")
        logger.info(f"Token output rate for {model['name']}: {token_rate:.1f} tokens/sec")
        opensource_results[model['name']] = (score, latency, token_rate)

    generate_benchmark_report(proprietary_results, opensource_results)
    print("Benchmark report generated successfully at reports/benchmark.html")


if __name__ == "__main__":
    main()
