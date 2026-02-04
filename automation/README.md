# AI Projects Automation

Generates practical AI mini-projects that solve real-world use cases, runs them, and pushes to GitHub twice per day at random times.

## What it creates
Each run creates a new self-contained project with sample data:

```
Projects_<topic>_YYYYMMDD_HHMMSS/
  README.md
  requirements.txt
  src/
    main.py
  run.log
```

## Project Types

Real-world applications covering:

- **Email Auto-Responder** - Generates professional email responses  
- **Product FAQ System** - RAG-based customer support
- **Customer Review Analyzer** - Sentiment & theme extraction
- **Meeting Notes Summarizer** - Actionable summaries from transcripts
- **Content Categorizer** - Multi-label content classification
- **Document Q&A Assistant** - Query company documents
- **Code Documentation Generator** - Auto-generate docstrings
- **Data Extraction Tool** - Structured data from unstructured text
- **Multi-Step Content Pipeline** - Chained AI workflows
- **Intelligent Query Router** - Intent-based routing

Each project is 50-150 lines, self-contained with sample data, and demonstrates a clear real-world use case.

## Setup

1. **Set API Key**
   ```powershell
   $env:ANTHROPIC_API_KEY = "your-api-key"
   ```

2. **Install SDK** (if not already installed)
   ```powershell
   pip install anthropic
   ```

3. **Optional:** Set custom model
   ```powershell
   $env:CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
   ```

## Run manually

From the repo root:

```powershell
py -3 automation/generate_project.py
```

Projects are tested before commit - only pushed if execution succeeds.

## Configure

Edit [automation/config.json](automation/config.json):
- `projects_root` - Where to create projects (relative to repo root)
- `project_prefix` - Folder name prefix
- `git_path` - Path to git.exe
- `topics` - List of project types to generate

## Schedule (Twice Daily)

Run in PowerShell as your user:

```powershell
automation/setup_tasks.ps1
```
Creates task `AIProjects-Generator` with two random daily runs:
- 00:00-12:00 window
- 12:00-24:00 window

## How it works

1. Selects random project type
2. Generates code with embedded sample data
3. Runs project and saves output to `run.log`
4. If successful, commits and pushes to GitHub
5. If failed, stops (no commit)

Logs saved to `automation/logs/generator.log`
