"""Modern Clean Gradio UI for Travel Assistant - User Friendly Design."""

import logging
import gradio as gr
from typing import List, Tuple
import time

from ..agents.graph import TravelAssistantGraph
from ..core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize agent
logger.info("Initializing Travel Assistant Agent for Gradio UI...")
agent = TravelAssistantGraph()
logger.info("Agent initialized successfully")


def format_sources(sources: List[dict]) -> str:
    """Format sources with clean modern design."""
    if not sources:
        return """
        <div style='padding: 24px; background: #f0f9ff; border-radius: 10px; text-align: center; border: 2px solid #bae6fd;'>
            <div style='font-size: 40px; margin-bottom: 10px;'>📚</div>
            <h3 style='margin: 0; font-size: 18px; color: #0284c7; font-weight: 700;'>No Sources Found</h3>
            <p style='margin: 8px 0 0 0; color: #64748b; font-size: 13px;'>Try asking a travel-related question</p>
        </div>
        """

    html = """
    <div style='padding: 20px; background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%); border-radius: 12px; border: 2px solid #c7d2fe; box-shadow: 0 2px 12px rgba(102,126,234,0.1);'>
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid #a5b4fc;'>
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 8px; border-radius: 8px;'>
                <span style='font-size: 20px;'>📚</span>
            </div>
            <h3 style='margin: 0; font-size: 18px; font-weight: 700; color: #4c1d95;'>Knowledge Sources</h3>
        </div>
    """

    for i, source in enumerate(sources, 1):
        score = source.get("score", 0)

        # Clean color scheme
        if score > 0.8:
            border_color = "#10b981"
            badge_bg = "#10b981"
            icon_bg = "#d1fae5"
        elif score > 0.6:
            border_color = "#667eea"
            badge_bg = "#667eea"
            icon_bg = "#e0e7ff"
        else:
            border_color = "#8b5cf6"
            badge_bg = "#8b5cf6"
            icon_bg = "#ede9fe"

        reliability = source.get("reliability_score", 0)
        content_preview = source.get("content", "")[:150] + "..."

        html += f"""
        <div style='background: white; padding: 16px; margin: 12px 0; border-radius: 10px; border-left: 4px solid {border_color}; border: 2px solid #e0e7ff; box-shadow: 0 2px 8px rgba(102,126,234,0.08);'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                <div style='display: flex; align-items: center; gap: 8px; flex: 1;'>
                    <div style='background: {icon_bg}; padding: 4px 10px; border-radius: 6px; font-weight: 700; color: {border_color}; font-size: 12px;'>#{i}</div>
                    <h4 style='margin: 0; color: #1e293b; font-size: 15px; font-weight: 600;'>{source.get("title", "Unknown Document")}</h4>
                </div>
                <div style='background: {badge_bg}; color: white; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: 700; white-space: nowrap; margin-left: 10px;'>{score:.0%}</div>
            </div>
            <div style='background: #f8f9ff; padding: 10px; border-radius: 6px; margin: 10px 0; border-left: 3px solid {border_color};'>
                <p style='color: #475569; font-size: 13px; line-height: 1.5; margin: 0;'>{content_preview}</p>
            </div>
            <div style='display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px;'>
                <div style='display: flex; align-items: center; gap: 4px; padding: 4px 10px; background: #dbeafe; border-radius: 6px;'>
                    <span style='font-size: 12px;'>🏷️</span>
                    <span style='color: #0369a1; font-size: 11px; font-weight: 600;'>{source.get("category", "N/A").replace("_", " ").title()}</span>
                </div>
                <div style='display: flex; align-items: center; gap: 4px; padding: 4px 10px; background: #dcfce7; border-radius: 6px;'>
                    <span style='font-size: 12px;'>🌍</span>
                    <span style='color: #047857; font-size: 11px; font-weight: 600;'>{source.get("country", "Global")}</span>
                </div>
                <div style='display: flex; align-items: center; gap: 4px; padding: 4px 10px; background: #fef3c7; border-radius: 6px;'>
                    <span style='font-size: 12px;'>⭐</span>
                    <span style='color: #b45309; font-size: 11px; font-weight: 600;'>{reliability:.1f}/10</span>
                </div>
            </div>
        </div>
        """

    html += "</div>"
    return html


