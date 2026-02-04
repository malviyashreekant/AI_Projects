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
    "LLM Fundamentals",
    "RAG Fundamentals",
    "SLM Fundamentals",
    "LangChain Basics",
    "LangGraph Basics",
]

TOPIC_LIBRARY = {
    "LLM Fundamentals": {
        "summary": "Introduce prompt formatting, system/user roles, and a minimal LLM call.",
        "goals": [
            "Understand prompt structure",
            "See a simple request/response loop",
            "Learn how to keep model I/O isolated",
        ],
        "code": """import textwrap\n\n\nSYSTEM_PROMPT = \"You are a helpful assistant.\"\n\n\nUSER_PROMPT = \"Explain the difference between tokens and words.\"\n\n\n\ndef fake_llm(system_prompt, user_prompt):\n    \"\"\"A tiny deterministic stand-in for a real model.\"\"\"\n    response = f"{system_prompt}\\nUser asked: {user_prompt}\\nAnswer: Tokens are model-level units, words are human-level units."\n    return textwrap.fill(response, width=80)\n\n\n\ndef run_demo():\n    output = fake_llm(SYSTEM_PROMPT, USER_PROMPT)\n    print(output)\n\n\nif __name__ == \"__main__\":\n    run_demo()\n""",
    },
    "RAG Fundamentals": {
        "summary": "Show a tiny retrieval step over local docs and a mocked generation step.",
        "goals": [
            "Understand chunk selection",
            "See retrieval + generation separation",
            "Keep everything local and deterministic",
        ],
        "code": """import textwrap\n\n\nDOCS = [\n    \"RAG combines retrieval with generation to ground responses.\",\n    \"Chunking splits documents into smaller passages.\",\n    \"Similarity search retrieves the best matching chunks.\",\n    \"A generator uses retrieved context to answer.\",\n]\n\n\nQUERY = \"How does RAG keep responses grounded?\"\n\n\n\ndef retrieve(query, docs, top_k=2):\n    tokens = set(query.lower().split())\n    scored = []\n    for doc in docs:\n        score = len(tokens.intersection(doc.lower().split()))\n        scored.append((score, doc))\n    scored.sort(reverse=True, key=lambda item: item[0])\n    return [doc for _, doc in scored[:top_k]]\n\n\n\ndef generate(query, context):\n    joined = " ".join(context)\n    response = f"Q: {query}\\nA: Based on context: {joined}"\n    return textwrap.fill(response, width=80)\n\n\n\ndef run_demo():\n    context = retrieve(QUERY, DOCS)\n    output = generate(QUERY, context)\n    print(output)\n\n\nif __name__ == \"__main__\":\n    run_demo()\n""",
    },
    "SLM Fundamentals": {
        "summary": "Demonstrate a tiny 'small language model' style decision system.",
        "goals": [
            "See a compact model footprint",
            "Compare small vs large behaviors",
            "Keep outputs predictable",
        ],
        "code": """import random\n\n\nINTENTS = {\n    "hello": "Hi there. How can I help?",
    "help": "I can summarize basics of LLMs, RAG, SLMs, LangChain, and LangGraph.",
    "rag": "RAG retrieves documents then generates using that context.",
    "bye": "Goodbye!",
}\n\n\ndef small_model_reply(message):\n    message = message.lower()\n    for key, response in INTENTS.items():\n        if key in message:\n            return response\n    return random.choice(list(INTENTS.values()))\n\n\nif __name__ == "__main__":\n    print(small_model_reply("hello"))\n    print(small_model_reply("tell me about rag"))\n""",
    },
    "LangChain Basics": {
        "summary": "Illustrate a tiny chain of prompt -> parse -> post-process steps.",
        "goals": [
            "Show stepwise chaining",
            "Keep I/O explicit",
            "Encourage testable components",
        ],
        "code": """import textwrap\n\n\n\ndef prompt_step(topic):\n    return f"Explain {topic} in one sentence."\n\n\n\ndef model_step(prompt):\n    return f"{prompt} It is a structured way to compose LLM tools."\n\n\n\ndef post_process(text):\n    return textwrap.fill(text, width=80)\n\n\n\ndef run_chain(topic):\n    prompt = prompt_step(topic)\n    raw = model_step(prompt)\n    return post_process(raw)\n\n\nif __name__ == "__main__":\n    print(run_chain("LangChain"))\n""",
    },
    "LangGraph Basics": {
        "summary": "Show a tiny graph runner with nodes and edges.",
        "goals": [
            "Understand node orchestration",
            "See how state flows",
            "Keep graph logic simple",
        ],
        "code": """from collections import deque\n\n\nNODES = {\n    "start": lambda state: {**state, "steps": state["steps"] + ["start"]},\n    "retrieve": lambda state: {**state, "steps": state["steps"] + ["retrieve"]},\n    "generate": lambda state: {**state, "steps": state["steps"] + ["generate"]},\n}\n\nEDGES = {\n    "start": ["retrieve"],\n    "retrieve": ["generate"],\n    "generate": [],\n}\n\n\n\ndef run_graph(start_node):\n    state = {"steps": []}\n    queue = deque([start_node])\n    while queue:\n        node = queue.popleft()\n        state = NODES[node](state)\n        queue.extend(EDGES[node])\n    return state\n\n\nif __name__ == "__main__":\n    result = run_graph("start")\n    print(" -> ".join(result["steps"]))\n""",
    },
}


