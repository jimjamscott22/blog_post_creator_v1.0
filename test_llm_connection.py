"""
Test script for local LLM connection
Step 1.2: Verify that the LLM interface works correctly
"""
import sys
from utils.llm_interface import llm
from utils.logger import setup_logger

# Set up logger
logger = setup_logger(__name__)

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def main():
    logger.info("=" * 60)
    logger.info("Testing Local LLM Connection")
    logger.info("=" * 60)
    
    # Test 1: Connection Test
    logger.info("Test 1: Checking connection...")
    success, message = llm.test_connection()
    logger.info(message)
    
    if not success:
        logger.warning("Please ensure your LLM is running:")
        logger.warning("  - For Ollama: Run 'ollama serve' or ensure it's auto-started")
        logger.warning("  - For LM Studio: Start the local server in the app")
        return
    
    # Test 2: Simple Generation Test
    logger.info("Test 2: Testing text generation...")
    logger.info("Sending prompt: 'Say hello in one sentence.'")
    
    try:
        response = llm.generate(
            prompt="Say hello in one sentence.",
            system_prompt="You are a helpful assistant."
        )
        
        logger.info("[SUCCESS] Response received:")
        logger.info("-" * 60)
        logger.info(response)
        logger.info("-" * 60)
        logger.info("[PASS] All tests passed! LLM interface is working correctly.")
        logger.info("Configuration:")
        logger.info(f"  Provider: {llm.provider}")
        logger.info(f"  Model: {llm.model}")
        logger.info(f"  Base URL: {llm.base_url}")
        logger.info(f"  Temperature: {llm.temperature}")
        logger.info(f"  Max Tokens: {llm.max_tokens}")
        
    except Exception as e:
        logger.error(f"Error during generation: {str(e)}")
        logger.info("Troubleshooting:")
        logger.info("  1. Check that your LLM server is running")
        logger.info("  2. Verify the model name in your .env file")
        logger.info("  3. Check the base URL is correct")


if __name__ == "__main__":
    main()
