"""Qdrant vector store service with comprehensive logging and error handling."""

import logging
import uuid
from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    SearchRequest,
    ScoredPoint,
)
from qdrant_client.http import models

from ..config.settings import settings
from ..core.exceptions import (
    QdrantConnectionError,
    QdrantCollectionError,
    QdrantSearchError,
)
from ..core.utils import generate_request_id
from ..models.domain import TravelDocument, SearchResult

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for managing Qdrant vector store operations."""

    def __init__(self):
        """Initialize Qdrant client."""
        self.collection_name = settings.qdrant_collection
        self.client: Optional[QdrantClient] = None
        self.vector_size = 768  # Gemini embedding dimension

        logger.info(
            "Initializing Qdrant service",
            extra={"collection": self.collection_name, "vector_size": self.vector_size},
        )

    def connect(self) -> None:
        """
        Establish connection to Qdrant.

        Raises:
            QdrantConnectionError: If connection fails
        """
        try:
            logger.info(
                "Connecting to Qdrant",
                extra={
                    "host": settings.qdrant_host,
                    "port": settings.qdrant_port,
                    "use_memory": settings.qdrant_use_memory,
                },
            )

            if settings.qdrant_use_memory:
                # Use persistent local storage instead of in-memory
                import os

                storage_path = "./qdrant_storage"
                os.makedirs(storage_path, exist_ok=True)
                self.client = QdrantClient(path=storage_path)
                logger.info(
                    f"Connected to local Qdrant with persistent storage at {storage_path}"
                )
            else:
                # Use Qdrant server
                self.client = QdrantClient(
                    host=settings.qdrant_host,
                    port=settings.qdrant_port,
                    api_key=settings.qdrant_api_key,
                    timeout=60,
                )
                logger.info("Connected to Qdrant server")

        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}", exc_info=True)
            raise QdrantConnectionError(
                f"Failed to connect to Qdrant: {str(e)}",
                details={"host": settings.qdrant_host, "port": settings.qdrant_port},
            )

    def create_collection(self, vector_size: int = 768) -> None:
        """
        Create Qdrant collection with proper schema.

        Args:
            vector_size: Dimension of embedding vectors

        Raises:
            QdrantCollectionError: If collection creation fails
        """
        request_id = generate_request_id()

        try:
            logger.info(
                "Creating collection",
                extra={
                    "collection": self.collection_name,
                    "vector_size": vector_size,
                    "request_id": request_id,
                },
            )

            if not self.client:
                self.connect()

            # Check if collection exists
            collections = self.client.get_collections().collections
            exists = any(col.name == self.collection_name for col in collections)

            if exists:
                logger.info(f"Collection '{self.collection_name}' already exists")
                return

            # Create collection with vector configuration
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

            logger.info(
                f"Collection '{self.collection_name}' created successfully",
                extra={"request_id": request_id},
            )

            # Create payload indexes for filtering
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="category",
                field_schema="keyword",
            )

            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="country",
                field_schema="keyword",
            )

            logger.info("Payload indexes created", extra={"request_id": request_id})

        except Exception as e:
            logger.error(
                f"Failed to create collection: {e}",
                exc_info=True,
                extra={"request_id": request_id},
            )
            raise QdrantCollectionError(
                f"Failed to create collection: {str(e)}",
                details={"collection": self.collection_name},
            )

    def index_documents(
        self, documents: List[TravelDocument], embeddings: List[List[float]]
    ) -> None:
        """
        Index documents with their embeddings.

        Args:
            documents: List of travel documents
            embeddings: List of embedding vectors

        Raises:
            QdrantCollectionError: If indexing fails
        """
        request_id = generate_request_id()

        try:
            if len(documents) != len(embeddings):
                raise ValueError("Number of documents must match number of embeddings")

            logger.info(
                f"Indexing {len(documents)} documents",
                extra={"count": len(documents), "request_id": request_id},
            )

            if not self.client:
                self.connect()

            # Prepare points for insertion
            points = []
            for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
                # Generate UUID from string ID for in-memory Qdrant compatibility
                doc_id = doc.id or f"doc_{i}"
                point_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, doc_id)

                point = PointStruct(
                    id=point_uuid,
                    vector=embedding,
                    payload={
                        "id": doc_id,  # Keep original ID in payload
                        "title": doc.title,
                        "content": doc.content,
                        "category": doc.category.value,
                        "country": doc.country,
                        "source_country": doc.source_country,
                        "tags": doc.tags,
                        "source": doc.source,
                        "last_updated": doc.last_updated,
                        "reliability_score": doc.reliability_score,
                        "metadata": doc.metadata,
                    },
                )
                points.append(point)

            # Upload points in batches
            batch_size = 100
            for i in range(0, len(points), batch_size):
                batch = points[i : i + batch_size]
                self.client.upsert(collection_name=self.collection_name, points=batch)
                logger.debug(
                    f"Uploaded batch {i // batch_size + 1}",
                    extra={"batch_size": len(batch), "request_id": request_id},
                )

            logger.info(
                f"Successfully indexed {len(documents)} documents",
                extra={"count": len(documents), "request_id": request_id},
            )

        except Exception as e:
            logger.error(
                f"Failed to index documents: {e}",
                exc_info=True,
                extra={"request_id": request_id},
            )
            raise QdrantCollectionError(
                f"Failed to index documents: {str(e)}",
                details={"document_count": len(documents)},
            )

    def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """
        Search for similar documents using vector similarity.

        Args:
            query_vector: Query embedding vector
            limit: Maximum number of results
            filters: Optional filters (country, category)

        Returns:
            List of search results with documents and scores

        Raises:
            QdrantSearchError: If search fails
        """
        request_id = generate_request_id()

        try:
            logger.info(
                "Performing vector search",
                extra={"limit": limit, "filters": filters, "request_id": request_id},
            )

            if not self.client:
                self.connect()

            # Build filter conditions
            search_filter = None
            if filters:
                conditions = []

                if filters.get("country"):
                    conditions.append(
                        FieldCondition(
                            key="country", match=MatchValue(value=filters["country"])
                        )
                    )

                if filters.get("category"):
                    conditions.append(
                        FieldCondition(
                            key="category", match=MatchValue(value=filters["category"])
                        )
                    )

                if conditions:
                    search_filter = Filter(must=conditions)

            # Perform search using query_points (correct Qdrant API method)
            search_response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                query_filter=search_filter,
                with_payload=True,
            )

            # Extract points from response
            search_results = search_response.points

            logger.info(
                f"Search returned {len(search_results)} results",
                extra={"count": len(search_results), "request_id": request_id},
            )

            # Convert to SearchResult objects
            results = []
            for rank, hit in enumerate(search_results, 1):
                doc = TravelDocument(
                    id=hit.payload.get("id"),
                    title=hit.payload.get("title", ""),
                    content=hit.payload.get("content", ""),
                    category=hit.payload.get("category", "general"),
                    country=hit.payload.get("country"),
                    source_country=hit.payload.get("source_country"),
                    tags=hit.payload.get("tags", []),
                    source=hit.payload.get("source"),
                    last_updated=hit.payload.get("last_updated"),
                    reliability_score=hit.payload.get("reliability_score", 0.8),
                    metadata=hit.payload.get("metadata", {}),
                )

                result = SearchResult(document=doc, score=hit.score, rank=rank)
                results.append(result)

            logger.debug(
                "Search results parsed",
                extra={"scores": [r.score for r in results], "request_id": request_id},
            )

            return results

        except Exception as e:
            logger.error(
                f"Search failed: {e}", exc_info=True, extra={"request_id": request_id}
            )
            raise QdrantSearchError(
                f"Search failed: {str(e)}", details={"limit": limit, "filters": filters}
            )

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get collection information and statistics.

        Returns:
            Dictionary with collection info
        """
        try:
            if not self.client:
                self.connect()

            info = self.client.get_collection(self.collection_name)

            return {
                "name": self.collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status.name if info.status else "unknown",
            }

        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {}

    def delete_collection(self) -> None:
        """Delete the collection."""
        try:
            if not self.client:
                self.connect()

            self.client.delete_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' deleted")

        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            raise QdrantCollectionError(f"Failed to delete collection: {str(e)}")

    def health_check(self) -> bool:
        """
        Check if Qdrant is healthy and accessible.

        Returns:
            True if healthy, False otherwise
        """
        try:
            if not self.client:
                self.connect()

            collections = self.client.get_collections()
            logger.debug("Qdrant health check passed")
            return True

        except Exception as e:
            logger.error(f"Qdrant health check failed: {e}")
            return False
