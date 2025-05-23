# agno_vernebot/tools.py

from agno.tools.duckduckgo import DuckDuckGoTools


# ✅ Instantiate built-in Agno tools
duckduckgo_search = DuckDuckGoTools()


# ✅ Optional helper function (not needed if only using in agent)
def summarize_result(result_text: str) -> str:
    """
    Dummy summarizer to simulate result processing.
    In production, replace this with an LLM or semantic summarizer.
    """
    lines = result_text.strip().split("\n")
    summary = f"Found {len(lines)} result(s)."
    return summary
