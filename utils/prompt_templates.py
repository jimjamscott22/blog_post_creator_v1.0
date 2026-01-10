"""
Prompt templates for different content generators
"""


def get_blog_outline_prompt(topic: str, audience: str, length: str, content_type: str, custom_context: str = None) -> str:
    """
    Generate a prompt for creating a blog post outline
    
    Args:
        topic: The main topic/keyword focus
        audience: Target audience level (beginners, intermediate, experts)
        length: Desired length (short, medium, long)
        content_type: Type of content (tutorial, listicle, how-to, opinion)
        custom_context: Optional custom information to incorporate
    
    Returns:
        Formatted prompt string
    """
    
    # Map length to word counts for clarity
    length_guide = {
        "short": "800-1200 words (5-7 minute read)",
        "medium": "1500-2000 words (8-12 minute read)",
        "long": "2500-3500 words (15-20 minute read)"
    }
    
    length_description = length_guide.get(length.lower(), "1500-2000 words")
    
    # Add custom context section if provided
    context_section = ""
    if custom_context and custom_context.strip():
        context_section = f"""\n\nCUSTOM CONTEXT/KNOWLEDGE BASE:
{custom_context}

IMPORTANT: Use the information from the custom context above to make the blog outline more specific, 
accurate, and relevant. Reference specific features, technologies, or details mentioned in the context.
"""
    
    prompt = f"""Create a comprehensive technical blog post outline about "{topic}" for {audience} readers.{context_section}

Content Type: {content_type}
Target Length: {length_description}

Please provide:

1. HEADLINES (5-7 options):
   - SEO-friendly and attention-grabbing
   - Include power words and numbers where appropriate
   - Each should be under 70 characters

2. STRUCTURED OUTLINE:
   - Introduction (with hook and what readers will learn)
   - Main sections (3-5 major sections with descriptive headers)
   - Each section should have 2-4 key points to cover
   - Conclusion (summary and call-to-action)

3. KEY POINTS:
   - Important facts, statistics, or examples to include
   - Common pain points to address
   - Actionable takeaways

4. SUBTOPICS:
   - Related topics to mention or link to
   - Supporting concepts to explain

Format the output clearly with headers and bullet points. Make it actionable and ready to use for writing."""
    
    return prompt


def get_social_media_prompt(theme: str, frequency: str, platform: str, 
                            timeframe: str, tone: str) -> str:
    """
    Generate a prompt for creating a social media calendar
    
    Args:
        theme: Content theme/category
        frequency: Posting frequency (daily, 3x week, weekly)
        platform: Platform focus (Twitter, LinkedIn, Instagram)
        timeframe: Time period (week, month, quarter)
        tone: Brand voice/tone preferences
    
    Returns:
        Formatted prompt string
    """
    
    prompt = f"""Create a social media content calendar about "{theme}" for {platform}.

Posting Frequency: {frequency}
Time Period: {timeframe}
Brand Voice: {tone}

Please provide:

1. CONTENT IDEAS:
   - Specific post ideas with suggested dates
   - Mix of content types (educational, entertaining, promotional)
   - Each post should align with {tone} tone

2. POST FORMATS:
   - Specify format: text post, image post, video, thread, carousel, etc.
   - Suggested content structure for each post

3. ENGAGEMENT PROMPTS:
   - Questions to ask the audience
   - Calls-to-action that drive engagement
   - Interactive elements (polls, challenges, etc.)

4. HASHTAG RECOMMENDATIONS:
   - Relevant hashtags for each post
   - Mix of popular and niche tags
   - Platform-optimized suggestions

Format each post idea as:
[Date/Day]: [Post Type] - [Content Idea]
Caption/Hook: [Engaging first line]
Engagement Prompt: [Question or CTA]
Hashtags: [Relevant tags]"""
    
    return prompt


def get_writing_prompt_template(genre: str, prompt_type: str, 
                                complexity: str, constraints: str = None) -> str:
    """
    Generate a prompt for creating creative writing prompts
    
    Args:
        genre: Genre preference (sci-fi, mystery, romance, fantasy)
        prompt_type: Type of prompt (character, plot, world-building)
        complexity: Complexity level (simple, moderate, complex)
        constraints: Additional constraints (optional)
    
    Returns:
        Formatted prompt string
    """
    
    constraint_text = f"\nAdditional Constraints: {constraints}" if constraints else ""
    
    prompt = f"""Create an original creative writing prompt for {genre} genre.

Prompt Type: {prompt_type}
Complexity Level: {complexity}{constraint_text}

Please provide:

1. MAIN PROMPT:
   - An engaging scenario or concept
   - Clear conflict or tension
   - Specific details that spark imagination

2. CHARACTER ELEMENTS (if relevant):
   - Character archetypes or traits
   - Motivations and goals
   - Relationships or dynamics

3. SETTING DETAILS:
   - Time period and location
   - Atmospheric elements
   - World-building considerations

4. PLOT DIRECTIONS:
   - Potential story arcs
   - Twist possibilities
   - Conflict escalation ideas

5. DEVELOPMENT QUESTIONS:
   - Questions to help writers explore the prompt
   - Themes to consider
   - Possible challenges for characters

Make the prompt specific enough to be inspiring but open enough for creative interpretation."""
    
    return prompt
