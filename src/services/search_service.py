"""Hybrid search service combining semantic and keyword search."""

import logging
from typing import List, Optional, Dict, Any
from collections import defaultdict
from rank_bm25 import BM25Okapi

from ..config.settings import settings
from ..core.exceptions import SearchError
from ..core.utils import generate_request_id
from ..models.domain import TravelDocument, SearchResult, TravelQuery
from .qdrant_service import QdrantService
from .embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class SearchService:
    """Service for hybrid search (semantic + keyword)."""

    def __init__(
        self,
        qdrant_service: Optional[QdrantService] = None,
        embedding_service: Optional[EmbeddingService] = None,
    ):
        """
        Initialize search service.

        Args:
            qdrant_service: Qdrant service instance
            embedding_service: Embedding service instance
        """
        self.qdrant = qdrant_service or QdrantService()
        self.embedder = embedding_service or EmbeddingService()

        logger.info("Search service initialized")

    def semantic_search(
        self, query: str, limit: int = 10, filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Perform semantic search using vector similarity.

        Args:
            query: Search query
            limit: Maximum number of results
            filters: Optional filters (country, category)

        Returns:
            List of search results
        """
        request_id = generate_request_id()

        try:
            logger.info(
                f"Performing semantic search: {query[:100]}...",
                extra={
                    "query_length": len(query),
                    "limit": limit,
                    "filters": filters,
                    "request_id": request_id,
                },
            )

            # Generate query embedding
            logger.debug(
                "Generating query embedding...", extra={"request_id": request_id}
            )
            query_embedding = self.embedder.embed_query(query)
            logger.debug(
                f"Query embedding generated (dim: {len(query_embedding)})",
                extra={"request_id": request_id},
            )

            # Search in Qdrant
            logger.debug("Searching in Qdrant...", extra={"request_id": request_id})
            results = self.qdrant.search(
                query_vector=query_embedding, limit=limit, filters=filters
            )

            logger.info(
                f"Semantic search returned {len(results)} results",
                extra={
                    "count": len(results),
                    "scores": [r.score for r in results],
                    "request_id": request_id,
                },
            )

            return results

        except Exception as e:
            logger.error(
                f"Semantic search failed: {e}",
                exc_info=True,
                extra={"request_id": request_id},
            )
            raise SearchError(
                f"Semantic search failed: {str(e)}", details={"query": query[:100]}
            )

    def keyword_search(
        self, query: str, documents: List[TravelDocument], limit: int = 10
    ) -> List[SearchResult]:
        """
        Perform keyword-based search using BM25 algorithm.

        Args:
            query: Search query
            documents: List of documents to search
            limit: Maximum number of results

        Returns:
            List of search results with BM25 scores
        """
        request_id = generate_request_id()

        try:
            logger.debug(
                f"Performing BM25 keyword search: {query[:100]}...",
                extra={"request_id": request_id},
            )

            if not documents:
                return []

            # Prepare corpus for BM25
            # Combine title (weighted) + content for better relevance
            corpus = []
            for doc in documents:
                # Title appears twice to give it more weight in BM25 scoring
                combined_text = f"{doc.title} {doc.title} {doc.content}"
                corpus.append(combined_text.lower())

            # Tokenize corpus
            tokenized_corpus = [doc.split() for doc in corpus]

            # Initialize BM25 with default parameters (k1=1.5, b=0.75)
            bm25 = BM25Okapi(tokenized_corpus)

            # Tokenize query
            tokenized_query = query.lower().split()

            # Get BM25 scores for all documents
            scores = bm25.get_scores(tokenized_query)

            # Normalize scores to 0-1 range
            max_score = max(scores) if len(scores) > 0 and max(scores) > 0 else 1.0

            # Create search results
            scored_docs = []
            for idx, score in enumerate(scores):
                if score > 0:
                    normalized_score = float(score) / max_score
                    result = SearchResult(
                        document=documents[idx],
                        score=normalized_score,
                        metadata={
                            "search_type": "keyword_bm25",
                            "raw_bm25_score": float(score),
                        },
                    )
                    scored_docs.append(result)

            # Sort by score and limit
            scored_docs.sort(key=lambda x: x.score, reverse=True)
            results = scored_docs[:limit]

            logger.debug(
                f"BM25 keyword search returned {len(results)} results",
                extra={"count": len(results), "request_id": request_id},
            )

            return results

        except Exception as e:
            logger.error(f"BM25 keyword search failed: {e}", exc_info=True)
            return []

    def reciprocal_rank_fusion(
        self,
        semantic_results: List[SearchResult],
        keyword_results: List[SearchResult],
        k: int = 60,
    ) -> List[SearchResult]:
        """
        Combine semantic and keyword results using Reciprocal Rank Fusion (RRF).

        Args:
            semantic_results: Results from semantic search
            keyword_results: Results from keyword search
            k: RRF constant (default: 60)

        Returns:
            Fused and re-ranked results
        """
        request_id = generate_request_id()

        try:
            logger.debug(
                "Performing Reciprocal Rank Fusion",
                extra={
                    "semantic_count": len(semantic_results),
                    "keyword_count": len(keyword_results),
                    "request_id": request_id,
                },
            )

            # Calculate RRF scores
            doc_scores: Dict[str, float] = defaultdict(float)
            doc_map: Dict[str, SearchResult] = {}

            # Add semantic results
            for rank, result in enumerate(semantic_results, 1):
                doc_id = result.document.id or result.document.title
                doc_scores[doc_id] += 1.0 / (k + rank)
                doc_map[doc_id] = result

            # Add keyword results
            for rank, result in enumerate(keyword_results, 1):
                doc_id = result.document.id or result.document.title
                doc_scores[doc_id] += 1.0 / (k + rank)
                if doc_id not in doc_map:
                    doc_map[doc_id] = result

            # Create fused results
            fused_results = []
            for doc_id, score in doc_scores.items():
                result = doc_map[doc_id]
                # Normalize score to 0-1 range
                normalized_score = min(
                    score / 0.1, 1.0
                )  # Adjust normalization as needed
                fused_result = SearchResult(
                    document=result.document, score=normalized_score
                )
                fused_results.append(fused_result)

            # Sort by fused score
            fused_results.sort(key=lambda x: x.score, reverse=True)

            # Assign ranks
            for rank, result in enumerate(fused_results, 1):
                result.rank = rank

            logger.debug(
                f"RRF produced {len(fused_results)} results",
                extra={
                    "count": len(fused_results),
                    "top_scores": [r.score for r in fused_results[:5]],
                    "request_id": request_id,
                },
            )

            return fused_results

        except Exception as e:
            logger.error(f"RRF fusion failed: {e}", exc_info=True)
            # Fallback to semantic results
            return semantic_results

    def hybrid_search(
        self, query: TravelQuery, alpha: Optional[float] = None
    ) -> List[SearchResult]:
        """
        Perform hybrid search combining semantic and keyword search.

        Args:
            query: Travel query object
            alpha: Weight for semantic vs keyword (0=keyword only, 1=semantic only)
                  If None, uses settings.hybrid_alpha

        Returns:
            List of search results ranked by hybrid score
        """
        request_id = generate_request_id()

        try:
            alpha = alpha if alpha is not None else settings.hybrid_alpha

            logger.info(
                f"Performing hybrid search: {query.query[:100]}...",
                extra={
                    "query": query.query[:100],
                    "alpha": alpha,
                    "max_results": query.max_results,
                    "request_id": request_id,
                },
            )

            # Build filters
            filters = {}
            if query.country:
                filters["country"] = query.country
            if query.category:
                filters["category"] = (
                    query.category.value
                    if hasattr(query.category, "value")
                    else query.category
                )

            # Perform semantic search
            logger.debug(
                "Starting semantic search...", extra={"request_id": request_id}
            )
            semantic_results = self.semantic_search(
                query=query.query,
                limit=query.max_results * 2,  # Get more for fusion
                filters=filters if filters else None,
            )

            # If alpha is 1.0, return only semantic results
            if alpha >= 0.99:
                logger.info(
                    "Using semantic-only results (alpha=1.0)",
                    extra={"request_id": request_id},
                )
                return semantic_results[: query.max_results]

            # Perform keyword search on retrieved documents
            # (In production, this would search all documents or use a keyword index)
            if semantic_results:
                logger.debug(
                    "Starting keyword search...", extra={"request_id": request_id}
                )
                all_docs = [r.document for r in semantic_results]
                keyword_results = self.keyword_search(
                    query=query.query, documents=all_docs, limit=query.max_results * 2
                )
            else:
                keyword_results = []

            # If alpha is 0.0, return only keyword results
            if alpha <= 0.01:
                logger.info(
                    "Using keyword-only results (alpha=0.0)",
                    extra={"request_id": request_id},
                )
                return keyword_results[: query.max_results]

            # Fuse results using RRF
            logger.debug("Fusing results with RRF...", extra={"request_id": request_id})
            fused_results = self.reciprocal_rank_fusion(
                semantic_results=semantic_results, keyword_results=keyword_results
            )

            # Apply alpha weighting
            final_results = []
            for result in fused_results:
                # Get semantic score
                semantic_score = next(
                    (
                        r.score
                        for r in semantic_results
                        if r.document.id == result.document.id
                    ),
                    0.0,
                )
                # Get keyword score
                keyword_score = next(
                    (
                        r.score
                        for r in keyword_results
                        if r.document.id == result.document.id
                    ),
                    0.0,
                )

                # Weighted combination
                hybrid_score = alpha * semantic_score + (1 - alpha) * keyword_score

                final_result = SearchResult(
                    document=result.document, score=hybrid_score, rank=result.rank
                )
                final_results.append(final_result)

            # Sort by hybrid score
            final_results.sort(key=lambda x: x.score, reverse=True)

            # Update ranks
            for rank, result in enumerate(final_results, 1):
                result.rank = rank

            # Limit to requested number
            final_results = final_results[: query.max_results]

            logger.info(
                f"Hybrid search completed with {len(final_results)} results",
                extra={
                    "count": len(final_results),
                    "top_scores": [r.score for r in final_results[:3]],
                    "request_id": request_id,
                },
            )

            return final_results

        except Exception as e:
            logger.error(
                f"Hybrid search failed: {e}",
                exc_info=True,
                extra={"request_id": request_id},
            )
            raise SearchError(
                f"Hybrid search failed: {str(e)}", details={"query": query.query[:100]}
            )
