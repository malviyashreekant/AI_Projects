# AI Projects Automation

This automation generates a simple AI mini-project, runs it, and pushes it to GitHub twice per day at random times.

## What it creates
Each run creates a new folder in the repo root with this pattern:

```
Projects_<topic>_YYYYMMDD_HHMMSS/
  README.md
  requirements.txt
  src/
    main.py
```

Topics include LLM, RAG, SLM, LangChain, and LangGraph fundamentals.

Each run executes `python src/main.py` and writes output to `run.log`. If the run fails, the project is not committed or pushed.

## Claude setup
- Set `ANTHROPIC_API_KEY` in your environment.
- Optional: set `CLAUDE_MODEL` (default is `claude-3-5-sonnet-20241022`).
- Ensure the Python used by the scheduler has the SDK installed: `pip install anthropic`.

## Configure
Edit [automation/config.json](automation/config.json) to change:
- `projects_root` (relative to repo root)
- `project_prefix`
- `git_path`
- `topics`

## Run manually
From the repo root:

```powershell
py -3 automation/generate_project.py
```

## Schedule twice daily (random times)
Run in PowerShell (as your user):

```powershell
automation/setup_tasks.ps1
```

This creates a single task named `AIProjects-Generator` with two daily triggers:
- 00:00 with random delay up to 12 hours
- 12:00 with random delay up to 12 hours

This yields two random runs per day within 0-12 and 12-24 hour windows.
