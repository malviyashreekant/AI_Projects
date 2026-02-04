# Projects_multi_step_content_pipeline_20260204_171145

**Topic:** Multi-Step Content Pipeline

**Created:** 2026-02-04 17:11:45

## Overview
Chains multiple AI steps: extract->summarize->categorize->format.

## Learning Goals
- Demonstrate chaining
- Pass state between steps
- Handle errors gracefully

## Structure
```
Projects_multi_step_content_pipeline_20260204_171145/
  README.md
  requirements.txt
  src/
    main.py
  run.log
```

## Setup
Set `ANTHROPIC_API_KEY` in your environment. Optional: `CLAUDE_MODEL`.

## Run
```bash
python src/main.py
```

Output is saved to `run.log`.
