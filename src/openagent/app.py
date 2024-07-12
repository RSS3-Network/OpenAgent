import os

from chainlit.utils import mount_chainlit
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import FileResponse, JSONResponse
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


@app.get("/widget/swap")
async def swap_root():
    print("swap_root")
    return FileResponse(os.path.join("dist", "index.html"))


app.mount("/assets", StaticFiles(directory="dist/assets"), name="widget")

mount_chainlit(app=app, target="openagent/ui/app.py", path="/ui")


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return JSONResponse(content={"status": "ok"})
