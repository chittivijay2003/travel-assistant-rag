"""API request and response schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    dependencies: Dict[str, str] = Field(
        default_factory=dict, description="Dependency statuses"
    )


class ErrorResponse(BaseModel):
    """Error response schema."""

    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(
        None, description="Additional error details"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None


class RAGRequest(BaseModel):
    """RAG query request schema."""

    query: str = Field(..., min_length=1, max_length=2000, description="User query")
    country: Optional[str] = Field(None, description="Target country filter")
    category: Optional[str] = Field(None, description="Category filter")
    max_results: int = Field(
        default=5, ge=1, le=20, description="Max results to retrieve"
    )
    session_id: Optional[str] = Field(None, description="Session ID for context")
    chat_history: Optional[List[Dict[str, str]]] = Field(
        None, description="Chat history"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are visa requirements for Indians traveling to Japan?",
                "country": "Japan",
                "max_results": 5,
            }
        }


# Keep old name for backward compatibility
RAGQueryRequest = RAGRequest


class SourceDocument(BaseModel):
    """Source document in response."""

    id: Optional[str] = None
    title: str
    content: str
    category: str
    country: Optional[str] = None
    score: float
    rank: Optional[int] = None


class RAGResponse(BaseModel):
    """RAG query response schema."""

    query: str
    answer: str
    sources: List[SourceDocument] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0)
    processing_time: float
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are visa requirements for Indians traveling to Japan?",
                "answer": "Indian citizens require a tourist visa to visit Japan...",
                "sources": [
                    {
                        "title": "Japan Visa Requirements",
                        "content": "...",
                        "category": "visa_requirements",
                        "score": 0.95,
                    }
                ],
                "confidence_score": 0.92,
                "processing_time": 2.34,
            }
        }


# Keep old name for backward compatibility
RAGQueryResponse = RAGResponse


class DocumentCreateRequest(BaseModel):
    """Document creation request."""

    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    category: str = Field(default="general")
    country: Optional[str] = None
    source_country: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    source: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DocumentResponse(BaseModel):
    """Document response schema."""

    id: str
    title: str
    content: str
    category: str
    country: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime


class SearchRequest(BaseModel):
    """Search request schema."""

    query: str = Field(..., min_length=1, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=20)
    country: Optional[str] = None
    category: Optional[str] = None
    hybrid_alpha: float = Field(default=0.7, ge=0.0, le=1.0)


class SearchResponse(BaseModel):
    """Search response schema."""

    query: str
    results: List[SourceDocument]
    total_results: int
    processing_time: float
