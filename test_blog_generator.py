"""
Test script for Blog Generator
Step 1.3: Test the blog outline generation functionality
"""
import sys
from generators.blog_generator import generate_blog_outline

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def main():
    print("=" * 60)
    print("Testing Blog Outline Generator")
    print("=" * 60)
    print()
    
    # Test parameters
    test_topic = "Getting Started with Local AI Models"
    test_audience = "beginners"
    test_length = "medium"
    test_type = "tutorial"
    
    print(f"Topic: {test_topic}")
    print(f"Audience: {test_audience}")
    print(f"Length: {test_length}")
    print(f"Type: {test_type}")
    print()
    print("Generating blog outline... (this may take 10-30 seconds)")
    print()
    
    try:
        # Generate the outline
        result = generate_blog_outline(
            topic=test_topic,
            audience=test_audience,
            length=test_length,
            content_type=test_type
        )
        
        print("[SUCCESS] Blog outline generated!")
        print("=" * 60)
        print()
        print(result.to_markdown())
        print()
        print("=" * 60)
        print()
        print("Metadata:")
        print(f"  Model: {result.metadata['model']}")
        print(f"  Provider: {result.metadata['provider']}")
        print(f"  Audience: {result.metadata['audience']}")
        print(f"  Length: {result.metadata['length']}")
        print(f"  Type: {result.metadata['content_type']}")
        print()
        print("[PASS] Blog generator is working correctly!")
        
    except Exception as e:
        print(f"[ERROR] Failed to generate outline: {str(e)}")
        print()
        print("Troubleshooting:")
        print("  1. Ensure Ollama is running")
        print("  2. Check your .env configuration")
        print("  3. Verify the model is available")


if __name__ == "__main__":
    main()
