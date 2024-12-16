from typing import List, Dict
import asyncio
import aiohttp
from loguru import logger

from openagent.conf.env import settings

HEADERS = {"Content-Type": "application/json"}


async def api_request(endpoint: str, payload: Dict) -> Dict:
    """
    Make an asynchronous POST request to the API

    :param endpoint: API endpoint
    :param payload: Request payload
    :return: JSON response as a dictionary
    """
    url = f"{settings.OVM_API_BASE_URL}/{endpoint}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=HEADERS, json=payload) as response:
            return await response.json()


async def create_task(messages: List[Dict], contract_address: str = settings.CONTRACT_ADDRESS) -> Dict:
    """
    Create a new task asynchronously

    :param messages: List of message dictionaries
    :param contract_address: Contract address for the task
    :return: Response object
    """
    logger.info(f"Creating task with messages: {messages}")
    payload = {
        "messages": messages,
        "contract_address": contract_address
    }
    resp = await api_request("tasks", payload)
    logger.info(f"Task creation response: {resp}")
    return resp


async def submit_result(task_id: str, content: str, contract_address: str= settings.CONTRACT_ADDRESS) -> Dict:
    """
    Submit task result asynchronously

    :param task_id: Task ID
    :param content: Result content
    :param contract_address: Contract address for the task
    :return: Response object
    """
    logger.info(f"Submitting result for task {task_id}: {content}")
    payload = {
        "task_id": task_id,
        "content": content,
        "contract_address": contract_address
    }
    resp = await api_request("results", payload)
    logger.info(f"Result submission response: {resp}")
    return resp


async def main():
    # Example contract address

    # Create task
    messages0 = [{"role": "user", "content": "Hello!"}]
    task_response = await create_task(messages0)
    print("Task creation response:", task_response)

    # Submit result
    task_id = task_response["task_id"]
    content = "Salute!"
    result_response = await submit_result(task_id, content)
    print("Result submission response:", result_response)


# Usage example
if __name__ == "__main__":
    asyncio.run(main())
