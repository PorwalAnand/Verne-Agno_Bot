# agno_vernebot/__init__.py

"""
Agno-enhanced VerneBot module.

This package contains:
- `agent.py` for initializing and managing the Agno agent.
- `tools.py` for custom tool integrations such as web search and data utilities.
"""

from .agent import create_verne_agno_agent
from .tools import duckduckgo_search

__all__ = ["create_verne_agno_agent", "duckduckgo_search"]
