"""
Content Idea Generator App - Main Streamlit Application
"""
import streamlit as st
import re
from generators.blog_generator import generate_blog_outline
from generators.social_generator import generate_social_calendar
from generators.writing_generator import generate_writing_prompt


def sanitize_filename(text: str) -> str:
    """Sanitize text for use in filenames by removing or replacing unsafe characters"""
    # Replace spaces with underscores
    text = text.replace(' ', '_')
    # Remove or replace characters that are not alphanumeric, underscore, or hyphen
    text = re.sub(r'[^\w\-]', '', text)
    # Limit length to avoid overly long filenames
    return text[:100]

# Page configuration
st.set_page_config(
    page_title="Content Generator",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #155a8a;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Header
    st.markdown('<div class="main-header">💻 Content Idea Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-powered content creation with custom knowledge base using local LLMs</div>', unsafe_allow_html=True)
    
    # Sidebar - Generator Selection (for now just Blog)
    with st.sidebar:
        st.header("🎯 Content Tools")
        generator_type = st.radio(
            "Choose tool:",
            ["📝 Tech Blog Outline", "📱 Social Media Calendar", "✨ Creative Writing Prompts"],
            index=0
        )
        
        st.markdown("---")
        st.subheader("🤖 Model Selection")
        
        # Get available models
        try:
            from utils.llm_interface import llm, LocalLLM
            
            available_models = LocalLLM.get_available_models()
            
            if available_models:
                # Model selector
                selected_model = st.selectbox(
                    "Choose Model:",
                    options=available_models,
                    index=available_models.index(llm.model) if llm.model in available_models 
                          else (available_models.index(f"{llm.model}:latest") if f"{llm.model}:latest" in available_models else 0),
                    help="Select which local model to use for generation"
                )
                
                # Store in session state
                st.session_state['selected_model'] = selected_model
                
                # Display model info
                st.caption(f"Provider: {llm.provider}")
                
                # Refresh button
                if st.button("🔄 Refresh Models"):
                    st.rerun()
            else:
                st.warning(f"⚠️ Could not load models from {llm.provider}")
                st.caption("Make sure your LLM service is running")
                st.session_state['selected_model'] = None
        except Exception as e:
            st.error(f"Error loading models: {str(e)}")
            st.session_state['selected_model'] = None
        
        st.markdown("---")
        st.subheader("ℹ️ About")
        st.info(
            "This app uses local AI models (Ollama/LM Studio) to generate "
            "content ideas. No data is sent to external APIs!"
        )
    
    # Main content area
    if "Tech Blog Outline" in generator_type:
        render_blog_generator()
    elif "Social Media Calendar" in generator_type:
        render_social_generator()
    elif "Creative Writing Prompts" in generator_type:
        render_writing_generator()
    else:
        st.info("🚧 This feature is coming soon! Stay tuned.")


def render_blog_generator():
    """Render the blog post outline generator interface"""
    
    st.header("📝 Tech Blog Outline Generator")
    st.markdown("Generate SEO-friendly technical blog post outlines with headlines, structure, and key points.")
    
    # Input form
    with st.form("blog_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input(
                "📌 Topic / Keyword Focus",
                placeholder="e.g., Getting Started with Python Programming",
                help="The main topic or keyword for your blog post"
            )
            
            audience = st.selectbox(
                "👥 Target Audience",
                ["beginners", "intermediate", "experts"],
                index=1,
                help="Who is your target reader?"
            )
        
        with col2:
            length = st.selectbox(
                "📏 Content Length",
                ["short", "medium", "long"],
                index=1,
                help="Short: 800-1200 words | Medium: 1500-2000 words | Long: 2500-3500 words"
            )
            
            content_type = st.selectbox(
                "📄 Content Type",
                ["tutorial", "listicle", "how-to", "opinion"],
                index=2,
                help="What type of blog post are you writing?"
            )
        
        # Custom context input (full width)
        custom_context = st.text_area(
            "📚 Custom Context (Optional)",
            placeholder="Add any specific information, requirements, or context for your blog post...",
            help="Provide additional context that will be used to customize your blog outline",
            height=100
        )
        
        # Submit button
        submitted = st.form_submit_button("🚀 Generate Blog Outline")
    
    # Show example
    with st.expander("💡 See Example Tech Topics"):
        st.markdown("""
        - **Backend:** "Building a RESTful API with FastAPI and PostgreSQL"
        - **DevOps:** "Complete Guide to CI/CD with GitHub Actions"
        - **Frontend:** "State Management in React: Redux vs Context API"
        - **Cloud:** "Deploying Microservices on AWS EKS"
        - **AI/ML:** "Fine-tuning Large Language Models for Production"
        - **Security:** "Implementing OAuth 2.0 in Modern Web Applications"
        """)
    
    # Process form submission
    if submitted:
        if not topic or len(topic.strip()) < 3:
            st.error("⚠️ Please enter a valid topic (at least 3 characters)")
            return
        
        # Generate outline
        with st.spinner("🤔 Generating your tech blog outline... This may take 10-30 seconds"):
            try:
                # Get selected model from session state
                selected_model = st.session_state.get('selected_model', None)
                
                result = generate_blog_outline(
                    topic=topic.strip(),
                    audience=audience,
                    length=length,
                    content_type=content_type,
                    custom_context=custom_context.strip() if custom_context else None,
                    model_override=selected_model
                )
                
                # Store in session state
                st.session_state['last_result'] = result
                st.session_state['last_type'] = 'blog'
                
                # Success message
                st.success("✅ Blog outline generated successfully!")
                
                # Display result
                display_blog_result(result)
                
            except Exception as e:
                st.error(f"❌ Error generating outline: {str(e)}")
                st.info("""
                **Troubleshooting:**
                - Ensure Ollama is running (`ollama list` to verify)
                - Check your `.env` file configuration
                - Verify the model is available
                - Try a simpler topic if the generation fails
                """)
    
    # Display previous result if exists
    elif 'last_result' in st.session_state and st.session_state.get('last_type') == 'blog':
        st.info("📋 Showing previous result. Generate a new one using the form above.")
        display_blog_result(st.session_state['last_result'])


def display_blog_result(result):
    """Display the generated blog outline"""
    
    st.markdown("---")
    st.subheader("📄 Generated Outline")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📖 Formatted View", "📝 Markdown", "ℹ️ Metadata"])
    
    with tab1:
        # Display the outline in a nice format
        st.markdown(result.outline)
        
        # Copy button
        st.download_button(
            label="💾 Download as Markdown",
            data=result.to_markdown(),
            file_name=f"blog_outline_{sanitize_filename(result.topic)}.md",
            mime="text/markdown"
        )
    
    with tab2:
        # Raw markdown view with copy functionality
        st.code(result.to_markdown(), language="markdown")
        
        # Text area for easy copying
        st.text_area(
            "Copy the outline below:",
            value=result.to_markdown(),
            height=300,
            help="Select all (Ctrl+A) and copy (Ctrl+C)"
        )
    
    with tab3:
        # Display metadata
        st.json(result.metadata)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Audience", result.metadata['audience'].title())
            st.metric("Content Type", result.metadata['content_type'].title())
        with col2:
            st.metric("Length", result.metadata['length'].title())
            st.metric("Model", result.metadata['model'])


def render_social_generator():
    """Render the social media calendar generator interface"""
    
    st.header("📱 Social Media Calendar Generator")
    st.markdown("Generate platform-optimized social media content calendars with post ideas, engagement prompts, and hashtags.")
    
    # Input form
    with st.form("social_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            theme = st.text_input(
                "🎨 Theme",
                placeholder="e.g., Artificial Intelligence and Machine Learning",
                help="The main theme for your social media content"
            )
            
            platform = st.selectbox(
                "📱 Platform",
                ["LinkedIn", "Twitter", "Instagram", "Facebook", "TikTok"],
                index=0,
                help="Which social media platform are you targeting?"
            )
            
            frequency = st.selectbox(
                "📅 Frequency",
                ["daily", "3x week", "2x week", "weekly"],
                index=1,
                help="How often do you want to post?"
            )
        
        with col2:
            timeframe = st.selectbox(
                "⏰ Timeframe",
                ["week", "month", "quarter"],
                index=1,
                help="What time period should the calendar cover?"
            )
            
            tone = st.selectbox(
                "🎭 Tone",
                ["professional", "casual", "friendly", "educational", "inspirational", "humorous"],
                index=0,
                help="What tone should your content have?"
            )
        
        # Submit button
        submitted = st.form_submit_button("🚀 Generate Social Calendar")
    
    # Show example
    with st.expander("💡 See Example Themes"):
        st.markdown("""
        - **Tech/AI:** "Artificial Intelligence and Machine Learning Trends"
        - **Marketing:** "Digital Marketing Tips for Small Businesses"
        - **Productivity:** "Remote Work and Productivity Hacks"
        - **Health:** "Fitness and Wellness Journey"
        - **Business:** "Entrepreneurship and Startup Insights"
        - **Design:** "UI/UX Design Best Practices"
        """)
    
    # Process form submission
    if submitted:
        if not theme or len(theme.strip()) < 3:
            st.error("⚠️ Please enter a valid theme (at least 3 characters)")
            return
        
        # Generate calendar
        with st.spinner("🤔 Generating your social media calendar... This may take 10-30 seconds"):
            try:
                # Get selected model from session state
                selected_model = st.session_state.get('selected_model', None)
                
                result = generate_social_calendar(
                    theme=theme.strip(),
                    platform=platform,
                    frequency=frequency,
                    timeframe=timeframe,
                    tone=tone,
                    model_override=selected_model
                )
                
                # Store in session state
                st.session_state['last_result'] = result
                st.session_state['last_type'] = 'social'
                
                # Success message
                st.success("✅ Social media calendar generated successfully!")
                
                # Display result
                display_social_result(result)
                
            except Exception as e:
                st.error(f"❌ Error generating calendar: {str(e)}")
                st.info("""
                **Troubleshooting:**
                - Ensure Ollama is running (`ollama list` to verify)
                - Check your `.env` file configuration
                - Verify the model is available
                - Try a simpler theme if the generation fails
                """)
    
    # Display previous result if exists
    elif 'last_result' in st.session_state and st.session_state.get('last_type') == 'social':
        st.info("📋 Showing previous result. Generate a new one using the form above.")
        display_social_result(st.session_state['last_result'])


def display_social_result(result):
    """Display the generated social media calendar"""
    
    st.markdown("---")
    st.subheader("📄 Generated Calendar")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📖 Formatted View", "📝 Markdown", "ℹ️ Metadata"])
    
    with tab1:
        # Display the calendar in a nice format
        st.markdown(result.calendar)
        
        # Copy button
        st.download_button(
            label="💾 Download as Markdown",
            data=result.to_markdown(),
            file_name=f"social_calendar_{sanitize_filename(result.theme)}.md",
            mime="text/markdown"
        )
    
    with tab2:
        # Raw markdown view with copy functionality
        st.code(result.to_markdown(), language="markdown")
        
        # Text area for easy copying
        st.text_area(
            "Copy the calendar below:",
            value=result.to_markdown(),
            height=300,
            help="Select all (Ctrl+A) and copy (Ctrl+C)"
        )
    
    with tab3:
        # Display metadata
        st.json(result.metadata)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Platform", result.metadata['platform'])
            st.metric("Frequency", result.metadata['frequency'])
            st.metric("Timeframe", result.metadata['timeframe'])
        with col2:
            st.metric("Tone", result.metadata['tone'].title())
            st.metric("Model", result.metadata['model'])
            if 'provider' in result.metadata:
                st.metric("Provider", result.metadata['provider'])


def render_writing_generator():
    """Render the creative writing prompt generator interface"""
    
    st.header("✨ Creative Writing Prompt Generator")
    st.markdown("Generate original, inspiring creative writing prompts with rich details, character ideas, and plot directions.")
    
    # Input form
    with st.form("writing_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            genre = st.selectbox(
                "📚 Genre",
                ["sci-fi", "mystery", "romance", "fantasy", "horror", "thriller", "historical", "literary fiction", "adventure"],
                index=0,
                help="Choose your preferred writing genre"
            )
            
            prompt_type = st.selectbox(
                "🎯 Prompt Type",
                ["character", "plot", "world-building", "dialogue", "setting"],
                index=1,
                help="What aspect should the prompt focus on?"
            )
        
        with col2:
            complexity = st.selectbox(
                "📊 Complexity Level",
                ["simple", "moderate", "complex"],
                index=1,
                help="Simple: Straightforward prompts | Moderate: Multiple elements | Complex: Layered narratives"
            )
        
        # Constraints input (full width)
        constraints = st.text_area(
            "🔧 Additional Constraints (Optional)",
            placeholder="e.g., Must include a time travel element, Set in Victorian era, Include a mentor character...",
            help="Add specific requirements or elements you want in the prompt",
            height=80
        )
        
        # Submit button
        submitted = st.form_submit_button("🚀 Generate Writing Prompt")
    
    # Show example
    with st.expander("💡 See Example Prompt Ideas"):
        st.markdown("""
        **Character Prompts:**
        - "A retired superhero who discovers they're losing their powers"
        - "Twins separated at birth with opposing magical abilities"
        
        **Plot Prompts:**
        - "A murder mystery set on a generation ship"
        - "The last day before an apocalyptic event"
        
        **World-Building Prompts:**
        - "A society where memories can be bought and sold"
        - "A city built entirely in the canopy of giant trees"
        
        **Dialogue Prompts:**
        - "A conversation between a time traveler and their past self"
        - "Two enemies forced to work together"
        
        **Setting Prompts:**
        - "An abandoned theme park reclaimed by nature"
        - "A library that exists outside of time"
        """)
    
    # Process form submission
    if submitted:
        # Generate prompt
        with st.spinner("🤔 Crafting your creative writing prompt... This may take 10-30 seconds"):
            try:
                # Get selected model from session state
                selected_model = st.session_state.get('selected_model', None)
                
                result = generate_writing_prompt(
                    genre=genre,
                    prompt_type=prompt_type,
                    complexity=complexity,
                    constraints=constraints.strip() if constraints else None,
                    model_override=selected_model
                )
                
                # Store in session state
                st.session_state['last_result'] = result
                st.session_state['last_type'] = 'writing'
                
                # Success message
                st.success("✅ Writing prompt generated successfully!")
                
                # Display result
                display_writing_result(result)
                
            except Exception as e:
                st.error(f"❌ Error generating prompt: {str(e)}")
                st.info("""
                **Troubleshooting:**
                - Ensure Ollama is running (`ollama list` to verify)
                - Check your `.env` file configuration
                - Verify the model is available
                - Try without additional constraints if the generation fails
                """)
    
    # Display previous result if exists
    elif 'last_result' in st.session_state and st.session_state.get('last_type') == 'writing':
        st.info("📋 Showing previous result. Generate a new one using the form above.")
        display_writing_result(st.session_state['last_result'])


def display_writing_result(result):
    """Display the generated creative writing prompt"""
    
    st.markdown("---")
    st.subheader("📄 Generated Writing Prompt")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📖 Formatted View", "📝 Markdown", "ℹ️ Metadata"])
    
    with tab1:
        # Display the prompt in a nice format
        st.markdown(result.prompt)
        
        # Copy button
        st.download_button(
            label="💾 Download as Markdown",
            data=result.to_markdown(),
            file_name=f"writing_prompt_{sanitize_filename(result.genre)}.md",
            mime="text/markdown"
        )
    
    with tab2:
        # Raw markdown view with copy functionality
        st.code(result.to_markdown(), language="markdown")
        
        # Text area for easy copying
        st.text_area(
            "Copy the prompt below:",
            value=result.to_markdown(),
            height=300,
            help="Select all (Ctrl+A) and copy (Ctrl+C)"
        )
    
    with tab3:
        # Display metadata
        st.json(result.metadata)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Genre", result.genre.title())
            st.metric("Prompt Type", result.metadata['prompt_type'].title())
            st.metric("Complexity", result.metadata['complexity'].title())
        with col2:
            st.metric("Model", result.metadata['model'])
            st.metric("Provider", result.metadata['provider'])
            if result.metadata.get('constraints') and result.metadata['constraints'] != "None":
                st.metric("Constraints", "Yes")


if __name__ == "__main__":
    main()
