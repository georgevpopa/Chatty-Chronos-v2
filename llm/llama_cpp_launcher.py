"""llama.cpp auto-launcher — detects GPU and starts the right binary.

Ported from Chatty llama.cpp Local AI. Auto-detects AMD vs NVIDIA
and selects the appropriate llama-server binary.
"""
import os
import subprocess
import sys
from pathlib import Path


# Binary paths (newest builds)
BINARIES = {
    "vulkan": Path(r"E:\AI_Sandbox\llama-b9827-bin-win-vulkan-x64\llama-server.exe"),
    "hip": Path(r"E:\AI_Sandbox\llama-b9827-bin-win-hip-radeon-x64\llama-server.exe"),
}

# Fallback older builds
FALLBACK_BINARIES = {
    "vulkan": Path(r"E:\AI_Sandbox\llama-b9627-bin-win-vulkan-x64\llama-server.exe"),
    "hip": Path(r"E:\AI_Sandbox\llama-b9672-bin-win-hip-radeon-x64\llama-server.exe"),
}


def detect_gpu_backend() -> str:
    """Detect the best GPU backend for this system.

    Returns 'hip' for AMD GPUs, 'vulkan' for NVIDIA/AMD (universal).
    """
    try:
        # Check for AMD ROCm/HIP
        result = subprocess.run(
            ["wmic", "path", "win32_videocontroller", "get", "name"],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout.lower()
        if "amd" in output or "radeon" in output:
            return "hip"
    except Exception:
        pass

    # Default to Vulkan (works on both NVIDIA and AMD)
    return "vulkan"


def get_server_binary(backend: str | None = None) -> Path | None:
    """Get the path to the llama-server binary.

    Args:
        backend: 'vulkan' or 'hip'. Auto-detects if None.

    Returns:
        Path to the binary, or None if not found.
    """
    if backend is None:
        backend = detect_gpu_backend()

    # Try primary binary
    binary = BINARIES.get(backend)
    if binary and binary.exists():
        return binary

    # Try fallback
    binary = FALLBACK_BINARIES.get(backend)
    if binary and binary.exists():
        return binary

    return None


def start_server(
    model_path: str,
    port: int = 8080,
    n_gpu_layers: int = -1,
    context_size: int = 4096,
    backend: str | None = None,
) -> subprocess.Popen | None:
    """Start llama-server as a background process.

    Returns the Popen object, or None if the binary wasn't found.
    """
    binary = get_server_binary(backend)
    if binary is None:
        print("ERROR: No llama-server binary found.", file=sys.stderr)
        print("Expected at:", file=sys.stderr)
        for b in BINARIES.values():
            print(f"  {b}", file=sys.stderr)
        return None

    cmd = [
        str(binary),
        "-m", model_path,
        "--port", str(port),
        "-ngl", str(n_gpu_layers),
        "-c", str(context_size),
        "--host", "0.0.0.0",
    ]

    # AMD HIP environment variables
    if backend == "hip" or detect_gpu_backend() == "hip":
        env = os.environ.copy()
        env["HSA_OVERRIDE_GFX_VERSION"] = "11.0.2"
        env["HIP_VISIBLE_DEVICES"] = "0"
    else:
        env = None

    print(f"Starting llama-server ({backend or detect_gpu_backend()})...")
    print(f"  Binary: {binary}")
    print(f"  Model:  {model_path}")
    print(f"  Port:   {port}")

    return subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def is_server_running(port: int = 8080) -> bool:
    """Check if a llama-server is already running on the given port."""
    import httpx
    try:
        resp = httpx.get(f"http://localhost:{port}/health", timeout=2)
        return resp.status_code == 200
    except Exception:
        return False
