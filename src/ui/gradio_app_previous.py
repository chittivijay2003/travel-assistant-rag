"""Working Gradio UI for Travel Assistant"""

import logging
import gradio as gr
from ..agents.graph import TravelAssistantGraph
from ..core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize agent
logger.info("Initializing Travel Assistant Agent for Gradio UI...")
agent = TravelAssistantGraph()
logger.info("Agent initialized successfully")


def chat(message, history):
    if not message.strip():
        return history, ""

    try:
        # Convert history format for agent
        messages = []
        if history:
            for pair in history:
                if isinstance(pair, (list, tuple)) and len(pair) >= 2:
                    messages.append({"role": "user", "content": str(pair[0])})
                    messages.append({"role": "assistant", "content": str(pair[1])})

        # Get response from agent
        response = agent.invoke(
            query=message,
            country=None,
            category=None,
            max_results=5,
            messages=messages,
        )

        # Format response
        answer = response.get("answer", "I couldn't process your request.")
        sources = response.get("sources", [])

        formatted_answer = answer
        if sources:
            formatted_answer += "\n\n**📚 Sources:**\n"
            for i, source in enumerate(sources[:3], 1):
                title = source.get("title", "Unknown")
                formatted_answer += f"{i}. {title}\n"

        # Add to history
        if history is None:
            history = []
        history.append([message, formatted_answer])

        return history, ""

    except Exception as e:
        logger.error(f"Chat error: {e}")
        if history is None:
            history = []
        history.append([message, "❌ Error processing request. Please try again."])
        return history, ""


# Create Gradio app
with gr.Blocks(title="🌍 Travel Assistant") as demo:
    gr.HTML(
        "<h1 style='text-align: center; color: #667eea;'>🌍 Travel Assistant AI</h1>"
    )

    chatbot = gr.Chatbot(height=400)

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Ask about travel requirements, visas, customs...",
            scale=4,
            show_label=False,
        )
        send = gr.Button("Send", variant="primary", scale=1)

    clear = gr.Button("Clear", variant="secondary", size="sm")

    # Suggestion buttons
    gr.HTML("<h3>✨ Try these:</h3>")
    with gr.Row():
        btn1 = gr.Button("🛂 Japan Visa", size="sm")
        btn2 = gr.Button("🕌 UAE Customs", size="sm")
        btn3 = gr.Button("🛡️ France Safety", size="sm")

    # Event handlers
    send.click(chat, [msg, chatbot], [chatbot, msg])
    msg.submit(chat, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: [], outputs=chatbot)

    btn1.click(lambda: "What are visa requirements for Japan from India?", outputs=msg)
    btn2.click(lambda: "What customs should I know for UAE?", outputs=msg)
    btn3.click(lambda: "Is France safe to travel?", outputs=msg)


def launch_ui(server_port: int = 7860, share: bool = False):
    logger.info(f"Launching UI on port {server_port}")
    demo.launch(server_name="0.0.0.0", server_port=server_port, share=share)


if __name__ == "__main__":
    launch_ui()
