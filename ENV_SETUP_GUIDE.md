# Environment Configuration Guide

## Create Your .env File

Create a file named `.env` in the project root with the following content:

### For Ollama (Recommended):

```env
# LLM Provider Configuration
LLM_PROVIDER=ollama

# Ollama Settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Generation Settings
MAX_TOKENS=2000
TEMPERATURE=0.7
```

### For LM Studio:

```env
# LLM Provider Configuration
LLM_PROVIDER=lm_studio

# LM Studio Settings
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=local-model

# Generation Settings
MAX_TOKENS=2000
TEMPERATURE=0.7
```

## Available Models

### Ollama Models (Popular choices):
- `llama3.2` - Latest Llama model (3B or 1B)
- `llama3.1` - Llama 3.1 (8B, 70B, or 405B)
- `mistral` - Mistral 7B
- `phi3` - Microsoft Phi-3
- `codellama` - Code-specialized Llama
- `gemma2` - Google's Gemma 2

To install a model with Ollama:
```bash
ollama pull llama3.2
```

### LM Studio Models:
- Any model you've downloaded in LM Studio
- The model name can usually be `local-model` or check LM Studio's server settings

## Settings Explanation

| Setting | Description | Recommended Value |
|---------|-------------|-------------------|
| `LLM_PROVIDER` | Which LLM to use | `ollama` or `lm_studio` |
| `OLLAMA_BASE_URL` | Ollama server address | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model name | `llama3.2` |
| `LM_STUDIO_BASE_URL` | LM Studio server address | `http://localhost:1234/v1` |
| `LM_STUDIO_MODEL` | Model name in LM Studio | `local-model` |
| `MAX_TOKENS` | Maximum response length | `2000` |
| `TEMPERATURE` | Creativity level (0-1) | `0.7` |

## Quick Copy-Paste (Ollama):

Save this as `.env` in your project root:

```
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
MAX_TOKENS=2000
TEMPERATURE=0.7
```