def format_metadata(metadata: dict, processing_time: float, confidence: float) -> str:
    """Format metadata with clean modern cards."""
    confidence_color = (
        "#10b981" if confidence > 0.8 else "#0ea5e9" if confidence > 0.6 else "#64748b"
    )
    intent = metadata.get("intent", "unknown")
    intent_emoji = "🔍" if intent == "rag_query" else "💬"
    sources_count = metadata.get("sources_count", 0)

    html = f"""
    <div style='background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%); padding: 16px; border-radius: 12px; border: 2px solid #c7d2fe; box-shadow: 0 2px 12px rgba(102,126,234,0.1);'>
        <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 2px solid #a5b4fc;'>
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 6px; border-radius: 6px;'>
                <span style='font-size: 16px;'>📊</span>
            </div>
            <h3 style='margin: 0; font-size: 16px; font-weight: 700; color: #4c1d95;'>Analytics</h3>
        </div>
        <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;'>
            <div style='background: white; padding: 12px; border-radius: 8px; text-align: center; border: 2px solid #e0e7ff; box-shadow: 0 1px 4px rgba(102,126,234,0.1);'>
                <div style='font-size: 24px; margin-bottom: 4px;'>⚡</div>
                <div style='font-size: 20px; font-weight: 700; margin-bottom: 2px; color: #667eea;'>{processing_time:.2f}s</div>
                <div style='font-size: 10px; color: #64748b; font-weight: 600; text-transform: uppercase;'>Time</div>
            </div>
            <div style='background: white; padding: 12px; border-radius: 8px; text-align: center; border: 2px solid #e0e7ff; box-shadow: 0 1px 4px rgba(102,126,234,0.1);'>
                <div style='font-size: 24px; margin-bottom: 4px;'>🎯</div>
                <div style='font-size: 20px; font-weight: 700; margin-bottom: 2px; color: {confidence_color};'>{confidence:.0%}</div>
                <div style='font-size: 10px; color: #64748b; font-weight: 600; text-transform: uppercase;'>Confidence</div>
            </div>
            <div style='background: white; padding: 12px; border-radius: 8px; text-align: center; border: 2px solid #e0e7ff; box-shadow: 0 1px 4px rgba(102,126,234,0.1);'>
                <div style='font-size: 24px; margin-bottom: 4px;'>{intent_emoji}</div>
                <div style='font-size: 12px; font-weight: 700; margin-bottom: 2px; color: #667eea;'>{intent.replace("_", " ").title()}</div>
                <div style='font-size: 10px; color: #64748b; font-weight: 600; text-transform: uppercase;'>Type</div>
            </div>
            <div style='background: white; padding: 12px; border-radius: 8px; text-align: center; border: 2px solid #e0e7ff; box-shadow: 0 1px 4px rgba(102,126,234,0.1);'>
                <div style='font-size: 24px; margin-bottom: 4px;'>📄</div>
                <div style='font-size: 20px; font-weight: 700; margin-bottom: 2px; color: #667eea;'>{sources_count}</div>
                <div style='font-size: 10px; color: #64748b; font-weight: 600; text-transform: uppercase;'>Sources</div>
            </div>
        </div>
    </div>
    """
    return html


def chat(
    message: str,
    history: List[List[str]],
    country: str,
    category: str,
    max_results: int,
) -> Tuple[str, List[List[str]], str, str]:
    """Handle chat messages."""
    if not message.strip():
        return "", history, "", ""

    start_time = time.time()

    try:
        logger.info(f"Processing chat message: {message[:100]}...")

        # Convert Gradio history format to agent messages format
        messages = []
        for chat_pair in history:
            if len(chat_pair) >= 2:
                user_msg, bot_msg = chat_pair[0], chat_pair[1]
                messages.append({"role": "user", "content": user_msg})
                if bot_msg:
                    messages.append({"role": "assistant", "content": bot_msg})

        # Process query through agent
        response = agent.invoke(
            query=message,
            country=country if country != "All" else None,
            category=category if category != "All" else None,
            max_results=max_results,
            messages=messages,
        )

        processing_time = time.time() - start_time

        # Extract response data
        answer = response.get(
            "answer", "I apologize, but I couldn't generate a response."
        )
        sources = response.get("sources", [])
        confidence = response.get("confidence_score", 0.0)
        metadata = response.get("metadata", {})
        metadata["sources_count"] = len(sources)

        # Format displays
        sources_display = format_sources(sources)
        metadata_display = format_metadata(metadata, processing_time, confidence)

        # Update history with Gradio list format
        history.append([message, answer])

        logger.info(f"Chat message processed in {processing_time:.2f}s")

        return "", history, sources_display, metadata_display

    except Exception as e:
        logger.error(f"Error processing chat: {e}", exc_info=True)
        processing_time = time.time() - start_time
        error_msg = (
            f"❌ **Error:** {str(e)}\n\nPlease try again or rephrase your question."
        )

        error_display = f"""
        <div style='padding: 20px; background: #fef2f2; border-radius: 10px; border: 2px solid #fecaca;'>
            <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
                <div style='font-size: 32px;'>⚠️</div>
                <h3 style='margin: 0; font-size: 18px; font-weight: 700; color: #dc2626;'>Error</h3>
            </div>
            <p style='margin: 8px 0; color: #991b1b; font-size: 14px; line-height: 1.5;'>An error occurred while processing your query.</p>
            <div style='background: white; padding: 12px; border-radius: 8px; margin-top: 12px; font-family: monospace; font-size: 12px; color: #7f1d1d;'>{str(e)[:200]}</div>
        </div>
        """

        history.append([message, error_msg])
        return "", history, error_display, format_metadata({}, processing_time, 0.0)


def clear_chat():
    """Clear chat history."""
    logger.info("Chat cleared")
    return [], "", ""


