"""RAG endpoints."""

import logging
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ...models.schemas import RAGRequest, RAGResponse as RAGResponseSchema
from ...agents.graph import TravelAssistantGraph
from ...core.utils import generate_request_id

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize agent (singleton pattern)
_agent = None


def get_agent() -> TravelAssistantGraph:
    """Get or create agent instance."""
    global _agent
    if _agent is None:
        logger.info("Initializing Travel Assistant Agent...")
        _agent = TravelAssistantGraph()
    return _agent


@router.post("/rag-travel", response_model=RAGResponseSchema)
async def rag_travel(request: RAGRequest):
    """
    Process travel query through RAG pipeline.

    Args:
        request: RAG request with query and optional filters

    Returns:
        RAG response with answer and sources
    """
    request_id = generate_request_id()

    logger.info(
        f"RAG request received: {request.query[:100]}...",
        extra={
            "query": request.query[:100],
            "country": request.country,
            "category": request.category,
            "request_id": request_id,
        },
    )

    try:
        # Get agent
        agent = get_agent()

        # Process query
        response = agent.invoke(
            query=request.query,
            country=request.country,
            category=request.category,
            max_results=request.max_results,
            messages=request.chat_history,
        )

        logger.info(
            "RAG request processed successfully",
            extra={
                "answer_length": len(response["answer"]),
                "sources_count": len(response["sources"]),
                "confidence": response["confidence_score"],
                "request_id": request_id,
            },
        )

        return RAGResponseSchema(**response)

    except Exception as e:
        logger.error(
            f"RAG request failed: {e}", exc_info=True, extra={"request_id": request_id}
        )
        raise HTTPException(
            status_code=500, detail=f"Failed to process RAG query: {str(e)}"
        )


class ValidateRequest(BaseModel):
    """Query validation request."""

    query: str = Field(..., min_length=1, max_length=2000)


class ValidateResponse(BaseModel):
    """Query validation response."""

    valid: bool
    issues: List[str]
    suggestions: List[str]
    length: int


@router.post("/validate-query", response_model=ValidateResponse)
async def validate_query(request: ValidateRequest):
    """
    Validate a travel query.

    Args:
        request: Validation request

    Returns:
        Validation results
    """
    logger.debug(f"Query validation requested: {request.query[:100]}...")

    try:
        agent = get_agent()
        validation = agent.rag_service.validate_query(request.query)

        return ValidateResponse(**validation)

    except Exception as e:
        logger.error(f"Query validation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")
