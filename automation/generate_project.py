import json
import logging
import os
import random
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("config.json")

DEFAULT_TOPICS = [
    "Email Auto-Responder",
    "Product FAQ System",
    "Customer Review Analyzer",
    "Meeting Notes Summarizer",
    "Content Categorizer",
    "Document Q&A Assistant",
    "Code Documentation Generator",
    "Data Extraction Tool",
    "Multi-Step Content Pipeline",
    "Intelligent Query Router",
]

TOPIC_LIBRARY = {
    "Email Auto-Responder": {
        "summary": "Analyzes incoming emails and generates professional, context-aware responses.",
        "goals": [
            "Parse email content and intent",
            "Generate appropriate responses",
            "Handle multiple email types",
        ],
    },
    "Product FAQ System": {
        "summary": "Retrieves relevant product documentation and generates answers to customer questions.",
        "goals": [
            "Index and search product documentation",
            "Match questions to relevant docs",
            "Generate accurate, grounded answers",
        ],
    },
    "Customer Review Analyzer": {
        "summary": "Analyzes customer reviews for sentiment, themes, and actionable insights.",
        "goals": [
            "Extract sentiment from reviews",
            "Identify common themes",
            "Generate summary insights",
        ],
    },
    "Meeting Notes Summarizer": {
        "summary": "Transforms raw meeting transcripts into structured, actionable summaries.",
        "goals": [
            "Extract key points and decisions",
            "Identify action items",
            "Generate concise summaries",
        ],
    },
    "Content Categorizer": {
        "summary": "Automatically categorizes and tags content into predefined categories.",
        "goals": [
            "Multi-label classification",
            "Extract relevant tags",
            "Handle edge cases",
        ],
    },
    "Document Q&A Assistant": {
        "summary": "Answers questions about documents using retrieval-augmented generation.",
        "goals": [
            "Chunk and index documents",
            "Retrieve relevant sections",
            "Generate contextual answers",
        ],
    },
    "Code Documentation Generator": {
        "summary": "Analyzes code and generates clear, comprehensive documentation.",
        "goals": [
            "Parse code structure",
            "Generate docstrings and comments",
            "Explain complex logic",
        ],
    },
    "Data Extraction Tool": {
        "summary": "Extracts structured data from unstructured text (emails, invoices, forms).",
        "goals": [
            "Identify key fields",
            "Extract with high accuracy",
            "Handle format variations",
        ],
    },
    "Multi-Step Content Pipeline": {
        "summary": "Chains multiple AI steps: extract->summarize->categorize->format.",
        "goals": [
            "Demonstrate chaining",
            "Pass state between steps",
            "Handle errors gracefully",
        ],
    },
    "Intelligent Query Router": {
        "summary": "Routes user queries to appropriate handlers based on intent and complexity.",
        "goals": [
            "Classify query intent",
            "Route to specialized handlers",
            "Provide fallback logic",
        ],
    },
}

