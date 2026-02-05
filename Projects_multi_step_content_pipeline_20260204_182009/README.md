# Projects_multi_step_content_pipeline_20260204_182009

> **Multi-Step Content Pipeline** | *Created: 2026-02-04 18:20:09*

## 🎯 Project Overview

This project demonstrates how to chain multiple AI operations in sequence, where each step processes the output of the previous step. It takes a news article through a complete content processing pipeline.

**Summary:** Chains multiple AI steps: extract->summarize->categorize->format.

## 🧠 Technical Approach

Uses Claude AI in a sequential workflow:
1. **Extract Facts** - Identifies and extracts key information from raw text
2. **Summarize** - Condenses extracted facts into concise summaries  
3. **Categorize** - Classifies content into appropriate categories
4. **Format** - Outputs structured results

Each step validates input and handles potential errors gracefully.

## 📋 Sample Workflow

Input: Raw news article about tech earnings
↓
Extract: Key facts about revenue, stock performance, hiring
↓  
Summarize: One-sentence summary of main points
↓
Categorize: Classification as "Tech/Business/Finance"
↓
Output: Structured, processed content ready for publication

## 🎓 Learning Goals

- Demonstrate chaining
- Pass state between steps
- Handle errors gracefully

## 🚀 Use Cases

- News article processing pipelines
- Content management systems
- Automated content moderation workflows
- Document processing automation
- Content classification systems

## 📁 Project Structure

```
Projects_multi_step_content_pipeline_20260204_182009/
  ├── README.md           # This documentation
  ├── requirements.txt    # Python dependencies  
  ├── src/
  │   └── main.py        # Main application code
  └── run.log            # Execution output log
```

## ⚙️ Setup & Installation

1. **Prerequisites:**
   - Python 3.8 or higher
   - Anthropic API key

2. **Environment Setup:**
   ```bash
   # Set your API key
   export ANTHROPIC_API_KEY="your-api-key-here"
   
   # Optional: Set specific Claude model
   export CLAUDE_MODEL="claude-haiku-4-5-20251001"
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Running the Project

```bash
# Execute the main script
python src/main.py

# View detailed output
cat run.log
```

## 🔧 Customization Options

- **Model Selection:** Change `CLAUDE_MODEL` environment variable to use different Claude models
- **Parameters:** Modify temperature and max_tokens in the code for different response styles
- **Input Data:** Replace sample data with your own content in the source code
- **Output Format:** Customize the output structure in the main function

## 📊 Expected Output

The program will:
1. Process the embedded sample data
2. Generate AI-powered results
3. Display results in the console  
4. Save detailed logs to `run.log`

## 🔍 Code Architecture

- **`main()`:** Entry point and workflow orchestration
- **AI Functions:** Modular functions for each AI operation
- **Error Handling:** Robust error management for API failures
- **Logging:** Comprehensive output logging for debugging

## 💡 Learning Outcomes

After exploring this project, you'll understand:
- How to integrate Claude AI into Python applications
- Best practices for AI API error handling
- Structuring multi-step AI workflows
- Practical AI application design patterns

## 🛠️ Troubleshooting

**API Key Issues:**
- Ensure `ANTHROPIC_API_KEY` is set correctly
- Verify your API key has sufficient credits

**Import Errors:**
- Run `pip install anthropic>=0.40.0`
- Check Python version compatibility

**Model Errors:**
- Verify model name in `CLAUDE_MODEL` variable
- Check model availability for your API tier

---

*This project demonstrates practical AI integration using Claude. Explore the code, modify the examples, and adapt it for your own use cases!*
