Tiny Agent
==========

This is a very minimal AI Agent implementation as a Python package and
command line interface.

## Prerequisites

You need an OpenAI API key from <https://platform.openai.com/api-keys>.
Define that API key as environment variable `OPENAI_API_KEY`.

Install uv required by the Python environment, see
<https://docs.astral.sh/uv/getting-started/installation/>.

Install Playwright required by the fetch tool.

```bash
uv run playwright install webkit
```

## Command Line Interface

```bash
PYTHONPATH=. uv run tinyagent/agent.py
```

## Python Package

```python
TODO
```