CLAUDE_TEMPLATES = {
    "Email Auto-Responder": '''import os
from anthropic import Anthropic

# Sample emails for demonstration
SAMPLE_EMAILS = [
    {"from": "customer@example.com", "subject": "Order Status", "body": "Hi, I ordered product #12345 last week. Can you check the delivery status?"},
    {"from": "support@vendor.com", "subject": "Meeting Request", "body": "Would you be available for a call on Friday at 2 PM to discuss the integration?"},
    {"from": "info@newsletter.com", "subject": "Unsubscribe", "body": "Please remove me from your marketing list."},
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def generate_response(email):
    client = get_client()
    prompt = f"""Generate a professional email response.

From: {email['from']}
Subject: {email['subject']}
Body: {email['body']}

Write a helpful, concise response (2-3 sentences)."""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=200,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Email Auto-Responder ===\\n")
    for i, email in enumerate(SAMPLE_EMAILS, 1):
        print(f"Email {i}: {email['subject']}")
        print(f"Response:\\n{generate_response(email)}\\n")

if __name__ == "__main__":
    main()
''',

    "Product FAQ System": '''import os
from anthropic import Anthropic

# Sample product knowledge base
KNOWLEDGE_BASE = [
    "Our Pro plan costs $49/month and includes unlimited users, 100GB storage, and priority support.",
    "Free trial lasts 14 days with full access to Pro features. No credit card required.",
    "You can upgrade or downgrade your plan anytime from the billing section.",
    "We accept Visa, Mastercard, American Express, and PayPal.",
    "Data is encrypted at rest and in transit. We're SOC 2 Type II certified.",
    "API rate limits: Free tier 100 req/hour, Pro tier 1000 req/hour.",
]

SAMPLE_QUESTIONS = [
    "How much does the Pro plan cost?",
    "Do I need a credit card for the trial?",
    "What payment methods do you accept?",
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def retrieve_relevant_docs(question, docs, top_k=3):
    """Simple keyword-based retrieval"""
    question_words = set(question.lower().split())
    scored = []
    for doc in docs:
        doc_words = set(doc.lower().split())
        score = len(question_words & doc_words)
        scored.append((score, doc))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [doc for _, doc in scored[:top_k]]

def answer_question(question):
    context = retrieve_relevant_docs(question, KNOWLEDGE_BASE)
    client = get_client()
    
    prompt = f"""Answer the question using only the provided context.

Context:
{chr(10).join(f"- {doc}" for doc in context)}

Question: {question}

Answer concisely and accurately."""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=150,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Product FAQ System ===\\n")
    for q in SAMPLE_QUESTIONS:
        print(f"Q: {q}")
        print(f"A: {answer_question(q)}\\n")

if __name__ == "__main__":
    main()
''',

    "Customer Review Analyzer": '''import os
from anthropic import Anthropic

SAMPLE_REVIEWS = [
    "Love this product! Setup was easy and support team was super helpful. 5 stars!",
    "Good overall but the mobile app crashes frequently. Desktop version works fine.",
    "Disappointed. Features promised in marketing don't work as expected. Refund requested.",
    "Been using for 3 months. Solid tool, fair price. Wish it had better integrations.",
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def analyze_review(review):
    client = get_client()
    prompt = f"""Analyze this customer review and extract:
1. Sentiment (positive/negative/mixed)
2. Key themes (comma-separated)
3. Action items (if any)

Review: {review}

Format:
Sentiment: 
Themes: 
Action:"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=150,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Customer Review Analyzer ===\\n")
    for i, review in enumerate(SAMPLE_REVIEWS, 1):
        print(f"Review {i}: {review}")
        print(f"{analyze_review(review)}\\n")

if __name__ == "__main__":
    main()
''',

    "Meeting Notes Summarizer": '''import os
from anthropic import Anthropic

SAMPLE_TRANSCRIPT = """
John: Let's discuss Q1 roadmap. Top priority is mobile app launch.
Sarah: Agree. We need design mockups by Feb 15. I'll coordinate with design team.
Mike: Backend APIs are 80% done. Should finish by Feb 10.
John: Great. Sarah, can you also schedule user testing for March 1?
Sarah: Will do. I'll send calendar invites this week.
Mike: One blocker - we need final sign-off on data schema.
John: I'll get that approved by Friday. Any other concerns?
Sarah: All good. Let's sync again next Monday.
"""

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def summarize_meeting(transcript):
    client = get_client()
    prompt = f"""Summarize this meeting transcript.

Extract:
1. Key decisions
2. Action items (who, what, when)
3. Next steps

Transcript:
{transcript}"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=300,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Meeting Notes Summarizer ===\\n")
    print(summarize_meeting(SAMPLE_TRANSCRIPT))

if __name__ == "__main__":
    main()
''',

    "Content Categorizer": '''import os
from anthropic import Anthropic

CATEGORIES = ["Technology", "Business", "Health", "Education", "Entertainment"]

SAMPLE_ARTICLES = [
    "New AI model achieves breakthrough in natural language understanding, outperforming previous benchmarks.",
    "Market analysis shows tech stocks rising amid strong Q4 earnings reports from major companies.",
    "Study reveals regular exercise reduces risk of chronic diseases by up to 40 percent.",
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def categorize_content(text):
    client = get_client()
    prompt = f"""Categorize this content into one or more categories: {', '.join(CATEGORIES)}

Content: {text}

Respond with categories (comma-separated) and confidence (high/medium/low)."""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=100,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Content Categorizer ===\\n")
    for i, article in enumerate(SAMPLE_ARTICLES, 1):
        print(f"Article {i}: {article[:60]}...")
        print(f"Categories: {categorize_content(article)}\\n")

if __name__ == "__main__":
    main()
''',

    "Document Q&A Assistant": '''import os
from anthropic import Anthropic

COMPANY_HANDBOOK = """
Vacation Policy: Employees accrue 15 days PTO per year. Must request 2 weeks in advance.
Remote Work: Hybrid schedule - 3 days in office, 2 days remote. Full remote requires manager approval.
Health Benefits: Medical, dental, vision coverage starts after 30 days. Company pays 80% of premiums.
Performance Reviews: Conducted quarterly. Raises based on performance and market data.
"""

SAMPLE_QUESTIONS = [
    "How many vacation days do I get?",
    "When does health insurance start?",
    "What's the remote work policy?",
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def answer_from_document(question):
    client = get_client()
    prompt = f"""Answer the question using only information from the document.

Document:
{COMPANY_HANDBOOK}

Question: {question}

Answer:"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=150,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Document Q&A Assistant ===\\n")
    for q in SAMPLE_QUESTIONS:
        print(f"Q: {q}")
        print(f"A: {answer_from_document(q)}\\n")

if __name__ == "__main__":
    main()
''',

    "Code Documentation Generator": '''import os
from anthropic import Anthropic

SAMPLE_CODE = """
def calculate_discount(price, customer_tier, quantity):
    base_discount = 0.0
    if customer_tier == "gold":
        base_discount = 0.15
    elif customer_tier == "silver":
        base_discount = 0.10
    elif customer_tier == "bronze":
        base_discount = 0.05
    
    bulk_discount = min(quantity * 0.01, 0.20)
    total_discount = min(base_discount + bulk_discount, 0.30)
    return price * (1 - total_discount)
"""

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def generate_docs(code):
    client = get_client()
    prompt = f"""Generate comprehensive documentation for this function.

Include:
1. Clear docstring
2. Parameter descriptions
3. Return value description
4. Example usage

Code:
{code}"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=400,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Code Documentation Generator ===\\n")
    print(generate_docs(SAMPLE_CODE))

if __name__ == "__main__":
    main()
''',

    "Data Extraction Tool": '''import os
from anthropic import Anthropic

SAMPLE_EMAIL = """
From: orders@webstore.com
Subject: Order Confirmation #ORD-2024-5678

Thank you for your order!

Customer: Jane Smith
Email: jane.smith@email.com
Order Total: $234.99
Payment Method: Visa ending in 4242

Items:
- Laptop Stand (x1) - $89.99
- USB-C Cable (x2) - $24.99 each
- Wireless Mouse (x1) - $69.99

Estimated Delivery: February 10, 2024
Tracking: 1Z999AA10123456784
"""

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def extract_order_data(text):
    client = get_client()
    prompt = f"""Extract structured data from this order confirmation email.

Email:
{text}

Output JSON with fields: order_id, customer_name, customer_email, total, delivery_date, tracking_number, items (array)"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=300,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Data Extraction Tool ===\\n")
    print(extract_order_data(SAMPLE_EMAIL))

if __name__ == "__main__":
    main()
''',

    "Multi-Step Content Pipeline": '''import os
from anthropic import Anthropic

SAMPLE_ARTICLE = """
Breaking: Tech Giant Announces Record Quarterly Earnings

XYZ Corp reported Q4 revenue of $52 billion, exceeding analyst expectations by 12%. 
CEO stated AI investments driving growth. Stock jumped 8% in after-hours trading.
Company also announced 1000 new AI researcher hires for 2024.
"""

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def extract_facts(text):
    client = get_client()
    prompt = f"Extract key facts as bullet points from:\\n{text}"
    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=150, temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def summarize(text):
    client = get_client()
    prompt = f"Summarize in one sentence:\\n{text}"
    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=100, temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def categorize(text):
    client = get_client()
    prompt = f"Categorize (Business/Tech/Finance/Other):\\n{text}"
    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=50, temperature=0.1,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Multi-Step Content Pipeline ===\\n")
    print("Step 1 - Extract Facts:")
    facts = extract_facts(SAMPLE_ARTICLE)
    print(facts)
    
    print("\\nStep 2 - Summarize:")
    summary = summarize(facts)
    print(summary)
    
    print("\\nStep 3 - Categorize:")
    category = categorize(summary)
    print(category)

if __name__ == "__main__":
    main()
''',

    "Intelligent Query Router": '''import os
from anthropic import Anthropic

SAMPLE_QUERIES = [
    "How do I reset my password?",
    "Analyze sales trends from Q3 data in attached spreadsheet",
    "What's your refund policy?",
    "Calculate compound interest for $10000 at 5% over 10 years",
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def classify_and_route(query):
    client = get_client()
    prompt = f"""Classify this query and route to the appropriate handler.

Handlers:
- FAQ: Simple policy/process questions
- SUPPORT: Technical issues requiring human help
- ANALYTICS: Data analysis requests
- CALCULATOR: Math/computation tasks

Query: {query}

Respond with: Handler name, Confidence (high/medium/low), Brief reasoning"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=150,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Intelligent Query Router ===\\n")
    for i, query in enumerate(SAMPLE_QUERIES, 1):
        print(f"Query {i}: {query}")
        print(f"Routing: {classify_and_route(query)}\\n")

if __name__ == "__main__":
    main()
''',
}


