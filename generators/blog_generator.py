"""
Blog Post Outline Generator
"""
from typing import Optional
from pydantic import BaseModel, Field
from utils.llm_interface import llm, LocalLLM
from utils.prompt_templates import get_blog_outline_prompt
from utils.logger import setup_logger

# Set up logger
logger = setup_logger(__name__)


class BlogInput(BaseModel):
    """Input parameters for blog post generation"""
    topic: str = Field(..., min_length=1, description="The main topic or keyword focus")
    audience: str = Field(default="intermediate", description="Target audience level")
    length: str = Field(default="medium", description="Desired content length")
    content_type: str = Field(default="how-to", description="Type of content")
    
    class Config:
        # Valid options for each field
        json_schema_extra = {
            "example": {
                "topic": "Getting Started with Python Programming",
                "audience": "beginners",
                "length": "medium",
                "content_type": "tutorial"
            }
        }


class BlogOutline(BaseModel):
    """Generated blog post outline"""
    topic: str
    outline: str
    metadata: dict
    
    def to_markdown(self) -> str:
        """Convert to formatted markdown"""
        md = f"# Blog Post Outline: {self.topic}\n\n"
        md += self.outline
        return md


def generate_blog_outline(
    topic: str,
    audience: str = "intermediate",
    length: str = "medium",
    content_type: str = "how-to",
    custom_context: Optional[str] = None,
    model_override: Optional[str] = None
) -> BlogOutline:
    """
    Generate a blog post outline using the local LLM
    
    Args:
        topic: The main topic or keyword focus
        audience: Target audience (beginners, intermediate, experts)
        length: Desired length (short, medium, long)
        content_type: Type of content (tutorial, listicle, how-to, opinion)
        custom_context: Optional custom information/documentation to reference
        model_override: Optional specific model to use (overrides default)
    
    Returns:
        BlogOutline object with generated content
    
    Raises:
        ValueError: If parameters are invalid
        Exception: If generation fails
    """
    
    logger.info(f"Generating blog outline for topic: '{topic}'")
    logger.debug(f"Parameters - audience: {audience}, length: {length}, type: {content_type}")
    if model_override:
        logger.debug(f"Using model override: {model_override}")
    
    # Validate inputs
    valid_audiences = ["beginners", "intermediate", "experts"]
    valid_lengths = ["short", "medium", "long"]
    valid_types = ["tutorial", "listicle", "how-to", "opinion"]
    
    if audience.lower() not in valid_audiences:
        logger.error(f"Invalid audience: {audience}")
        raise ValueError(f"Audience must be one of: {', '.join(valid_audiences)}")
    
    if length.lower() not in valid_lengths:
        logger.error(f"Invalid length: {length}")
        raise ValueError(f"Length must be one of: {', '.join(valid_lengths)}")
    
    if content_type.lower() not in valid_types:
        logger.error(f"Invalid content type: {content_type}")
        raise ValueError(f"Content type must be one of: {', '.join(valid_types)}")
    
    # Generate the prompt
    prompt = get_blog_outline_prompt(topic, audience, length, content_type, custom_context)
    logger.debug("Prompt generated successfully")
    
    # System prompt for consistent output
    system_prompt = """You are an expert technical content strategist and SEO specialist.
You create detailed, actionable technical blog post outlines that are easy to follow and implement.
Your outlines are well-structured, comprehensive, and tailored to the target audience.
When provided with custom context or documentation, you incorporate that information accurately.
Always format your output clearly with proper headers, bullet points, and sections."""
    
    try:
        # Use model override if provided, otherwise use default
        llm_instance = LocalLLM(model_override=model_override) if model_override else llm
        
        # Generate the outline
        logger.info("Sending request to LLM...")
        response = llm_instance.generate(prompt=prompt, system_prompt=system_prompt)
        logger.info("Successfully received response from LLM")
        
        # Create the outline object
        outline = BlogOutline(
            topic=topic,
            outline=response,
            metadata={
                "audience": audience,
                "length": length,
                "content_type": content_type,
                "model": llm_instance.model,
                "provider": llm_instance.provider
            }
        )
        
        logger.info(f"Blog outline created successfully for '{topic}'")
        return outline
        
    except Exception as e:
        logger.error(f"Failed to generate blog outline: {str(e)}")
        raise Exception(f"Failed to generate blog outline: {str(e)}")


def validate_blog_input(data: dict) -> BlogInput:
    """
    Validate blog input data using Pydantic
    
    Args:
        data: Dictionary with blog input parameters
    
    Returns:
        Validated BlogInput object
    
    Raises:
        ValidationError: If data is invalid
    """
    return BlogInput(**data)
