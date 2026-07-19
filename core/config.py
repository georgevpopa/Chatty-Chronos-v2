"""Configuration manager — persistent settings in ~/.chatty-chronos/config.json."""
import json
import os
from pathlib import Path
from pydantic import BaseModel, Field

class AppConfigSchema(BaseModel):
    provider: str = "nvidia"
    model: str = "nvidia/llama-3.1-nemotron-70b-instruct"
    base_url: str = "https://integrate.api.nvidia.com/v1"
    ollama_host: str = "http://localhost:11434"
    llamacpp_host: str = "http://localhost:8080"
    embedding_provider: str = "local"
    embedding_model: str = "all-MiniLM-L6-v2"
    streaming: bool = True
    max_context_messages: int = 20
    local_server_enabled: bool = False
    local_server_bin: str = "E:\\AI_Sandbox\\llama-b9672-bin-win-hip-radeon-x64\\llama-server.exe"
    local_server_model: str = ""
    local_server_port: int = 8080
    local_server_ngl: int = 99
    local_server_ctx: int = 16384
    local_server_parallel: int = 1
    local_server_reasoning_budget: int = 1024
    local_server_cache_ram: int = 512
    llamacpp_timeout: int = 600
    agent_max_iterations: int = 15
    local_server_env: dict = Field(default_factory=lambda: {
        "HSA_OVERRIDE_GFX_VERSION": "11.0.2",
        "HIP_VISIBLE_DEVICES": "0"
    })
    compaction_enabled: bool = True
    self_reflection: bool = False
    enable_reflection: bool = True


class Config:
    def __init__(self):
        self.dir = Path.home() / ".chatty-chronos"
        self.dir.mkdir(exist_ok=True)
        self.path = self.dir / "config.json"
        self._schema = self._load()

    @property
    def data(self):
        return self._schema.model_dump()

    def _load(self) -> AppConfigSchema:
        if self.path.exists():
            try:
                with open(self.path, "r") as f:
                    saved = json.load(f)
                return AppConfigSchema(**saved)
            except Exception:
                return AppConfigSchema()
        return AppConfigSchema()

    def save(self):
        with open(self.path, "w") as f:
            f.write(self._schema.model_dump_json(indent=2))

    def get(self, key, default=None):
        return getattr(self._schema, key, default)

    def set(self, key, value):
        setattr(self._schema, key, value)
        self.save()