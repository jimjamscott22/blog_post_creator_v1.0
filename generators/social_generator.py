"""
Social Media Calendar Generator
"""
from typing import Optional
from pydantic import BaseModel, Field
from utils.llm_interface import llm, LocalLLM
from utils.prompt_templates import get_social_media_prompt
from utils.logger import setup_logger

# Set up logger
logger = setup_logger(__name__)


class SocialCalendarInput(BaseModel):
    """Input parameters for social media calendar generation"""
    theme: str = Field(..., min_length=1, description="Content theme or topic focus")
    platform: str = Field(default="LinkedIn", description="Target social media platform")
    frequency: str = Field(default="3x week", description="Posting frequency")
    timeframe: str = Field(default="month", description="Calendar timeframe")
    tone: str = Field(default="professional", description="Brand voice/tone")
    
    class Config:
        # Valid options for each field
        json_schema_extra = {
            "example": {
                "theme": "Artificial Intelligence and Machine Learning",
                "platform": "LinkedIn",
                "frequency": "3x week",
                "timeframe": "month",
                "tone": "professional"
            }
        }


class SocialCalendar(BaseModel):
    """Generated social media calendar"""
    theme: str
    calendar: str
    metadata: dict
    
    def to_markdown(self) -> str:
        """Convert to formatted markdown"""
        md = f"# Social Media Calendar: {self.theme}\n\n"
        md += self.calendar
        return md


def generate_social_calendar(
    theme: str,
    platform: str = "LinkedIn",
    frequency: str = "3x week",
    timeframe: str = "month",
    tone: str = "professional",
    model_override: Optional[str] = None
) -> SocialCalendar:
    """
    Generate a social media content calendar using the local LLM
    
    Args:
        theme: Content theme or topic focus
        platform: Target platform (LinkedIn, Twitter, Instagram, Facebook, TikTok)
        frequency: Posting frequency (daily, 3x week, 2x week, weekly)
        timeframe: Calendar timeframe (week, month, quarter)
        tone: Brand voice/tone (professional, casual, friendly, educational, inspirational, humorous)
        model_override: Optional specific model to use (overrides default)
    
    Returns:
        SocialCalendar object with generated content
    
    Raises:
        ValueError: If parameters are invalid
        Exception: If generation fails
    """
    
    logger.info(f"Generating social media calendar for theme: '{theme}'")
    logger.debug(f"Parameters - platform: {platform}, frequency: {frequency}, timeframe: {timeframe}, tone: {tone}")
    if model_override:
        logger.debug(f"Using model override: {model_override}")
    
    # Validate inputs
    valid_platforms = ["LinkedIn", "Twitter", "Instagram", "Facebook", "TikTok"]
    valid_frequencies = ["daily", "3x week", "2x week", "weekly"]
    valid_timeframes = ["week", "month", "quarter"]
    valid_tones = ["professional", "casual", "friendly", "educational", "inspirational", "humorous"]
    
    if platform not in valid_platforms:
        logger.error(f"Invalid platform: {platform}")
        raise ValueError(f"Platform must be one of: {', '.join(valid_platforms)}")
    
    if frequency not in valid_frequencies:
        logger.error(f"Invalid frequency: {frequency}")
        raise ValueError(f"Frequency must be one of: {', '.join(valid_frequencies)}")
    
    if timeframe not in valid_timeframes:
        logger.error(f"Invalid timeframe: {timeframe}")
        raise ValueError(f"Timeframe must be one of: {', '.join(valid_timeframes)}")
    
    if tone not in valid_tones:
        logger.error(f"Invalid tone: {tone}")
        raise ValueError(f"Tone must be one of: {', '.join(valid_tones)}")
    
    # Generate the prompt
    prompt = get_social_media_prompt(theme, frequency, platform, timeframe, tone)
    logger.debug(f"Prompt generated successfully (length: {len(prompt)} chars)")
    
    # System prompt for consistent output
    system_prompt = """You are an expert social media strategist and content creator.
You create engaging, platform-optimized social media content calendars that drive engagement.
Your calendars are well-structured, actionable, and tailored to the target platform and audience.
Always format your output clearly with dates, post types, captions, and engagement elements."""
    
    try:
        # Use model override if provided, otherwise use default
        llm_instance = LocalLLM(model_override=model_override) if model_override else llm
        
        # Generate the calendar
        logger.info("Sending request to LLM...")
        response = llm_instance.generate(prompt=prompt, system_prompt=system_prompt)
        logger.info("Successfully received response from LLM")
        
        # Create the calendar object
        calendar = SocialCalendar(
            theme=theme,
            calendar=response,
            metadata={
                "platform": platform,
                "frequency": frequency,
                "timeframe": timeframe,
                "tone": tone,
                "model": llm_instance.model,
                "provider": llm_instance.provider
            }
        )
        
        logger.info(f"Social media calendar created successfully for '{theme}'")
        return calendar
        
    except Exception as e:
        logger.error(f"Failed to generate social media calendar: {str(e)}")
        raise Exception(f"Failed to generate social media calendar: {str(e)}")


def validate_social_input(data: dict) -> SocialCalendarInput:
    """
    Validate social calendar input data using Pydantic
    
    Args:
        data: Dictionary with social calendar input parameters
    
    Returns:
        Validated SocialCalendarInput object
    
    Raises:
        ValidationError: If data is invalid
    """
    return SocialCalendarInput(**data)
