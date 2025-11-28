"""Enterprise-Grade Gradio UI for Travel Assistant - Compatible Version."""

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
    """Format sources with beautiful HTML styling."""
    if not sources:
        return """<div style='padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   border-radius: 16px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                   <div style='font-size: 48px; margin-bottom: 12px;'>📚</div>
                   <h3 style='margin: 0; font-size: 20px;'>No sources retrieved</h3>
                   <p style='margin: 8px 0 0 0; opacity: 0.9; font-size: 14px;'>Try a more specific travel-related question</p>
                   </div>"""

    html = """<div style='padding: 24px; background: #f7fafc; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
              <h3 style='color: #2d3748; margin: 0 0 20px 0; display: flex; align-items: center; gap: 10px; font-size: 22px;'>
              <span style='font-size: 28px;'>📚</span> Knowledge Sources</h3>"""

    for i, source in enumerate(sources, 1):
        score = source.get("score", 0)
        score_color = (
            "#10b981" if score > 0.8 else "#f59e0b" if score > 0.6 else "#ef4444"
        )
        score_bg = "#d1fae5" if score > 0.8 else "#fef3c7" if score > 0.6 else "#fee2e2"
        reliability = source.get("reliability_score", 0)
        content_preview = source.get("content", "")[:150] + "..."

        html += f"""<div style='background: white; padding: 20px; margin: 16px 0; border-radius: 12px; 
                    border-left: 5px solid {score_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;'>
                        <h4 style='margin: 0; color: #1a202c; font-size: 18px; font-weight: 600; flex: 1;'>
                            <span style='color: {score_color}; font-weight: bold;'>#{i}</span> {source.get("title", "Unknown Document")}
                        </h4>
                        <span style='background: {score_bg}; color: {score_color}; padding: 6px 14px; border-radius: 20px; 
                              font-size: 13px; font-weight: 700; white-space: nowrap; margin-left: 12px;'>
                              {score:.1%} Match</span>
                    </div>
                    <p style='color: #4a5568; font-size: 14px; line-height: 1.6; margin: 12px 0; 
                       padding: 12px; background: #f7fafc; border-radius: 8px; font-style: italic;'>
                        "{content_preview}"
                    </p>
                    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin-top: 14px;'>
                        <div style='display: flex; align-items: center; gap: 8px; padding: 8px; background: #edf2f7; border-radius: 8px;'>
                            <span style='font-size: 18px;'>🏷️</span>
                            <span style='color: #2d3748; font-size: 13px; font-weight: 500;'>{source.get("category", "N/A").replace("_", " ").title()}</span>
                        </div>
                        <div style='display: flex; align-items: center; gap: 8px; padding: 8px; background: #edf2f7; border-radius: 8px;'>
                            <span style='font-size: 18px;'>🌍</span>
                            <span style='color: #2d3748; font-size: 13px; font-weight: 500;'>{source.get("country", "Global")}</span>
                        </div>
                        <div style='display: flex; align-items: center; gap: 8px; padding: 8px; background: #edf2f7; border-radius: 8px;'>
                            <span style='font-size: 18px;'>⭐</span>
                            <span style='color: #2d3748; font-size: 13px; font-weight: 500;'>Trust: {reliability:.1f}/10</span>
                        </div>
                    </div>
                    </div>"""

    html += "</div>"
    return html


def format_metadata(metadata: dict, processing_time: float, confidence: float) -> str:
    """Format metadata with beautiful gradient cards."""
    confidence_color = (
        "#10b981" if confidence > 0.8 else "#f59e0b" if confidence > 0.6 else "#ef4444"
    )
    confidence_bg = (
        "#d1fae5" if confidence > 0.8 else "#fef3c7" if confidence > 0.6 else "#fee2e2"
    )
    intent = metadata.get("intent", "unknown")
    intent_emoji = "🔍" if intent == "rag_query" else "💬"
    sources_count = metadata.get("sources_count", 0)

    html = f"""<div style='padding: 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
               border-radius: 16px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);'>
               <h3 style='margin: 0 0 20px 0; display: flex; align-items: center; gap: 10px; font-size: 22px;'>
               <span style='font-size: 28px;'>📊</span> Query Analytics</h3>
               <div style='background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; 
                    backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);'>
                   <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;'>
                       <div style='text-align: center; padding: 18px; background: rgba(255,255,255,0.2); border-radius: 12px;'>
                           <div style='font-size: 36px; margin-bottom: 10px;'>⏱️</div>
                           <div style='font-size: 28px; font-weight: bold; margin-bottom: 6px;'>{processing_time:.2f}s</div>
                           <div style='font-size: 12px; opacity: 0.95;'>Response Time</div>
                       </div>
                       <div style='text-align: center; padding: 18px; background: rgba(255,255,255,0.2); border-radius: 12px;'>
                           <div style='font-size: 36px; margin-bottom: 10px;'>🎯</div>
                           <div style='font-size: 24px; font-weight: bold; margin-bottom: 6px; 
                                background: {confidence_bg}; color: {confidence_color}; 
                                padding: 4px 12px; border-radius: 8px; display: inline-block;'>{confidence:.0%}</div>
                           <div style='font-size: 12px; opacity: 0.95;'>Confidence</div>
                       </div>
                       <div style='text-align: center; padding: 18px; background: rgba(255,255,255,0.2); border-radius: 12px;'>
                           <div style='font-size: 36px; margin-bottom: 10px;'>{intent_emoji}</div>
                           <div style='font-size: 16px; font-weight: bold; margin-bottom: 6px;'>{intent.replace("_", " ").title()}</div>
                           <div style='font-size: 12px; opacity: 0.95;'>Query Type</div>
                       </div>
                       <div style='text-align: center; padding: 18px; background: rgba(255,255,255,0.2); border-radius: 12px;'>
                           <div style='font-size: 36px; margin-bottom: 10px;'>📄</div>
                           <div style='font-size: 28px; font-weight: bold; margin-bottom: 6px;'>{sources_count}</div>
                           <div style='font-size: 12px; opacity: 0.95;'>Sources Used</div>
                       </div>
                   </div>
               </div>
           </div>"""
    return html


