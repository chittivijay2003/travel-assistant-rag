"""Seed Qdrant with travel documents."""

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
from src.models.domain import DocumentStatus

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


def seed_data(qdrant=None):
    """Seed Qdrant with travel documents.

    Args:
        qdrant: Optional QdrantService instance. If not provided, creates new one.
    """
    logger.info("=" * 80)
    logger.info("DATA SEEDING STARTING")
    logger.info("=" * 80)

    try:
        # Initialize services
        logger.info("Initializing services...")
        if qdrant is None:
            qdrant = QdrantService()
            # Connect to Qdrant
            logger.info("Connecting to Qdrant...")
            qdrant.connect()

            # Check if collection exists
            collection_info = qdrant.get_collection_info()
            if not collection_info:
                logger.error(
                    f"Collection '{settings.qdrant_collection}' does not exist"
                )
                logger.info("Please run 'python scripts/setup_qdrant.py' first")
                sys.exit(1)
        else:
            logger.info("Using provided Qdrant instance...")

        embedder = EmbeddingService()

        # Get documents
        logger.info("Loading travel documents...")
        documents = get_all_documents()
        logger.info(f"Loaded {len(documents)} documents")

        # Display document summary
        logger.info("\nDocument Summary:")
        categories = {}
        countries = {}
        for doc in documents:
            cat = doc.category.value
            categories[cat] = categories.get(cat, 0) + 1
            if doc.country:
                countries[doc.country] = countries.get(doc.country, 0) + 1

        logger.info(f"  By Category:")
        for cat, count in sorted(categories.items()):
            logger.info(f"    - {cat}: {count}")

        logger.info(f"  By Country:")
        for country, count in sorted(countries.items()):
            logger.info(f"    - {country}: {count}")

        # Generate embeddings for documents
        logger.info("\nGenerating embeddings...")
        document_texts = [doc.content for doc in documents]
        embeddings = embedder.embed_texts(document_texts)
        logger.info(f"Generated {len(embeddings)} embeddings")

        # Index documents
        logger.info("\nIndexing documents in Qdrant...")
        qdrant.index_documents(documents, embeddings)

        # Update document status
        for doc in documents:
            doc.status = DocumentStatus.INDEXED

        logger.info(f"✅ Successfully indexed {len(documents)} documents!")

        # Verify indexing
        logger.info("\nVerifying indexing...")
        collection_info = qdrant.get_collection_info()
        logger.info(
            f"Collection points count: {collection_info.get('points_count', 0)}"
        )

        logger.info("\n" + "=" * 80)
        logger.info("DATA SEEDING COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)

    except Exception as e:
        logger.error(f"❌ Data seeding failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    seed_data()
