def pytest_addoption(parser):
    parser.addoption(
        "--model",
        action="store",
        default="llama3.2",
        help="Model to use for testing, e.g. gemini-1.5-pro, gemini-1.5-flash, " "llama3.1:latest",
    )
