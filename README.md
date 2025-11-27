# Travel Assistant RAG

A simple Python application for travel assistance using RAG (Retrieval-Augmented Generation).

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -e .
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
python main.py
```

## Configuration

See `.env.example` for available configuration options.

## Development

Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Project Structure

```
.
├── main.py              # Main application entry point
├── .env                 # Environment variables (not committed)
├── .env.example         # Environment variables template
├── pyproject.toml       # Project dependencies and metadata
└── README.md           # This file
```
