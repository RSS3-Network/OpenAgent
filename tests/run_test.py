import glob
import sys

import pytest
from jinja2 import Environment, FileSystemLoader


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
    # Convert results format
    proprietary_models = [
        {'name': model_name, 'score': score}
        for model_name, score in proprietary_results.items()
    ]

    open_source_models = [
        {'name': model_name, 'score': score}
        for model_name, score in opensource_results.items()
    ]

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
                 # + glob.glob("agent_trajectory/*.py")
    pytest.main(["--count=1", "-n", "11"] + test_files + [f"--model={model_name}"] + sys.argv[1:], plugins=[stats])
    return stats.calculate_model_score()


def run_all_tests(proprietary_models, opensource_models):
    proprietary_results = {}
    opensource_results = {}

    # Test proprietary models
    for model in proprietary_models:
        proprietary_results[model] = run_model_tests(model)

    # Test open source models
    for model in opensource_models:
        opensource_results[model] = run_model_tests(model)

    # Generate report
    generate_model_report(proprietary_results, opensource_results)


if __name__ == "__main__":
    # Proprietary model list
    proprietary_models = [
        "gpt-4o-mini",
        "gpt-4o",
    ]

    # Open source model list
    opensource_models = [
        # "llama3.2",
    ]

    run_all_tests(proprietary_models, opensource_models)
