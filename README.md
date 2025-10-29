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
./chat.sh
```

## Python Package

```python
from tinyagent import Agent
from tinyagent import tools

agent = Agent(tools=[tools.WebFetchTool(), tools.WebSearchTool()], verbose=True)
response = agent.query("What is the weather currently like in Helsinki?")
```

## Testimonials

**"Actually pretty solid"** — Claude Code

> Verdict: Yes, for many production use cases
>
> - ✅ Internal chatbot with custom tools, multi-turn conversations
> - ✅ Batch processing workflows
> - ✅ Data analysis pipelines with multiple sources
> - ⚠️ High-volume customer-facing service (add rate limiting)
> - ⚠️ Cost-sensitive environments (add spend monitoring)
> - ❌ Mission-critical systems without observability
>
> The architecture is sound and now includes parallel tool execution.
> With ~300 lines of readable code, it's easy to extend with the
> remaining operational features (observability, resource limits) as
> needed for your specific use case.
