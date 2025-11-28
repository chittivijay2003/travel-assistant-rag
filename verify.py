"""Quick verification script to test all components."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("RAG TRAVEL ASSISTANT - COMPONENT VERIFICATION")
print("=" * 80)

# Test 1: Settings
print("\n[1/8] Testing Settings...")
try:
    from src.config.settings import settings

    print(f"  ✓ Settings loaded")
    print(f"    - API Port: {settings.api_port}")
    print(f"    - UI Port: {settings.ui_port}")
    print(f"    - Gemini Model: {settings.gemini_model}")
    print(f"    - API Key configured: {'Yes' if settings.google_api_key else 'No'}")
except Exception as e:
    print(f"  ✗ Settings failed: {e}")
    sys.exit(1)

# Test 2: Logging
print("\n[2/8] Testing Logging...")
try:
    from src.core.logging import setup_logging, get_logger

    setup_logging()
    logger = get_logger(__name__)
    logger.info("Test log message")
    print("  ✓ Logging configured")
except Exception as e:
    print(f"  ✗ Logging failed: {e}")
    sys.exit(1)

# Test 3: Models
print("\n[3/8] Testing Domain Models...")
try:
    from src.models.domain import TravelDocument, SearchResult, RAGResponse, TravelQuery
    from src.models.schemas import RAGRequest, RAGResponse as RAGResponseSchema

    print("  ✓ Models imported")
except Exception as e:
    print(f"  ✗ Models failed: {e}")
    sys.exit(1)

# Test 4: Travel Documents
print("\n[4/8] Testing Travel Documents...")
try:
    from src.data.travel_documents import get_all_documents

    docs = get_all_documents()
    print(f"  ✓ {len(docs)} travel documents loaded")
    print(f"    - Categories: {len(set(doc.category for doc in docs))}")
    print(f"    - Countries: {len(set(doc.country for doc in docs if doc.country))}")
except Exception as e:
    print(f"  ✗ Travel documents failed: {e}")
    sys.exit(1)

# Test 5: Services
print("\n[5/8] Testing Services...")
try:
    from src.services.qdrant_service import QdrantService
    from src.services.embedding_service import EmbeddingService
    from src.services.search_service import SearchService
    from src.services.llm_service import LLMService
    from src.services.rag_service import RAGService

    print("  ✓ All services imported")
except Exception as e:
    print(f"  ✗ Services failed: {e}")
    sys.exit(1)

# Test 6: Agent
print("\n[6/8] Testing LangGraph Agent...")
try:
    from src.agents.graph import TravelAssistantGraph

    print("  ✓ Agent imported")
    # Note: Don't initialize here as it requires API key
except Exception as e:
    print(f"  ✗ Agent failed: {e}")
    sys.exit(1)

# Test 7: API
print("\n[7/8] Testing FastAPI Application...")
try:
    from src.api.main import app
    from src.api.routes import rag, health

    print("  ✓ FastAPI application imported")
    print(f"    - Routes configured")
except Exception as e:
    print(f"  ✗ FastAPI failed: {e}")
    sys.exit(1)

# Test 8: UI
print("\n[8/8] Testing Gradio UI...")
try:
    from src.ui.gradio_app import launch_ui

    print("  ✓ Gradio UI imported")
except Exception as e:
    print(f"  ✗ Gradio UI failed: {e}")
    sys.exit(1)

print("\n" + "=" * 80)
print("✅ ALL COMPONENTS VERIFIED SUCCESSFULLY!")
print("=" * 80)
print("\nNext steps:")
print("1. Run 'python main.py --mode setup' to initialize Qdrant and seed data")
print("2. Run 'python main.py --mode both' to start the application")
print("3. Access Gradio UI at http://localhost:7860")
print("4. Access API docs at http://localhost:8000/docs")
print("=" * 80)
