"""
Creative Writing Prompt Generator
"""
from typing import Optional
from pydantic import BaseModel, Field
from utils.llm_interface import llm, LocalLLM
from utils.prompt_templates import get_writing_prompt_template
from utils.logger import setup_logger

# Set up logger
logger = setup_logger(__name__)


class WritingPromptInput(BaseModel):
    """Input parameters for creative writing prompt generation"""
    genre: str = Field(..., min_length=1, description="Genre preference")
    prompt_type: str = Field(default="plot", description="Type of prompt")
    complexity: str = Field(default="moderate", description="Complexity level")
    constraints: Optional[str] = Field(default=None, description="Additional constraints")
    
    class Config:
        # Valid options for each field
        json_schema_extra = {
            "example": {
                "genre": "sci-fi",
                "prompt_type": "character",
                "complexity": "moderate",
                "constraints": "Must include a time travel element"
            }
        }


class WritingPrompt(BaseModel):
    """Generated creative writing prompt"""
    genre: str
    prompt: str
    metadata: dict
    
    def to_markdown(self) -> str:
        """Convert to formatted markdown"""
        md = f"# Creative Writing Prompt: {self.genre.title()}\n\n"
        md += self.prompt
        return md


def generate_writing_prompt(
    genre: str,
    prompt_type: str = "plot",
    complexity: str = "moderate",
    constraints: Optional[str] = None,
    model_override: Optional[str] = None,
    provider_override: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None
) -> WritingPrompt:
    """
    Generate a creative writing prompt using the local LLM
    
    Args:
        genre: Genre preference (sci-fi, mystery, romance, fantasy, horror, thriller, historical, literary fiction, adventure)
        prompt_type: Type of prompt (character, plot, world-building, dialogue, setting)
        complexity: Complexity level (simple, moderate, complex)
        constraints: Optional additional constraints or requirements
        model_override: Optional specific model to use (overrides default)
        provider_override: Optional provider to use ('ollama' or 'lm_studio')
        temperature: Optional temperature setting (0.0-2.0)
        max_tokens: Optional max tokens for response
    
    Returns:
        WritingPrompt object with generated content
    
    Raises:
        ValueError: If parameters are invalid
        Exception: If generation fails
    """
    
    logger.info(f"Generating writing prompt for genre: '{genre}'")
    logger.debug(f"Parameters - prompt_type: {prompt_type}, complexity: {complexity}, constraints: {constraints}")
    if model_override:
        logger.debug(f"Using model override: {model_override}")
    if provider_override:
        logger.debug(f"Using provider override: {provider_override}")
    
    # Validate inputs
    valid_genres = ["sci-fi", "mystery", "romance", "fantasy", "horror", "thriller", "historical", "literary fiction", "adventure"]
    valid_prompt_types = ["character", "plot", "world-building", "dialogue", "setting"]
    valid_complexity = ["simple", "moderate", "complex"]
    
    if genre.lower() not in valid_genres:
        logger.error(f"Invalid genre: {genre}")
        raise ValueError(f"Genre must be one of: {', '.join(valid_genres)}")
    
    if prompt_type.lower() not in valid_prompt_types:
        logger.error(f"Invalid prompt type: {prompt_type}")
        raise ValueError(f"Prompt type must be one of: {', '.join(valid_prompt_types)}")
    
    if complexity.lower() not in valid_complexity:
        logger.error(f"Invalid complexity: {complexity}")
        raise ValueError(f"Complexity must be one of: {', '.join(valid_complexity)}")
    
    # Generate the prompt
    prompt = get_writing_prompt_template(genre, prompt_type, complexity, constraints)
    logger.debug(f"Prompt generated successfully (length: {len(prompt)} chars)")
    
    # System prompt for consistent output
    system_prompt = """You are a creative writing expert and professional author.
You create inspiring, detailed creative writing prompts that spark imagination and encourage unique storytelling.
Your prompts are specific enough to provide direction but open enough to allow creative freedom.
Always include rich details about characters, settings, conflicts, and potential story directions."""
    
    try:
        # Use overrides if provided, otherwise use default
        llm_instance = LocalLLM(model_override=model_override, temperature=temperature, max_tokens=max_tokens) if model_override or temperature is not None or max_tokens is not None else llm
        
        # Override provider if specified
        if provider_override:
            from config import settings
            llm_instance.provider = provider_override
            if provider_override == "ollama":
                llm_instance.base_url = settings.OLLAMA_BASE_URL
                if not model_override:
                    llm_instance.model = settings.OLLAMA_MODEL
            elif provider_override == "lm_studio":
                llm_instance.base_url = settings.LM_STUDIO_BASE_URL
                if not model_override:
                    llm_instance.model = settings.LM_STUDIO_MODEL
        
        # Update temperature and max_tokens if provided
        if temperature is not None:
            llm_instance.temperature = temperature
        if max_tokens is not None:
            llm_instance.max_tokens = max_tokens
        
        # Generate the writing prompt
        logger.info("Sending request to LLM...")
        response = llm_instance.generate(prompt=prompt, system_prompt=system_prompt)
        logger.info("Successfully received response from LLM")
        
        # Create the prompt object
        writing_prompt = WritingPrompt(
            genre=genre,
            prompt=response,
            metadata={
                "prompt_type": prompt_type,
                "complexity": complexity,
                "constraints": constraints if constraints else "None",
                "model": llm_instance.model,
                "provider": llm_instance.provider
            }
        )
        
        logger.info(f"Writing prompt created successfully for '{genre}'")
        return writing_prompt
        
    except Exception as e:
        logger.error(f"Failed to generate writing prompt: {str(e)}")
        raise Exception(f"Failed to generate writing prompt: {str(e)}")


def validate_writing_input(data: dict) -> WritingPromptInput:
    """
    Validate writing prompt input data using Pydantic
    
    Args:
        data: Dictionary with writing prompt input parameters
    
    Returns:
        Validated WritingPromptInput object
    
    Raises:
        ValidationError: If data is invalid
    """
    return WritingPromptInput(**data)
