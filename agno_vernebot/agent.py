from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools

load_dotenv()

def create_verne_agno_agent():
    model = Groq(id="llama-3.3-70b-versatile")  # Based on the Agno sample
    duck_tool = DuckDuckGoTools()               # ✅ Create the instance properly

    return Agent(
        model=model,
        tools=[duck_tool],                      # ✅ Pass the instance (not class)
        description="You are VerneBot — a business coach using Scaling Up frameworks.",
        show_tool_calls=True,                   # Optional: shows which tools are triggered
        markdown=True                           # For clean formatting in Streamlit
    )
