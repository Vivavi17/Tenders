"""Основной модуль"""

import uvicorn
from fastapi import FastAPI

from bids.router import router as router_bids
from tenders.router import router as router_tenders

app = FastAPI(root_path="/api")


@app.get("/ping")
async def ping() -> str:
    """Проверка доступности сервера"""
    return "ok"


app.include_router(router_tenders)
app.include_router(router_bids)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
