# AI Project Automation 🤖

A powerful automation system that generates, executes, and commits real-world AI projects using Claude AI.

## Overview

This automation creates **practical, self-contained AI projects** that solve real-world problems using the Anthropic Claude API. Each project includes:

- **Complete working code** (50-150 lines)
- **Embedded sample data** (no external dependencies needed)
- **Actual AI integration** using Claude
- **Auto-execution** with output logging
- **Git integration** for automatic commits

## Quick Start

### 1. Prerequisites

- Python 3.8+
- Anthropic API key
- Git installed
- Virtual environment (already set up: `.venv/`)

### 2. Set Up Your API Key

**Option A: Permanent Setup (Recommended)**

```powershell
[Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'your-key-here', 'User')
```

This sets the key permanently for your user account and persists across sessions.

**Option B: Session-Only Setup**

```powershell
$env:ANTHROPIC_API_KEY = 'your-key-here'
```

This only works for the current PowerShell session.

### 3. Get Your API Key

1. Go to [Anthropic Console](https://console.anthropic.com/account/keys)
2. Create or copy an API key
3. Set it using one of the methods above

### 4. Run the Automation

```powershell
cd AI_Projects
..\\.venv\\Scripts\\python.exe automation/generate_project.py
```

That's it! The automation will:
- Randomly select an AI project type
- Generate the project with working code
- Execute the project (calls Claude API)
- Save output to `run.log`
- Commit everything to GitHub

## Project Types

The automation creates one of these 10 AI projects:

### 1. **Email Auto-Responder**
Analyzes incoming emails and generates professional, context-aware responses.
- Parse email intent
- Generate appropriate replies
- Handle multiple email types

### 2. **Product FAQ System**
Retrieves product documentation and answers customer questions using RAG principles.
- Index and search documentation
- Match questions to relevant docs
- Generate grounded answers

### 3. **Customer Review Analyzer**
Extracts sentiment, themes, and actionable insights from customer reviews.
- Sentiment analysis
- Identify common themes
- Generate summary insights

### 4. **Meeting Notes Summarizer**
Transforms meeting transcripts into structured, actionable summaries.
- Extract key decisions
- Identify action items
- Generate concise summaries

### 5. **Content Categorizer**
Automatically categorizes content into predefined categories with confidence scores.
- Multi-label classification
- Extract relevant tags
- Handle edge cases

### 6. **Document Q&A Assistant**
Answers questions about documents using retrieval-augmented generation.
- Chunk and index documents
- Retrieve relevant sections
- Generate contextual answers

### 7. **Code Documentation Generator**
Analyzes code and generates clear, comprehensive documentation.
- Parse code structure
- Generate docstrings
- Explain complex logic

### 8. **Data Extraction Tool**
Extracts structured data from unstructured text (emails, invoices, forms).
- Identify key fields
- Extract with high accuracy
- Handle format variations

### 9. **Multi-Step Content Pipeline**
Chains multiple AI operations: extract → summarize → categorize → format.
- Demonstrate chaining
- Pass state between steps
- Handle errors gracefully

### 10. **Intelligent Query Router**
Routes queries to appropriate handlers based on intent and complexity.
- Classify query intent
- Route to specialized handlers
- Provide fallback logic

## Project Structure

Each generated project looks like this:

```
Projects_email_auto_responder_20250204_171229/
├── README.md              # Project documentation
├── requirements.txt       # Dependencies (just anthropic)
├── run.log               # Execution output and results
└── src/
    └── main.py           # Complete working AI code
```

### Running a Generated Project Manually

```powershell
cd Projects_email_auto_responder_20250204_171229
..\\..\\.venv\\Scripts\\python.exe src/main.py
```

Output is logged to `run.log`.

## Configuration

Edit `AI_Projects/automation/config.json` to customize:

```json
{
  "projects_root": ".",                          // Where to create projects
  "project_prefix": "Projects_",                 // Naming prefix
  "git_path": "C:\\Users\\...\\git.exe",        // Path to git executable
  "topics": [                                    // Which project types to generate
    "Email Auto-Responder",
    "Product FAQ System",
    // ... 8 more types
  ]
}
```

## Environment Variables

### Required
- **`ANTHROPIC_API_KEY`** - Your Anthropic API key

### Optional
- **`CLAUDE_MODEL`** - Model to use (default: `claude-haiku-4-5-20251001`)
  
  Example:
  ```powershell
  $env:CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
  ```

## Advanced Usage

### Schedule Automation to Run Automatically

#### Windows Task Scheduler (via script)

```powershell
cd AI_Projects/automation
.\\setup_tasks.ps1
```

This creates a scheduled task that runs the automation twice daily with random delays.

#### Manual Scheduling

1. **Open Task Scheduler** (Win + R → `taskschd.msc`)
2. **Create Basic Task**:
   - Name: "AI Project Generator"
   - Trigger: Daily at 9 AM and 5 PM
   - Action: Run `python.exe automation/generate_project.py`
   - Advanced: Add random delay (5-15 minutes)

### Generate Specific Project Type

Modify `automation/generate_project.py` line 710 to specify a project:

```python
# Line 710 - Change from:
topic = random.choice(topics)

# To:
topic = "Email Auto-Responder"  # Always generate this type
```

### Run Generated Projects Only

To execute a project without the automation:

```powershell
cd Projects_email_auto_responder_20250204_171229
..\\..\\.venv\\Scripts\\python.exe src/main.py
```

## Understanding the Code

### Project Template Structure

Every generated project follows this pattern:

```python
import os
from anthropic import Anthropic

# 1. Sample Data (self-contained)
SAMPLE_DATA = [...]

# 2. Client Setup
def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

# 3. AI Function
def process_data(data):
    client = get_client()
    prompt = f"..."
    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=300,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

# 4. Main
def main():
    print("Processing...")
    result = process_data(SAMPLE_DATA)
    print(result)

if __name__ == "__main__":
    main()
```

### Automation Script Breakdown

**`automation/generate_project.py`** (812 lines)

1. **Load Config** - Read `config.json`
2. **Select Topic** - Random choice from available projects
3. **Create Project** - Generate folder + files
4. **Write Code** - Use template for selected project type
5. **Execute** - Run `src/main.py` and capture output
6. **Log Output** - Save results to `run.log`
7. **Commit to Git** - Stage, commit, and push automatically

## Troubleshooting

### API Key Issues

**Red Flags:**
- `ANTHROPIC_API_KEY not set` - Key wasn't found
- `invalid x-api-key` - Key is invalid/revoked
- `model not found` - Account doesn't have model access

**Fixes:**
1. Verify key in [Anthropic Console](https://console.anthropic.com/account/keys)
2. Check account has active billing/plan
3. Recreate the key if suspected revoked
4. Set it again with `[Environment]::SetEnvironmentVariable(...)`

### Import Errors

```
ModuleNotFoundError: No module named 'anthropic'
```

**Fix:** Install dependencies in the venv:
```powershell
.venv/Scripts/pip install anthropic>=0.40.0
```

### Git Commit Fails

**Error:** Git command not found

**Fix:** Update `git_path` in `automation/config.json` with correct path to `git.exe`

### Project Already Exists

**Error:** Project folder already exists

This is normal—skip and try again. Each project gets a unique timestamp.

## File Structure

```
MY_GITHUB_AUTOMATION/
├── .venv/                          # Python virtual environment
├── .git/                           # Git repository
├── README.md                       # This file
├── AI_Projects/
│   ├── automation/
│   │   ├── config.json            # Configuration
│   │   ├── generate_project.py    # Main automation script
│   │   ├── generate_project.py.bak # Backup
│   │   ├── README.md              # Automation docs
│   │   ├── setup_tasks.ps1        # Task scheduler setup
│   │   └── logs/
│   │       └── generator.log      # Execution logs
│   └── Projects_*/                # Generated projects (auto-created)
└── .gitignore
```

## Model Availability

The automation defaults to **Claude Haiku 4.5** (`claude-haiku-4-5-20251001`) for:
- Fast execution
- Low cost
- Excellent quality for structured tasks

To use a different model:

```powershell
$env:CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
```

**Available models** (check your account):
- `claude-haiku-4-5-20251001` (fast, cheap)
- `claude-3-5-sonnet-20241022` (balanced)
- `claude-3-opus-20250219` (most capable)

## Real-World Examples

### Example 1: Customer Support Automation

Run the automation multiple times to build a **Product FAQ System** that answers 100s of customer questions using your knowledge base.

### Example 2: Content Pipeline

Use **Multi-Step Content Pipeline** to process articles:
1. Extract key facts
2. Summarize
3. Categorize
4. Format for publishing

### Example 3: Code Documentation

Feed the **Code Documentation Generator** your proprietary code to auto-generate professional documentation.

## Performance Notes

- **Execution Time:** 5-15 seconds per project (API dependent)
- **Cost:** ~$0.005 per project (Haiku pricing)
- **Rate Limits:** No limits with free tier, higher with paid

## Contributing

To add a new project type:

1. Add entry to `TOPIC_LIBRARY` with summary + goals
2. Create template in `CLAUDE_TEMPLATES` with working code
3. Add to `config.json` topics array
4. Test by running automation

## Support

- **API Issues:** Check [Anthropic Documentation](https://docs.anthropic.com)
- **Git Issues:** Ensure git is properly installed and in PATH
- **Python Issues:** Use `.venv/Scripts/python.exe` for consistency

## License

This automation is part of your private AI project suite.

---

**Last Updated:** 2026-02-04  
**Model:** Claude Haiku 4.5  
**API Version:** anthropic>=0.40.0
