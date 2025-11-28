"""Domain models for travel assistant."""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class TravelCategory(str, Enum):
    """Travel information categories."""

    VISA_REQUIREMENTS = "visa_requirements"
    LOCAL_LAWS = "local_laws"
    CULTURAL_ETIQUETTE = "cultural_etiquette"
    SAFETY_GUIDELINES = "safety_guidelines"
    TRAVEL_TIPS = "travel_tips"
    ACCOMMODATION = "accommodation"
    TRANSPORTATION = "transportation"
    FOOD_DINING = "food_dining"
    ACTIVITIES = "activities"
    BUDGET = "budget"
    WEATHER = "weather"
    HEALTH = "health"
    GENERAL = "general"


class DocumentStatus(str, Enum):
    """Document processing status."""

    PENDING = "pending"
    PROCESSING = "processing"
    INDEXED = "indexed"
    FAILED = "failed"


class TravelDocument(BaseModel):
    """Travel document model."""

    model_config = ConfigDict(from_attributes=True)

    id: Optional[str] = None
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    category: TravelCategory = Field(default=TravelCategory.GENERAL)
    country: Optional[str] = Field(None, description="Target country")
    source_country: Optional[str] = Field(
        None, description="Source country (e.g., India)"
    )
    tags: List[str] = Field(default_factory=list, description="Document tags")
    source: Optional[str] = Field(None, description="Information source")
    last_updated: Optional[str] = Field(None, description="Last update date")
    reliability_score: float = Field(
        default=0.8, ge=0.0, le=1.0, description="Information reliability"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
    status: DocumentStatus = Field(default=DocumentStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __str__(self) -> str:
        return f"TravelDocument(id={self.id}, title={self.title}, category={self.category.value})"


class SearchResult(BaseModel):
    """Search result with document and score."""

    model_config = ConfigDict(from_attributes=True)

    document: TravelDocument
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")
    rank: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.document.id,
            "title": self.document.title,
            "content": self.document.content,
            "category": self.document.category.value,
            "country": self.document.country,
            "score": self.score,
            "rank": self.rank,
        }


class TravelQuery(BaseModel):
    """Travel query model."""

    model_config = ConfigDict(from_attributes=True)

    query: str = Field(..., min_length=1, max_length=2000, description="User query")
    country: Optional[str] = Field(None, description="Target country filter")
    category: Optional[TravelCategory] = Field(None, description="Category filter")
    max_results: int = Field(default=5, ge=1, le=20, description="Maximum results")
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    request_id: Optional[str] = None

    def __str__(self) -> str:
        return f"TravelQuery(query={self.query[:50]}..., country={self.country})"


class RAGResponse(BaseModel):
    """RAG pipeline response model."""

    model_config = ConfigDict(from_attributes=True)

    query: str = Field(..., description="Original query")
    answer: str = Field(..., description="Generated answer")
    sources: List[SearchResult] = Field(
        default_factory=list, description="Source documents"
    )
    confidence_score: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Confidence score"
    )
    processing_time: float = Field(
        default=0.0, description="Processing time in seconds"
    )
    retrieval_count: int = Field(default=0, description="Number of documents retrieved")
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "query": self.query,
            "answer": self.answer,
            "sources": [s.to_dict() for s in self.sources],
            "confidence_score": self.confidence_score,
            "processing_time": self.processing_time,
            "retrieval_count": self.retrieval_count,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


class AgentState(BaseModel):
    """LangGraph agent state."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    query: str
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    context: List[SearchResult] = Field(default_factory=list)
    answer: Optional[str] = None
    confidence: float = 0.0
    next_step: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
