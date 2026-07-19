"""RAG Retriever v2 — wraps chatty-core's RAGPipeline.

Drop-in replacement for retriever.py when chatty-core is installed.
"""
try:
    from chatty_core.rag import RAGPipeline as CoreRAG
    HAS_CORE = True
except ImportError:
    HAS_CORE = False

from core.config import Config


_rag_instance = None


def _get_rag(config: Config = None):
    global _rag_instance
    if _rag_instance is None:
        if HAS_CORE:
            _rag_instance = CoreRAG(collection_name="project")
        else:
            return None
    return _rag_instance


def query_knowledge(question: str, collection_name: str = "project", n_results: int = 5, config: Config = None) -> list[dict]:
    """Query the vector database for relevant chunks."""
    rag = _get_rag(config)
    if rag is None:
        from rag.retriever import query_knowledge as _legacy_query
        return _legacy_query(question, collection_name, n_results, config)

    results = rag.query(question, n_results)
    return [{"text": r.content, "file": r.source, "score": 1 - r.distance} for r in results]


def index_directory(directory: str, extensions: list[str] = None, config: Config = None) -> int:
    """Index a directory into the RAG store."""
    rag = _get_rag(config)
    if rag is None:
        from rag.indexer import index_directory as _legacy_index
        return _legacy_index(directory, config)

    return rag.index_directory(directory, extensions)
