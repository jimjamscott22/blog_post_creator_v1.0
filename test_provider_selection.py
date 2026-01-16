"""
Test script for provider selection functionality
Tests both Ollama and LM Studio provider configuration
"""
import os
from utils.llm_interface import LocalLLM
from config import settings

def test_provider_initialization():
    """Test that providers can be initialized correctly"""
    print("=" * 60)
    print("Testing Provider Initialization")
    print("=" * 60)
    
    # Test Ollama provider
    print("\n1. Testing Ollama provider...")
    try:
        ollama_llm = LocalLLM()
        ollama_llm.provider = "ollama"
        ollama_llm.base_url = settings.OLLAMA_BASE_URL
        ollama_llm.model = settings.OLLAMA_MODEL
        print(f"   ✓ Ollama initialized")
        print(f"   - Provider: {ollama_llm.provider}")
        print(f"   - Base URL: {ollama_llm.base_url}")
        print(f"   - Model: {ollama_llm.model}")
        
        # Test connection
        success, message = ollama_llm.test_connection()
        if success:
            print(f"   ✓ Connection test: {message}")
        else:
            print(f"   ✗ Connection test: {message}")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    # Test LM Studio provider
    print("\n2. Testing LM Studio provider...")
    try:
        lmstudio_llm = LocalLLM()
        lmstudio_llm.provider = "lm_studio"
        lmstudio_llm.base_url = settings.LM_STUDIO_BASE_URL
        lmstudio_llm.model = settings.LM_STUDIO_MODEL
        print(f"   ✓ LM Studio initialized")
        print(f"   - Provider: {lmstudio_llm.provider}")
        print(f"   - Base URL: {lmstudio_llm.base_url}")
        print(f"   - Model: {lmstudio_llm.model}")
        
        # Test connection
        success, message = lmstudio_llm.test_connection()
        if success:
            print(f"   ✓ Connection test: {message}")
        else:
            print(f"   ✗ Connection test: {message}")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")

def test_model_listing():
    """Test fetching available models from both providers"""
    print("\n" + "=" * 60)
    print("Testing Model Listing")
    print("=" * 60)
    
    # Test Ollama models
    print("\n1. Fetching Ollama models...")
    try:
        ollama_models = LocalLLM.get_available_models(provider="ollama")
        if ollama_models:
            print(f"   ✓ Found {len(ollama_models)} Ollama model(s):")
            for model in ollama_models[:5]:  # Show first 5
                print(f"      - {model}")
            if len(ollama_models) > 5:
                print(f"      ... and {len(ollama_models) - 5} more")
        else:
            print(f"   ✗ No Ollama models found (is Ollama running?)")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    # Test LM Studio models
    print("\n2. Fetching LM Studio models...")
    try:
        lmstudio_models = LocalLLM.get_available_models(provider="lm_studio")
        if lmstudio_models:
            print(f"   ✓ Found {len(lmstudio_models)} LM Studio model(s):")
            for model in lmstudio_models[:5]:  # Show first 5
                print(f"      - {model}")
            if len(lmstudio_models) > 5:
                print(f"      ... and {len(lmstudio_models) - 5} more")
        else:
            print(f"   ✗ No LM Studio models found (is LM Studio server running?)")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")

def test_provider_override():
    """Test using provider_override in generators"""
    print("\n" + "=" * 60)
    print("Testing Provider Override")
    print("=" * 60)
    
    # This would normally be done by the generators
    print("\n1. Testing provider override mechanism...")
    try:
        # Create an LLM instance
        llm = LocalLLM()
        original_provider = llm.provider
        print(f"   ✓ Original provider: {original_provider}")
        
        # Override to different provider
        new_provider = "lm_studio" if original_provider == "ollama" else "ollama"
        llm.provider = new_provider
        
        if new_provider == "ollama":
            llm.base_url = settings.OLLAMA_BASE_URL
            llm.model = settings.OLLAMA_MODEL
        else:
            llm.base_url = settings.LM_STUDIO_BASE_URL
            llm.model = settings.LM_STUDIO_MODEL
        
        print(f"   ✓ Override successful:")
        print(f"      - New provider: {llm.provider}")
        print(f"      - New base URL: {llm.base_url}")
        print(f"      - New model: {llm.model}")
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "LLM PROVIDER SELECTION TEST SUITE" + " " * 14 + "║")
    print("╚" + "=" * 58 + "╝")
    
    print("\nCurrent configuration:")
    print(f"  Default Provider: {settings.LLM_PROVIDER}")
    print(f"  Ollama URL: {settings.OLLAMA_BASE_URL}")
    print(f"  Ollama Model: {settings.OLLAMA_MODEL}")
    print(f"  LM Studio URL: {settings.LM_STUDIO_BASE_URL}")
    print(f"  LM Studio Model: {settings.LM_STUDIO_MODEL}")
    
    # Run tests
    test_provider_initialization()
    test_model_listing()
    test_provider_override()
    
    print("\n" + "=" * 60)
    print("Test suite completed!")
    print("=" * 60)
    print("\n✓ If both providers showed connection errors, make sure at least")
    print("  one LLM service (Ollama or LM Studio) is running.\n")
    print("✓ The provider selection feature is working if you can see both")
    print("  providers initialize without errors.\n")

if __name__ == "__main__":
    main()
