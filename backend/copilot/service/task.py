import asyncio
import json
import threading
import time
from datetime import datetime
from typing import Dict

import aiohttp
from loguru import logger
from sqlalchemy.sql.operators import and_
from starlette.websockets import WebSocket

from copilot.db.database import DBSession
from copilot.db.models import Task
from copilot.dto.task import (
    TaskStatus,
    TaskDTO,
    build_task_dto,
    ConfirmTransferDTO,
)
from copilot.tool import get_token_by_address


async def cancel_task(user_id: str, task_id: str):
    with DBSession() as db_session:
        task = (
            db_session.query(Task)
            .filter(
                and_(
                    Task.user_id == user_id,
                    Task.task_id == task_id,
                )
            )
            .first()
        )
        if task is None:
            raise ValueError("task not found")
        if TaskStatus(task.status) in [
            TaskStatus.canceled,
            TaskStatus.done,
            TaskStatus.failed,
            TaskStatus.running,
        ]:
            raise ValueError("task cannot be cancelled")
        task.status = TaskStatus.canceled
        db_session.commit()


async def transfer(req: ConfirmTransferDTO):
    task_id = req.task_id
    task = await fetch_task(task_id)

    if TaskStatus(task.status) is not TaskStatus.idle:
        raise ValueError("task status is not idle")
    tx_id = task.task_id

    resp = await do_transfer(req, tx_id)
    if resp.__contains__("hash"):
        logger.info(f"transfer success: {resp}")
        hash0 = resp["hash"]
        await save_task(req, task, hash0)
        return resp
    else:
        logger.error(f"transfer failed: {resp}")
        raise ValueError(resp["error"])


async def fetch_task(task_id):
    with DBSession() as db_session:
        task = db_session.query(Task).filter(Task.task_id == task_id).first()
        if task is None:
            raise ValueError("task not found")
        return task


async def save_task(req, task, hash0):
    with DBSession() as db_session:
        body = task.body
        body_json = json.loads(body)

        body_json["user_id"] = req.user_id
        body_json["wallet_id"] = req.wallet_id
        body_json["to_address"] = req.to_address
        body_json["amount"] = req.amount
        body_json["token_address"] = req.token_address
        task.body = json.dumps(body_json)

        db_session.query(Task).filter(Task.task_id == task.task_id).update(
            {
                "body": task.body,
                "status": TaskStatus.running,
                "run_at": datetime.utcnow(),
                "hash": hash0,
            }
        )

        db_session.commit()


async def do_transfer(req, tx_id):
    user_id = req.user_id
    wallet_id = req.wallet_id
    to_address = req.to_address
    amount = req.amount
    token_address = req.token_address
    token = await get_token_by_address(token_address)
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://wallet-api.dev.copilot.xyz/wallets/withdraw",
            headers={"Content-Type": "application/json"},
            json={
                "txId": tx_id,
                "userId": user_id,
                "walletId": wallet_id,
                "toAddress": to_address,
                "amount": amount,
                "tokenAddress": token_address,
                "tokenDecimal": token["decimals"],  # noqa
            },
        ) as resp:
            return await resp.json()


def query_list(user_id, session_id, status, offset, limit) -> list[TaskDTO]:
    cond = [Task.user_id == user_id]
    if session_id is not None:
        cond.append(Task.session_id == session_id)
    if status is not None:
        cond.append(Task.status == status)

    with DBSession() as db_session:
        all0 = (
            db_session.query(Task)
            .filter(*cond)
            .order_by(Task.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return list(map(build_task_dto, all0))


async def get_notifications(user_id: str, websocket: WebSocket):
    await websocket.accept()
    with DBSession() as db_session:
        while True:
            tasks = (
                db_session.query(Task)
                .filter(
                    Task.user_id == user_id,
                    Task.is_notified == False,  # noqa
                )
                .all()
            )
            for task in tasks:
                await websocket.send_json(build_task_dto(task))

            time.sleep(1)


def check_task_status():
    threading.Thread(target=async_do_check_task_status).start()


def async_do_check_task_status():
    asyncio.run(do_check_task_status())


user2ws: Dict[str, WebSocket] = {}


async def do_check_task_status():
    with DBSession() as db_session:
        while True:
            try:
                tasks = (
                    db_session.query(Task)
                    .filter(Task.status == TaskStatus.running)
                    .all()
                )
                # logger.debug(f"check task status, {len(tasks)} tasks")
                for task in tasks:
                    tx_id = task.task_id
                    status = await get_task_status(tx_id)
                    if status == TaskStatus.done or status == TaskStatus.failed:
                        task.status = TaskStatus.done
                        task.done_at = datetime.utcnow()
                        if user2ws.__contains__(task.user_id):
                            ws = user2ws[task.user_id]
                            await ws.send_json(build_task_dto(task).model_dump_json())
                        db_session.commit()
                time.sleep(1)
            except Exception as e:
                logger.error(f"check task status error: {e}")


async def get_task_status(tx_id: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://wallet-api.dev.copilot.xyz/wallets/tx/status",
            json={"txId": tx_id},
        ) as resp:
            resp_json = await resp.json()
            if resp_json.__contains__("status"):
                status = resp_json["status"]
                if status == "success":
                    return TaskStatus.done
            return TaskStatus.running


async def fetch_one_task(user_id: str, task_id):
    with DBSession() as db_session:
        task = (
            db_session.query(Task)
            .filter(
                and_(
                    Task.user_id == user_id,
                    Task.task_id == task_id,
                )
            )
            .first()
        )
        if task is None:
            raise ValueError("task not found")
        return build_task_dto(task)
