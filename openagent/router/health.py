from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

router = APIRouter(tags=["health"])

@router.get("/health", status_code=status.HTTP_200_OK, include_in_schema=False)
async def health_check():
    return JSONResponse(content={"status": "ok"}) 