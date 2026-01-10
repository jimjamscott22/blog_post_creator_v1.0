"""
Blog Post Outline Generator
"""
from typing import Optional
from pydantic import BaseModel, Field
from utils.llm_interface import llm
from utils.prompt_templates import get_blog_outline_prompt


class BlogInput(BaseModel):
    """Input parameters for blog post generation"""
    topic: str = Field(..., min_length=1, description="The main topic or keyword focus")
    audience: str = Field(default="intermediate", description="Target audience level")
    length: str = Field(default="medium", description="Desired content length")
    content_type: str = Field(default="how-to", description="Type of content")
    
    class Config:
        # Valid options for each field
        schema_extra = {
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
    content_type: str = "how-to"
) -> BlogOutline:
    """
    Generate a blog post outline using the local LLM
    
    Args:
        topic: The main topic or keyword focus
        audience: Target audience (beginners, intermediate, experts)
        length: Desired length (short, medium, long)
        content_type: Type of content (tutorial, listicle, how-to, opinion)
    
    Returns:
        BlogOutline object with generated content
    
    Raises:
        ValueError: If parameters are invalid
        Exception: If generation fails
    """
    
    # Validate inputs
    valid_audiences = ["beginners", "intermediate", "experts"]
    valid_lengths = ["short", "medium", "long"]
    valid_types = ["tutorial", "listicle", "how-to", "opinion"]
    
    if audience.lower() not in valid_audiences:
        raise ValueError(f"Audience must be one of: {', '.join(valid_audiences)}")
    
    if length.lower() not in valid_lengths:
        raise ValueError(f"Length must be one of: {', '.join(valid_lengths)}")
    
    if content_type.lower() not in valid_types:
        raise ValueError(f"Content type must be one of: {', '.join(valid_types)}")
    
    # Generate the prompt
    prompt = get_blog_outline_prompt(topic, audience, length, content_type)
    
    # System prompt for consistent output
    system_prompt = """You are an expert content strategist and SEO specialist. 
You create detailed, actionable blog post outlines that are easy to follow and implement.
Your outlines are well-structured, comprehensive, and tailored to the target audience.
Always format your output clearly with proper headers, bullet points, and sections."""
    
    try:
        # Generate the outline
        response = llm.generate(prompt=prompt, system_prompt=system_prompt)
        
        # Create the outline object
        outline = BlogOutline(
            topic=topic,
            outline=response,
            metadata={
                "audience": audience,
                "length": length,
                "content_type": content_type,
                "model": llm.model,
                "provider": llm.provider
            }
        )
        
        return outline
        
    except Exception as e:
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
