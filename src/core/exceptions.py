"""Custom exception classes for the application."""


class TravelAssistantException(Exception):
    """Base exception for all application errors."""

    def __init__(
        self, message: str, code: str = "INTERNAL_ERROR", details: dict = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Convert exception to dictionary."""
        return {"error": self.code, "message": self.message, "details": self.details}


# Configuration Errors
class ConfigurationError(TravelAssistantException):
    """Raised when configuration is invalid or missing."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="CONFIGURATION_ERROR", details=details)


# Qdrant Errors
class QdrantError(TravelAssistantException):
    """Base exception for Qdrant-related errors."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="QDRANT_ERROR", details=details)


class QdrantConnectionError(QdrantError):
    """Raised when connection to Qdrant fails."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, details=details)
        self.code = "QDRANT_CONNECTION_ERROR"


class QdrantCollectionError(QdrantError):
    """Raised when collection operations fail."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, details=details)
        self.code = "QDRANT_COLLECTION_ERROR"


class QdrantSearchError(QdrantError):
    """Raised when search operations fail."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, details=details)
        self.code = "QDRANT_SEARCH_ERROR"


# Embedding Errors
class EmbeddingError(TravelAssistantException):
    """Raised when embedding generation fails."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="EMBEDDING_ERROR", details=details)


class EmbeddingGenerationError(EmbeddingError):
    """Raised when embedding generation fails."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, details=details)
        self.code = "EMBEDDING_GENERATION_ERROR"


# Search Errors
class SearchError(TravelAssistantException):
    """Raised when search operations fail."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="SEARCH_ERROR", details=details)


# LLM Errors
class LLMError(TravelAssistantException):
    """Raised when LLM operations fail."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="LLM_ERROR", details=details)


class LLMAPIError(LLMError):
    """Raised when LLM API calls fail."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, details=details)
        self.code = "LLM_API_ERROR"


class LLMRateLimitError(LLMError):
    """Raised when LLM rate limit is exceeded."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, details=details)
        self.code = "LLM_RATE_LIMIT_ERROR"


# RAG Errors
class RAGError(TravelAssistantException):
    """Raised when RAG pipeline fails."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="RAG_ERROR", details=details)


class RAGContextError(RAGError):
    """Raised when context retrieval fails."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, details=details)
        self.code = "RAG_CONTEXT_ERROR"


# Validation Errors
class ValidationError(TravelAssistantException):
    """Raised when input validation fails."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="VALIDATION_ERROR", details=details)


# Not Found Errors
class NotFoundError(TravelAssistantException):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="NOT_FOUND", details=details)


# Agent Errors
class AgentError(TravelAssistantException):
    """Raised when agent operations fail."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="AGENT_ERROR", details=details)


class AgentRoutingError(AgentError):
    """Raised when agent routing fails."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, details=details)
        self.code = "AGENT_ROUTING_ERROR"


# API Errors
class APIError(TravelAssistantException):
    """Raised when API operations fail."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="API_ERROR", details=details)


class RateLimitError(TravelAssistantException):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="RATE_LIMIT_EXCEEDED", details=details)
