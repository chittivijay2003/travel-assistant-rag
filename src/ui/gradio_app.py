"""Working Gradio UI for Travel Assistant with robust error handling"""

import logging
import requests
import gradio as gr
from typing import List, Tuple, Optional, Dict, Any
from ..core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize agent
logger.info("Initializing Travel Assistant UI to use API backend...")


class TravelUI:
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self._check_api_health()

    def _check_api_health(self):
        """Check if the API is healthy and accessible"""
        try:
            response = requests.get(f"{self.api_base_url}/api/v1/health", timeout=5)
            if response.status_code == 200:
                logger.info("API backend is healthy and accessible")
            else:
                logger.warning(
                    f"API backend returned status code: {response.status_code}"
                )
        except Exception as e:
            logger.error(f"Failed to connect to API backend: {e}")

    def _call_api(self, query: str) -> Dict[str, Any]:
        """Make API call to the RAG endpoint"""
        try:
            payload = {"query": query, "max_results": 5}
            response = requests.post(
                f"{self.api_base_url}/api/v1/rag-travel", json=payload, timeout=30
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    f"API call failed with status {response.status_code}: {response.text}"
                )
                return {
                    "query": query,
                    "answer": f"API error: {response.status_code}",
                    "sources": [],
                    "confidence_score": 0.0,
                }
        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            return {
                "query": query,
                "answer": "Request timed out. Please try again.",
                "sources": [],
                "confidence_score": 0.0,
            }
        except Exception as e:
            logger.error(f"API call failed: {e}")
            return {
                "query": query,
                "answer": f"Failed to connect to backend service: {str(e)}",
                "sources": [],
                "confidence_score": 0.0,
            }

    def process_message(
        self, message: str, history: Optional[List[List[str]]] = None
    ) -> Tuple[List[List[str]], str]:
        """Process user message and return updated history"""

        if not message or not message.strip():
            return history or [], ""

        # Initialize history if None
        if history is None:
            history = []

        try:
            # Simple keyword-based routing for better reliability
            message_lower = message.lower()

            # Check for greetings
            greetings = ["hi", "hello", "hey"]
            if any(greet in message_lower for greet in greetings):
                response = """Hello! 👋 I'm your Travel Assistant AI. 

I can help you with:
🛂 Visa requirements and immigration
🏛️ Local laws and regulations  
🌍 Cultural etiquette and customs
🛡️ Safety guidelines and travel advisories

What would you like to know about your travel destination?"""
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": response})
                return history, ""

            # Check for simple responses
            if message_lower.strip() in ["thanks", "thank you"]:
                response = "You're welcome! 😊 Safe travels!"
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": response})
                return history, ""

            if message_lower.strip() in ["bye", "goodbye"]:
                response = "Goodbye! Have a wonderful trip! ✈️"
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": response})
                return history, ""

            # Get response from API
            logger.info(f"Processing query via API: {message[:50]}...")

            response_data = self._call_api(message)

            # Extract response
            answer = response_data.get("answer", "I couldn't process your request.")
            sources = response_data.get("sources", [])

            # Format response with sources
            formatted_response = str(answer)

            if sources and len(sources) > 0:
                formatted_response += "\n\n**📚 Sources Used:**"
                for i, source in enumerate(sources[:3], 1):
                    title = source.get("title", "Travel Document")
                    country = source.get("country", "")
                    if country:
                        formatted_response += f"\n{i}. {title} ({country})"
                    else:
                        formatted_response += f"\n{i}. {title}"

            # Add to history in Gradio 6.0.1 format
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": formatted_response})
            logger.info("Response generated successfully")

            return history, ""

        except Exception as e:
            logger.error(f"Error in chat processing: {e}", exc_info=True)
            error_msg = f"❌ Sorry, I encountered an error: {str(e)}\n\nPlease try again with a different question."
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": error_msg})
            return history, ""


# Create UI instance
travel_ui = TravelUI()


def chat_wrapper(message, history):
    """Wrapper function for Gradio"""
    return travel_ui.process_message(message, history)


def suggestion_handler(suggestion_text):
    """Handle suggestion button clicks"""
    return suggestion_text


# Create Gradio interface - Simple version without themes for compatibility
with gr.Blocks(title="🌍 Travel Assistant AI") as demo:
    # Header
    gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #667eea; margin-bottom: 10px;">🌍 Travel Assistant AI</h1>
            <p style="color: #666; font-size: 16px;">Your intelligent guide for travel requirements, visas, customs, and safety</p>
        </div>
    """)

    # Chat interface
    with gr.Row():
        with gr.Column(scale=1):
            chatbot = gr.Chatbot(height=500, show_label=False)

            with gr.Row():
                with gr.Column(scale=8):
                    msg_box = gr.Textbox(
                        placeholder="Ask me about visa requirements, customs, local laws, or travel safety...",
                        show_label=False,
                    )
                with gr.Column(scale=1):
                    send_btn = gr.Button("Send", variant="primary")

            with gr.Row():
                clear_btn = gr.Button("Clear Chat", variant="secondary")

    # Quick suggestions
    gr.HTML("<h3 style='margin-top: 20px; color: #667eea;'>✨ Quick Questions:</h3>")

    with gr.Row():
        visa_btn = gr.Button("🛂 Japan Visa Requirements")
        customs_btn = gr.Button("🕌 UAE Cultural Customs")
        safety_btn = gr.Button("🛡️ France Travel Safety")

    with gr.Row():
        law_btn = gr.Button("⚖️ UK Immigration Laws")
        health_btn = gr.Button("🏥 USA Health Requirements")
        general_btn = gr.Button("🌏 General Travel Tips")

    # Event handlers
    send_btn.click(
        fn=chat_wrapper, inputs=[msg_box, chatbot], outputs=[chatbot, msg_box]
    )

    msg_box.submit(
        fn=chat_wrapper, inputs=[msg_box, chatbot], outputs=[chatbot, msg_box]
    )

    clear_btn.click(fn=lambda: ([], ""), inputs=None, outputs=[chatbot, msg_box])

    # Suggestion button events - simplified for compatibility
    visa_btn.click(
        fn=lambda: "What are the visa requirements for Indian citizens traveling to Japan?",
        inputs=None,
        outputs=msg_box,
    )

    customs_btn.click(
        fn=lambda: "What cultural customs and etiquette should I know when visiting UAE?",
        inputs=None,
        outputs=msg_box,
    )

    safety_btn.click(
        fn=lambda: "Is France safe to travel to? Any safety guidelines I should know?",
        inputs=None,
        outputs=msg_box,
    )

    law_btn.click(
        fn=lambda: "What are the immigration laws and requirements for visiting UK?",
        inputs=None,
        outputs=msg_box,
    )

    health_btn.click(
        fn=lambda: "What health requirements and vaccinations are needed for USA travel?",
        inputs=None,
        outputs=msg_box,
    )

    general_btn.click(
        fn=lambda: "Give me general travel tips and advice for international travel.",
        inputs=None,
        outputs=msg_box,
    )


def launch_ui(server_port: int = 7860, share: bool = False):
    """Launch the Gradio UI"""
    logger.info(f"Launching Travel Assistant UI on port {server_port}")
    demo.launch(
        server_name="0.0.0.0", server_port=server_port, share=share, show_error=True
    )


if __name__ == "__main__":
    launch_ui()
