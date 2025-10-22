# -*- coding: utf-8 -*-

import json
import openai

from collections.abc import Iterable
from tinyagent import util

SYSTEM_MESSAGE = """
You are an intelligent, reliable and helpful AI agent. Your goal is to help the
user by reasoning carefully. You have access to a list of tools, each defined
by name, description and an input parameter specification. When a tool is
needed, respond with a `tool_calls` object. Otherwise, reply directly to the
user in natural language. If a tool call fails or returns an error, explain
what went wrong and suggest alternatives if possible.

General rules:
- Think carefully about what the user wants before acting.
- Use tools only when necessary.
- Do not invent tools or parameters that are not provided.
- Be concise and factual in your responses.
- If uncertain, ask clarifying questions before acting.
""".strip()

USER_MESSAGE = """
User query:
{message}

Available tools:
{tools}

Respond directly or use one of the tools.
""".strip()

# TODO: Abstract out the provider.
# https://github.com/BerriAI/litellm ?
class Agent:

    def __init__(self, *,
                 model: str = "gpt-5-nano",
                 system_message: str = SYSTEM_MESSAGE,
                 tools: Iterable = (),
                 verbose: bool = False):

        self._client = openai.OpenAI()
        self._messages = []
        self._model = model
        self._system_message = system_message
        self._tools = list(tools)
        self._verbose = verbose

    def _append_message(self, role: str, content: str) -> None:
        self._messages.append({"role": role, "content": content})
        if self._verbose:
            print(f":{role}:")
            print(content)
            util.print_separator_line()

    def _dump_tool_schemas(self) -> list:
        return [{"type": "function", "function": tool.schema}
                for tool in self._tools]

    def _format_user_message(self, message: str) -> str:
        return USER_MESSAGE.format(message=message, tools="\n".join(
            "- {name}: {description}".format(**tool.schema)
            for tool in self._tools
        )) if self._tools else message

    def query(self, message: str) -> str:
        if not self._messages:
            self._append_message("system", self._system_message)
        self._append_message("user", self._format_user_message(message))
        tools = self._dump_tool_schemas()
        if self._verbose:
            print(":tools:")
            print(json.dumps(tools, ensure_ascii=False, indent=2))
            util.print_separator_line()
            print("Thinking...", end="", flush=True)
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=self._messages,
            tools=tools,
        )
        if self._verbose:
            print("\r", end="", flush=True)
        # TODO: Check completion.choices[0].tool_calls!
        response = completion.choices[0].message
        self._append_message(response.role, response.content)
        return response.content

if __name__ == "__main__":
    from tinyagent import tools
    agent = Agent(tools=(tools.WebFetchTool(), tools.WebSearchTool()), verbose=True)
    print(agent.query("What is the weather currently like in Helsinki?"))
