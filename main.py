"""
Content Idea Generator App - Main Streamlit Application
"""
import streamlit as st
from generators.blog_generator import generate_blog_outline

# Page configuration
st.set_page_config(
    page_title="Tech Blog Generator",
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
    st.markdown('<div class="main-header">💻 Tech Blog Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-powered technical blog creation with custom knowledge base using local LLMs</div>', unsafe_allow_html=True)
    
    # Sidebar - Generator Selection (for now just Blog)
    with st.sidebar:
        st.header("🎯 Tech Blog Tools")
        generator_type = st.radio(
            "Choose tool:",
            ["📝 Tech Blog Outline", "📱 Social Media Calendar (Coming Soon)", "✨ Writing Prompts (Coming Soon)"],
            index=0
        )
        
        st.markdown("---")
        st.subheader("ℹ️ About")
        st.info(
            "This app uses local AI models (Ollama/LM Studio) to generate "
            "content ideas. No data is sent to external APIs!"
        )
        
        # Display current model info
        try:
            from utils.llm_interface import llm
            st.markdown("---")
            st.subheader("🤖 Current Model")
            st.text(f"Provider: {llm.provider}")
            st.text(f"Model: {llm.model}")
        except:
            pass
    
    # Main content area
    if "Tech Blog Outline" in generator_type:
        render_blog_generator()
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
                result = generate_blog_outline(
                    topic=topic.strip(),
                    audience=audience,
                    length=length,
                    content_type=content_type,
                    custom_context=custom_context.strip() if custom_context else None
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
            file_name=f"blog_outline_{result.topic.replace(' ', '_')}.md",
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


if __name__ == "__main__":
    main()