# Build modern, clean Gradio interface with fixed chat at top
with gr.Blocks(title="🌍 Travel Assistant AI") as demo:
    # Modern compact header
    gr.HTML("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
         padding: 20px 24px; margin: -8px -8px 24px -8px; box-shadow: 0 4px 16px rgba(102,126,234,0.3);'>
        <div style='display: flex; align-items: center; justify-content: space-between; max-width: 1400px; margin: 0 auto;'>
            <div style='display: flex; align-items: center; gap: 16px;'>
                <div style='font-size: 42px;'>🌍</div>
                <div>
                    <h1 style='margin: 0; font-size: 28px; font-weight: 800; color: white;'>Travel Assistant AI</h1>
                    <p style='margin: 4px 0 0 0; font-size: 13px; color: rgba(255,255,255,0.9);'>Powered by Gemini 1.5 Pro • Qdrant • LangGraph</p>
                </div>
            </div>
            <div style='display: flex; gap: 12px;'>
                <div style='background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 8px; text-align: center; backdrop-filter: blur(10px);'>
                    <div style='font-size: 20px;'>🛂</div>
                    <div style='font-size: 11px; color: white; font-weight: 600;'>Visa</div>
                </div>
                <div style='background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 8px; text-align: center; backdrop-filter: blur(10px);'>
                    <div style='font-size: 20px;'>⚖️</div>
                    <div style='font-size: 11px; color: white; font-weight: 600;'>Laws</div>
                </div>
                <div style='background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 8px; text-align: center; backdrop-filter: blur(10px);'>
                    <div style='font-size: 20px;'>🙏</div>
                    <div style='font-size: 11px; color: white; font-weight: 600;'>Culture</div>
                </div>
                <div style='background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 8px; text-align: center; backdrop-filter: blur(10px);'>
                    <div style='font-size: 20px;'>🛡️</div>
                    <div style='font-size: 11px; color: white; font-weight: 600;'>Safety</div>
                </div>
            </div>
        </div>
    </div>
    """)

    # Main chat interface - FIXED AT TOP
    with gr.Row():
        with gr.Column(scale=8):
            chatbot = gr.Chatbot(
                label="💬 Chat",
                height=500,
                show_label=False,
                container=True,
            )

            with gr.Row():
                msg = gr.Textbox(
                    label="",
                    placeholder="Ask me anything about travel: visa requirements, local laws, cultural tips, safety guidelines...",
                    lines=1,
                    scale=10,
                    show_label=False,
                    container=False,
                )
                submit_btn = gr.Button("Send 🚀", variant="primary", scale=1, size="lg")

            with gr.Row():
                clear_btn = gr.Button(
                    "🗑️ Clear", variant="secondary", size="sm", scale=1
                )

                gr.Examples(
                    examples=[
                        "What are the visa requirements for Indians traveling to Japan?",
                        "What cultural customs should I know before visiting UAE?",
                        "What items are prohibited in Japan?",
                        "Is it safe to travel to France right now?",
                    ],
                    inputs=msg,
                    label="",
                )

        # Sidebar with filters
        with gr.Column(scale=2):
            gr.Markdown("### ⚙️ Filters")

            country_filter = gr.Dropdown(
                label="🌍 Country",
                choices=["All", "Japan", "USA", "UK", "UAE", "Schengen Area", "France"],
                value="All",
            )

            category_filter = gr.Dropdown(
                label="📂 Category",
                choices=[
                    "All",
                    "visa_requirements",
                    "local_laws",
                    "cultural_etiquette",
                    "safety_guidelines",
                ],
                value="All",
            )

            max_results_slider = gr.Slider(
                minimum=1, maximum=10, value=5, step=1, label="📊 Sources"
            )

    # Collapsible analytics section
    with gr.Accordion("📊 Query Analytics", open=False):
        metadata_display = gr.HTML(
            value="<p style='text-align: center; padding: 20px; color: #666;'>Analytics will appear here</p>"
        )

    # Collapsible sources section
    with gr.Accordion("📚 Knowledge Sources", open=False):
        sources_display = gr.HTML(
            value="<p style='text-align: center; padding: 20px; color: #666;'>Sources will appear after your first query</p>"
        )

    # Event handlers
    submit_btn.click(
        fn=chat,
        inputs=[msg, chatbot, country_filter, category_filter, max_results_slider],
        outputs=[msg, chatbot, sources_display, metadata_display],
    )

    msg.submit(
        fn=chat,
        inputs=[msg, chatbot, country_filter, category_filter, max_results_slider],
        outputs=[msg, chatbot, sources_display, metadata_display],
    )

    clear_btn.click(fn=clear_chat, outputs=[chatbot, sources_display, metadata_display])


def launch_ui(server_port: int = 7860, share: bool = False):
    """Launch the Gradio UI."""
    logger.info(f"Launching Gradio UI on port {server_port}...")
    demo.launch(
        server_name="0.0.0.0", server_port=server_port, share=share, show_error=True
    )


if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from src.config.settings import settings

    launch_ui(server_port=settings.ui_port, share=False)
