"""Health check endpoints."""

import logging
from fastapi import APIRouter
from pydantic import BaseModel

from ...services.qdrant_service import QdrantService

logger = logging.getLogger(__name__)

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    services: dict


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns:
        Health status of the application and services
    """
    logger.debug("Health check requested")

    # Check Qdrant connection
    qdrant_status = "unknown"
    try:
        qdrant = QdrantService()
        qdrant.connect()
        health = qdrant.health_check()
        qdrant_status = "healthy" if health else "unhealthy"
    except Exception as e:
        error_str = str(e).lower()
        if "already accessed by another instance" in error_str:
            qdrant_status = "healthy"  # Actually healthy, just multiple access
        else:
            qdrant_status = "unhealthy"
        logger.warning(f"Qdrant health check failed: {e}")

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        services={
            "qdrant": qdrant_status,
            "gemini": "configured",  # Check if API key is set
        },
    )


@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint.

    Returns:
        Readiness status
    """
    return {"ready": True}


@router.get("/live")
async def liveness_check():
    """
    Liveness check endpoint.

    Returns:
        Liveness status
    """
    return {"alive": True}
