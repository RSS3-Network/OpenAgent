import sys
import unittest

from openagent.conf.llm_provider import set_current_llm


def run_tests(model_name, specific_test=None):
    # Set the model name globally
    set_current_llm(model_name)

    # Discover and run all tests
    test_loader = unittest.TestLoader()

    if specific_test:
        specific_test = specific_test.replace("tests.", "", 1)
        test_suite = test_loader.loadTestsFromName(specific_test)
    else:
        test_suite = test_loader.discover("agent_trajectory", pattern="*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py <model_name> OR python run_tests.py <model_name> [specific_test] ")
        sys.exit(1)

    model_name = sys.argv[1]
    specific_test = sys.argv[2] if len(sys.argv) > 2 else None

    result = run_tests(model_name, specific_test)

    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
