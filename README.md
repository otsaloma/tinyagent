Tiny Agent
==========

This is a minimal AI Agent implementation as a Python package and
command line interface. At around 300 lines, the code should be easy to
read and extend. Two tools are included: web search and web fetch. Thus,
the agentic capabilities can be easily tested by questions about current
or upcoming events, weather etc. Uses gpt-5-mini by default.

## Prerequisites

You need an OpenAI API key from <https://platform.openai.com/api-keys>.
Define that API key as environment variable `OPENAI_API_KEY`.

Install uv required by the Python environment, see
<https://docs.astral.sh/uv/getting-started/installation/>. A virtualenv
will be created implicitly by the below `uv run` commands.

Install a Playwright browser required by the web tools.

```bash
uv run playwright install webkit
```

## Command Line Chat Interface

```bash
PYTHONPATH=. uv run tinyagent/cli.py
```

## Python Package

```python
from tinyagent import Agent
from tinyagent import tools

agent = Agent(tools=[tools.WebFetchTool(), tools.WebSearchTool()], verbose=True)
response = agent.query("What is the weather currently like in Helsinki?")
```

## Testimonials

**“Not fundamentally broken”** — Claude Code

> Verdict: Maybe, for simple cases
>
> - ✅ Internal chatbot with 3-5 custom tools, <10 turn conversations
> - ✅ Batch processing where latency doesn't matter
> - ❌ High-volume customer-facing service
> - ❌ Long-running conversational agents
> - ❌ Cost-sensitive environments without guardrails
>
> The architecture is sound - it's missing operational features, not
> fundamentally broken. Add parallel execution, observability, and
> resource limits, and it could absolutely work.
