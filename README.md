# Salesforce AI Code Assistant & Documentation Generator

This project offers two primary functionalities:

1.  **AI Code Assistant**: An interactive chat agent that uses a Retrieval-Augmented Generation (RAG) architecture to answer questions about your Salesforce codebase.
2.  **Legacy Documentation Generator**: A command-line tool to automatically generate Markdown documentation for Salesforce objects, fields, and validation rules.

---

## AI Code Assistant

### Overview

This provides an AI-powered assistant that can answer questions about a Salesforce codebase. It leverages the `agno` library to create a knowledge base from your project files. You can then interact with an AI agent in a chat interface to ask questions about your code.

This tool is particularly useful for:

-   **Developers**: Quickly understand the purpose and functionality of different parts of a Salesforce project.
-   **Onboarding New Team Members**: Help new developers get up to speed on a complex codebase.
-   **Architects and Analysts**: Gain high-level insights into the project structure.

### Features

-   **AI-Powered Knowledge Base**: Automatically reads files in your Salesforce project, generates intelligent summaries, and stores them in a vector database.
-   **Interactive Chat Agent**: Ask questions about your codebase in natural language and get answers synthesized from the relevant file summaries.
-   **RAG Architecture**: Uses the `agno` library for a robust agentic workflow and `ChromaDB` for efficient vector storage.

### Getting Started (AI Assistant)

#### Prerequisites

-   Python 3.8+
-   An OpenAI API key.

#### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd sf-auto-doc
    ```

2.  **Set up your OpenAI API Key:**
    The agent requires an OpenAI API key. You must set it as an environment variable.
    ```bash
    export OPENAI_API_KEY='your-api-key-here'
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### How It Works (AI Assistant)

The tool has two main commands, managed by `generate_kb.py`.

#### 1. `fill`: Create the Knowledge Base

This command builds the knowledge base that the agent will use.

**Usage:**
```bash
python generate_kb.py fill --sf-project-path <path/to/your/force-app> --db-path <path/to/save/db>
```

**Example:**
```bash
python generate_kb.py fill --sf-project-path tests/data/force-app --db-path test_kb
```

#### 2. `chat`: Talk to Your Code

This command starts an interactive chat session with the AI agent.

**Usage:**
```bash
python generate_kb.py chat --db-path <path/to/your/db>
```

**Example:**
```bash
python generate_kb.py chat --db-path test_kb
```

---

## Documentation Generator

### Overview

This is a Python-based tool designed to automatically generate documentation for Salesforce objects. It parses Salesforce metadata files (`.field-meta.xml` and `.validationRule-meta.xml`) to extract information about fields and validation rules, and then generates Markdown files that provide a clear and concise overview of each object's configuration.

### Usage (Legacy Generator)

The tool is executed from the command line via `main.py`.

```bash
python main.py --objects <ObjectAPIName> --output-dir <path/to/your/docs> --base-path <path/to/your/force-app/main/default>
```

#### Arguments

-   `--objects`: (Required) A comma-separated list of Salesforce object API names to document (e.g., `Account,Contact`), or `'All'` to document all objects found in the `base-path`.
-   `--output-dir`: (Optional) The directory where the documentation files will be saved. Defaults to `docs/`.
-   `--base-path`: (Optional) The base path to your Salesforce metadata files. Defaults to `force-app/main/default/`.
-   `--debug`: (Optional) Enable debug mode for more detailed output.

---

## Project Structure

```
/home/thomas/Projects/sf-auto-doc/
├───generate_kb.py           # Main entry point for AI Assistant
├───main.py                  # Main entry point for Legacy Generator
├───src/
│   ├───file_system_knowledge_base.py  # Custom agno knowledge base for local files
│   └───utils.py               # Utils for the legacy generator
└───tests/
    ├───test_agent.py            # Tests for the new agent and KB functionality
    └───data/                      # Sample Salesforce data for testing
```

## Running Tests

To run the tests for the AI Assistant:
```bash
python -m unittest tests/test_agent.py
```

To run the tests for the Legacy Documentation Generator:
```bash
python -m unittest tests/test_documentation.py
```