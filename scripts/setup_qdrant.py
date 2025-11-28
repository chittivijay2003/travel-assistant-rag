"""Setup Qdrant collection and index travel documents."""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings
from src.core.logging import setup_logging
from src.services.qdrant_service import QdrantService
from src.services.embedding_service import EmbeddingService
from src.data.travel_documents import get_all_documents

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


def setup_qdrant():
    """Setup Qdrant collection.

    Returns:
        QdrantService: The initialized Qdrant service instance
    """
    logger.info("=" * 80)
    logger.info("QDRANT SETUP STARTING")
    logger.info("=" * 80)

    try:
        # Initialize services
        logger.info("Initializing services...")
        qdrant = QdrantService()
        embedder = EmbeddingService()

        # Connect to Qdrant
        logger.info("Connecting to Qdrant...")
        qdrant.connect()

        # Check if collection exists
        logger.info(f"Checking collection: {settings.qdrant_collection}")
        collection_info = qdrant.get_collection_info()

        if collection_info:
            logger.warning(f"Collection '{settings.qdrant_collection}' already exists")
            logger.info("Deleting and recreating collection...")
            qdrant.delete_collection()

        # Create collection
        logger.info("Creating collection...")
        embedding_dim = embedder.get_embedding_dimension()
        qdrant.create_collection(vector_size=embedding_dim)

        logger.info("✅ Qdrant setup completed successfully!")
        logger.info(f"Collection: {settings.qdrant_collection}")
        logger.info(f"Dimension: {embedding_dim}")
        logger.info(f"Distance: Cosine")

        return qdrant

    except Exception as e:
        logger.error(f"❌ Qdrant setup failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    setup_qdrant()
