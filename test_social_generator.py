"""
Test script for Social Media Calendar Generator
Step 2.1: Test the social media calendar generation functionality
"""
import sys
from generators.social_generator import generate_social_calendar
<<<<<<< HEAD
from utils. logger import setup_logger
=======
from utils.logger import setup_logger
>>>>>>> 5e41ca495c21ebb6653e087d73e0ccd052029116

# Set up logger
logger = setup_logger(__name__)

# Fix Windows console encoding
if sys.platform == 'win32':
<<<<<<< HEAD
    sys. stdout.reconfigure(encoding='utf-8')
=======
    sys.stdout.reconfigure(encoding='utf-8')
>>>>>>> 5e41ca495c21ebb6653e087d73e0ccd052029116


def main():
    logger.info("=" * 60)
    logger.info("Testing Social Media Calendar Generator")
    logger.info("=" * 60)
    
    # Test parameters
    test_theme = "Artificial Intelligence and Machine Learning"
<<<<<<< HEAD
    test_frequency = "3x week"
    test_platform = "LinkedIn"
=======
    test_platform = "LinkedIn"
    test_frequency = "3x week"
>>>>>>> 5e41ca495c21ebb6653e087d73e0ccd052029116
    test_timeframe = "month"
    test_tone = "professional"
    
    logger.info(f"Theme: {test_theme}")
<<<<<<< HEAD
    logger.info(f"Frequency: {test_frequency}")
    from utils.logger import setup_logger
=======
    logger.info(f"Platform: {test_platform}")
    logger.info(f"Frequency: {test_frequency}")
>>>>>>> 5e41ca495c21ebb6653e087d73e0ccd052029116
    logger.info(f"Timeframe: {test_timeframe}")
    logger.info(f"Tone: {test_tone}")
        sys.stdout.reconfigure(encoding='utf-8')
    
    try:
        # Generate the calendar
        result = generate_social_calendar(
            theme=test_theme,
<<<<<<< HEAD
            frequency=test_frequency,
            platform=test_platform,
        test_platform = "LinkedIn"
        test_frequency = "3x week"
            frequency=test_frequency,
>>>>>>> 5e41ca495c21ebb6653e087d73e0ccd052029116
            timeframe=test_timeframe,
            tone=test_tone
        logger.info(f"Platform: {test_platform}")
        logger.info(f"Frequency: {test_frequency}")
        logger.info("[SUCCESS] Social media calendar generated!")
        logger.info("=" * 60)
        logger.info(result.to_markdown())
        logger.info("=" * 60)
        logger.info("Metadata:")
        logger.info(f"  Model: {result.metadata['model']}")
        logger.info(f"  Provider: {result.metadata['provider']}")
        logger.info(f"  Platform: {result.metadata['platform']}")
                platform=test_platform,
                frequency=test_frequency,
        logger.info(f"  Tone: {result.metadata['tone']}")
<<<<<<< HEAD
        logger.info(f"  Generated:  {result.metadata['generated_date']}")
        logger.info("[PASS] Social media calendar generator is working correctly!")
        
    except Exception as e:
        logger. error(f"Failed to generate calendar: {str(e)}")
        logger.info("Troubleshooting:")
        logger.info("  1. Ensure Ollama is running")
        logger.info("  2. Check your . env configuration")
=======
        logger.info("[PASS] Social media calendar generator is working correctly!")
        
    except Exception as e:
        logger.error(f"Failed to generate calendar: {str(e)}")
            logger.info(f"  Generated:  {result.metadata.get('generated_date')}")
            logger.info("[PASS] Social media calendar generator is working correctly!")
        logger.info("  2. Check your .env configuration")
>>>>>>> 5e41ca495c21ebb6653e087d73e0ccd052029116
            logger.error(f"Failed to generate calendar: {str(e)}")


if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
        main()
>>>>>>> 5e41ca495c21ebb6653e087d73e0ccd052029116