def slugify(text):
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "project"


def load_config():
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8-sig") as handle:
            return json.load(handle)
    return {}


def resolve_repo_root():
    return Path(__file__).resolve().parents[1]


def setup_logging(repo_root):
    log_dir = repo_root / "automation" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "generator.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def resolve_projects_root(repo_root, config):
    projects_root = config.get("projects_root", ".")
    root_path = Path(projects_root)
    if not root_path.is_absolute():
        root_path = repo_root / root_path
    root_path.mkdir(parents=True, exist_ok=True)
    return root_path


def build_readme(project_name, topic, summary, goals, created_at):
    goals_lines = "\n".join(f"- {goal}" for goal in goals)
    structure = """{name}/
  README.md
  requirements.txt
  src/
    main.py
  run.log
""".format(name=project_name)
    return (
        f"# {project_name}\n\n"
        f"**Topic:** {topic}\n\n"
        f"**Created:** {created_at}\n\n"
        f"## Overview\n{summary}\n\n"
        f"## Learning Goals\n{goals_lines}\n\n"
        "## Structure\n"
        f"```\n{structure}```\n\n"
        "## Setup\n"
        "Set `ANTHROPIC_API_KEY` in your environment. Optional: `CLAUDE_MODEL`.\n\n"
        "## Run\n"
        "```bash\npython src/main.py\n```\n\n"
        "Output is saved to `run.log`.\n"
    )


