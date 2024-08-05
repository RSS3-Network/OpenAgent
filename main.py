import uvicorn
from dotenv import load_dotenv
from loguru import logger

if __name__ == "__main__":
    load_dotenv()
    logger.info("Starting OpenAgent")
    uvicorn.run("openagent.app:app", host="localhost", reload=False, port=8000)
