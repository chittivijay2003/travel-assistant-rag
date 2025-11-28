"""LangGraph agent nodes for travel assistant."""

import logging
from typing import Dict, Any
import time

from .state import AgentState
from ..models.domain import TravelQuery, TravelCategory
from ..services.rag_service import RAGService
from ..core.utils import generate_request_id

logger = logging.getLogger(__name__)


class TravelAgentNodes:
    """Node functions for travel assistant agent."""

    def __init__(self, rag_service: RAGService):
        """
        Initialize agent nodes.

        Args:
            rag_service: RAG service instance
        """
        self.rag = rag_service
        logger.info("Travel agent nodes initialized")

    def classify_intent(self, state: AgentState) -> AgentState:
        """
        Classify user intent to route to appropriate node.

        Args:
            state: Current agent state

        Returns:
            Updated state with intent classification
        """
        request_id = state.get("request_id", generate_request_id())
        query = state["query"].lower()

        logger.info(
            f"Classifying intent for query: {query[:100]}...",
            extra={"request_id": request_id},
        )

        # Simple intent classification based on keywords
        intent = "general_chat"

        # Travel-specific keywords
        travel_keywords = [
            "visa",
            "passport",
            "immigration",
            "travel",
            "visit",
            "trip",
            "law",
            "legal",
            "regulation",
            "rule",
            "prohibited",
            "allowed",
            "culture",
            "custom",
            "etiquette",
            "tradition",
            "behavior",
            "safe",
            "danger",
            "crime",
            "emergency",
            "health",
            "flight",
            "hotel",
            "transport",
            "accommodation",
            "currency",
            "food",
            "restaurant",
            "eat",
            "drink",
            "cuisine",
        ]

        if any(keyword in query for keyword in travel_keywords):
            intent = "rag_query"

        # Update state
        state["intent"] = intent
        state["metadata"]["intent_classification"] = {
            "intent": intent,
            "confidence": 0.8,  # Simplified
        }

        logger.info(
            f"Intent classified as: {intent}",
            extra={"intent": intent, "request_id": request_id},
        )

        return state

    def rag_node(self, state: AgentState) -> AgentState:
        """
        Process query through RAG pipeline.

        Args:
            state: Current agent state

        Returns:
            Updated state with RAG response
        """
        request_id = state.get("request_id", generate_request_id())
        start_time = time.time()

        logger.info(
            f"Processing RAG query: {state['query'][:100]}...",
            extra={"request_id": request_id},
        )

        try:
            # Build travel query
            travel_query = TravelQuery(
                query=state["query"],
                country=state.get("country"),
                category=TravelCategory(state["category"])
                if state.get("category")
                else None,
                max_results=state.get("max_results", 5),
            )

            # Get chat history from messages
            chat_history = state.get("messages", [])

            # Process through RAG
            rag_response = self.rag.process_query(
                query=travel_query, chat_history=chat_history, include_sources=True
            )

            # Update state
            state["answer"] = rag_response.answer
            state["context"] = rag_response.sources
            state["confidence_score"] = rag_response.confidence_score
            state["processing_time"] = time.time() - start_time
            state["next_step"] = "end"

            # Update metadata
            state["metadata"].update(
                {
                    "retrieval_count": rag_response.retrieval_count,
                    "rag_processing_time": rag_response.processing_time,
                    "rag_metadata": rag_response.metadata,
                }
            )

            logger.info(
                "RAG query processed successfully",
                extra={
                    "answer_length": len(rag_response.answer),
                    "sources_count": len(rag_response.sources),
                    "confidence": rag_response.confidence_score,
                    "request_id": request_id,
                },
            )

        except Exception as e:
            logger.error(
                f"RAG node failed: {e}", exc_info=True, extra={"request_id": request_id}
            )

            state["answer"] = f"I encountered an error processing your query: {str(e)}"
            state["confidence_score"] = 0.0
            state["processing_time"] = time.time() - start_time
            state["next_step"] = "end"
            state["metadata"]["error"] = str(e)

        return state

    def general_chat_node(self, state: AgentState) -> AgentState:
        """
        Handle general chat (non-travel queries).

        Args:
            state: Current agent state

        Returns:
            Updated state with chat response
        """
        request_id = state.get("request_id", generate_request_id())

        logger.info(
            f"Processing general chat: {state['query'][:100]}...",
            extra={"request_id": request_id},
        )

        # Simple responses for common greetings
        query_lower = state["query"].lower().strip()

        responses = {
            "hi": "Hello! I'm your travel assistant. How can I help you with your travel plans?",
            "hello": "Hello! I'm here to help with travel information. What would you like to know?",
            "hey": "Hey there! Ask me anything about visa requirements, local laws, cultural tips, or travel safety.",
            "help": "I can help you with:\n- Visa requirements and immigration\n- Local laws and regulations\n- Cultural etiquette and customs\n- Safety guidelines\n- Travel tips and recommendations\n\nWhat would you like to know?",
            "thanks": "You're welcome! Safe travels!",
            "thank you": "You're welcome! Feel free to ask if you have more questions.",
            "bye": "Goodbye! Have a great trip!",
        }

        answer = responses.get(
            query_lower,
            "I'm a travel assistant specialized in visa requirements, local laws, cultural etiquette, and safety information. "
            "How can I help you with your travel plans?",
        )

        state["answer"] = answer
        state["confidence_score"] = 1.0
        state["next_step"] = "end"

        logger.info("General chat processed", extra={"request_id": request_id})

        return state

    def router(self, state: AgentState) -> str:
        """
        Route to appropriate node based on intent.

        Args:
            state: Current agent state

        Returns:
            Name of next node
        """
        intent = state.get("intent", "general_chat")

        logger.debug(
            f"Routing based on intent: {intent}",
            extra={"intent": intent, "request_id": state.get("request_id")},
        )

        if intent == "rag_query":
            return "rag"
        else:
            return "general_chat"
