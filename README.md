# AI Coding Agent

A Python-based AI coding agent powered by Google's Gemini 2.0 Flash model. This agent can interact with your filesystem to read, write, and execute Python files within a designated working directory.

## Features

- **File Operations**: List, read, and write files within a secure working directory
- **Code Execution**: Run Python scripts with optional command-line arguments
- **Function Calling**: Uses Gemini's function calling capabilities for structured interactions
- **Security**: All file operations are constrained to the working directory to prevent unauthorized access
- **Verbose Mode**: Optional detailed logging of function calls and responses

## Prerequisites

- Python 3.12 or higher
- Google Gemini API key

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd ai-agent
```

2. Install dependencies using `uv` or `pip`:
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

3. Create a `.env` file in the project root and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the agent with a natural language prompt:

```bash
python main.py "your prompt here"
```

### Examples

List files in the calculator directory:
```bash
python main.py "What files are in the calculator directory?"
```

Create and run a Python script:
```bash
python main.py "Create a Python script that calculates fibonacci numbers and run it"
```

Read and modify existing code:
```bash
python main.py "Read the calculator.py file and add error handling"
```

### Verbose Mode

Enable verbose mode to see detailed function calls and responses:
```bash
python main.py "your prompt here" --verbose
```

## Available Functions

The AI agent has access to the following functions:

### `get_files_info`
Lists files in a directory with their sizes and types.
- **Parameter**: `directory` (optional, defaults to working directory)

### `get_file_content`
Reads and returns the content of a file (truncated at 10,000 characters).
- **Parameter**: `file_path` (relative to working directory)

### `write_file`
Writes content to a file, creating or overwriting as needed.
- **Parameters**: 
  - `file_path` (relative to working directory)
  - `content` (string content to write)

### `run_python_file`
Executes a Python file with optional arguments.
- **Parameters**:
  - `file_path` (relative to working directory)
  - `args` (optional array of command-line arguments)

## Security

All file operations are restricted to the configured working directory (currently set to `./calculator`). The agent cannot:
- Access files outside the working directory
- Execute non-Python files
- Perform system-level operations

## Limitations

- Maximum of 20 function calls per session
- File content truncated at 10,000 characters
- Python script execution timeout: 30 seconds
- Only Python files can be executed

## License

This project is part of the Boot.dev curriculum.
