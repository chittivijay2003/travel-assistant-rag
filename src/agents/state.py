"""LangGraph agent state definition."""

from typing import TypedDict, List, Dict, Any, Optional
from ..models.domain import SearchResult


class AgentState(TypedDict):
    """State for the travel assistant agent."""

    # Input
    query: str
    country: Optional[str]
    category: Optional[str]
    max_results: int

    # Processing
    messages: List[Dict[str, Any]]
    context: List[SearchResult]
    intent: Optional[str]

    # Output
    answer: Optional[str]
    confidence_score: float
    processing_time: float

    # Control flow
    next_step: str

    # Metadata
    metadata: Dict[str, Any]
    request_id: str