def write_project(project_dir, assets, topic):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    project_dir.mkdir(parents=True, exist_ok=False)
    (project_dir / "src").mkdir(parents=True, exist_ok=True)

    readme = build_readme(
        project_dir.name,
        topic,
        assets["summary"],
        assets["goals"],
        created_at,
    )
    (project_dir / "README.md").write_text(readme, encoding="utf-8")
    requirements = "anthropic>=0.40.0\n"
    (project_dir / "requirements.txt").write_text(requirements, encoding="utf-8")
    code = CLAUDE_TEMPLATES.get(topic) or CLAUDE_TEMPLATES["Email Auto-Responder"]
    (project_dir / "src" / "main.py").write_text(code, encoding="utf-8")


def resolve_git_path(config):
    git_path = config.get("git_path")
    if git_path:
        candidate = Path(git_path)
        if candidate.exists():
            return str(candidate)
        logging.warning("Configured git_path not found: %s", git_path)
    return "git"


def run_git(repo_root, git_path, args):
    return subprocess.run(
        [git_path] + args,
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )


def run_project(project_dir):
    script_path = project_dir / "src" / "main.py"
    log_path = project_dir / "run.log"
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=project_dir,
        capture_output=True,
        text=True,
    )
    log_path.write_text(
        "stdout:\n" + (result.stdout or "") + "\n\nstderr:\n" + (result.stderr or ""),
        encoding="utf-8",
    )
    if result.returncode != 0:
        logging.error("Project run failed. See %s", log_path)
        return False
    logging.info("Project run succeeded. Output saved to %s", log_path)
    return True


def main():
    repo_root = resolve_repo_root()
    setup_logging(repo_root)
    config = load_config()

    if not (repo_root / ".git").exists():
        logging.error("No .git directory found at %s", repo_root)
        return 1

    topics = config.get("topics") or DEFAULT_TOPICS
    topic = random.choice(topics)
    assets = TOPIC_LIBRARY.get(topic) or TOPIC_LIBRARY["Email Auto-Responder"]

    projects_root = resolve_projects_root(repo_root, config)
    prefix = config.get("project_prefix", "Projects_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_name = f"{prefix}{slugify(topic)}_{timestamp}"
    project_dir = projects_root / project_name

    try:
        write_project(project_dir, assets, topic)
        logging.info("Created project at %s", project_dir)
    except FileExistsError:
        logging.warning("Project already exists: %s", project_dir)
        return 0

    if not run_project(project_dir):
        return 1

    git_path = resolve_git_path(config)
    try:
        run_git(
            repo_root,
            git_path,
            ["add", str(project_dir.relative_to(repo_root))],
        )
        status = run_git(repo_root, git_path, ["status", "--porcelain"]).stdout.strip()
        if not status:
            logging.info("No changes to commit.")
            return 0
        message = f"Add AI project: {project_dir.name}"
        run_git(repo_root, git_path, ["commit", "-m", message])
        branch = run_git(repo_root, git_path, ["rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
        run_git(repo_root, git_path, ["push", "origin", branch])
        logging.info("Committed and pushed to %s", branch)
    except subprocess.CalledProcessError as exc:
        logging.error("Git command failed: %s", exc.stderr.strip())
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
