"""Simple Gradio UI compatible with version 6.0.1"""

import logging
import gradio as gr
from typing import List, Tuple, Optional
from ..agents.graph import TravelAssistantGraph
from ..core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize agent
logger.info("Initializing Travel Assistant Agent for Gradio UI...")


class TravelUI:
    def __init__(self):
        self.agent = None
        self._initialize_agent()

    def _initialize_agent(self):
        try:
            self.agent = TravelAssistantGraph()
            logger.info("Agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            self.agent = None

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
            # Handle agent initialization error
            if self.agent is None:
                error_msg = "❌ Agent not initialized. Please restart the application."
                history.append([message, error_msg])
                return history, ""

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
                history.append([message, response])
                return history, ""

            # Check for simple responses
            if message_lower.strip() in ["thanks", "thank you"]:
                response = "You're welcome! 😊 Safe travels!"
                history.append([message, response])
                return history, ""

            if message_lower.strip() in ["bye", "goodbye"]:
                response = "Goodbye! Have a wonderful trip! ✈️"
                history.append([message, response])
                return history, ""

            # Prepare chat history for agent
            agent_messages = []
            for chat_pair in history:
                if isinstance(chat_pair, (list, tuple)) and len(chat_pair) >= 2:
                    agent_messages.append(
                        {"role": "user", "content": str(chat_pair[0])}
                    )
                    agent_messages.append(
                        {"role": "assistant", "content": str(chat_pair[1])}
                    )

            # Get response from agent
            logger.info(f"Processing query: {message[:50]}...")

            response_data = self.agent.invoke(
                query=message,
                country=None,
                category=None,
                max_results=5,
                messages=agent_messages,
            )

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

            # Add to history
            history.append([message, formatted_response])
            logger.info("Response generated successfully")

            return history, ""

        except Exception as e:
            logger.error(f"Error in chat processing: {e}", exc_info=True)
            error_msg = f"❌ Sorry, I encountered an error: {str(e)}\n\nPlease try again with a different question."
            history.append([message, error_msg])
            return history, ""


# Create UI instance
travel_ui = TravelUI()


def chat_wrapper(message, history):
    """Wrapper function for Gradio"""
    return travel_ui.process_message(message, history)


# Create a simple Gradio interface compatible with 6.0.1
def create_demo():
    """Create Gradio demo interface"""

    # Main interface
    with gr.Blocks() as demo:
        # Header
        gr.HTML("""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 28px;">🌍 Travel Assistant AI</h1>
                <p style="margin: 10px 0 0 0; font-size: 16px;">Your intelligent guide for travel requirements, visas, customs, and safety</p>
            </div>
        """)

        # Chat interface
        chatbot = gr.Chatbot(label="Chat with Travel Assistant", height=400)

        with gr.Row():
            msg_box = gr.Textbox(
                placeholder="Ask me about visa requirements, customs, local laws, or travel safety...",
                label="Your Question",
                lines=2,
            )
            send_btn = gr.Button("Send", variant="primary")

        with gr.Row():
            clear_btn = gr.Button("Clear Chat", variant="secondary")

        # Quick suggestions
        gr.HTML(
            "<h3 style='color: #667eea; margin-top: 20px;'>✨ Quick Questions:</h3>"
        )

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

        # Suggestion button events
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

    return demo


# Create the demo
demo = create_demo()


def launch_ui(server_port: int = 7860, share: bool = False):
    """Launch the Gradio UI"""
    logger.info(f"Launching Travel Assistant UI on port {server_port}")
    demo.launch(
        server_name="0.0.0.0",
        server_port=server_port,
        share=share,
        show_error=True,
    )


if __name__ == "__main__":
    launch_ui()
