"""Embedding service using Sentence Transformers with comprehensive logging and error handling."""

import logging
from typing import List
from sentence_transformers import SentenceTransformer

from ..core.exceptions import EmbeddingError, EmbeddingGenerationError
from ..core.utils import generate_request_id

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating embeddings using Sentence Transformers (local)."""

    def __init__(self):
        """Initialize Sentence Transformers embedding service."""
        try:
            logger.info(
                "Initializing Sentence Transformers embedding service",
                extra={"model": "all-MiniLM-L6-v2"},
            )

            # Load the model (lightweight and fast)
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.model_name = "all-MiniLM-L6-v2"
            self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2

            logger.info(
                "Sentence Transformers embedding service initialized successfully"
            )

        except Exception as e:
            logger.error(f"Failed to initialize embedding service: {e}", exc_info=True)
            raise EmbeddingError(
                f"Failed to initialize embedding service: {str(e)}",
                details={"model": "all-MiniLM-L6-v2"},
            )

    def embed_text(
        self, text: str, task_type: str = "retrieval_document"
    ) -> List[float]:
        """
        Generate embedding for a single text using Sentence Transformers.

        Args:
            text: Text to embed
            task_type: Task type (ignored for Sentence Transformers, kept for compatibility)

        Returns:
            Embedding vector as list of floats

        Raises:
            EmbeddingGenerationError: If embedding generation fails
        """
        request_id = generate_request_id()

        try:
            logger.debug(
                f"Generating embedding for text (length: {len(text)})",
                extra={
                    "text_length": len(text),
                    "request_id": request_id,
                },
            )

            # Generate embedding using Sentence Transformers
            embedding = self.model.encode(text, convert_to_numpy=True)
            embedding_list = embedding.tolist()

            logger.debug(
                f"Embedding generated successfully (dim: {len(embedding_list)})",
                extra={"dimension": len(embedding_list), "request_id": request_id},
            )

            return embedding_list

        except Exception as e:
            logger.error(
                f"Failed to generate embedding: {e}",
                exc_info=True,
                extra={"text_length": len(text), "request_id": request_id},
            )
            raise EmbeddingGenerationError(
                f"Failed to generate embedding: {str(e)}",
                details={"text_length": len(text)},
            )

    def embed_texts(
        self,
        texts: List[str],
        task_type: str = "retrieval_document",
        batch_size: int = 100,
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts using Sentence Transformers.

        Args:
            texts: List of texts to embed
            task_type: Task type (ignored, kept for compatibility)
            batch_size: Batch size for processing

        Returns:
            List of embedding vectors

        Raises:
            EmbeddingGenerationError: If embedding generation fails
        """
        request_id = generate_request_id()

        try:
            logger.info(
                f"Generating embeddings for {len(texts)} texts",
                extra={
                    "count": len(texts),
                    "request_id": request_id,
                },
            )

            # Generate all embeddings at once (Sentence Transformers is efficient)
            embeddings = self.model.encode(
                texts, convert_to_numpy=True, show_progress_bar=False
            )
            embeddings_list = [emb.tolist() for emb in embeddings]

            logger.info(
                f"Generated {len(embeddings_list)} embeddings successfully",
                extra={"count": len(embeddings_list), "request_id": request_id},
            )

            return embeddings_list

        except Exception as e:
            logger.error(
                f"Failed to generate batch embeddings: {e}",
                exc_info=True,
                extra={"text_count": len(texts), "request_id": request_id},
            )
            raise EmbeddingGenerationError(
                f"Failed to generate batch embeddings: {str(e)}",
                details={"text_count": len(texts)},
            )

    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings.

        Returns:
            Embedding dimension
        """
        # all-MiniLM-L6-v2 produces 384-dimensional vectors
        return self.embedding_dim

    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.

        Args:
            query: Search query text

        Returns:
            Query embedding vector
        """
        logger.debug(f"Generating query embedding: {query[:100]}...")
        return self.embed_text(query, task_type="retrieval_query")
