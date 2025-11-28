"""Main entry point for RAG Travel Assistant."""

import logging
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import settings
from src.core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


def run_api():
    """Run FastAPI server."""
    import uvicorn
    from src.api.main import app

    logger.info("Starting FastAPI server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.api_port,
        log_level=settings.log_level.lower(),
    )


def run_ui():
    """Run Gradio UI."""
    from src.ui.gradio_app import launch_ui

    logger.info("Starting Gradio UI...")
    launch_ui(server_port=settings.ui_port, share=False)


def run_both():
    """Run both API and UI in separate processes."""
    import multiprocessing

    logger.info("Starting both API and UI...")

    # Start API in separate process
    api_process = multiprocessing.Process(target=run_api)
    api_process.start()

    # Start UI in separate process
    ui_process = multiprocessing.Process(target=run_ui)
    ui_process.start()

    try:
        api_process.join()
        ui_process.join()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        api_process.terminate()
        ui_process.terminate()


def setup_database():
    """Run database setup scripts."""
    from scripts.setup_qdrant import setup_qdrant
    from scripts.seed_data import seed_data

    logger.info("Setting up database...")
    qdrant = setup_qdrant()

    logger.info("\nSeeding data...")
    seed_data(qdrant)

    logger.info("\n✅ Database setup complete!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="RAG-Enhanced Travel Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --mode ui                  # Run Gradio UI only
  %(prog)s --mode api                 # Run FastAPI only
  %(prog)s --mode both                # Run both (default)
  %(prog)s --mode setup               # Setup Qdrant and seed data
        """,
    )

    parser.add_argument(
        "--mode",
        choices=["api", "ui", "both", "setup"],
        default="both",
        help="Run mode (default: both)",
    )

    parser.add_argument(
        "--api-port",
        type=int,
        default=settings.api_port,
        help=f"FastAPI port (default: {settings.api_port})",
    )

    parser.add_argument(
        "--ui-port",
        type=int,
        default=settings.ui_port,
        help=f"Gradio UI port (default: {settings.ui_port})",
    )

    args = parser.parse_args()

    # Update settings if custom ports provided
    if args.api_port != settings.api_port:
        settings.api_port = args.api_port
    if args.ui_port != settings.ui_port:
        settings.ui_port = args.ui_port

    logger.info("=" * 80)
    logger.info("RAG-ENHANCED TRAVEL ASSISTANT")
    logger.info("=" * 80)
    logger.info(f"Mode: {args.mode}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"API Port: {settings.api_port}")
    logger.info(f"UI Port: {settings.ui_port}")
    logger.info("=" * 80)

    try:
        if args.mode == "api":
            run_api()
        elif args.mode == "ui":
            run_ui()
        elif args.mode == "both":
            run_both()
        elif args.mode == "setup":
            setup_database()
        else:
            parser.print_help()

    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down gracefully...")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
