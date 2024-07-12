import multiprocessing
import os

import uvicorn
from dotenv import load_dotenv
from loguru import logger

if __name__ == "__main__":
    load_dotenv()
    env = os.getenv("ENV", "dev")

    if env == "prod":
        logger.info("Starting UI")
        from openagent.ui.app import start_ui

        ui_process = multiprocessing.Process(target=start_ui)
        ui_process.start()
    else:
        ui_process = None

    logger.info("Starting API")
    uvicorn.run("openagent.app:app", host="0.0.0.0", reload=False, port=8001)

    if ui_process:
        ui_process.join()
