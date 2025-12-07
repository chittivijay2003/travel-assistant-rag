"""FastAPI application for RAG Travel Assistant."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..config.settings import settings
from ..core.logging import setup_logging
from .routes import rag, health
from .middleware.logging_middleware import LoggingMiddleware
from .middleware.error_handler import ErrorHandlerMiddleware

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting RAG Travel Assistant API...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"API Port: {settings.api_port}")

    yield

    # Shutdown
    logger.info("Shutting down RAG Travel Assistant API...")


# Create FastAPI app
app = FastAPI(
    title="RAG Travel Assistant API",
    description="Production-ready travel assistant powered by RAG and LangGraph",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(rag.router, prefix="/api/v1", tags=["RAG"])

# Legacy endpoint for test.py compatibility
app.include_router(rag.router, prefix="", tags=["RAG (Legacy)"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "RAG Travel Assistant API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=settings.api_port,
        reload=settings.environment == "development",
        log_level=settings.log_level.lower(),
    )
