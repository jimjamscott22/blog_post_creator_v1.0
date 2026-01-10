"""
LLM Interface for local model inference
Supports both Ollama and LM Studio
"""
import requests
import json
from typing import Optional
from config import settings
from utils.logger import setup_logger

# Set up logger
logger = setup_logger(__name__)


class LocalLLM:
    """Wrapper for local LLM inference"""
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        
        if self.provider == "ollama":
            self.base_url = settings.OLLAMA_BASE_URL
            self.model = settings.OLLAMA_MODEL
        elif self.provider == "lm_studio":
            self.base_url = settings.LM_STUDIO_BASE_URL
            self.model = settings.LM_STUDIO_MODEL
        else:
            logger.error(f"Unsupported LLM provider: {self.provider}")
            raise ValueError(f"Unsupported provider: {self.provider}")
        
        logger.info(f"Initialized LocalLLM with provider: {self.provider}, model: {self.model}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text completion from the local LLM
        
        Args:
            prompt: The user prompt/question
            system_prompt: Optional system prompt for context
            
        Returns:
            Generated text response
        """
        logger.debug(f"Generating response using {self.provider}")
        try:
            if self.provider == "ollama":
                return self._generate_ollama(prompt, system_prompt)
            elif self.provider == "lm_studio":
                return self._generate_lm_studio(prompt, system_prompt)
        except requests.exceptions.ConnectionError:
            logger.error(f"Could not connect to {self.provider}")
            raise ConnectionError(
                f"Could not connect to {self.provider}. "
                f"Please ensure {self.provider} is running."
            )
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise Exception(f"Error generating response: {str(e)}")
    
    def _generate_ollama(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using Ollama API"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "").strip()
    
    def _generate_lm_studio(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using LM Studio OpenAI-compatible API"""
        url = f"{self.base_url}/chat/completions"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    
    def test_connection(self) -> tuple[bool, str]:
        """
        Test connection to the LLM
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if self.provider == "ollama":
                # Test Ollama connection
                response = requests.get(f"{self.base_url}/api/tags", timeout=5)
                response.raise_for_status()
                models = response.json().get("models", [])
                model_names = [m.get("name") for m in models]
                
                if self.model in model_names:
                    return True, f"[OK] Connected to Ollama. Model '{self.model}' is available."
                else:
                    return False, f"[ERROR] Model '{self.model}' not found. Available: {', '.join(model_names)}"
            
            elif self.provider == "lm_studio":
                # Test LM Studio connection
                response = requests.get(f"{self.base_url}/models", timeout=5)
                response.raise_for_status()
                return True, f"[OK] Connected to LM Studio server."
            
        except requests.exceptions.ConnectionError:
            return False, f"[ERROR] Cannot connect to {self.provider}. Is it running?"
        except Exception as e:
            return False, f"[ERROR] Error: {str(e)}"


# Create a singleton instance
llm = LocalLLM()
