"""Adapter bridging Chronos provider interface to chatty-core.

Use this module as a drop-in replacement for fallback.py when chatty-core
is installed. Falls back to the original fallback.py if chatty-core is
not available.
"""
import os
from typing import Any

try:
    from chatty_core.provider import ProviderRouter
    from chatty_core.config import Settings
    HAS_CORE = True
except ImportError:
    HAS_CORE = False


def chat_with_fallback_core(messages: list, config) -> str:
    """Chat using chatty-core's ProviderRouter with auto-fallback.

    Drop-in replacement for fallback.chat_with_fallback().
    """
    if not HAS_CORE:
        from llm.fallback import chat_with_fallback
        return chat_with_fallback(messages, config)

    settings = Settings()
    router = ProviderRouter(settings)

    # Map Chronos provider name to litellm model string
    provider_name = config.get("provider", "ollama")
    model = config.get("model")

    # Build model string from provider config
    model_map = {
        "ollama": f"ollama/{model}" if model else None,
        "llamacpp": f"openai/{config.get('llamacpp_host', 'http://localhost:8080')}/v1",
        "nvidia": f"nvidia_nim/{model}" if model else None,
        "groq": f"groq/{model}" if model else None,
        "gemini": f"gemini/{model}" if model else None,
    }

    resolved_model = model_map.get(provider_name) or model

    import asyncio
    response = asyncio.run(router.complete(
        messages=messages,
        model=resolved_model,
    ))
    return response.content


def get_available_providers_core() -> list[dict]:
    """Get available providers using chatty-core's config.

    Drop-in replacement for fallback.get_available_providers().
    """
    if not HAS_CORE:
        from llm.fallback import get_available_providers
        return get_available_providers()

    settings = Settings()
    providers = []
    for name in settings.available_providers:
        providers.append({
            "name": name,
            "type": "openai_compatible",
            "status": "configured",
        })

    # Always include ollama as local
    providers.insert(0, {
        "name": "ollama",
        "type": "ollama",
        "is_local": True,
        "status": "local",
    })

    return providers


def list_models_core() -> dict[str, str]:
    """List all available models from chatty-core."""
    if not HAS_CORE:
        return {}

    settings = Settings()
    return settings.litellm_model_map
