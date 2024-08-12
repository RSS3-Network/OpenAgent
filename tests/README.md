# Running Tests and Generating Reports

## Execute Tests

Use the following command to run tests and generate a report (example for `supervisor_chain.py`):

```bash
pytest --count=3 -n 11 supervisor_chain.py --alluredir allure-results
```

Command breakdown:
- `--count=3`: Repeats each test case 3 times
- `-n 11`: Uses 11 parallel processes
- `--alluredir allure-results`: Specifies the output directory for Allure report results

## View Report

After running the tests, view the report with:

```bash
allure serve allure-results
```

## Note

Ensure the Allure command-line tool is installed before use. For installation, refer to the [official installation guide](https://allurereport.org/docs/install/).