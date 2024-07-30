import json
import os

from chainlit.utils import mount_chainlit
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel
from sse_starlette import EventSourceResponse
from starlette import status
from starlette.responses import JSONResponse, FileResponse
from starlette.staticfiles import StaticFiles

from openagent.workflows.workflow import build_workflow

load_dotenv()
app = FastAPI(title="OpenAgent", description="")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return JSONResponse(content={"status": "ok"})


@app.get("/widget/swap")
async def swap_root():
    return FileResponse(os.path.join("dist", "index.html"))


@app.get("/widget/price-chart")
async def chart_price_root():
    return FileResponse(os.path.join("dist", "index.html"))


class Input(BaseModel):
    text: str


@app.post("/api/stream_chat", description="streaming chat api for openagent")
async def outline_creation(req: Input):
    agent = build_workflow()

    async def stream():
        async for event in agent.astream_events({"input": req.text}, version="v1"):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                yield json.dumps(event["data"]["chunk"].dict(), ensure_ascii=False)

    return EventSourceResponse(stream(), media_type="text/event-stream")


# Check and create static files directory
static_dir = os.path.join("dist", "static")
if not os.path.exists(static_dir):
    try:
        os.makedirs(static_dir)
        logger.info(f"Created directory: {static_dir}")
    except OSError as e:
        logger.error(f"Error creating directory {static_dir}: {e}")

app.mount("/static", StaticFiles(directory=static_dir), name="widget")


mount_chainlit(app=app, target="openagent/ui/app.py", path="")
