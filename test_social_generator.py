"""
Test script for Social Media Calendar Generator
Step 2.1: Test the social media calendar generation functionality
"""
import sys
from generators.social_generator import generate_social_calendar
from utils.logger import setup_logger

# Set up logger
logger = setup_logger(__name__)

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def main():
    logger.info("=" * 60)
    logger.info("Testing Social Media Calendar Generator")
    logger.info("=" * 60)
    
    # Test parameters
    test_theme = "Artificial Intelligence and Machine Learning"
    test_platform = "LinkedIn"
    test_frequency = "3x week"
    test_timeframe = "month"
    test_tone = "professional"
    
    logger.info(f"Theme: {test_theme}")
    logger.info(f"Platform: {test_platform}")
    logger.info(f"Frequency: {test_frequency}")
    logger.info(f"Timeframe: {test_timeframe}")
    logger.info(f"Tone: {test_tone}")
    logger.info("Generating social media calendar... (this may take 10-30 seconds)")
    
    try:
        # Generate the calendar
        result = generate_social_calendar(
            theme=test_theme,
            platform=test_platform,
            frequency=test_frequency,
            timeframe=test_timeframe,
            tone=test_tone
        )
        
        logger.info("[SUCCESS] Social media calendar generated!")
        logger.info("=" * 60)
        logger.info(result.to_markdown())
        logger.info("=" * 60)
        logger.info("Metadata:")
        logger.info(f"  Model: {result.metadata['model']}")
        logger.info(f"  Provider: {result.metadata['provider']}")
        logger.info(f"  Platform: {result.metadata['platform']}")
        logger.info(f"  Frequency: {result.metadata['frequency']}")
        logger.info(f"  Timeframe: {result.metadata['timeframe']}")
        logger.info(f"  Tone: {result.metadata['tone']}")
        logger.info("[PASS] Social media calendar generator is working correctly!")
        
    except Exception as e:
        logger.error(f"Failed to generate calendar: {str(e)}")
        logger.info("Troubleshooting:")
        logger.info("  1. Ensure Ollama is running")
        logger.info("  2. Check your .env configuration")
        logger.info("  3. Verify the model is available")


if __name__ == "__main__":
    main()
