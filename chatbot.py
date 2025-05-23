import os
from dotenv import load_dotenv
import google.generativeai as genai
from embedder import load_vectorstore
from langchain_core.documents import Document

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model and retriever
model = genai.GenerativeModel("models/gemini-1.5-flash")
vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Define VerneBot system prompt
VERNE_PROMPT = """
You are VerneBot — a virtual business strategist and AI coach modeled after Verne Harnish.
You provide clear, strategic, and actionable guidance to entrepreneurs, CEOs, and business teams.

You specialize in:
- Scaling Up framework (People, Strategy, Execution, Cash)
- Rockefeller Habits 2.0
- One-Page Strategic Plan (OPSP)
- Execution rhythms and cash flow optimization
- Compensation strategy and growth metrics
- Decision-making under pressure

Speak confidently and use proven frameworks. Avoid fluff. Use practical steps and tools like:
• OPSP
• Daily/Weekly huddles
• Cash Conversion Cycle
• Power of One
• 13-week cash forecasts

End your responses with an offer to help further like:
“Would you like a step-by-step for that?” or “Want a worksheet or tool to get started?”

Only use verified content from Verne Harnish’s books and teachings. Never make up information.
"""

# ✅ Main response handler (for Gemini RAG)
def get_response(user_input, chat_history):
    docs = retriever.invoke(user_input)
    context = "\n\n".join(doc.page_content for doc in docs)
    memory = "\n".join([f"{sender.capitalize()}: {msg}" for sender, msg in chat_history[-6:]])

    full_prompt = f"""{VERNE_PROMPT}

Here’s some context from Verne’s verified content:
{context}

Here’s our conversation so far:
{memory}

User: {user_input}
VerneBot:"""

    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Something went wrong, but we're still scaling: \n\n`{e}`"

# Utility to expose RAG-only answer for hybrid handling in 1_Chat.py
def get_knowledgebase_response(prompt: str):
    docs = retriever.invoke(prompt)

    if not docs:
        return None, None

    top_doc = docs[0]
    return top_doc.page_content, None


