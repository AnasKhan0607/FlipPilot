from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import health, watchlist
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress INFO-level websocket connection logs from uvicorn
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

app = FastAPI(title="FlipPilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(watchlist.router)