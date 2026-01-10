# Setup Instructions

## Step 1: Install Local LLM (Choose One)

### Option A: Ollama (Recommended - Easier)

1. **Download Ollama:**
   - Windows: https://ollama.com/download/windows
   - Mac: https://ollama.com/download/mac
   - Linux: `curl -fsSL https://ollama.com/install.sh | sh`

2. **Install a Model:**
   ```bash
   ollama pull llama3.2
   ```
   
   Or try other models:
   ```bash
   ollama pull mistral
   ollama pull phi3
   ```

3. **Verify Ollama is Running:**
   ```bash
   ollama list
   ```

### Option B: LM Studio

1. **Download LM Studio:**
   - Go to https://lmstudio.ai/
   - Download for your OS (Windows/Mac/Linux)
   - Install and launch

2. **Download a Model:**
   - In LM Studio, go to the Search tab
   - Download a model (e.g., "Mistral-7B", "Llama-3.2")
   - Wait for download to complete

3. **Start the Server:**
   - Go to "Local Server" tab in LM Studio
   - Click "Start Server"
   - Default port: 1234

## Step 2: Create Virtual Environment

```bash
python -m venv venv
```

## Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 5: Configure Environment Variables

Create a `.env` file in the project root:

**For Ollama:**
```
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
MAX_TOKENS=2000
TEMPERATURE=0.7
```

**For LM Studio:**
```
LLM_PROVIDER=lm_studio
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=local-model
MAX_TOKENS=2000
TEMPERATURE=0.7
```

## Step 6: Test Your Setup

Once your local LLM is running and configured, you're ready to move to Step 1.2!

## Quick Start Commands

**Start Ollama (if not auto-started):**
```bash
ollama serve
```

**Test Ollama:**
```bash
ollama run llama3.2 "Hello, how are you?"
```

**Check if LM Studio server is running:**
Visit http://localhost:1234/v1/models in your browser

## Step 7: Launch the Tech Blog Generator

Once everything is set up, activate your virtual environment and launch the web UI:

```bash
source venv/bin/activate
streamlit run main.py
```

The app will open in your browser at http://localhost:8501 (or 8502 if 8501 is in use).

## Using the Custom Knowledge Base

The Tech Blog Generator includes a powerful **Custom Knowledge Base** feature:

1. Click the "📚 Custom Knowledge Base (Optional)" expander
2. Add any technical information you want the AI to reference:
   - API documentation
   - Technical specifications
   - Product features
   - Code examples
   - Company-specific terminology
3. Generate your blog outline - the AI will incorporate your custom context

**Example:** If you're writing about "Building a REST API" and provide FastAPI documentation in the knowledge base, the generated outline will reference specific FastAPI features and best practices.
