"""
Test script for Tech Blog Generator with Custom Context
"""
import sys
from generators.blog_generator import generate_blog_outline
from utils.logger import setup_logger

# Set up logger
logger = setup_logger(__name__)

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def main():
    logger.info("=" * 60)
    logger.info("Testing Tech Blog Generator with Custom Context")
    logger.info("=" * 60)
    
    # Test parameters
    test_topic = "Building a Real-time Chat Application"
    test_audience = "intermediate"
    test_length = "medium"
    test_type = "tutorial"
    
    # Custom technical context
    custom_context = """
    Technology Stack:
    - Backend: FastAPI (Python 3.11+)
    - WebSocket support: FastAPI's native WebSocket implementation
    - Database: PostgreSQL with SQLAlchemy ORM
    - Real-time features: Redis for pub/sub messaging
    - Authentication: JWT tokens with OAuth2
    - Deployment: Docker containers on AWS ECS
    
    Key Features:
    - Real-time message delivery with <100ms latency
    - Support for group chats and direct messages
    - Message persistence and history retrieval
    - Typing indicators and read receipts
    - File sharing (images, documents up to 10MB)
    - End-to-end encryption using AES-256
    """
    
    logger.info(f"Topic: {test_topic}")
    logger.info(f"Audience: {test_audience}")
    logger.info(f"Length: {test_length}")
    logger.info(f"Type: {test_type}")
    logger.info("Custom Context: Yes (provided)")
    logger.info("Generating tech blog outline... (this may take 15-40 seconds)")
    
    try:
        # Generate the outline with custom context
        result = generate_blog_outline(
            topic=test_topic,
            audience=test_audience,
            length=test_length,
            content_type=test_type,
            custom_context=custom_context
        )
        
        logger.info("[SUCCESS] Tech blog outline generated with custom context!")
        logger.info("=" * 60)
        logger.info(result.to_markdown())
        logger.info("=" * 60)
        logger.info("Metadata:")
        logger.info(f"  Model: {result.metadata['model']}")
        logger.info(f"  Provider: {result.metadata['provider']}")
        logger.info(f"  Audience: {result.metadata['audience']}")
        logger.info(f"  Length: {result.metadata['length']}")
        logger.info(f"  Type: {result.metadata['content_type']}")
        logger.info("[PASS] Tech Blog Generator with custom context is working!")
        
    except Exception as e:
        logger.error(f"Failed to generate outline: {str(e)}")
        logger.info("Troubleshooting:")
        logger.info("  1. Ensure Ollama is running")
        logger.info("  2. Check your .env configuration")
        logger.info("  3. Verify the model is available")


if __name__ == "__main__":
    main()
