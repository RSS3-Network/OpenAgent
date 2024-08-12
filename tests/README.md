# Running Tests and Generating Allure Reports

Use the following command to run tests and generate an Allure report:

```bash
pytest --count=3 -n 11 supervisor_chain.py --alluredir allure-results
```

## Command Breakdown

- `pytest`: Runs the pytest testing framework
- `--count=3`: Repeats each test case 3 times
- `-n 11`: Uses 11 parallel processes to run the tests
- `supervisor_chain.py`: Specifies the Python file to be tested
- `--alluredir allure-results`: Specifies the output directory for Allure report results

## Prerequisites

Ensure that the Allure command-line tool is installed. If not yet installed, please refer to the official installation guide:

[Allure Installation Guide](https://allurereport.org/docs/install/)

Choose the appropriate installation method based on your operating system and preferences.

## Running Tests

1. Open a terminal or command prompt
2. Navigate to the directory containing `supervisor_chain.py`
3. Run the command mentioned above

## Viewing the Allure Report

After running the tests, Allure results will be saved in the `allure-results` directory. To view the report, use the following command:

```bash
allure serve allure-results
```

This will open the Allure report in your default web browser.

