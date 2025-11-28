"""Simple Working Gradio UI for Travel Assistant"""

import logging
import gradio as gr
from typing import List

from ..agents.graph import TravelAssistantGraph
from ..core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize agent
logger.info("Initializing Travel Assistant Agent for Gradio UI...")
agent = TravelAssistantGraph()
logger.info("Agent initialized successfully")


def process_message(message: str, history: List[List[str]]) -> str:
    """Process a chat message using the travel assistant."""
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

        logger.info("Message processed successfully")
        return formatted_response

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        return f"❌ Error: {str(e)}\n\nPlease try again or rephrase your question."


# Create interface
with gr.Blocks(title="🌍 Travel Assistant AI") as demo:
    # Header
    gr.Markdown("""
    # 🌍 Travel Assistant AI
    
    Ask me anything about travel requirements, visa information, cultural customs, local laws, or safety guidelines!
    
    **Powered by:** Google Gemini 2.0 Flash • Qdrant Vector DB • LangGraph Agents
    """)

    # Chat interface
    chatbot = gr.Chatbot(
        height=500,
        placeholder="Ask me about travel requirements, visa info, cultural customs, or safety guidelines...",
    )

    msg = gr.Textbox(
        placeholder="Type your travel question here...",
        lines=1,
        max_lines=3,
        show_label=False,
    )

    # Examples
    gr.Examples(
        examples=[
            "What are the visa requirements for Indians traveling to Japan?",
            "What cultural customs should I know before visiting UAE?",
            "What items are prohibited when traveling to USA?",
            "Is it safe to travel to France right now?",
            "Tell me about Schengen visa requirements",
        ],
        inputs=msg,
    )

    # Clear button
    clear = gr.Button("🗑️ Clear Chat")

    # Event handlers
    msg.submit(process_message, [msg, chatbot], [chatbot], queue=False).then(
        lambda: gr.update(value=""), [], [msg]
    )

    clear.click(lambda: [], [], chatbot, queue=False)


def launch_ui(server_port: int = 7860, share: bool = False):
    """Launch the Gradio UI."""
    logger.info(f"Launching simple Gradio UI on port {server_port}...")
    demo.launch(
        server_name="0.0.0.0", server_port=server_port, share=share, show_error=True
    )


if __name__ == "__main__":
    launch_ui()
