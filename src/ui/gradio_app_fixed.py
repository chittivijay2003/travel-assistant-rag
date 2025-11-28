"""Fixed Gradio UI for Travel Assistant with Submit Button and Proper Styling"""

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


def chat_with_assistant(
    message: str, history: List[List[str]]
) -> Tuple[List[List[str]], str]:
    """Process a chat message and update history."""
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


def clear_chat():
    """Clear the chat history."""
    return []


# Create the Gradio interface
with gr.Blocks(
    title="🌍 Travel Assistant AI",
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        max-width: 1200px !important;
        margin: 0 auto;
    }
    .header-style {
        text-align: center; 
        padding: 30px; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border-radius: 15px; 
        margin-bottom: 20px; 
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .chat-container {
        border-radius: 10px;
        border: 2px solid #e0e7ff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .input-container {
        background: #f8f9ff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #c7d2fe;
    }
    """,
) as demo:
    # Header with styling
    gr.HTML("""
    <div class="header-style">
        <h1 style="font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🌍 Travel Assistant AI</h1>
        <p style="font-size: 1.2em; margin: 0; opacity: 0.9;">Your intelligent companion for travel planning and information</p>
        <p style="font-size: 0.9em; margin: 10px 0 0 0; opacity: 0.8;">Powered by Google Gemini 2.0 Flash • Qdrant Vector DB • LangGraph Agents</p>
    </div>
    """)

    # Main content area
    with gr.Row():
        with gr.Column(scale=1):
            # Chatbot component
            chatbot = gr.Chatbot(
                value=[],
                height=500,
                show_label=False,
                container=True,
                elem_classes=["chat-container"],
                show_copy_button=True,
            )

            # Input area with submit button
            with gr.Row(elem_classes=["input-container"]):
                with gr.Column(scale=5):
                    msg = gr.Textbox(
                        placeholder="💬 Ask me about travel requirements, visa info, cultural customs, or safety guidelines...",
                        show_label=False,
                        lines=2,
                        max_lines=5,
                        container=False,
                    )
                with gr.Column(scale=1, min_width=120):
                    submit_btn = gr.Button(
                        "🚀 Send", variant="primary", size="lg", scale=1
                    )

            # Action buttons
            with gr.Row():
                clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary", size="sm")

            # Quick access info
            gr.HTML("""
            <div style="background: #f0f9ff; padding: 15px; border-radius: 10px; margin-top: 15px; border-left: 4px solid #0ea5e9;">
                <h4 style="margin: 0 0 10px 0; color: #0c4a6e;">💡 What you can ask:</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; font-size: 0.9em;">
                    <div>🛂 Visa requirements & documents</div>
                    <div>🌍 Cultural customs & etiquette</div>
                    <div>⚖️ Local laws & regulations</div>
                    <div>🛡️ Safety guidelines & advisories</div>
                </div>
            </div>
            """)

    # Example queries in a collapsible section
    with gr.Accordion("📝 Example Questions", open=False):
        gr.Examples(
            examples=[
                "What are the visa requirements for Indians traveling to Japan?",
                "What cultural customs should I know before visiting UAE?",
                "What items are prohibited when traveling to USA?",
                "Is it safe to travel to France right now?",
                "Tell me about Schengen visa requirements",
                "What documents do I need for a tourist visa to UK?",
                "Are there any dress code requirements in religious places in India?",
            ],
            inputs=msg,
            label="Click any example to try it:",
        )

    # Event handlers
    submit_btn.click(
        fn=chat_with_assistant, inputs=[msg, chatbot], outputs=[chatbot, msg]
    )

    msg.submit(fn=chat_with_assistant, inputs=[msg, chatbot], outputs=[chatbot, msg])

    clear_btn.click(fn=clear_chat, inputs=[], outputs=[chatbot])


def launch_ui(server_port: int = 7860, share: bool = False):
    """Launch the Gradio UI."""
    logger.info(f"Launching Travel Assistant UI on port {server_port}...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=server_port,
        share=share,
        show_error=True,
        show_tips=False,
    )


if __name__ == "__main__":
    launch_ui()
