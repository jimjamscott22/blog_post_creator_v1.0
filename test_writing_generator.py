"""
Test script for Creative Writing Prompt Generator
Step 3.1: Test the writing prompt generation functionality
"""
import sys
from generators.writing_generator import generate_writing_prompt
from utils.logger import setup_logger

# Set up logger
logger = setup_logger(__name__)

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def main():
    logger.info("=" * 60)
    logger.info("Testing Creative Writing Prompt Generator")
    logger.info("=" * 60)
    
    # Test parameters
    test_genre = "sci-fi"
    test_prompt_type = "character"
    test_complexity = "moderate"
    test_constraints = "Must include a time travel element"
    
    logger.info(f"Genre: {test_genre}")
    logger.info(f"Prompt Type: {test_prompt_type}")
    logger.info(f"Complexity: {test_complexity}")
    logger.info(f"Constraints: {test_constraints}")
    logger.info("Generating writing prompt... (this may take 10-30 seconds)")
    
    try:
        # Generate the prompt
        result = generate_writing_prompt(
            genre=test_genre,
            prompt_type=test_prompt_type,
            complexity=test_complexity,
            constraints=test_constraints
        )
        
        logger.info("[SUCCESS] Writing prompt generated!")
        logger.info("=" * 60)
        logger.info(result.to_markdown())
        logger.info("=" * 60)
        logger.info("Metadata:")
        logger.info(f"  Model: {result.metadata['model']}")
        logger.info(f"  Provider: {result.metadata['provider']}")
        logger.info(f"  Genre: {result.genre}")
        logger.info(f"  Prompt Type: {result.metadata['prompt_type']}")
        logger.info(f"  Complexity: {result.metadata['complexity']}")
        logger.info(f"  Constraints: {result.metadata['constraints']}")
        logger.info("[PASS] Writing prompt generator is working correctly!")
        
    except Exception as e:
        logger.error(f"Failed to generate writing prompt: {str(e)}")
        logger.info("Troubleshooting:")
        logger.info("  1. Ensure Ollama is running")
        logger.info("  2. Check your .env configuration")
        logger.info("  3. Verify the model is available")


if __name__ == "__main__":
    main()
