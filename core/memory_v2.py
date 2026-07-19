"""Memory v2 — wraps chatty-core's VectorMemory with Chronos's interface.

Drop-in replacement for memory.py when chatty-core is installed.
"""
try:
    from chatty_core.memory import VectorMemory as CoreMemory
    HAS_CORE = True
except ImportError:
    HAS_CORE = False

from core.config import Config


_memory_instance = None


def init_memory():
    """Initialize memory store."""
    global _memory_instance
    if HAS_CORE:
        _memory_instance = CoreMemory(collection_name="agent_memory")
    else:
        from core.memory import init_memory as _legacy_init
        _legacy_init()


def store_memory(key: str, content: str, metadata: dict = None):
    """Store an item in long-term memory."""
    if HAS_CORE and _memory_instance:
        _memory_instance.store(key, content, metadata or {})
        return True
    else:
        from core.memory import store_memory as _legacy_store
        return _legacy_store(key, content, metadata)


def search_memory(query: str, n_results: int = 3):
    """Search memory for semantic matches."""
    if HAS_CORE and _memory_instance:
        results = _memory_instance.search(query, n_results)
        return [{"key": r.key, "content": r.content, "metadata": r.metadata} for r in results]
    else:
        from core.memory import search_memory as _legacy_search
        return _legacy_search(query, n_results)
