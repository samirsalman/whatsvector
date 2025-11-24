# 🚀 WhatsVector

<div align="center">

<img src="./wv-logo.png" alt="WhatsVector Logo" width="500"/>


![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Version](https://img.shields.io/badge/version-0.1.0-green.svg)

**Vectorize your WhatsApp conversations and chat with them using AI.**

Transform your WhatsApp chat exports into a searchable vector database and interact with your conversation history through an intelligent AI agent.

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
  - [Loading WhatsApp Data](#loading-whatsapp-data)
  - [Chatting with Your Data](#chatting-with-your-data)
- [Configuration](#-configuration)
- [Architecture](#-architecture)
- [Examples](#-examples)
- [TODO](#-todo)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**WhatsVector** is a powerful tool that allows you to:

1. **Load** WhatsApp chat exports into a vector database (Qdrant)
2. **Search** through your conversations using semantic search
3. **Chat** with an AI agent that has access to your conversation history

The tool uses state-of-the-art embedding models and LangGraph agents to provide intelligent, context-aware responses based on your actual WhatsApp conversations.

---

## ✨ Features

- 🔄 **Multi-format Support**: Load WhatsApp chat exports from `.txt` files
- 🎯 **Semantic Search**: Find messages based on meaning, not just keywords
- 🤖 **AI-Powered Agent**: Chat with an intelligent agent that understands your conversation history
- 🔍 **Advanced Filtering**: Filter messages by sender, date ranges, and more
- 🌍 **Multilingual Support**: Works with conversations in multiple languages
- 📦 **Flexible Storage**: Use local Qdrant instances or remote servers
- 🎨 **Multiple LLM Providers**: Support for OpenAI, Groq, and other providers
- 📊 **Progress Tracking**: Visual progress bars during data loading
- 💾 **Profile Management**: Save and reuse configurations for different chat collections

---

## 🛠 Installation

### Prerequisites

- Python 3.11 or higher
- WhatsApp chat export files (`.txt` format)

### Install from source

```bash
git clone https://github.com/samirsalman/whatsvector.git
cd whatsvector
pip install -e .
```

### Dependencies

WhatsVector automatically installs the following dependencies:

- `langgraph` - For building the AI agent
- `qdrant-client` - Vector database client
- `fastembed` - Fast embedding generation
- `typer` - CLI framework
- `pydantic` - Data validation
- `tqdm` - Progress bars

---

## 🚀 Quick Start

### 1. Export Your WhatsApp Chat

1. Open WhatsApp on your phone
2. Go to the chat you want to export
3. Tap on the menu (⋮) → More → Export chat
4. Choose "Without Media" and save the `.txt` file

### 2. Load Your Data

```bash
whatsvector load my-profile /path/to/chat.txt --local-path ./qdrant_data
```

This command:
- Creates a profile named `my-profile`
- Loads your chat data into a local Qdrant instance
- Saves the configuration for future use

### 3. Start Chatting

```bash
whatsvector chat my-profile --username "Your Name"
```

Now you can ask questions about your conversations!

---

## 📖 Usage

### Loading WhatsApp Data

The `load` command processes WhatsApp chat exports and stores them in a vector database.

#### Basic Usage

```bash
whatsvector load <profile-name> <chat-file1> [chat-file2 ...] [OPTIONS]
```

#### Options

| Option                         | Short | Description            | Default                     |
| ------------------------------ | ----- | ---------------------- | --------------------------- |
| `--qdrant-host`                | `-h`  | Qdrant server host     | `None`                      |
| `--qdrant-port`                | `-p`  | Qdrant server port     | `6333`                      |
| `--qdrant-api-key`             | `-a`  | Qdrant API key         | `None`                      |
| `--qdrant-https`               |       | Use HTTPS for Qdrant   | `False`                     |
| `--local-path`                 | `-l`  | Local path for Qdrant  | `None`                      |
| `--embedding-model`            | `-e`  | Embedding model to use | `jinaai/jina-embeddings-v3` |
| `--progress` / `--no-progress` |       | Show progress bar      | `True`                      |

#### Examples

**Load a single chat with local Qdrant:**
```bash
whatsvector load family-chat ./family_chat.txt --local-path ./qdrant_data
```

**Load multiple chats:**
```bash
whatsvector load work-chats ./chat1.txt ./chat2.txt ./chat3.txt --local-path ./qdrant_data
```

**Use a remote Qdrant server:**
```bash
whatsvector load my-chats ./chat.txt \
  --qdrant-host your-qdrant-server.com \
  --qdrant-port 6333 \
  --qdrant-https \
  --qdrant-api-key your-api-key
```

**Use a custom embedding model:**
```bash
whatsvector load my-chats ./chat.txt \
  --local-path ./qdrant_data \
  --embedding-model sentence-transformers/all-MiniLM-L6-v2
```

---

### Chatting with Your Data

The `chat` command starts an interactive session with an AI agent that can search and reason about your WhatsApp conversations.

#### Basic Usage

```bash
whatsvector chat <profile-name> [OPTIONS]
```

#### Options

| Option        | Short | Description                                   | Default              |
| ------------- | ----- | --------------------------------------------- | -------------------- |
| `--username`  | `-u`  | Your name in the chat                         | `None`               |
| `--language`  | `-l`  | Preferred language (en, it, es, fr, de, etc.) | `en`                 |
| `--llm-model` | `-m`  | LLM model in format `provider/model`          | `openai/gpt-4o-mini` |

#### Examples

**Basic chat session:**
```bash
whatsvector chat family-chat --username "John"
```

**Use a different LLM:**
```bash
whatsvector chat family-chat \
  --username "John" \
  --llm-model groq/llama-3.1-70b-versatile
```

**Chat in a different language:**
```bash
whatsvector chat family-chat \
  --username "Marco" \
  --language it
```

#### Sample Chat Session

```
Welcome to WhatsVector chat! Type 'exit' to quit.
You: What did we discuss about the vacation plans?
WhatsVector Agent: Based on your messages, you discussed going to Spain in July. 
Alice suggested Barcelona, and you agreed to book hotels by next week. 
Bob mentioned the budget should be around €2000 per person.

Sources:
- Alice (Monday, 15 January 2024): "What about Barcelona? I heard it's amazing in summer!"
- You (Monday, 15 January 2024): "Great idea! Let's book the hotels by next week."
- Bob (Tuesday, 16 January 2024): "Budget-wise, I think €2000 per person is reasonable."

You: exit
Goodbye!
```

---

## ⚙️ Configuration

WhatsVector saves profile configurations in `.whatsvector/<profile-name>.yaml` files. These files store:

- Qdrant connection settings (host, port, API key, HTTPS)
- Local Qdrant path (if using local instance)
- Embedding model configuration
- Collection name

You can manually edit these files or let WhatsVector manage them automatically.

### Example Configuration File

```yaml
qdrant_host: null
qdrant_port: 6333
qdrant_api_key: null
qdrant_https: false
qdrant_local_path: ./qdrant_data
embedding_model: jinaai/jina-embeddings-v3
collection_name: whatsvector_collection
```

---

## 🏗 Architecture

### Components

```
┌─────────────────────────────────────────────────────────┐
│                    WhatsVector CLI                       │
├─────────────────┬───────────────────────────────────────┤
│   Load Command  │          Chat Command                 │
└────────┬────────┴──────────────┬────────────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌──────────────────┐
│  Data Loaders   │     │  Agent System    │
│  - WhatsApp TXT │     │  - LangGraph     │
│  - Validation   │     │  - Tools         │
│  - Parsing      │     │  - State Mgmt    │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         ▼                       ▼
┌─────────────────────────────────────────┐
│          Qdrant Vector Database          │
│  - Embeddings Storage                   │
│  - Semantic Search                      │
│  - Metadata Filtering                   │
└─────────────────────────────────────────┘
```

### Key Modules

- **`cli/`**: Command-line interface implementation
  - `load.py`: Data loading commands
  - `chat.py`: Interactive chat interface

- **`whatsvector/agent/`**: AI agent implementation
  - `agent.py`: Agent creation and system prompts
  - `tools.py`: Qdrant search tool
  - `state.py`: Agent state management
  - `context.py`: Runtime context

- **`whatsvector/data/`**: Data processing
  - `loaders/loader.py`: Data loader implementations (InMemory, Qdrant)

- **`whatsvector/types/`**: Data models
  - `data.py`: WhatsApp message and data models

- **`whatsvector/config/`**: Configuration management
  - `config_file.py`: Profile configuration handling

### Data Flow

1. **Loading Phase**:
   ```
   WhatsApp TXT → Parser → WhatsappMessage → Embeddings → Qdrant
   ```

2. **Chat Phase**:
   ```
   User Query → Agent → Qdrant Search Tool → Relevant Messages → LLM → Response
   ```

---

## 💡 Examples

### Example 1: Personal Journal Search

```bash
# Load your personal chat with yourself
whatsvector load my-journal ./my_notes.txt --local-path ./qdrant_data

# Chat with it
whatsvector chat my-journal --username "Me"
```

**Query**: "What were my thoughts about the project last month?"

### Example 2: Family Chat Analysis

```bash
# Load family group chat
whatsvector load family ./family_group.txt --local-path ./qdrant_data

# Chat with specific language preference
whatsvector chat family --username "Dad" --language en
```

**Query**: "When did we discuss the birthday party?"

### Example 3: Work Conversations

```bash
# Load multiple work chats
whatsvector load work-archive \
  ./team_chat.txt \
  ./client_chat.txt \
  ./standup_notes.txt \
  --local-path ./qdrant_data

# Use a powerful model for analysis
whatsvector chat work-archive \
  --username "You" \
  --llm-model openai/gpt-4
```

**Query**: "Summarize all the action items from last week's discussions"

---

## 📝 TODO

### High Priority

- [ ] **Add comprehensive unit tests**
  - Agent behavior and tool execution tests
  - Data loader and parser validation tests
  - Configuration management tests
  - Integration tests for CLI commands

- [ ] **Improve Qdrant loader for large datasets without GPU** (See `whatsvector/data/loaders/loader.py:103-109`)
  - Current implementation is slow for large datasets without GPU acceleration
  - Proposed solution: Merge messages into N messages per vector to reduce vector count
  - Requires metadata management changes to track message groupings
  - Need to balance between granularity and performance

### Medium Priority

- [ ] **Implement incremental data loading**
  - Add new messages without reloading the entire dataset
  - Detect and skip duplicate messages
  - Optimize for append-only operations

- [ ] **Add conversation summarization features**
  - Generate summaries for time periods or topics
  - Create conversation digests
  - Extract key insights from chat history

- [ ] **Improve WhatsApp parser**
  - Support additional date/time formats
  - Handle more edge cases in message parsing
  - Better handling of system messages

- [ ] **Add export functionality**
  - Export search results to JSON/CSV
  - Export conversation segments
  - Generate reports from queries

### Low Priority

- [ ] **Create web UI for easier interaction**
  - Interactive chat interface
  - Visual analytics dashboard
  - Profile management UI

- [ ] **Add conversation analytics**
  - Message frequency analysis
  - Sender statistics
  - Sentiment analysis over time
  - Word clouds and topic extraction

- [ ] **Support for other chat platforms**
  - Telegram export format
  - Discord export format
  - Generic JSON/CSV import

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup

```bash
# Clone the repository
git clone https://github.com/samirsalman/whatsvector.git
cd whatsvector

# Install in development mode
pip install -e .

# Run the CLI
whatsvector --help
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to all functions and classes
- Write tests for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Samir Salman
```

---

## 🙏 Acknowledgments

- **Qdrant** - For the excellent vector database
- **LangGraph** - For the agent framework
- **FastEmbed** - For fast embedding generation
- **Typer** - For the beautiful CLI framework

---

## 📧 Contact

**Samir Salman** - [@samirsalman](https://github.com/samirsalman)

Project Link: [https://github.com/samirsalman/whatsvector](https://github.com/samirsalman/whatsvector)

---

<div align="center">

**Made with ❤️ by Samir Salman**

⭐ Star this repo if you find it useful!

</div>
