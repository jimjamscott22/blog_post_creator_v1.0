"""
Social Media Calendar Generator
"""
from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from utils.llm_interface import llm, LocalLLM
from utils.prompt_templates import get_social_media_prompt
from utils.logger import setup_logger

# Set up logger
logger = setup_logger(__name__)


class SocialMediaInput(BaseModel):
    """Input parameters for social media calendar generation"""
    theme: str = Field(... , min_length=1, description="Content theme or topic")
    frequency: str = Field(default="3x week", description="Posting frequency")
    platform: str = Field(default="LinkedIn", description="Target platform")
    timeframe: str = Field(default="month", description="Calendar time period")
    tone: str = Field(default="professional", description="Brand voice/tone")
    
    class Config:
        # Valid options for each field
        json_schema_extra = {
            "example": {
                "theme": "AI and Machine Learning",
                "frequency": "3x week",
                "platform": "LinkedIn",
                "timeframe": "month",
                "tone": "professional"
            }
        }


class SocialMediaCalendar(BaseModel):
    """Generated social media calendar"""
    theme: str
    calendar:  str
    metadata: dict
    
    def to_markdown(self) -> str:
        """Convert to formatted markdown"""
        md = f"# Social Media Calendar:  {self.theme}\n\n"
        md += f"**Platform:** {self.metadata['platform']}\n"
        md += f"**Frequency:** {self.metadata['frequency']}\n"
        md += f"**Timeframe:** {self.metadata['timeframe']}\n"
        md += f"**Tone:** {self.metadata['tone']}\n\n"
        md += "---\n\n"
        md += self.calendar
        return md
    
    def get_formatted_calendar(self) -> str:
        """Get calendar with dates formatted"""
        # Add current date context
        start_date = datetime.now()
        formatted = f"**Start Date:** {start_date. strftime('%B %d, %Y')}\n\n"
        formatted += self.calendar
        return formatted


def generate_social_calendar(
    theme: str,
    frequency: str = "3x week",
    platform: str = "LinkedIn",
    timeframe: str = "month",
    tone: str = "professional",
    model_override: Optional[str] = None
) -> SocialMediaCalendar:
    """
    Generate a social media content calendar using the local LLM
    
    Args:
        theme: Content theme or topic focus
        frequency: Posting frequency (daily, 3x week, weekly, 2x week)
        platform: Target platform (LinkedIn, Twitter, Instagram, Facebook, TikTok)
        timeframe: Time period (week, month, quarter)
        tone: Brand voice/tone (professional, casual, friendly, educational, inspirational)
        model_override:  Optional specific model to use (overrides default)
    
    Returns:
        SocialMediaCalendar object with generated content
    
    Raises:
        ValueError: If parameters are invalid
        Exception: If generation fails
    """
    
    logger.info(f"Generating social media calendar for theme: '{theme}'")
    logger.debug(f"Parameters - frequency: {frequency}, platform: {platform}, timeframe: {timeframe}, tone:  {tone}")
    if model_override:
        logger. debug(f"Using model override: {model_override}")
    
    # Validate inputs
    valid_frequencies = ["daily", "3x week", "2x week", "weekly"]
    valid_platforms = ["linkedin", "twitter", "instagram", "facebook", "tiktok"]
    valid_timeframes = ["week", "month", "quarter"]
    valid_tones = ["professional", "casual", "friendly", "educational", "inspirational", "humorous"]
    
    if frequency. lower() not in valid_frequencies: 
        logger.error(f"Invalid frequency: {frequency}")
        raise ValueError(f"Frequency must be one of: {', '.join(valid_frequencies)}")
    
    if platform. lower() not in valid_platforms: 
        logger.error(f"Invalid platform: {platform}")
        raise ValueError(f"Platform must be one of: {', '.join(valid_platforms)}")
    
    if timeframe.lower() not in valid_timeframes:
        logger.error(f"Invalid timeframe: {timeframe}")
        raise ValueError(f"Timeframe must be one of: {', '. join(valid_timeframes)}")
    
    if tone.lower() not in valid_tones: 
        logger.error(f"Invalid tone: {tone}")
        raise ValueError(f"Tone must be one of: {', '.join(valid_tones)}")
    
    # Generate the prompt
    prompt = get_social_media_prompt(theme, frequency, platform, timeframe, tone)
    logger.debug("Prompt generated successfully")
    
    # System prompt for consistent output
    system_prompt = """You are an expert social media strategist and content creator.
You create engaging, platform-optimized social media calendars that drive audience engagement.
Your calendars are well-structured, actionable, and tailored to the specific platform and audience. 
You understand platform-specific best practices, optimal posting times, and content formats.
Always format your output clearly with dates, post ideas, engagement prompts, and hashtags."""
    
    try:
        # Use model override if provided, otherwise use default
        llm_instance = LocalLLM(model_override=model_override) if model_override else llm
        
        # Generate the calendar
        logger.info("Sending request to LLM...")
        response = llm_instance.generate(prompt=prompt, system_prompt=system_prompt)
        logger.info("Successfully received response from LLM")
        
        # Create the calendar object
        calendar = SocialMediaCalendar(
            theme=theme,
            calendar=response,
            metadata={
                "frequency": frequency,
                "platform":  platform,
                "timeframe":  timeframe,
                "tone":  tone,
                "model": llm_instance.model,
                "provider": llm_instance.provider,
                "generated_date": datetime.now().isoformat()
            }
        )
        
        logger.info(f"Social media calendar created successfully for '{theme}'")
        return calendar
        
    except Exception as e: 
        logger.error(f"Failed to generate social media calendar: {str(e)}")
        raise Exception(f"Failed to generate social media calendar: {str(e)}")


def calculate_post_dates(frequency: str, timeframe: str, start_date: Optional[datetime] = None) -> list[str]:
    """
    Calculate specific post dates based on frequency and timeframe
    
    Args:
        frequency: Posting frequency (daily, 3x week, weekly, 2x week)
        timeframe: Time period (week, month, quarter)
        start_date: Starting date (defaults to today)
    
    Returns:
        List of formatted date strings
    """
    if start_date is None:
        start_date = datetime.now()
    
    # Calculate end date based on timeframe
    timeframe_days = {
        "week": 7,
        "month": 30,
        "quarter": 90
    }
    
    end_date = start_date + timedelta(days=timeframe_days. get(timeframe. lower(), 30))
    
    # Calculate frequency in days
    frequency_map = {
        "daily": 1,
        "3x week": 2,  # Approximately every 2 days
        "2x week": 3,  # Approximately every 3 days
        "weekly": 7
    }
    
    days_between = frequency_map. get(frequency.lower(), 2)
    
    # Generate dates
    dates = []
    current_date = start_date
    while current_date <= end_date: 
        dates.append(current_date.strftime("%B %d, %Y (%A)"))
        current_date += timedelta(days=days_between)
    
    return dates