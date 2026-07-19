# 🤖 Chatty Chronos v2

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/georgevpopa/Chatty-Chronos-v2?style=social)](https://github.com/georgevpopa/Chatty-Chronos-v2/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/georgevpopa/Chatty-Chronos-v2?style=social)](https://github.com/georgevpopa/Chatty-Chronos-v2/network/members)
[![Local First](https://img.shields.io/badge/local--first-Ollama%20%7C%20llama.cpp-orange.svg)](https://ollama.com/)
[![VectorDB](https://img.shields.io/badge/VectorDB-Chroma-purple.svg)](https://trychroma.com)
[![ReAct Mode](https://img.shields.io/badge/Agent-ReAct%20Loop-lightgrey.svg)]()
[![Web UI](https://img.shields.io/badge/UI-Web%20Dashboard-blueviolet.svg)]()
[![Plugin System](https://img.shields.io/badge/Plugins-Dynamic%20Tool%20Injection-teal.svg)]()
[![Agent Registry](https://img.shields.io/badge/Agents-Specialised%20Registry-crimson.svg)]()

> A terminal-first autonomous coding agent. Chat with AI, execute tasks, search codebases, generate specs — and now extend everything with MCP, plugins, and a Multi-Agent Swarm. Runs locally with Ollama/llama.cpp or falls back to cloud LLMs.

---

## ✨ What's new in v2 (The Big 5 Improvements)

| Improvement | Description |
|---|---|
| **🔒 Sandboxed Execution** | Python REPL runs in `RestrictedPython` in an isolated IPC background subprocess. Plugins now require strict `plugin.json` manifests declaring their capabilities. |
| **🗃️ Pydantic v2 Core** | Complete refactoring of config, internal schemas, and `Tools` (inputs now fully typed & validated with Pydantic `BaseModel`). |
| **📊 OpenTelemetry & Structlog** | The entire ReAct Loop (Thought → Action → Observation) is instrumented with `opentelemetry-api` spans and `structlog` for deep observability. View traces via `/api/traces` in the Web UI. |
| **🧪 Pytest Suite & LLM Mocking** | Deep test coverage with `pytest`, property-based testing with `hypothesis` for file IO idempotency, and full ReAct loop mocked integrations. |
| **🐳 Docker & DevOps** | Shipped with a multi-stage `Dockerfile`, a `docker-compose.yml` for unified App+ChromaDB+Ollama boot, and VS Code `.devcontainer` support! |

---

## 🌟 Standard Features

| Feature | Description |
|---------|-------------|
| **🤖 Multi-Provider LLMs** | Ollama (local), llama.cpp (local GGUF auto-launcher), Nvidia NIM, Google Gemini, Groq Cloud, OpenRouter |
| **🔄 Auto-Fallback** | Instantly falls back to alternative providers/models when a service is rate-limited or unavailable |
| **🧠 ReAct Agent Loop** | Autonomous step-by-step reasoning loop (Thought → Action → Observation) with safe limits |
| **🌐 Web Dashboard** | Glassmorphism dashboard with SSE streaming, permission modals, workspace explorer, and live log console |
| **🕸️ Multi-Agent Swarm UI** | A visual Swarm dashboard that tracks tasks moving between Planner, Writer, and Reviewer sub-agents |
| **🔌 MCP Protocol Support** | Instantly consume any MCP server (Model Context Protocol) to add new tools to Chronos (`/mcp add`) |
| **💾 Multi-Session History** | Save, load, delete, and manage multiple chat histories dynamically from the sidebar |
| **📊 Hardware Monitor** | iGPU / RAM telemetry card showing system loads and background `llama-server` VRAM footprint |
| **💾 Context Compaction** | LLM-driven summarisation that automatically condenses long chat history to save context tokens |
| **🗂️ RAG Semantic Search** | Chunk, embed, and index files into a local ChromaDB database for smart project queries |
| **🧠 Vector Memory** | Persistent long-term memory for agent preferences and facts via ChromaDB (`store_memory`, `search_memory`) |
| **👥 Specialised Sub-Agents** | Delegate to typed child agents (file_analyst, shell_runner, writer, researcher) each with focused tool-sets |
| **🐍 Sandboxed Python REPL** | Secure, stateful Python REPL running in an isolated background daemon with a strict timeout limit |
| **🌐 Web Fetcher** | Fetch and parse documentation dynamically from the web |
| **🙋 Ask User Tool** | Chronos can ask the user clarifying questions before making destructive changes |
| **🔌 Dynamic Plugin System** | Plugins inject new slash commands and new agent tools. Hot-reload without restarting |
| **🗂️ Agent Registry** | Register, discover and instantiate named agent types at runtime or from plugins |
| **🛡️ 3-Tier Security** | Granular execution security (Yes-Once, Yes-Session, Trust Workspace Permanently) for dangerous tools |
| **🖥️ Interactive Web Permissions** | Tool permission requests surface as interactive modals in the browser — no terminal needed |
| **📋 Git Auto-Commit UI** | View `git status` visually in the dashboard and ask Chronos to generate conventional commit messages |

---

## Requirements

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Python** | 3.10+ | [python.org/downloads](https://www.python.org/downloads/) — check "Add to PATH" |
| **Local LLM Engine** | - | **llama.cpp / llama-server** (Recommended for GPU hardware acceleration) OR **Ollama** |

**Supported OS:** Windows (primary), Linux, macOS

---

## 🚀 Installation (Simple Guide for Windows)

No terminal experience required! Just follow these steps:

1. **Install Python:** Download Python 3.10+ from [python.org/downloads](https://www.python.org/downloads/). 
   *⚠️ CRITICAL: During installation, you MUST check the box that says **"Add Python.exe to PATH"** at the bottom of the installer window!*
2. **Download Chatty Chronos:** Click the green **"<> Code"** button at the top of this GitHub page and select **"Download ZIP"**.
3. **Extract the folder:** Right-click the downloaded ZIP file and select "Extract All...".
4. **Install:** Open the extracted folder and double-click the **`Install_Windows.bat`** file. A window will appear and install everything automatically.
5. **Get the AI Brain:** Download and install [Ollama](https://ollama.com/) (it's a simple installer). Once installed, it runs in your taskbar.

That's it! To play with Chronos, just double-click **`Start_Chronos.bat`** in the folder!

---

## 💻 Advanced / Developer Installation

If you prefer the command line or are on Linux/macOS, use these instructions.

### 🐧 Linux & 🍏 macOS

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git curl

# macOS
brew install python git

# Clone and Deploy
git clone https://github.com/georgevpopa/Chatty-Chronos-v1.git
cd Chatty-Chronos-v1
python3 deploy.py
```

### 🪟 Windows (via Git)

```bash
git clone https://github.com/georgevpopa/Chatty-Chronos-v1.git
cd Chatty-Chronos-v1
python deploy.py
```

*Deploy options (CLI):*
```bash
python deploy.py --skip-models      # Don't pull Ollama models
python deploy.py --path "D:\mypath" # Install to specific directory
python deploy.py --update           # Update existing install
```

---

### 🧠 Setting Up Local AI Brains

#### **Option A: llama.cpp / llama-server (Recommended for AMD & NVIDIA GPUs)**
1. Download a pre-compiled `llama-server` binary for your OS from [llama.cpp releases](https://github.com/ggerganov/llama.cpp/releases).
2. Download a GGUF model (e.g. `Qwen3.5-9B-Instruct-Q4_K_M.gguf`) and save it locally.
3. On Windows, double-click `Start_Chronos.bat`. It will prompt you to select the GGUF model and launch `llama-server.exe` automatically on port `8069` with hardware optimisations.

#### **Option B: Ollama (Simple alternative)**
```bash
# Windows/macOS: Download installer from https://ollama.com
# Linux:
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
ollama pull llama3.1
ollama pull nomic-embed-text
```

### Uninstall

```bash
cd Chatty-Chronos-v1
python uninstall.py          # Interactive — asks what to remove
python uninstall.py --all    # Remove everything including user data
```

---

## 🚀 Starting Commands & Environments

Chronos v2 offers multiple ways to run, test, and deploy the application.

### 1. Standard Run (CLI or Web GUI)
Run Chronos natively on your host machine (requires Python 3.10+).

```bash
# Terminal REPL (CLI Mode)
python main.py

# Web Dashboard with GUI (auto-opens browser on http://localhost:8000)
python main.py --web

# Windows Users — double-click the starter batch file
Start_Chronos.bat
```

### 2. Docker & Docker Compose (Containerized Ecosystem)
Launch the entire ecosystem (Chronos App + ChromaDB + Ollama sidecar) fully isolated from your host system.
Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
# Build and start all services in the background
docker-compose up --build -d

# View the live logs of the Chronos app
docker-compose logs -f chronos

# Stop the ecosystem
docker-compose down
```

### 3. Running the Test Suite (`pytest`)
Chronos v2 includes a comprehensive test suite to validate the Agent ReAct loop, sandboxed tools, and Pydantic schemas.

**Step 1: Install testing dependencies**
```bash
pip install pytest hypothesis
```

**Step 2: Run the automated tests**
```bash
# Run all tests in the project
pytest tests/

# Run specific files with verbose output
pytest tests/test_filesystem.py -v
pytest tests/test_agent.py -v
```

### 🌐 Web UI Dashboard

Chronos ships with a premium glassmorphism web interface accessible from any browser:

```bash
python main.py --web        # starts on http://localhost:8000
# or from within the REPL:
chronos > /web
```

**New in the Web UI:**
- **Interactive Permission Modals** — tool execution requests pop up as browser dialogs with Allow Once / Allow Session / Trust Workspace / Deny buttons
- **Workspace Explorer & Git UI** — browse files and view real-time Git status with AI-generated commit messages
- **Multi-Agent Swarm Tab** — watch in real-time as tasks are passed between Planner, Writer, and Reviewer
- **Live Log Console** — view `chronos.log` + `llama_server.log` in real time (📋 button)
- **GGUF Server Restart** — restart `llama-server` without leaving the browser

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `/help` | Show all commands |
| `/model [name]` | Show or switch the active model |
| `/provider [name]` | Show or switch the active LLM provider |
| `/models` | List available models for current provider |
| `/tools` | List all tools and their permission levels |
| `/agent <task>` | Run autonomous ReAct agent (multi-step, uses tools) |
| `/team <task>` | Pass a task through a Multi-Agent Swarm (Planner → Writer → Reviewer) |
| `/mcp add <name> <cmd>` | Connect an MCP server to add tools to Chronos (e.g. `/mcp add fetch npx -y @anthropic-ai/fetch-server`) |
| `/web [port]` | Launch the interactive web dashboard |
| `/index <path>` | Index a directory for semantic search (RAG) |
| `/index_web <url>` | Index a web page into the knowledge base |
| `/knowledge <question>` | Query indexed knowledge (RAG) |
| `/memory` | Show persistent memory facts |
| `/memory add <fact>` | Teach Chronos a persistent fact |
| `/memory remove <n>` | Remove a fact by index |
| `/memory clear` | Clear all memory |
| `/spec <feature>` | Generate requirements + design + tasks documents |
| `/specs` | List existing specs |
| `/providers` | Show LLM provider status (local + cloud) |
| `/add_provider` | Wizard to dynamically add a new LLM provider |
| `/plugins` | List loaded plugins (shows slash commands + injected tools) |
| `/plugins reload` | Hot-reload plugins from disk without restarting |
| `/agents` | List all registered agent types |
| `/agents register <name> <desc>` | Register a new agent type inline |
| `/doctor` | System health check (LLM, RAG, plugins, memory) |
| `/config` | Show current configuration and file path |
| `/config <key> <value>` | Change a setting (saved immediately) |
| `/save` | Save conversation |
| `/load` | Load last saved conversation |
| `/export [file.md]` | Export conversation to Markdown |
| `/stats` | Show session statistics and token usage |
| `/history` | Show last 5 user messages |
| `/clear` | Clear conversation and reset permissions |
| `/exit` | Quit (auto-saves session) |

---

## Concepts

### Agent (`/agent`)

Autonomous mode. Chronos enters a **ReAct loop** (Reason → Act → Observe → Repeat) to complete complex tasks. It uses tools, checks results, and self-corrects. Max 30 steps with a safety breaker.

```
chronos > /agent Find all Python files with TODO comments and create a summary
```

### Tools (`/tools`)

Built-in capabilities the agent can call autonomously:

| Tool | Permission | What it does |
|------|-----------|--------------|
| `read_file` | auto | Read file contents |
| `write_file` | ask | Create or overwrite a file |
| `search_replace` | ask | Replace exact text in a file |
| `list_directory` | auto | List files in a directory |
| `glob_search` | auto | Find files by pattern (e.g. `**/*.py`) |
| `grep` | auto | Search for text patterns across files |
| `move_file` | ask | Move or rename a file |
| `execute_command` | ask | Run a shell command |
| `delegate_subtask` | ask | Spawn a specialised child agent |
| `ask_user` | auto | Ask you a clarifying question before taking an action |
| `fetch_webpage` | auto | Fetch and read content from URLs |
| `run_python` | ask | Execute Python in a persistent, isolated background REPL |
| `store_memory` / `search_memory` | auto | Manage persistent facts across sessions via Vector DB |

**Tool permission levels:**
- `y` — allow this one invocation
- `ya` — allow all for this session
- `yw` — trust this workspace permanently (saved to disk)

> In Web UI mode, these appear as interactive browser modals.

### Index & Knowledge (`/index`, `/knowledge`)

Index a project into ChromaDB. Chronos chunks files, generates embeddings, and stores them locally. Ask semantic questions about your code without sending anything to the cloud.

```
chronos > /index . --include *.py
chronos > /knowledge how does the config system work
```

### Memory (`/memory`)

Persistent facts that survive across sessions. Teach Chronos your preferences, project conventions, or important context.

```
chronos > /memory add My preferred language is Python with type hints
chronos > /memory add The project uses FastAPI for the backend
```

Stored at `~/.chatty-chronos/memory.json`.

### Spec (`/spec`)

AI-powered spec-driven development. Generates structured documents from a feature description:
- `requirements.md` — user stories, acceptance criteria
- `design.md` — architecture, components, API design
- `tasks.md` — implementation checklist

```
chronos > /spec Add user authentication with JWT
```

Creates `specs/add-user-authentication-with-jwt/` with all three files.

---

## Plugin System

Plugins are `.py` files dropped into `~/.chatty-chronos/plugins/`. They are **auto-loaded on startup** and can be hot-reloaded with `/plugins reload`.

A plugin can do **two things**:
1. Register **slash commands** (e.g. `/git-status`)
2. Inject **new tools** directly into the ReAct agent — no code changes required

### Command-only plugin (minimal)

```python
# ~/.chatty-chronos/plugins/hello.py
from plugins.base import Plugin

class HelloPlugin(Plugin):
    name = "hello"
    description = "A greeting plugin"
    commands = {"/hello": "Say hello to someone"}

    def handle_command(self, command, arg):
        if command == "/hello":
            return f"Hello, {arg or 'world'}!"
```

### Plugin that injects a tool into the agent

```python
# ~/.chatty-chronos/plugins/git_plugin.py
from plugins.base import Plugin
from tools.base import Tool
import subprocess

class GitStatusTool(Tool):
    def __init__(self):
        super().__init__(
            name="git_status",
            description="Return the current git status of a repository directory.",
            parameters={
                "path": {"type": "string", "description": "Repo directory", "required": False}
            },
            requires_permission=False,
        )
    def execute(self, path=".", **kwargs):
        result = subprocess.run(["git", "status", "--short"], cwd=path,
                                capture_output=True, text=True, timeout=10)
        return result.stdout or "(working tree clean)"

class GitPlugin(Plugin):
    name        = "git"
    description = "Git integration: commands + agent tools"
    version     = "1.0.0"
    commands    = {"/git-status": "Show git status"}
    tools       = [GitStatusTool()]        # ← injected into the agent automatically

    def handle_command(self, command, arg):
        if command == "/git-status":
            return GitStatusTool().execute(path=arg or ".")
```

Once loaded, the agent can call `git_status` autonomously when you ask it about git state — just like any built-in tool.

---

## Agent Registry

Chronos ships with a registry of **named, specialised agent types** that can be instantiated via `delegate_subtask`. Each type has its own system prompt and a whitelist of tools it is allowed to use.

### Built-in agent types

| Agent Type | Tools Allowed | Purpose |
|---|---|---|
| `file_analyst` | read_file, list_directory, glob_search, grep | Read-only codebase analysis and summarisation |
| `shell_runner` | execute_command, read_file, write_file | DevOps automation, command execution |
| `writer` | read_file, write_file, search_replace | File generation and editing |
| `researcher` | read_file, list_directory, glob_search, grep | Knowledge gathering without modification |

### Using specialised agents

**From the CLI:**
```
chronos > /agents                              # list all registered types
chronos > /agent Analyse src/ for dead code    # the LLM may pick file_analyst automatically
```

**The LLM decides** which agent type to use when delegating a subtask:
```
delegate_subtask(task="Review all Python files for security issues", agent_type="file_analyst")
delegate_subtask(task="Run the test suite and collect results",      agent_type="shell_runner")
```

### Registering a custom agent type

**From the CLI:**
```
chronos > /agents register security_auditor "Audits code for security vulnerabilities"
```

**From Python (e.g. inside a plugin):**
```python
from core.agent_registry import register_agent, AgentSpec

register_agent(AgentSpec(
    name           = "security_auditor",
    description    = "Audits code for security vulnerabilities",
    system_prompt  = (
        "You are a senior security engineer. Find vulnerabilities, "
        "injection points, and insecure patterns. Never modify files."
    ),
    tool_names     = ["read_file", "glob_search", "grep"],
    max_iterations = 25,
))
```

---

## Configuration

### Config file (`~/.chatty-chronos/config.json`)

```json
{
  "provider": "ollama",
  "model": "llama3.1:latest",
  "ollama_host": "http://localhost:11434",
  "llamacpp_host": "http://localhost:8080",
  "streaming": true,
  "max_context_messages": 20
}
```

Use `/config` inside Chronos to view/edit, or edit the file directly.

### Using a custom llama.cpp server

```bash
# Start your custom build
llama.exe --server --host 127.0.0.1 --port 8069 --model "path\to\model.gguf" --n-gpu-layers 99
```

```
chronos > /config provider llamacpp
chronos > /config llamacpp_host http://localhost:8069
chronos > /config model local
```

### Adding cloud LLM providers

Create `.env` in the project root:
```bash
GROQ_API_KEY=gsk_your_key_here          # https://console.groq.com/keys
GEMINI_API_KEY=your_key_here            # https://aistudio.google.com/apikey
NVIDIA_API_KEY=your_key_here            # https://build.nvidia.com/
MISTRAL_API_KEY=your_key_here           # https://console.mistral.ai/api-keys
OPENROUTER_API_KEY=sk-or-your_key_here  # https://openrouter.ai/keys
```

Verify with `/providers`. Keys are hot-reloaded — no restart needed.

**Add any OpenAI-compatible provider** (`~/.chatty-chronos/providers.json`):
```json
{
    "name": "together",
    "type": "openai_compatible",
    "base_url": "https://api.together.xyz/v1",
    "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    "env_key": "TOGETHER_API_KEY"
}
```

---

## Data Locations

| Path | Contents |
|------|----------|
| `~/.chatty-chronos/config.json` | Settings (model, host, provider) |
| `~/.chatty-chronos/providers.json` | LLM provider list |
| `~/.chatty-chronos/memory.json` | Persistent memory (taught facts) |
| `~/.chatty-chronos/session.json` | Last saved conversation |
| `~/.chatty-chronos/vectordb/` | ChromaDB embeddings (RAG index) |
| `~/.chatty-chronos/plugins/` | Drop-in plugin `.py` files |
| `~/.chatty-chronos/prompt_history.txt` | Input history (arrow keys) |
| `~/.chatty-chronos/trusted_workspaces` | Permanently trusted directories |
| `~/.chatty-chronos/.env` | Global API keys (optional) |

---

## Architecture

```
Chatty-Chronos-v1/
├── main.py                  # REPL entry point + CLI command router
├── deploy.py                # Cross-platform installer
├── uninstall.py             # Uninstaller
├── pyproject.toml           # Package configuration
├── STEERING.md              # Project conventions for self-development
├── Start_Chronos.bat        # Model selection starter (Windows)
│
├── core/                    # Agent core
│   ├── agent.py             # ReActAgent — Thought → Tool → Observe loop
│   ├── agent_registry.py    # ★ Named specialised agent types + build_agent()
│   ├── config.py            # Persistent JSON config (~/.chatty-chronos/)
│   ├── permissions.py       # 3-tier trust system + web modal event loop
│   ├── memory.py            # ★ Cross-session persistent vector memory via ChromaDB
│   ├── context.py           # LLM-driven context compaction
│   ├── delegator.py         # Sub-agent spawning with agent_type routing
│   ├── team.py              # ★ Multi-Agent Swarm Orchestration logic
│   ├── mcp_client.py        # ★ Model Context Protocol (MCP) Manager
│   ├── repl_daemon.py       # ★ Secure, sandboxed background Python daemon
│   └── logger.py            # Rotating file logger
│
├── llm/                     # LLM backends
│   ├── ollama_provider.py   # Chat + tool calls via Ollama
│   ├── llamacpp_provider.py # Chat + tool calls via llama-server
│   ├── openai_provider.py   # Universal OpenAI-compatible client
│   ├── fallback.py          # Auto-fallback across providers
│   └── server_manager.py    # Auto-launch/stop llama-server.exe
│
├── tools/                   # Agent tools
│   ├── base.py              # Tool dataclass + Ollama schema converter
│   ├── registry.py          # ★ Dynamic registry (built-ins + plugin tools)
│   ├── filesystem.py        # ReadFile, WriteFile, Grep, Glob, Move...
│   ├── shell.py             # ExecuteCommand
│   ├── human.py             # ★ AskUser tool
│   ├── web.py               # ★ FetchWebpage tool
│   ├── python_repl.py       # ★ Stateful Python execution
│   ├── memory_tools.py      # ★ StoreMemory, SearchMemory
│   ├── mcp_tool.py          # ★ MCP tool wrapper
│   └── agent_delegator.py   # ★ DelegateSubtask with agent_type support
│
├── plugins/                 # Plugin system
│   ├── base.py              # ★ Plugin base class (tools field + get_tools())
│   └── loader.py            # Auto-load + hot-reload from ~/.chatty-chronos/plugins/
│
├── ui/                      # Web Dashboard backend
│   └── web.py               # ThreadingHTTPServer, SSE, permission API, workspace/logs endpoints
│
├── static/                  # Web Dashboard frontend
│   └── index.html           # Glassmorphism UI (streaming, modals, explorer, log console)
│
├── rag/                     # Semantic search
│   ├── indexer.py           # Chunk + embed + store in ChromaDB
│   ├── embeddings.py        # Embedding provider abstraction
│   └── retriever.py         # Semantic query + context assembly
│
├── spec/                    # Spec-driven development
│   ├── generator.py         # AI-powered spec document generator
│   └── templates/           # Markdown templates
│
└── docs/                    # Documentation
    └── CHRONOS_KNOW_HOW.md  # Deep-dive technical reference
```

Items marked **★** are newly added or significantly extended features.

---

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=georgevpopa/Chatty-Chronos-v1&type=Date)](https://star-history.com/#georgevpopa/Chatty-Chronos-v1&Date)

---

## License

MIT — see [LICENSE](LICENSE) for details.

> **Author:** [georgevpopa](https://github.com/georgevpopa) 🚀
> If you find this project useful, drop a ⭐!
