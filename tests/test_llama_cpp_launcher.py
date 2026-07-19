"""Tests for llm/llama_cpp_launcher.py — GPU detection and llama-server launcher."""
import sys
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


class TestDetectGPU:
    def test_detect_amd(self):
        from llm.llama_cpp_launcher import detect_gpu_backend
        mock_result = MagicMock()
        mock_result.stdout = "AMD Radeon RX 580\n"
        with patch("subprocess.run", return_value=mock_result):
            assert detect_gpu_backend() == "hip"

    def test_detect_nvidia(self):
        from llm.llama_cpp_launcher import detect_gpu_backend
        mock_result = MagicMock()
        mock_result.stdout = "NVIDIA GeForce GTX 1080\n"
        with patch("subprocess.run", return_value=mock_result):
            assert detect_gpu_backend() == "vulkan"

    def test_detect_exception(self):
        from llm.llama_cpp_launcher import detect_gpu_backend
        with patch("subprocess.run", side_effect=Exception("fail")):
            assert detect_gpu_backend() == "vulkan"

    def test_detect_no_amd(self):
        from llm.llama_cpp_launcher import detect_gpu_backend
        mock_result = MagicMock()
        mock_result.stdout = "Intel UHD Graphics\n"
        with patch("subprocess.run", return_value=mock_result):
            assert detect_gpu_backend() == "vulkan"


class TestGetServerBinary:
    def test_primary_exists(self):
        from llm.llama_cpp_launcher import get_server_binary
        with patch("pathlib.Path.exists", return_value=True):
            result = get_server_binary("vulkan")
            assert result is not None

    def test_fallback_exists(self):
        from llm.llama_cpp_launcher import get_server_binary, BINARIES, FALLBACK_BINARIES
        with patch("pathlib.Path.exists", side_effect=lambda self: False):
            pass
        # Mock BINARIES to not exist, FALLBACK to exist
        mock_primary = MagicMock()
        mock_primary.exists.return_value = False
        mock_fallback = MagicMock()
        mock_fallback.exists.return_value = True
        with patch.dict("llm.llama_cpp_launcher.BINARIES", {"vulkan": mock_primary}), \
             patch.dict("llm.llama_cpp_launcher.FALLBACK_BINARIES", {"vulkan": mock_fallback}):
            result = get_server_binary("vulkan")
            assert result is mock_fallback

    def test_not_found(self):
        from llm.llama_cpp_launcher import get_server_binary
        mock_primary = MagicMock()
        mock_primary.exists.return_value = False
        mock_fallback = MagicMock()
        mock_fallback.exists.return_value = False
        with patch.dict("llm.llama_cpp_launcher.BINARIES", {"vulkan": mock_primary}), \
             patch.dict("llm.llama_cpp_launcher.FALLBACK_BINARIES", {"vulkan": mock_fallback}):
            result = get_server_binary("vulkan")
            assert result is None

    def test_auto_detect(self):
        from llm.llama_cpp_launcher import get_server_binary
        with patch("llm.llama_cpp_launcher.detect_gpu_backend", return_value="vulkan"), \
             patch("pathlib.Path.exists", return_value=True):
            result = get_server_binary()
            assert result is not None


class TestStartServer:
    def test_success_vulkan(self):
        from llm.llama_cpp_launcher import start_server
        mock_binary = MagicMock()
        mock_binary.exists.return_value = True
        with patch.dict("llm.llama_cpp_launcher.BINARIES", {"vulkan": mock_binary}), \
             patch.dict("llm.llama_cpp_launcher.FALLBACK_BINARIES", {"vulkan": mock_binary}), \
             patch("llm.llama_cpp_launcher.detect_gpu_backend", return_value="vulkan"), \
             patch("subprocess.Popen") as mock_popen:
            result = start_server("/model.gguf", port=8080, backend="vulkan")
            assert result is not None

    def test_success_hip(self):
        from llm.llama_cpp_launcher import start_server
        mock_binary = MagicMock()
        mock_binary.exists.return_value = True
        with patch.dict("llm.llama_cpp_launcher.BINARIES", {"hip": mock_binary}), \
             patch.dict("llm.llama_cpp_launcher.FALLBACK_BINARIES", {"hip": mock_binary}), \
             patch("llm.llama_cpp_launcher.detect_gpu_backend", return_value="hip"), \
             patch("subprocess.Popen") as mock_popen:
            result = start_server("/model.gguf", port=8080, backend="hip")
            assert result is not None
            call_kwargs = mock_popen.call_args
            assert call_kwargs[1]["env"]["HSA_OVERRIDE_GFX_VERSION"] == "11.0.2"

    def test_no_binary(self):
        from llm.llama_cpp_launcher import start_server
        mock_primary = MagicMock()
        mock_primary.exists.return_value = False
        mock_fallback = MagicMock()
        mock_fallback.exists.return_value = False
        with patch.dict("llm.llama_cpp_launcher.BINARIES", {"vulkan": mock_primary}), \
             patch.dict("llm.llama_cpp_launcher.FALLBACK_BINARIES", {"vulkan": mock_fallback}), \
             patch("llm.llama_cpp_launcher.detect_gpu_backend", return_value="vulkan"):
            result = start_server("/model.gguf", backend="vulkan")
            assert result is None


class TestIsServerRunning:
    def test_running(self):
        from llm.llama_cpp_launcher import is_server_running
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        with patch("httpx.get", return_value=mock_resp):
            assert is_server_running(8080) is True

    def test_not_running(self):
        from llm.llama_cpp_launcher import is_server_running
        with patch("httpx.get", side_effect=Exception("Connection refused")):
            assert is_server_running(8080) is False

    def test_non_200(self):
        from llm.llama_cpp_launcher import is_server_running
        mock_resp = MagicMock()
        mock_resp.status_code = 503
        with patch("httpx.get", return_value=mock_resp):
            assert is_server_running(8080) is False
