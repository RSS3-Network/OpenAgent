from fastapi import APIRouter
from starlette.responses import FileResponse
import os

router = APIRouter(tags=["widget"])

@router.get("/widget/swap", include_in_schema=False)
async def swap_root():
    return FileResponse(os.path.join("dist", "index.html"))

@router.get("/widget/price-chart", include_in_schema=False)
async def chart_price_root():
    return FileResponse(os.path.join("dist", "index.html"))

@router.get("/widget/transfer", include_in_schema=False)
async def transfer_root():
    return FileResponse(os.path.join("dist", "index.html")) 