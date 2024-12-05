import glob
import sys

import pytest
from jinja2 import Environment, FileSystemLoader

# Global model configurations
PROPRIETARY_MODELS = [
    {"name": "gpt-4o-mini", "function_call_support": True},
    {"name": "gpt-4o", "function_call_support": True},
    {"name": "gemini-1.5-flash", "function_call_support": True},
    {"name": "gemini-1.5-pro", "function_call_support": True},
    {"name": "claude-3-5-sonnet", "function_call_support": True},
]

OPENSOURCE_MODELS = [
    {"name": "qwen2", "function_call_support": True, "parameters": "7B"},
    {"name": "mistral", "function_call_support": True, "parameters": "7B"},
    {"name": "qwen2.5", "function_call_support": True, "parameters": "7B"},
    {"name": "llama3.1", "function_call_support": True, "parameters": "8B"},
    {"name": "llama3.2", "function_call_support": True, "parameters": "3B"},
    {"name": "mistral-nemo", "function_call_support": True, "parameters": "12B"},
    {"name": "olmo", "function_call_support": False, "parameters": "7B"},
    {"name": "gemma", "function_call_support": False, "parameters": "7B"},
    {"name": "llava", "function_call_support": False, "parameters": "13B"},
    {"name": "deepseek-coder-v2", "function_call_support": False, "parameters": "16B"}
]


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


def generate_model_report(proprietary_results, opensource_results):
    def bool_to_emoji(value):
        return "✅" if value else "❌"

    # Convert results format and sort by score
    proprietary_models = []
    for model in PROPRIETARY_MODELS:
        if model['name'] in proprietary_results:
            proprietary_models.append({
                'name': model['name'],
                'score': proprietary_results[model['name']],
                'function_call_support': bool_to_emoji(model['function_call_support'])
            })
    
    open_source_models = []
    for model in OPENSOURCE_MODELS:
        if model['name'] in opensource_results:
            open_source_models.append({
                'name': model['name'],
                'score': opensource_results[model['name']],
                'function_call_support': bool_to_emoji(model['function_call_support']),
                'parameters': model['parameters']
            })
    
    # Sort models, putting '-' scores at the end
    proprietary_models.sort(
        key=lambda x: float('-inf') if x['score'] == '-' else x['score'], 
        reverse=True
    )
    open_source_models.sort(
        key=lambda x: float('-inf') if x['score'] == '-' else x['score'], 
        reverse=True
    )

    # Set up template environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('compatible-models.mdx.j2')

    # Render template
    output = template.render(
        open_source_models=open_source_models,
        proprietary_models=proprietary_models
    )

    # Save to file
    with open('compatible-models.mdx', 'w') as f:
        f.write(output)


def run_model_tests(model_name):
    print(f"\nTesting model: {model_name}")
    stats = TestStats()
    test_files = ["supervisor_chain.py"] \
                 + glob.glob("agent_trajectory/*.py")
    pytest.main(["--count=3", "-n", "11"] + test_files + [f"--model={model_name}"] + sys.argv[1:], plugins=[stats])
    return stats.calculate_model_score()


def run_all_tests():
    proprietary_results = {}
    opensource_results = {}

    # Test proprietary models
    for model in PROPRIETARY_MODELS:
        if model['function_call_support']:
            proprietary_results[model['name']] = run_model_tests(model['name'])
        else:
            proprietary_results[model['name']] = '-'

    # Test open source models
    for model in OPENSOURCE_MODELS:
        if model['function_call_support']:
            opensource_results[model['name']] = run_model_tests(model['name'])
        else:
            opensource_results[model['name']] = '-'

    # Generate report
    generate_model_report(proprietary_results, opensource_results)


if __name__ == "__main__":
    run_all_tests()
