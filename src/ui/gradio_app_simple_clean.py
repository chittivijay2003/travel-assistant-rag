"""Clean and Simple Gradio UI for Travel Assistant"""

import logging
import gradio as gr
from typing import List, Tuple

from ..agents.graph import TravelAssistantGraph
from ..core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize agent
logger.info("Initializing Travel Assistant Agent for Gradio UI...")
agent = TravelAssistantGraph()
logger.info("Agent initialized successfully")


def chat_function(
    message: str, history: List[List[str]]
) -> Tuple[List[List[str]], str]:
    """Process a chat message and return updated history."""
    if not message.strip():
        return history, ""

    try:
        logger.info(f"Processing message: {message[:100]}...")

        # Convert history to messages format
        messages = []
        for chat_pair in history:
            if len(chat_pair) >= 2:
                user_msg, bot_msg = chat_pair[0], chat_pair[1]
                messages.append({"role": "user", "content": user_msg})
                if bot_msg:
                    messages.append({"role": "assistant", "content": bot_msg})

        # Process through agent
        response = agent.invoke(
            query=message,
            country=None,
            category=None,
            max_results=5,
            messages=messages,
        )

        # Extract answer
        answer = response.get(
            "answer", "I apologize, but I couldn't generate a response."
        )
        sources = response.get("sources", [])
        confidence = response.get("confidence_score", 0.0)

        # Format response with sources
        formatted_response = f"{answer}\n\n"

        if sources:
            formatted_response += "**📚 Sources:**\n"
            for i, source in enumerate(sources[:3], 1):
                title = source.get("title", "Unknown Document")
                score = source.get("score", 0) * 100
                formatted_response += f"{i}. {title} (Confidence: {score:.1f}%)\n"

        formatted_response += f"\n*Response confidence: {confidence:.1%}*"

        # Update history
        history.append([message, formatted_response])

        logger.info("Message processed successfully")
        return history, ""

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        error_msg = f"❌ Error: {str(e)}\n\nPlease try again or rephrase your question."
        history.append([message, error_msg])
        return history, ""


def clear_history():
    """Clear the chat history."""
    return []


# Create simple Gradio interface
demo = gr.Blocks(title="🌍 Travel Assistant AI")

with demo:
    # Header
    gr.HTML("""
    <div style="text-align: center; padding: 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; margin-bottom: 20px; color: white;">
        <h1 style="font-size: 2.2em; margin: 0 0 8px 0;">🌍 Travel Assistant AI</h1>
        <p style="font-size: 1.1em; margin: 0; opacity: 0.9;">Your intelligent companion for travel planning</p>
        <p style="font-size: 0.85em; margin: 8px 0 0 0; opacity: 0.8;">Powered by Google Gemini • Qdrant • LangGraph</p>
    </div>
    """)

    # Chat interface
    chatbot = gr.Chatbot(height=450, show_label=False)

    # Input row
    with gr.Row():
        msg_input = gr.Textbox(
            placeholder="Ask me about travel requirements, visa info, cultural customs, or safety guidelines...",
            show_label=False,
            lines=2,
            scale=5,
        )
        send_btn = gr.Button("Send 🚀", variant="primary", scale=1)

    # Clear button
    clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary", size="sm")

    # Info box
    gr.HTML("""
    <div style="background: #f0f9ff; padding: 12px; border-radius: 8px; margin-top: 15px; border-left: 3px solid #0ea5e9;">
        <strong>💡 What you can ask:</strong><br>
        🛂 Visa requirements • 🌍 Cultural customs • ⚖️ Local laws • 🛡️ Safety guidelines
    </div>
    """)

    # Examples
    gr.Examples(
        examples=[
            "What are the visa requirements for Indians traveling to Japan?",
            "What cultural customs should I know before visiting UAE?",
            "What items are prohibited when traveling to USA?",
            "Is it safe to travel to France right now?",
            "Tell me about Schengen visa requirements",
        ],
        inputs=msg_input,
    )

    # Event handlers
    send_btn.click(
        fn=chat_function, inputs=[msg_input, chatbot], outputs=[chatbot, msg_input]
    )

    msg_input.submit(
        fn=chat_function, inputs=[msg_input, chatbot], outputs=[chatbot, msg_input]
    )

    clear_btn.click(fn=clear_history, outputs=[chatbot])


def launch_ui(server_port: int = 7860, share: bool = False):
    """Launch the Gradio UI."""
    logger.info(f"Launching Travel Assistant UI on port {server_port}...")
    demo.launch(
        server_name="0.0.0.0", server_port=server_port, share=share, show_error=True
    )


if __name__ == "__main__":
    launch_ui()
