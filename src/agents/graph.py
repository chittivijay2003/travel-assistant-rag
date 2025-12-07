"""LangGraph workflow for travel assistant agent."""

import logging
from typing import Dict, Any
from langgraph.graph import StateGraph, END

from .state import AgentState
from .nodes import TravelAgentNodes
from ..services.rag_service import RAGService
from ..core.utils import generate_request_id

logger = logging.getLogger(__name__)


class TravelAssistantGraph:
    """LangGraph workflow for travel assistant."""

    def __init__(self, rag_service: RAGService = None):
        """
        Initialize travel assistant graph.

        Args:
            rag_service: RAG service instance
        """
        self.rag_service = rag_service or RAGService()
        self.nodes = TravelAgentNodes(self.rag_service)

        # Build graph
        self.graph = self._build_graph()
        self.app = self.graph.compile()

        logger.info("Travel assistant graph initialized")

    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow.

        Returns:
            Compiled graph
        """
        logger.debug("Building LangGraph workflow...")

        # Create graph
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("classify_intent", self.nodes.classify_intent)
        workflow.add_node("rag", self.nodes.rag_node)
        workflow.add_node("general_chat", self.nodes.general_chat_node)

        # Set entry point
        workflow.set_entry_point("classify_intent")

        # Add conditional edges from classifier
        workflow.add_conditional_edges(
            "classify_intent",
            self.nodes.router,
            {"rag": "rag", "general_chat": "general_chat"},
        )

        # Add edges to END
        workflow.add_edge("rag", END)
        workflow.add_edge("general_chat", END)

        logger.debug("LangGraph workflow built successfully")

        return workflow

    def invoke(
        self,
        query: str,
        country: str = None,
        category: str = None,
        max_results: int = 5,
        messages: list = None,
    ) -> Dict[str, Any]:
        """
        Invoke the agent with a query.

        Args:
            query: User query
            country: Optional country filter
            category: Optional category filter
            max_results: Maximum search results
            messages: Optional chat history

        Returns:
            Agent response
        """
        request_id = generate_request_id()

        logger.info(
            f"Invoking agent with query: {query[:100]}...",
            extra={
                "query": query[:100],
                "country": country,
                "category": category,
                "request_id": request_id,
            },
        )

        # Initialize state
        initial_state: AgentState = {
            "query": query,
            "country": country,
            "category": category,
            "max_results": max_results,
            "messages": messages or [],
            "context": [],
            "intent": None,
            "answer": None,
            "confidence_score": 0.0,
            "processing_time": 0.0,
            "next_step": "classify_intent",
            "metadata": {},
            "request_id": request_id,
        }

        try:
            # Run graph
            logger.debug(
                "Running LangGraph workflow...", extra={"request_id": request_id}
            )

            final_state = self.app.invoke(initial_state)

            logger.info(
                "Agent invocation completed",
                extra={
                    "answer_length": len(final_state.get("answer", "")),
                    "confidence": final_state.get("confidence_score", 0.0),
                    "intent": final_state.get("intent"),
                    "request_id": request_id,
                },
            )

            return {
                "query": query,
                "answer": final_state.get("answer", "No response generated"),
                "sources": [
                    result.to_dict() for result in final_state.get("context", [])
                ],
                "retrieved_context": [
                    {
                        "id": result.document.id,
                        "text": result.document.content,
                        "score": result.score,
                    }
                    for result in final_state.get("context", [])
                ]
                if final_state.get("context")
                else [{"id": "none", "text": "", "score": 0.0}],
                "confidence_score": final_state.get("confidence_score", 0.0),
                "processing_time": final_state.get("processing_time", 0.0),
                "metadata": final_state.get("metadata", {}),
                "request_id": request_id,
            }

        except Exception as e:
            logger.error(
                f"Agent invocation failed: {e}",
                exc_info=True,
                extra={"request_id": request_id},
            )

            return {
                "query": query,
                "answer": f"Error processing query: {str(e)}",
                "sources": [],
                "retrieved_context": [{"id": "error", "text": "", "score": 0.0}],
                "confidence_score": 0.0,
                "processing_time": 0.0,
                "metadata": {"error": str(e)},
                "request_id": request_id,
            }

    async def astream(
        self,
        query: str,
        country: str = None,
        category: str = None,
        max_results: int = 5,
        messages: list = None,
    ):
        """
        Stream agent responses.

        Args:
            query: User query
            country: Optional country filter
            category: Optional category filter
            max_results: Maximum search results
            messages: Optional chat history

        Yields:
            State updates
        """
        request_id = generate_request_id()

        logger.info(
            f"Streaming agent response: {query[:100]}...",
            extra={"request_id": request_id},
        )

        # Initialize state
        initial_state: AgentState = {
            "query": query,
            "country": country,
            "category": category,
            "max_results": max_results,
            "messages": messages or [],
            "context": [],
            "intent": None,
            "answer": None,
            "confidence_score": 0.0,
            "processing_time": 0.0,
            "next_step": "classify_intent",
            "metadata": {},
            "request_id": request_id,
        }

        try:
            async for state in self.app.astream(initial_state):
                yield state

        except Exception as e:
            logger.error(f"Streaming failed: {e}", exc_info=True)
            yield {"error": str(e)}
