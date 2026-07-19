"""Tests for core/agent_v2.py, core/memory_v2.py, rag/retriever_v2.py — v2 adapters."""
import sys
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path
import llm.core_adapter as _ca_mod


# ─── agent_v2.py ─────────────────────────────────────────────────────────────
class TestAgentV2:
    def _fresh(self):
        import core.agent_v2 as mod
        mod.HAS_CORE = True
        return mod

    def test_chrono_tools_core(self):
        mod = self._fresh()
        with patch.object(mod, "HAS_CORE", True):
            mock_tool = MagicMock()
            mock_tool.name = "read_file"
            mock_tool.description = "Read a file"
            mock_tool.input_schema = MagicMock()
            mock_tool.input_schema.model_json_schema.return_value = {"type": "object", "properties": {"path": {"type": "string"}}}

            mock_core_tool = MagicMock()
            with patch("tools.registry.get_all_tools", return_value=[mock_tool]), \
                 patch.object(mod, "CoreTool", return_value=mock_core_tool):
                result = mod._chrono_tools_to_core()
                assert len(result) == 1

    def test_chrono_tools_no_schema(self):
        mod = self._fresh()
        with patch.object(mod, "HAS_CORE", True):
            mock_tool = MagicMock()
            mock_tool.name = "test"
            mock_tool.description = "test"
            mock_tool.input_schema = None

            mock_core_tool = MagicMock()
            with patch("tools.registry.get_all_tools", return_value=[mock_tool]), \
                 patch.object(mod, "CoreTool", return_value=mock_core_tool):
                result = mod._chrono_tools_to_core()
                assert len(result) == 1

    def test_chrono_tools_no_core(self):
        mod = self._fresh()
        with patch.object(mod, "HAS_CORE", False):
            result = mod._chrono_tools_to_core()
            assert result == []

    def test_chronos_agent_init_core(self):
        mod = self._fresh()
        with patch.object(mod, "HAS_CORE", True), \
             patch.object(mod, "Settings"), \
             patch.object(mod, "ProviderRouter") as mock_router, \
             patch.object(mod, "CoreAgent") as mock_agent_cls, \
             patch.object(mod, "_chrono_tools_to_core", return_value=[]):
            config = MagicMock()
            config.get.return_value = "llama3.1"
            agent = mod.ChronosAgent(config, max_iterations=10)
            assert agent.max_iterations == 10

    def test_chronos_agent_init_fallback(self):
        mod = self._fresh()
        with patch.object(mod, "HAS_CORE", False), \
             patch("core.agent.ReActAgent") as mock_legacy:
            config = MagicMock()
            agent = mod.ChronosAgent(config, max_iterations=5)
            assert agent._legacy_agent is not None

    def test_chronos_agent_run_core(self):
        mod = self._fresh()
        with patch.object(mod, "HAS_CORE", True), \
             patch.object(mod, "Settings"), \
             patch.object(mod, "ProviderRouter"), \
             patch.object(mod, "CoreAgent") as mock_agent_cls, \
             patch.object(mod, "_chrono_tools_to_core", return_value=[]), \
             patch("asyncio.run") as mock_run:
            mock_result = MagicMock()
            mock_result.answer = "done"
            mock_run.return_value = mock_result

            config = MagicMock()
            config.get.return_value = "llama3.1"
            agent = mod.ChronosAgent(config)
            result = agent.run("do something")
            assert result == "done"

    def test_chronos_agent_run_fallback(self):
        mod = self._fresh()
        with patch.object(mod, "HAS_CORE", False), \
             patch("core.agent.ReActAgent") as mock_legacy_cls:
            mock_agent = MagicMock()
            mock_agent.run.return_value = "legacy result"
            mock_legacy_cls.return_value = mock_agent

            config = MagicMock()
            agent = mod.ChronosAgent(config)
            result = agent.run("do something")
            assert result == "legacy result"


