def pytest_addoption(parser):
    parser.addoption(
        "--model",
        action="store",
        default="gpt-3.5-turbo",
        help="Model to use for testing, e.g. gpt-3.5-turbo, gemini-1.5-pro, gemini-1.5-flash, " "llama3.1:latest",
    )
