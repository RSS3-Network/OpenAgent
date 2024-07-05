import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from openagent.router.chat import chat_router
from openagent.router.onboarding import onboarding_router
from openagent.router.session import session_router

load_dotenv()
app = FastAPI(title="OpenAgent", description="")

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


@app.get("/swap")
async def swap():
    return FileResponse(os.path.join("dist", "index.html"))


@app.get("/swap/select-wallet")
async def swap_select_wallet():
    print("swap_select_wallet")
    return FileResponse(os.path.join("dist", "index.html"))


@app.get("/swap/settings")
async def swap_setting():
    print("swap_setting")

    return FileResponse(os.path.join("dist", "index.html"))


app.mount("/", StaticFiles(directory="dist", html=True), name="static")
