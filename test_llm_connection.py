"""
Test script for local LLM connection
Step 1.2: Verify that the LLM interface works correctly
"""
import sys
from utils.llm_interface import llm

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def main():
    print("=" * 60)
    print("Testing Local LLM Connection")
    print("=" * 60)
    print()
    
    # Test 1: Connection Test
    print("Test 1: Checking connection...")
    success, message = llm.test_connection()
    print(message)
    print()
    
    if not success:
        print("[WARNING] Please ensure your LLM is running:")
        print("  - For Ollama: Run 'ollama serve' or ensure it's auto-started")
        print("  - For LM Studio: Start the local server in the app")
        print()
        return
    
    # Test 2: Simple Generation Test
    print("Test 2: Testing text generation...")
    print("Sending prompt: 'Say hello in one sentence.'")
    print()
    
    try:
        response = llm.generate(
            prompt="Say hello in one sentence.",
            system_prompt="You are a helpful assistant."
        )
        
        print("[SUCCESS] Response received:")
        print("-" * 60)
        print(response)
        print("-" * 60)
        print()
        print("[PASS] All tests passed! LLM interface is working correctly.")
        print()
        print("Configuration:")
        print(f"  Provider: {llm.provider}")
        print(f"  Model: {llm.model}")
        print(f"  Base URL: {llm.base_url}")
        print(f"  Temperature: {llm.temperature}")
        print(f"  Max Tokens: {llm.max_tokens}")
        
    except Exception as e:
        print(f"[ERROR] Error during generation: {str(e)}")
        print()
        print("Troubleshooting:")
        print("  1. Check that your LLM server is running")
        print("  2. Verify the model name in your .env file")
        print("  3. Check the base URL is correct")


if __name__ == "__main__":
    main()
