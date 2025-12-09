import logging 
import asyncio 

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import chat_api, health_api  

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_api.router)
app.include_router(health_api.router)

async def heartbeat():
    while True:
        logger.info("Heartbeat")
        await asyncio.sleep(30)


@app.on_event("startup")
async def startup_event():
    try:
        from app.agents.health_graph import HealthGraph
        app.state.health_graph = HealthGraph()
        app.state.heartbeat_task = asyncio.create_task(heartbeat())
        logger.info("Server startup complete")
    except Exception as e:
        logger.error(f"Server startup failed: {e}", exc_info=True)
        raise


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Server shutdown")
    task = getattr(app.state, "heartbeat_task", None)
    if task:
        task.cancel() 

