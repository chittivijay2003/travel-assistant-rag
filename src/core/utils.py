"""Utility functions and helpers."""

import uuid
from datetime import datetime
from typing import Any, Dict


def generate_request_id() -> str:
    """Generate a unique request ID."""
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat()


def format_sources(sources: list) -> str:
    """Format source documents for display."""
    if not sources:
        return "No sources found."

    formatted = []
    for i, source in enumerate(sources, 1):
        formatted.append(
            f"{i}. {source.get('title', 'Untitled')} (Score: {source.get('score', 0):.2f})"
        )

    return "\n".join(formatted)


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def calculate_confidence(scores: list[float]) -> float:
    """Calculate confidence score from search results."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two dictionaries."""
    result = dict1.copy()
    result.update(dict2)
    return result
