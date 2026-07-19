"""Agent v2 — wraps chatty-core's ReActAgent with Chronos's tool registry.

Use this as a drop-in replacement for agent.py when chatty-core is installed.
Falls back to the original agent.py if chatty-core is not available.
"""
import os
from typing import Any

try:
    from chatty_core.agent import ReActAgent as CoreAgent
    from chatty_core.agent import Tool as CoreTool
    from chatty_core.provider import ProviderRouter
    from chatty_core.config import Settings
    HAS_CORE = True
except ImportError:
    HAS_CORE = False

from core.config import Config


def _chrono_tools_to_core() -> list:
    """Convert Chronos's tool objects to chatty-core Tool objects."""
    if not HAS_CORE:
        return []

    from tools.registry import get_all_tools

    core_tools = []
    for tool in get_all_tools():
        # Chronos tools have: .name, .description, .input_schema, .execute(**kwargs)
        # chatty-core tools need: .name, .description, .parameters (JSON Schema), .func (async callable)

        # Get parameters from Pydantic schema
        if tool.input_schema:
            params = tool.input_schema.model_json_schema()
        else:
            params = {"type": "object", "properties": {}}

        # Wrap sync execute() as async func
        def make_wrapper(t):
            async def wrapper(**kwargs):
                return t.execute(**kwargs)
            return wrapper

        core_tool = CoreTool(
            name=tool.name,
            description=tool.description,
            parameters=params,
            func=make_wrapper(tool),
        )
        core_tools.append(core_tool)

    return core_tools


class ChronosAgent:
    """Chronos agent that uses chatty-core when available."""

    def __init__(self, config: Config, max_iterations: int = 30):
        self.config = config
        self.max_iterations = max_iterations

        if HAS_CORE:
            settings = Settings()
            self.router = ProviderRouter(settings)
            self.agent = CoreAgent(
                router=self.router,
                max_steps=max_iterations,
                model=config.get("model"),
            )
            # Register Chronos tools
            for tool in _chrono_tools_to_core():
                self.agent.register_tool(tool)
        else:
            # Fallback to original agent
            from core.agent import ReActAgent
            self._legacy_agent = ReActAgent(config, max_iterations)

    def run(self, task: str) -> str:
        """Execute a task autonomously."""
        if HAS_CORE:
            import asyncio
            result = asyncio.run(self.agent.run(task))
            return result.answer
        else:
            return self._legacy_agent.run(task)