# ─── memory_v2.py ────────────────────────────────────────────────────────────
class TestMemoryV2:
    def test_init_core(self):
        import core.memory_v2 as mod
        mod._memory_instance = None
        with patch.object(mod, "HAS_CORE", True), \
             patch.object(mod, "CoreMemory") as mock_cls:
            mod.init_memory()
            mock_cls.assert_called_once_with(collection_name="agent_memory")
            assert mod._memory_instance is not None
        mod._memory_instance = None

    def test_init_fallback(self):
        import core.memory_v2 as mod
        mod._memory_instance = None
        with patch.object(mod, "HAS_CORE", False), \
             patch("core.memory.init_memory") as mock_legacy:
            mod.init_memory()
            mock_legacy.assert_called_once()

    def test_store_core(self):
        import core.memory_v2 as mod
        mock_inst = MagicMock()
        mod._memory_instance = mock_inst
        with patch.object(mod, "HAS_CORE", True):
            result = mod.store_memory("key1", "content1", {"type": "test"})
            assert result is True
            mock_inst.store.assert_called_once_with("key1", "content1", {"type": "test"})
        mod._memory_instance = None

    def test_store_core_no_instance(self):
        import core.memory_v2 as mod
        mod._memory_instance = None
        with patch.object(mod, "HAS_CORE", True), \
             patch("core.memory.store_memory", return_value=True) as mock_legacy:
            result = mod.store_memory("key1", "content1")
            assert result is True
            mock_legacy.assert_called_once()

    def test_store_fallback(self):
        import core.memory_v2 as mod
        mod._memory_instance = None
        with patch.object(mod, "HAS_CORE", False), \
             patch("core.memory.store_memory", return_value=True) as mock_legacy:
            result = mod.store_memory("key1", "content1")
            assert result is True

    def test_search_core(self):
        import core.memory_v2 as mod
        mock_inst = MagicMock()
        mock_result = MagicMock()
        mock_result.key = "k1"
        mock_result.content = "c1"
        mock_result.metadata = {}
        mock_inst.search.return_value = [mock_result]
        mod._memory_instance = mock_inst
        with patch.object(mod, "HAS_CORE", True):
            results = mod.search_memory("query", n_results=1)
            assert len(results) == 1
            assert results[0]["key"] == "k1"
        mod._memory_instance = None

    def test_search_core_no_instance(self):
        import core.memory_v2 as mod
        mod._memory_instance = None
        with patch.object(mod, "HAS_CORE", True), \
             patch("core.memory.search_memory", return_value=[]) as mock_legacy:
            results = mod.search_memory("query")
            assert results == []

    def test_search_fallback(self):
        import core.memory_v2 as mod
        mod._memory_instance = None
        with patch.object(mod, "HAS_CORE", False), \
             patch("core.memory.search_memory", return_value=[]) as mock_legacy:
            results = mod.search_memory("query")
            assert results == []


# ─── retriever_v2.py ─────────────────────────────────────────────────────────
class TestRetrieverV2:
    def test_get_rag_core(self):
        import rag.retriever_v2 as mod
        mod._rag_instance = None
        with patch.object(mod, "HAS_CORE", True), \
             patch.object(mod, "CoreRAG") as mock_cls:
            rag = mod._get_rag()
            mock_cls.assert_called_once_with(collection_name="project")
            assert rag is not None
        mod._rag_instance = None

    def test_get_rag_core_cached(self):
        import rag.retriever_v2 as mod
        mock_rag = MagicMock()
        mod._rag_instance = mock_rag
        rag = mod._get_rag()
        assert rag is mock_rag
        mod._rag_instance = None

    def test_get_rag_no_core(self):
        import rag.retriever_v2 as mod
        mod._rag_instance = None
        with patch.object(mod, "HAS_CORE", False):
            rag = mod._get_rag()
            assert rag is None

    def test_query_core(self):
        import rag.retriever_v2 as mod
        mock_rag = MagicMock()
        mock_result = MagicMock()
        mock_result.content = "text"
        mock_result.source = "file.py"
        mock_result.distance = 0.2
        mock_rag.query.return_value = [mock_result]
        mod._rag_instance = mock_rag
        with patch.object(mod, "HAS_CORE", True):
            results = mod.query_knowledge("question")
            assert len(results) == 1
            assert results[0]["text"] == "text"
            assert results[0]["file"] == "file.py"
        mod._rag_instance = None

    def test_query_fallback(self):
        import rag.retriever_v2 as mod
        mod._rag_instance = None
        with patch.object(mod, "HAS_CORE", False), \
             patch("rag.retriever.query_knowledge", return_value=[]) as mock_legacy:
            results = mod.query_knowledge("question")
            assert results == []

    def test_index_core(self):
        import rag.retriever_v2 as mod
        mock_rag = MagicMock()
        mock_rag.index_directory.return_value = 5
        mod._rag_instance = mock_rag
        with patch.object(mod, "HAS_CORE", True):
            result = mod.index_directory("/some/dir")
            assert result == 5
        mod._rag_instance = None

    def test_index_fallback(self):
        import rag.retriever_v2 as mod
        mod._rag_instance = None
        with patch.object(mod, "HAS_CORE", False), \
             patch("rag.indexer.index_directory", return_value=3) as mock_legacy:
            result = mod.index_directory("/some/dir")
            assert result == 3
