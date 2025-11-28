"""LLM service for Google Gemini chat completion."""

import logging
from typing import List, Optional, Dict, Any, Generator
import time

import google.generativeai as genai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from ..config.settings import settings
from ..core.exceptions import LLMError
from ..core.utils import generate_request_id
from ..models.domain import SearchResult

logger = logging.getLogger(__name__)


# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)


class LLMService:
    """Service for LLM operations using Google Gemini."""

    TRAVEL_ASSISTANT_PROMPT = """You are an expert travel assistant with deep knowledge of:
- Visa requirements and immigration policies worldwide
- Local laws, customs, and regulations
- Cultural etiquette and social norms
- Safety guidelines and travel advisories
- Currency, transportation, and accommodation
- Health and insurance requirements
- Language tips and communication
- Food, dining customs, and restrictions
- Emergency contacts and procedures

Your role is to:
1. Provide accurate, up-to-date travel information based on the context provided
2. Be helpful, friendly, and culturally sensitive
3. Cite specific sources when providing information
4. Warn travelers about important legal or safety considerations
5. Offer practical, actionable advice
6. Ask clarifying questions when the query is ambiguous

Always base your answers on the provided context. If the context doesn't contain relevant information, acknowledge this and provide general guidance while noting that specific details should be verified."""

    def __init__(self):
        """Initialize LLM service."""
        # Remove 'models/' prefix if present, as genai.GenerativeModel adds it automatically
        model_name = settings.gemini_model
        if model_name.startswith("models/"):
            model_name = model_name.replace("models/", "", 1)
        self.model_name = model_name

        # Initialize Gemini model
        try:
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config={
                    "temperature": settings.llm_temperature,
                    "top_p": settings.llm_top_p,
                    "top_k": settings.llm_top_k,
                    "max_output_tokens": settings.llm_max_tokens,
                },
            )

            logger.info(
                f"LLM service initialized with model: {self.model_name}",
                extra={
                    "model": self.model_name,
                    "temperature": settings.llm_temperature,
                    "max_tokens": settings.llm_max_tokens,
                },
            )

        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}", exc_info=True)
            raise LLMError(f"Failed to initialize Gemini model: {str(e)}")

    def format_context(self, search_results: List[SearchResult]) -> str:
        """
        Format search results into context for the LLM.

        Args:
            search_results: List of search results to format

        Returns:
            Formatted context string
        """
        if not search_results:
            return "No specific context available."

        context_parts = ["# Relevant Travel Information\n"]

        for i, result in enumerate(search_results, 1):
            doc = result.document
            context_parts.append(f"\n## Source {i}: {doc.title}")

            # Add metadata
            metadata = []
            if doc.country:
                metadata.append(f"Country: {doc.country}")
            if doc.category:
                metadata.append(
                    f"Category: {doc.category.value if hasattr(doc.category, 'value') else doc.category}"
                )
            if doc.last_updated:
                metadata.append(f"Last Updated: {doc.last_updated}")

            if metadata:
                context_parts.append(f"*{' | '.join(metadata)}*")

            # Add content
            context_parts.append(f"\n{doc.content}\n")

            # Add relevance score
            context_parts.append(f"*Relevance Score: {result.score:.3f}*\n")

        return "\n".join(context_parts)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((LLMError, Exception)),
        reraise=True,
    )
    def generate_response(
        self,
        query: str,
        context: str,
        system_prompt: Optional[str] = None,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Generate response using Gemini LLM.

        Args:
            query: User query
            context: Context from search results
            system_prompt: Optional custom system prompt
            chat_history: Optional chat history for context

        Returns:
            Generated response text
        """
        request_id = generate_request_id()

        try:
            logger.info(
                f"Generating LLM response for query: {query[:100]}...",
                extra={
                    "query_length": len(query),
                    "context_length": len(context),
                    "has_history": bool(chat_history),
                    "request_id": request_id,
                },
            )

            start_time = time.time()

            # Build prompt
            prompt_parts = []

            # Add system prompt
            system = system_prompt or self.TRAVEL_ASSISTANT_PROMPT
            prompt_parts.append(f"System: {system}\n")

            # Add chat history if provided
            if chat_history:
                prompt_parts.append("\n# Previous Conversation:")
                for msg in chat_history[-5:]:  # Last 5 messages
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    prompt_parts.append(f"{role.capitalize()}: {content}")
                prompt_parts.append("")

            # Add context
            prompt_parts.append(context)

            # Add user query
            prompt_parts.append(f"\n# User Question:\n{query}")

            # Add instructions
            prompt_parts.append("\n# Instructions:")
            prompt_parts.append(
                "- Answer the question based on the context provided above"
            )
            prompt_parts.append("- Cite specific sources when referencing information")
            prompt_parts.append("- Be accurate, helpful, and concise")
            prompt_parts.append(
                "- If the context doesn't contain the answer, say so clearly"
            )

            prompt = "\n".join(prompt_parts)

            logger.debug(
                "Sending request to Gemini...",
                extra={"prompt_length": len(prompt), "request_id": request_id},
            )

            # Generate response
            response = self.model.generate_content(prompt)

            if not response or not response.text:
                raise LLMError("Empty response from Gemini")

            duration = time.time() - start_time

            logger.info(
                f"LLM response generated successfully",
                extra={
                    "response_length": len(response.text),
                    "duration_seconds": round(duration, 2),
                    "request_id": request_id,
                },
            )

            return response.text

        except Exception as e:
            logger.error(
                f"LLM generation failed: {e}",
                exc_info=True,
                extra={"request_id": request_id},
            )
            raise LLMError(
                f"Failed to generate response: {str(e)}", details={"query": query[:100]}
            )

    def generate_response_stream(
        self,
        query: str,
        context: str,
        system_prompt: Optional[str] = None,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> Generator[str, None, None]:
        """
        Generate streaming response using Gemini LLM.

        Args:
            query: User query
            context: Context from search results
            system_prompt: Optional custom system prompt
            chat_history: Optional chat history

        Yields:
            Response text chunks
        """
        request_id = generate_request_id()

        try:
            logger.info(
                f"Generating streaming LLM response: {query[:100]}...",
                extra={"request_id": request_id},
            )

            # Build prompt (same as generate_response)
            prompt_parts = []
            system = system_prompt or self.TRAVEL_ASSISTANT_PROMPT
            prompt_parts.append(f"System: {system}\n")

            if chat_history:
                prompt_parts.append("\n# Previous Conversation:")
                for msg in chat_history[-5:]:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    prompt_parts.append(f"{role.capitalize()}: {content}")
                prompt_parts.append("")

            prompt_parts.append(context)
            prompt_parts.append(f"\n# User Question:\n{query}")
            prompt_parts.append("\n# Instructions:")
            prompt_parts.append("- Answer based on the context provided")
            prompt_parts.append("- Cite sources when referencing information")
            prompt_parts.append("- Be accurate, helpful, and concise")

            prompt = "\n".join(prompt_parts)

            # Generate streaming response
            response_stream = self.model.generate_content(prompt, stream=True)

            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text

            logger.info(
                "Streaming response completed", extra={"request_id": request_id}
            )

        except Exception as e:
            logger.error(
                f"Streaming generation failed: {e}",
                exc_info=True,
                extra={"request_id": request_id},
            )
            raise LLMError(f"Failed to generate streaming response: {str(e)}")

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        try:
            result = self.model.count_tokens(text)
            return result.total_tokens
        except Exception as e:
            logger.warning(f"Token counting failed: {e}")
            # Rough estimation: ~4 chars per token
            return len(text) // 4

    def check_safety(self, text: str) -> Dict[str, Any]:
        """
        Check content safety ratings.

        Args:
            text: Text to check

        Returns:
            Safety ratings dictionary
        """
        try:
            response = self.model.generate_content(text)

            if hasattr(response, "prompt_feedback"):
                return {
                    "blocked": response.prompt_feedback.block_reason
                    if hasattr(response.prompt_feedback, "block_reason")
                    else None,
                    "safety_ratings": response.prompt_feedback.safety_ratings
                    if hasattr(response.prompt_feedback, "safety_ratings")
                    else [],
                }

            return {"blocked": None, "safety_ratings": []}

        except Exception as e:
            logger.warning(f"Safety check failed: {e}")
            return {"blocked": None, "safety_ratings": [], "error": str(e)}
