import pytest
import sys
import glob

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

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Skipped: {self.skipped}")
        print(f"Errors: {self.errors}")

if __name__ == "__main__":
    stats = TestStats()
    test_files = ["supervisor_chain.py"] + glob.glob("agent_trajectory/*.py")
    pytest.main(["--count=3", "-n", "11"] + test_files + ["--model=gpt-4o-mini"] + sys.argv[1:], plugins=[stats])
