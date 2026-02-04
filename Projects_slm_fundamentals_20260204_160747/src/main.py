import random


INTENTS = {
    "hello": "Hi there. How can I help?",
    "help": "I can summarize basics of LLMs, RAG, SLMs, LangChain, and LangGraph.",
    "rag": "RAG retrieves documents then generates using that context.",
    "bye": "Goodbye!",
}


def small_model_reply(message):
    message = message.lower()
    for key, response in INTENTS.items():
        if key in message:
            return response
    return random.choice(list(INTENTS.values()))


if __name__ == "__main__":
    print(small_model_reply("hello"))
    print(small_model_reply("tell me about rag"))
