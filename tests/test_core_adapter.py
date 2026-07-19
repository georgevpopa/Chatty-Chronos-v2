"""Tests for llm/core_adapter.py — chatty-core adapter with fallback."""
import sys
import pytest
from unittest.mock import patch, MagicMock
import llm.core_adapter as mod


# ─── HAS_CORE = False (fallback path) ────────────────────────────────────────
class TestFallbackPath:
    def test_chat_fallback(self):
        with patch.object(mod, "HAS_CORE", False), \
             patch("llm.fallback.chat_with_fallback", return_value="fallback response") as mock_fb:
            result = mod.chat_with_fallback_core(
                [{"role": "user", "content": "hi"}], MagicMock()
            )
            assert result == "fallback response"
            mock_fb.assert_called_once()

    def test_providers_fallback(self):
        with patch.object(mod, "HAS_CORE", False), \
             patch("llm.fallback.get_available_providers", return_value=[{"name": "ollama"}]) as mock_fb:
            result = mod.get_available_providers_core()
            assert result == [{"name": "ollama"}]
            mock_fb.assert_called_once()

    def test_list_models_fallback(self):
        with patch.object(mod, "HAS_CORE", False):
            result = mod.list_models_core()
            assert result == {}


# ─── HAS_CORE = True (chatty-core path) ─────────────────────────────────────
class TestCorePath:
    def _mock_config(self, provider="ollama", model="llama3.1", **extra):
        defaults = {"provider": provider, "model": model}
        defaults.update(extra)
        c = MagicMock()
        c.get.side_effect = lambda k, d=None: defaults.get(k, d)
        return c

    def test_chat_ollama(self):
        mock_resp = MagicMock()
        mock_resp.content = "response"
        mock_router = MagicMock()

        with patch.object(mod, "HAS_CORE", True), \
             patch.object(mod, "ProviderRouter", return_value=mock_router), \
             patch.object(mod, "Settings"), \
             patch("asyncio.run", return_value=mock_resp):
            result = mod.chat_with_fallback_core(
                [{"role": "user", "content": "hi"}],
                self._mock_config("ollama", "llama3.1"),
            )
            assert result == "response"

    def test_chat_llamacpp(self):
        mock_resp = MagicMock()
        mock_resp.content = "response"
        mock_router = MagicMock()

        with patch.object(mod, "HAS_CORE", True), \
             patch.object(mod, "ProviderRouter", return_value=mock_router), \
             patch.object(mod, "Settings"), \
             patch("asyncio.run", return_value=mock_resp):
            result = mod.chat_with_fallback_core(
                [{"role": "user", "content": "hi"}],
                self._mock_config("llamacpp", "test.gguf", **{"llamacpp_host": "http://localhost:8069"}),
            )
            assert result == "response"

    def test_chat_nvidia(self):
        mock_resp = MagicMock()
        mock_resp.content = "response"
        mock_router = MagicMock()

        with patch.object(mod, "HAS_CORE", True), \
             patch.object(mod, "ProviderRouter", return_value=mock_router), \
             patch.object(mod, "Settings"), \
             patch("asyncio.run", return_value=mock_resp):
            result = mod.chat_with_fallback_core(
                [{"role": "user", "content": "hi"}],
                self._mock_config("nvidia", "nvidia/llama-3.1"),
            )
            assert result == "response"

    def test_chat_groq(self):
        mock_resp = MagicMock()
        mock_resp.content = "response"
        mock_router = MagicMock()

        with patch.object(mod, "HAS_CORE", True), \
             patch.object(mod, "ProviderRouter", return_value=mock_router), \
             patch.object(mod, "Settings"), \
             patch("asyncio.run", return_value=mock_resp):
            result = mod.chat_with_fallback_core(
                [{"role": "user", "content": "hi"}],
                self._mock_config("groq", "llama-3.1-8b"),
            )
            assert result == "response"

    def test_chat_gemini(self):
        mock_resp = MagicMock()
        mock_resp.content = "response"
        mock_router = MagicMock()

        with patch.object(mod, "HAS_CORE", True), \
             patch.object(mod, "ProviderRouter", return_value=mock_router), \
             patch.object(mod, "Settings"), \
             patch("asyncio.run", return_value=mock_resp):
            result = mod.chat_with_fallback_core(
                [{"role": "user", "content": "hi"}],
                self._mock_config("gemini", "gemini-pro"),
            )
            assert result == "response"

    def test_chat_unknown_provider(self):
        mock_resp = MagicMock()
        mock_resp.content = "response"
        mock_router = MagicMock()

        with patch.object(mod, "HAS_CORE", True), \
             patch.object(mod, "ProviderRouter", return_value=mock_router), \
             patch.object(mod, "Settings"), \
             patch("asyncio.run", return_value=mock_resp):
            result = mod.chat_with_fallback_core(
                [{"role": "user", "content": "hi"}],
                self._mock_config("openrouter", "some/model"),
            )
            assert result == "response"

    def test_chat_no_model(self):
        mock_resp = MagicMock()
        mock_resp.content = "response"
        mock_router = MagicMock()

        with patch.object(mod, "HAS_CORE", True), \
             patch.object(mod, "ProviderRouter", return_value=mock_router), \
             patch.object(mod, "Settings"), \
             patch("asyncio.run", return_value=mock_resp):
            result = mod.chat_with_fallback_core(
                [{"role": "user", "content": "hi"}],
                self._mock_config("ollama", None),
            )
            assert result == "response"

    def test_providers_with_settings(self):
        mock_settings = MagicMock()
        mock_settings.available_providers = ["openai", "groq"]

        with patch.object(mod, "HAS_CORE", True), \
             patch.object(mod, "Settings", return_value=mock_settings):
            result = mod.get_available_providers_core()
            assert len(result) == 3
            assert result[0]["name"] == "ollama"
            assert result[0]["status"] == "local"
            assert result[1]["name"] == "openai"
            assert result[2]["name"] == "groq"

    def test_list_models_with_settings(self):
        mock_settings = MagicMock()
        mock_settings.litellm_model_map = {"ollama/llama3": "ollama/llama3"}

        with patch.object(mod, "HAS_CORE", True), \
             patch.object(mod, "Settings", return_value=mock_settings):
            result = mod.list_models_core()
            assert result == {"ollama/llama3": "ollama/llama3"}
