"""Error handling middleware."""

import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ...core.exceptions import (
    QdrantError,
    EmbeddingError,
    LLMError,
    SearchError,
    RAGError,
    AgentError,
)

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for centralized error handling."""

    async def dispatch(self, request: Request, call_next):
        """
        Process request with error handling.

        Args:
            request: FastAPI request
            call_next: Next middleware/endpoint

        Returns:
            Response or error response
        """
        try:
            return await call_next(request)

        except QdrantError as e:
            logger.error(f"Qdrant error: {e}", exc_info=True)
            return JSONResponse(
                status_code=503,
                content={
                    "error": "Vector database error",
                    "message": str(e),
                    "type": "QdrantError",
                },
            )

        except EmbeddingError as e:
            logger.error(f"Embedding error: {e}", exc_info=True)
            return JSONResponse(
                status_code=503,
                content={
                    "error": "Embedding service error",
                    "message": str(e),
                    "type": "EmbeddingError",
                },
            )

        except LLMError as e:
            logger.error(f"LLM error: {e}", exc_info=True)
            return JSONResponse(
                status_code=503,
                content={
                    "error": "Language model error",
                    "message": str(e),
                    "type": "LLMError",
                },
            )

        except SearchError as e:
            logger.error(f"Search error: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Search error",
                    "message": str(e),
                    "type": "SearchError",
                },
            )

        except RAGError as e:
            logger.error(f"RAG error: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "RAG pipeline error",
                    "message": str(e),
                    "type": "RAGError",
                },
            )

        except AgentError as e:
            logger.error(f"Agent error: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Agent execution error",
                    "message": str(e),
                    "type": "AgentError",
                },
            )

        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "message": "An unexpected error occurred",
                    "type": "InternalError",
                },
            )
