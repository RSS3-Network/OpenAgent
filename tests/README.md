# Running Tests and Generating Reports

## Execute Tests

Use the following command to run tests and generate a report:

```bash
pytest --count=3 -n 11 supervisor_chain.py --alluredir allure-results --model=gemini-1.5-pro
pytest --count=3 -n 11 agent_trajectory/*.py --alluredir allure-results --model=gpt-3.5-turbo
```


Command breakdown:
- `--count=3`: Repeats each test case 3 times
- `-n 11`: Uses 11 parallel processes
- `--alluredir allure-results`: Specifies the output directory for Allure report results
- `--model=gemini-1.5-pro`: Specifies the model to use for the test, e.g. gpt-3.5-turbo, gemini-1.5-pro, gemini-1.5-flash, llama3.1:latest etc.

## View Report

After running the tests, view the report with:

```bash
allure serve allure-results
```

## Note

Ensure the Allure command-line tool is installed before use. For installation, refer to the [official installation guide](https://allurereport.org/docs/install/).
