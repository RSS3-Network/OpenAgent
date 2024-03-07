from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from copilot.router.onboarding import onboarding_router
from copilot.router.chat import chat_router
from copilot.router.session import session_router
from copilot.router.task import task_router
from copilot.service.task import check_task_status

load_dotenv()
app = FastAPI(
    title="Copilot",
    description="""
### Task notification websocket API
- **URL**: `/tasks/notifications/{user_id}`
- **Websocket call example**: `/tasks/ws-test`
""",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(onboarding_router)
app.include_router(chat_router)
app.include_router(session_router)
app.include_router(task_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/tasks/ws-test", response_class=HTMLResponse, include_in_schema=False)
async def get_websocket_test_page():
    return HTMLResponse(content=open("./static/websocket_test.html", "r").read())


@app.on_event("startup")
async def startup_event():
    check_task_status()
