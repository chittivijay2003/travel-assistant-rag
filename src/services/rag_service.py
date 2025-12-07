"""RAG service orchestrating the entire retrieval-augmented generation pipeline."""

import logging
from typing import List, Optional, Dict, Any
import time

from ..config.settings import settings
from ..core.exceptions import RAGError
from ..core.utils import generate_request_id
from ..models.domain import TravelQuery, RAGResponse, SearchResult
from .search_service import SearchService
from .llm_service import LLMService

logger = logging.getLogger(__name__)


class RAGService:
    """Service orchestrating the RAG pipeline."""

    def __init__(
        self,
        search_service: Optional[SearchService] = None,
        llm_service: Optional[LLMService] = None,
    ):
        """
        Initialize RAG service.

        Args:
            search_service: Search service instance
            llm_service: LLM service instance
        """
        self.search = search_service or SearchService()
        self.llm = llm_service or LLMService()

        logger.info("RAG service initialized")

    def process_query(
        self,
        query: TravelQuery,
        chat_history: Optional[List[Dict[str, str]]] = None,
        include_sources: bool = True,
    ) -> RAGResponse:
        """
        Process travel query through RAG pipeline.

        Pipeline:
        1. Retrieve relevant documents using hybrid search
        2. Format context from retrieved documents
        3. Generate response using LLM with context
        4. Return response with sources and metadata

        Args:
            query: Travel query object
            chat_history: Optional chat history for context
            include_sources: Whether to include source documents in response

        Returns:
            RAG response with answer, sources, and metadata
        """
        request_id = generate_request_id()
        start_time = time.time()

        try:
            logger.info(
                f"Processing RAG query: {query.query[:100]}...",
                extra={
                    "query": query.query[:100],
                    "country": query.country,
                    "category": query.category,
                    "request_id": request_id,
                },
            )

            # Step 1: Retrieve relevant documents
            logger.debug(
                "Step 1: Retrieving documents...", extra={"request_id": request_id}
            )
            retrieval_start = time.time()

            search_results = self.search.hybrid_search(query=query)

            retrieval_duration = time.time() - retrieval_start

            logger.info(
                f"Retrieved {len(search_results)} documents",
                extra={
                    "count": len(search_results),
                    "duration_seconds": round(retrieval_duration, 2),
                    "top_scores": [r.score for r in search_results[:3]],
                    "request_id": request_id,
                },
            )

            # Check if we got any results
            if not search_results:
                logger.warning(
                    "No relevant documents found", extra={"request_id": request_id}
                )

                return RAGResponse(
                    query=query.query,
                    answer="I couldn't find specific information about your query in my knowledge base. Could you please rephrase your question or provide more details?",
                    sources=[],
                    confidence_score=0.0,
                    processing_time=time.time() - start_time,
                    retrieval_count=0,
                )

            # Check if results are actually relevant (low confidence threshold)
            top_score = search_results[0].score
            if top_score < 0.65:
                logger.warning(
                    f"Low relevance score ({top_score:.3f}) - results may not match query",
                    extra={"request_id": request_id, "top_score": top_score},
                )

                # Check if there's a country/citizenship mismatch
                mismatch_message = self._detect_knowledge_gap(
                    query.query, search_results
                )
                if mismatch_message:
                    return RAGResponse(
                        query=query.query,
                        answer=mismatch_message,
                        sources=search_results[:3],  # Include top 3 for reference
                        confidence_score=top_score,
                        processing_time=time.time() - start_time,
                        retrieval_count=len(search_results),
                    )

            # Step 2: Format context
            logger.debug(
                "Step 2: Formatting context...", extra={"request_id": request_id}
            )
            context = self.llm.format_context(search_results)

            logger.debug(
                f"Context formatted ({len(context)} chars)",
                extra={"context_length": len(context), "request_id": request_id},
            )

            # Step 3: Generate response
            logger.debug(
                "Step 3: Generating LLM response...", extra={"request_id": request_id}
            )
            generation_start = time.time()

            answer = self.llm.generate_response(
                query=query.query, context=context, chat_history=chat_history
            )

            generation_duration = time.time() - generation_start

            logger.info(
                "LLM response generated",
                extra={
                    "answer_length": len(answer),
                    "duration_seconds": round(generation_duration, 2),
                    "request_id": request_id,
                },
            )

            # Step 4: Build response
            total_duration = time.time() - start_time

            # Calculate confidence score based on search results
            confidence_score = self._calculate_confidence(search_results)

            # Prepare sources
            sources = search_results if include_sources else []

            # Format context as array of document contents for test.py
            retrieved_context = [result.document.content for result in search_results]

            response = RAGResponse(
                query=query.query,
                answer=answer,
                sources=sources,
                retrieved_context=retrieved_context,
                confidence_score=confidence_score,
                processing_time=total_duration,
                retrieval_count=len(search_results),
                metadata={
                    "retrieval_duration": retrieval_duration,
                    "generation_duration": generation_duration,
                    "top_score": search_results[0].score if search_results else 0.0,
                    "avg_score": sum(r.score for r in search_results)
                    / len(search_results)
                    if search_results
                    else 0.0,
                    "request_id": request_id,
                },
            )

            logger.info(
                "RAG query processed successfully",
                extra={
                    "total_duration": round(total_duration, 2),
                    "confidence": round(confidence_score, 3),
                    "request_id": request_id,
                },
            )

            return response

        except Exception as e:
            logger.error(
                f"RAG processing failed: {e}",
                exc_info=True,
                extra={"request_id": request_id},
            )
            raise RAGError(
                f"Failed to process RAG query: {str(e)}",
                details={"query": query.query[:100]},
            )

    def _calculate_confidence(self, search_results: List[SearchResult]) -> float:
        """
        Calculate confidence score based on search results.

        Args:
            search_results: List of search results

        Returns:
            Confidence score between 0 and 1
        """
        if not search_results:
            return 0.0

        # Factors:
        # 1. Top result score (40% weight)
        # 2. Average score of top 3 (30% weight)
        # 3. Number of results (30% weight, normalized)

        top_score = search_results[0].score

        top_3_avg = sum(r.score for r in search_results[:3]) / min(
            3, len(search_results)
        )

        result_count_score = min(
            len(search_results) / 5.0, 1.0
        )  # Normalize to 5 results

        confidence = 0.4 * top_score + 0.3 * top_3_avg + 0.3 * result_count_score

        return min(confidence, 1.0)

    def _detect_knowledge_gap(
        self, query: str, search_results: List[SearchResult]
    ) -> Optional[str]:
        """
        Detect if the query asks about topics not in our knowledge base.

        Args:
            query: User query
            search_results: Retrieved search results

        Returns:
            Warning message if knowledge gap detected, None otherwise
        """
        query_lower = query.lower()

        # List of countries/citizenships we DON'T have data for
        unsupported_countries = [
            "china",
            "chinese",
            "brazil",
            "brazilian",
            "russia",
            "russian",
            "australia",
            "australian",
            "canada",
            "canadian",
            "france",
            "french",
            "germany",
            "german",
            "italy",
            "italian",
            "spain",
            "spanish",
            "mexico",
            "mexican",
            "argentina",
            "south korea",
            "korean",
            "thailand",
            "saudi",
            "egypt",
            "turkish",
            "indonesia",
        ]

        # Check if query mentions unsupported countries
        mentioned_unsupported = [
            country for country in unsupported_countries if country in query_lower
        ]

        if mentioned_unsupported:
            # Check if results are about India (indicating a mismatch)
            top_result = search_results[0]
            if hasattr(top_result.document, "source_country"):
                source_country = top_result.document.source_country or ""
                if "india" in source_country.lower():
                    country_name = mentioned_unsupported[0].title()
                    return f"""I apologize, but my knowledge base currently focuses on travel information for Indian citizens and travel to India. I don't have specific information about {country_name} citizens or {country_name}-specific visa requirements.

My expertise covers:
- Visa requirements for Indian citizens traveling abroad
- Entry requirements for foreign nationals coming to India
- General travel information for destinations popular with Indian travelers

For {country_name}-specific visa and travel requirements, I recommend:
1. Contacting the relevant embassy or consulate
2. Visiting official government immigration websites
3. Consulting with authorized visa service providers

Is there anything about Indian travel requirements I can help you with instead?"""

        return None

    async def process_query_stream(
        self, query: TravelQuery, chat_history: Optional[List[Dict[str, str]]] = None
    ):
        """
        Process query with streaming response.

        Args:
            query: Travel query object
            chat_history: Optional chat history

        Yields:
            Response chunks
        """
        request_id = generate_request_id()

        try:
            logger.info(
                f"Processing streaming RAG query: {query.query[:100]}...",
                extra={"request_id": request_id},
            )

            # Retrieve documents
            search_results = self.search.hybrid_search(query=query)

            if not search_results:
                yield "I couldn't find specific information about your query. Could you rephrase?"
                return

            # Format context
            context = self.llm.format_context(search_results)

            # Stream response
            for chunk in self.llm.generate_response_stream(
                query=query.query, context=context, chat_history=chat_history
            ):
                yield chunk

        except Exception as e:
            logger.error(f"Streaming RAG failed: {e}", exc_info=True)
            yield f"Error processing query: {str(e)}"

    def validate_query(self, query: str) -> Dict[str, Any]:
        """
        Validate and analyze query.

        Args:
            query: Query string

        Returns:
            Validation results
        """
        issues = []
        suggestions = []

        # Check length
        if len(query) < 10:
            issues.append("Query is too short")
            suggestions.append(
                "Please provide more details about what you'd like to know"
            )

        if len(query) > 500:
            issues.append("Query is very long")
            suggestions.append("Try to make your query more concise")

        # Check for common issues
        if query.lower().strip() in ["hi", "hello", "hey", "help"]:
            suggestions.append(
                "Ask a specific question about travel, visas, local laws, or cultural information"
            )

        is_valid = len(issues) == 0

        return {
            "valid": is_valid,
            "issues": issues,
            "suggestions": suggestions,
            "length": len(query),
        }
