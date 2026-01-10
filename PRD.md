# Content Idea Generator - Product Requirements Document

## 1. What We're Building

A Python web app that helps content creators generate:
- Blog post outlines with SEO headlines
- Social media content calendars  
- Creative writing prompts

**Tech Stack:**
- **Frontend:** Streamlit (fastest to prototype, Python-based)
- **Backend:** Python
- **AI:** Local LLMs (Ollama or LM Studio) - No API costs!
- **Environment:** python-dotenv for config management

## 2. Success Criteria

✅ User can input parameters and get AI-generated content in <10 seconds  
✅ Output is coherent, actionable, and properly formatted  
✅ User can easily copy results  
✅ Clean, intuitive UI that doesn't require documentation

## 3. Implementation Steps

### **PHASE 1: Foundation & MVP (Blog Generator)**

#### Step 1.1: Environment Setup
- [ ] Create project structure with folders
- [ ] Set up virtual environment
- [ ] Create requirements.txt with dependencies
- [ ] Create .env.example for API key template
- [ ] Create .gitignore

**Deliverable:** Project skeleton ready for coding

---

#### Step 1.2: Basic Local LLM Connection Test
- [x] Create config/settings.py to load environment variables
- [x] Create utils/llm_interface.py with local LLM support (Ollama/LM Studio)
- [x] Write test script to verify LLM connection works
- [x] Handle connection errors gracefully
- [ ] User runs test and confirms connection

**Deliverable:** Confirmed working local LLM connection

---

#### Step 1.3: Blog Generator Backend
- [ ] Create generators/blog_generator.py
- [ ] Define input data model (topic, audience, length, format)
- [ ] Create prompt template for blog outlines
- [ ] Implement generate_blog_outline() function
- [ ] Parse and structure LLM response

**Deliverable:** Working Python function that generates blog outlines

---

#### Step 1.4: Basic Streamlit UI for Blog Generator
- [ ] Create main.py with Streamlit app structure
- [ ] Add title and description
- [ ] Create input form (text input, dropdowns for audience/length/format)
- [ ] Add "Generate" button
- [ ] Display output in formatted text area
- [ ] Add copy-to-clipboard functionality

**Deliverable:** Functional blog outline generator web app

---

#### Step 1.5: Test & Refine Blog Generator
- [ ] Test with 5+ different topics
- [ ] Verify output quality and format consistency
- [ ] Add loading spinner during generation
- [ ] Add error messages for failed generations
- [ ] Improve prompt if needed

**Deliverable:** Polished, tested blog generator

---

### **PHASE 2: Social Media Calendar Generator**

#### Step 2.1: Social Media Generator Backend
- [ ] Create generators/social_generator.py
- [ ] Define input data model (themes, frequency, platform, timeframe, tone)
- [ ] Create prompt template for social calendars
- [ ] Implement generate_social_calendar() function
- [ ] Format output with dates and structure

**Deliverable:** Working social media calendar generator function

---

#### Step 2.2: Add Social Media Tab to UI
- [ ] Add tab/section switcher in Streamlit (Blog vs Social)
- [ ] Create input form for social media parameters
- [ ] Display calendar output in readable format
- [ ] Add copy functionality
- [ ] Test with multiple scenarios

**Deliverable:** Two-feature app (Blog + Social Media)

---

### **PHASE 3: Creative Writing Prompt Generator**

#### Step 3.1: Writing Prompt Generator Backend
- [ ] Create generators/writing_generator.py
- [ ] Define input data model (genre, prompt type, complexity, constraints)
- [ ] Create prompt template for writing prompts
- [ ] Implement generate_writing_prompt() function

**Deliverable:** Working writing prompt generator function

---

#### Step 3.2: Add Writing Prompts Tab to UI
- [ ] Add third tab for creative writing
- [ ] Create input form for writing prompt parameters
- [ ] Display output with proper formatting
- [ ] Test with various genres and types

**Deliverable:** Three-feature complete app

---

### **PHASE 4: Enhancement & Polish**

#### Step 4.1: Export Functionality
- [ ] Add download buttons for each generator
- [ ] Implement text file export
- [ ] Add markdown export option
- [ ] Consider PDF export (optional)

**Deliverable:** Users can save generated content

---

#### Step 4.2: Generation History
- [ ] Add session state to store previous generations
- [ ] Create sidebar showing recent generations
- [ ] Allow users to switch between past results
- [ ] Add clear history button

**Deliverable:** Users can review previous generations

---

#### Step 4.3: UI/UX Polish
- [ ] Add custom CSS for better styling
- [ ] Improve layout and spacing
- [ ] Add helpful tooltips and instructions
- [ ] Add example inputs for each generator
- [ ] Create simple landing page with feature overview

**Deliverable:** Professional-looking, polished app

---

#### Step 4.4: Final Testing & Documentation
- [ ] Test all three generators thoroughly
- [ ] Write user guide in README
- [ ] Add setup instructions for other developers
- [ ] Create demo screenshots or video
- [ ] Add error handling edge cases

**Deliverable:** Production-ready app with documentation

---

## 4. File Structure

```
blog_post_creator_v1.0/
├── main.py                      # Streamlit app entry point
├── requirements.txt             # Python dependencies
├── .env                         # API keys (not in git)
├── .env.example                 # Template for .env
├── .gitignore                   # Git ignore file
├── README.md                    # User documentation
├── PRD.md                       # This file
├── config/
│   ├── __init__.py
│   └── settings.py              # Environment & config loader
├── generators/
│   ├── __init__.py
│   ├── blog_generator.py        # Blog outline logic
│   ├── social_generator.py      # Social media calendar logic
│   └── writing_generator.py     # Writing prompt logic
└── utils/
    ├── __init__.py
    ├── llm_interface.py         # OpenAI API wrapper
    └── prompt_templates.py      # Reusable prompt templates
```

## 5. Dependencies (requirements.txt)

```
streamlit>=1.31.0
requests>=2.31.0
python-dotenv>=1.0.0
pydantic>=2.6.0
```

## 6. Estimated Timeline

- **Phase 1 (MVP):** 3-5 hours - Blog Generator only
- **Phase 2:** 2-3 hours - Add Social Media
- **Phase 3:** 2-3 hours - Add Writing Prompts  
- **Phase 4:** 3-4 hours - Polish & enhancements

**Total:** 10-15 hours for complete app

## 7. Next Action

**Ready to start with Step 1.1: Environment Setup?**

This will create the project structure, virtual environment, and base files needed to begin development.