CLAUDE_TEMPLATES = {
    "LLM Fundamentals": """import os

from anthropic import Anthropic


SYSTEM_PROMPT = "You are a helpful assistant."
USER_PROMPT = "Explain the difference between tokens and words."


def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")
    return Anthropic(api_key=api_key)


def run_demo():
    client = get_client()
    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022"),
        max_tokens=200,
        temperature=0.2,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": USER_PROMPT}],
    )
    print(response.content[0].text)


if __name__ == "__main__":
    run_demo()
""",
    "RAG Fundamentals": """import os

from anthropic import Anthropic


DOCS = [
    "RAG combines retrieval with generation to ground responses.",
    "Chunking splits documents into smaller passages.",
    "Similarity search retrieves the best matching chunks.",
    "A generator uses retrieved context to answer.",
]

QUERY = "How does RAG keep responses grounded?"


def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")
    return Anthropic(api_key=api_key)


def retrieve(query, docs, top_k=2):
    tokens = set(query.lower().split())
    scored = []
    for doc in docs:
        score = len(tokens.intersection(doc.lower().split()))
        scored.append((score, doc))
    scored.sort(reverse=True, key=lambda item: item[0])
    return [doc for _, doc in scored[:top_k]]


def run_demo():
    context = retrieve(QUERY, DOCS)
    prompt = "Use the context to answer the question.\\n\\nContext: " + str(context) + "\\n\\nQuestion: " + QUERY
    client = get_client()
    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022"),
        max_tokens=220,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
    print(response.content[0].text)


if __name__ == "__main__":
    run_demo()
""",
    "SLM Fundamentals": """import os

from anthropic import Anthropic


INTENTS = {
    "hello": "Hi there. How can I help?",
    "help": "I can summarize basics of LLMs, RAG, SLMs, LangChain, and LangGraph.",
    "rag": "RAG retrieves documents then generates using that context.",
    "bye": "Goodbye!",
}


def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")
    return Anthropic(api_key=api_key)


def small_model_reply(message):
    message = message.lower()
    for key, response in INTENTS.items():
        if key in message:
            return response
    return INTENTS["help"]


def run_demo():
    local_response = small_model_reply("tell me about rag")
    prompt = "Compare a small, rule-based response with a large model response.\\nSmall response: " + local_response + "\\nNow answer as a large model in one sentence."
    client = get_client()
    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022"),
        max_tokens=120,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}],
    )
    print("Small model:", local_response)
    print("Claude:", response.content[0].text)


if __name__ == "__main__":
    run_demo()
""",
    "LangChain Basics": """import os

from anthropic import Anthropic


def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")
    return Anthropic(api_key=api_key)


def prompt_step(topic):
    return f"Explain {topic} in one sentence."


def model_step(client, prompt):
    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022"),
        max_tokens=120,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def post_process(text):
    return text.strip()


def run_chain(topic):
    prompt = prompt_step(topic)
    client = get_client()
    raw = model_step(client, prompt)
    return post_process(raw)


if __name__ == "__main__":
    print(run_chain("LangChain"))
""",
    "LangGraph Basics": """import os

from anthropic import Anthropic


NODES = ["start", "retrieve", "generate"]


def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")
    return Anthropic(api_key=api_key)


def run_graph(nodes):
    return " -> ".join(nodes)


def run_demo():
    path = run_graph(NODES)
    prompt = "Summarize this graph flow in one sentence.\\nFlow: " + path
    client = get_client()
    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022"),
        max_tokens=120,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
    print(path)
    print(response.content[0].text)


if __name__ == "__main__":
    run_demo()
""",
}


def slugify(text):
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "project"


def load_config():
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as handle:
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
""".format(name=project_name)
    return (
        f"# {project_name}\n\n"
        f"Topic: {topic}\n\n"
        f"Created: {created_at}\n\n"
        f"## Overview\n{summary}\n\n"
        f"## Learning Goals\n{goals_lines}\n\n"
        "## Structure\n"
        f"```\n{structure}```\n\n"
        "## Setup\n"
        "Set ANTHROPIC_API_KEY in your environment. Optional: CLAUDE_MODEL.\n\n"
        "## Run\n"
        "```bash\npython src/main.py\n```\n"
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
    code = CLAUDE_TEMPLATES.get(topic) or CLAUDE_TEMPLATES["LLM Fundamentals"]
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
    assets = TOPIC_LIBRARY.get(topic) or TOPIC_LIBRARY["LLM Fundamentals"]

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
