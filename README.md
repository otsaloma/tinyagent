Tiny Agent
==========

This is a minimal AI Agent implementation as a Python package and
command line interface. At around 300 lines, the code should be easy to
read and extend. Two tools are included: web search and web fetch. Thus,
the agentic capabilities can be easily tested by questions about current
or upcoming events, weather etc.

## Prerequisites

Install uv required by the Python environment, see
<https://docs.astral.sh/uv/getting-started/installation/>. A virtualenv
will be created implicitly by the below commands.

Install a Playwright browser required by the web tools.

```bash
uv run playwright install webkit
```

## Command Line Chat Interface

```bash
./chat.sh [MODEL]
```

By default Tiny Agent uses OpenAI's gpt-5-mini, but multiple providers
and models are supported. You can specify e.g. one of the following as
the optional MODEL argument above.

```
openai/gpt-5-mini
anthropic/claude-sonnet-4-5
xai/grok-4-fast
azure/...
openrouter/...
```

Tiny Agent uses LiteLLM and supports any provider that is listed as
supported by LiteLLM and supporting the `tools` argument for
completions, see below links for details.

* https://docs.litellm.ai/docs/providers
* https://docs.litellm.ai/docs/completion/input#translated-openai-params

You'll need your own API key. For example with OpenAI, you can get it
from from <https://platform.openai.com/api-keys> and define as
environment variable `OPENAI_API_KEY`.

## Python Package

```python
from tinyagent import Agent
from tinyagent import tools

def main():
    use_tools = [tools.WebFetchTool(), tools.WebSearchTool()]
    agent = Agent(model="openai/gpt-5-mini", tools=use_tools, verbose=True)
    response = agent.query("What is the weather currently like in Helsinki?")

if __name__ == "__main__":
    main()
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
