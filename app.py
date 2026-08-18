from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from models import ExecutionRequest, ExecutionResponse
from browser_pool import BrowserPool
from config import settings

pool = BrowserPool()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.start()
    yield
    await pool.stop()

app = FastAPI(title="Webhook-to-DOM Execution Engine", lifespan=lifespan)

@app.post("/api/v1/execute", response_model=ExecutionResponse)
async def execute_webhook(request: ExecutionRequest):
    response = await pool.execute_macro(request)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.error_message)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
