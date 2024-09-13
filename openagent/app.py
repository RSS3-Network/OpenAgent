import json
import os

import vertexai
from chainlit.utils import mount_chainlit
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from loguru import logger
from pydantic import BaseModel, Field
from sse_starlette import EventSourceResponse
from starlette import status
from starlette.responses import FileResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from openagent.conf.env import settings
from openagent.conf.llm_provider import get_available_providers
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


@app.get("/health", status_code=status.HTTP_200_OK, include_in_schema=False)
async def health_check():
    return JSONResponse(content={"status": "ok"})


@app.get("/widget/swap", include_in_schema=False)
async def swap_root():
    return FileResponse(os.path.join("dist", "index.html"))


@app.get("/widget/price-chart", include_in_schema=False)
async def chart_price_root():
    return FileResponse(os.path.join("dist", "index.html"))


@app.get("/widget/transfer", include_in_schema=False)
async def transfer_root():
    return FileResponse(os.path.join("dist", "index.html"))


class Input(BaseModel):
    text: str
    model: str = Field("gpt-3.5-turbo", title="Model name", description="The name of the model to use.")


@app.post("/api/stream_chat", description="streaming chat api for openagent")
async def outline_creation(req: Input):
    model = req.model
    llm = get_available_providers()[model]
    agent = build_workflow(llm)

    async def stream():
        async for event in agent.astream_events({"messages": [HumanMessage(content=req.text)]}, version="v1"):
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

if settings.VERTEX_PROJECT_ID:
    vertexai.init(project=settings.VERTEX_PROJECT_ID)
