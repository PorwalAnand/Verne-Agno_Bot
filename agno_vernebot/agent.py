# agno_vernebot/agent.py
import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from .tools import duckduckgo_search

load_dotenv()

def create_verne_agno_agent():
    model = Groq(id="llama-3.3-70b-versatile")  # Recommended for knowledge + reasoning
    tools = [duckduckgo_search]
    instructions = [
        "You are VerneBot — a business strategist.",
        "Use web search and your tools to guide founders and CEOs.",
        "Always cite or mention sources when helpful."
    ]
    return Agent(model=model, tools=tools, instructions=instructions)