def chat(
    message: str,
    history: List[Tuple[str, str]],
    country: str,
    category: str,
    max_results: int,
) -> Tuple[str, List[Tuple[str, str]], str, str]:
    """Handle chat messages."""
    if not message.strip():
        return "", history, "", ""

    start_time = time.time()

    try:
        logger.info(f"Processing chat message: {message[:100]}...")

        # Convert history to messages format
        messages = []
        for user_msg, assistant_msg in history:
            messages.append({"role": "user", "content": user_msg})
            if assistant_msg:
                messages.append({"role": "assistant", "content": assistant_msg})

        # Process query through agent
        response = agent.invoke(
            query=message,
            country=country if country != "All Countries" else None,
            category=category if category != "All Categories" else None,
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

        # Update history
        history.append((message, answer))

        logger.info(f"Chat message processed in {processing_time:.2f}s")

        return "", history, sources_display, metadata_display

    except Exception as e:
        logger.error(f"Error processing chat: {e}", exc_info=True)
        processing_time = time.time() - start_time
        error_msg = (
            f"❌ **Error:** {str(e)}\n\nPlease try again or rephrase your question."
        )

        error_display = f"""<div style='padding: 24px; background: linear-gradient(135deg, #fc5c7d 0%, #6a82fb 100%); 
                        border-radius: 16px; color: white;'>
                        <h3 style='margin: 0;'>⚠️ Error Occurred</h3>
                        <p style='margin: 12px 0; opacity: 0.9;'>{str(e)[:200]}</p>
                        </div>"""

        history.append((message, error_msg))
        return "", history, error_display, format_metadata({}, processing_time, 0.0)


def clear_chat():
    """Clear chat history."""
    logger.info("Chat cleared")
    return [], "", ""


# Build Gradio interface
with gr.Blocks(title="🌍 Enterprise RAG Travel Assistant") as demo:
    gr.Markdown(
        """
        # 🌍 Enterprise RAG Travel Assistant
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 16px; text-align: center;">
                <strong>Google Gemini 1.5 Pro</strong> • <strong>Sentence Transformers</strong> • 
                <strong>Qdrant Vector DB</strong> • <strong>LangGraph</strong> • <strong>FastAPI</strong>
            </p>
        </div>
        
        ### 🎯 Ask me about:
        - 🛂 **Visa Requirements** - Entry permits & documentation
        - ⚖️ **Local Laws** - Regulations & legal requirements  
        - 🙏 **Cultural Etiquette** - Customs & social norms
        - 🛡️ **Safety Guidelines** - Travel safety & precautions
        """
    )

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="💬 Conversation", height=500)

            with gr.Row():
                msg = gr.Textbox(
                    label="Your Question",
                    placeholder="💭 Ask me anything about travel requirements, regulations, culture, or safety...",
                    lines=2,
                )
                submit_btn = gr.Button("Send 📤", variant="primary")

            with gr.Row():
                clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")

            gr.Examples(
                examples=[
                    "What are the visa requirements for Indians traveling to Japan?",
                    "What cultural customs should I know before visiting UAE?",
                    "What items are prohibited in Japan?",
                    "Is it safe to travel to France right now?",
                ],
                inputs=msg,
                label="💡 Try these examples",
            )

        with gr.Column(scale=2):
            gr.Markdown("### 🎛️ Filters")

            country_filter = gr.Dropdown(
                label="🌍 Country Focus",
                choices=[
                    "All Countries",
                    "Japan",
                    "USA",
                    "UK",
                    "UAE",
                    "Schengen Area",
                    "France",
                ],
                value="All Countries",
            )

            category_filter = gr.Dropdown(
                label="📂 Category",
                choices=[
                    "All Categories",
                    "visa_requirements",
                    "local_laws",
                    "cultural_etiquette",
                    "safety_guidelines",
                ],
                value="All Categories",
            )

            max_results_slider = gr.Slider(
                minimum=1,
                maximum=10,
                value=5,
                step=1,
                label="📊 Max Sources",
            )

            gr.Markdown("---")
            metadata_display = gr.HTML(
                value="<p style='text-align: center; color: #718096;'>Analytics will appear here</p>"
            )

    gr.Markdown("---")
    gr.Markdown("### 📚 Retrieved Sources")
    sources_display = gr.HTML(
        value="<p style='text-align: center; padding: 30px; color: #718096;'>Sources will appear here after your first query</p>"
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

    gr.Markdown(
        """
        ---
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 12px;">
            <p style="margin: 0; color: #2d3748; font-weight: 600;">
                🚀 **Production-Ready Enterprise Application** | Built with ❤️ using RAG + LangGraph + AI
            </p>
        </div>
        """
    )


def launch_ui(server_port: int = 7860, share: bool = False):
    """Launch the Gradio UI."""
    logger.info(f"Launching Gradio UI on port {server_port}...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=server_port,
        share=share,
        show_error=True,
    )


if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from src.config.settings import settings

    launch_ui(server_port=settings.ui_port, share=False)
