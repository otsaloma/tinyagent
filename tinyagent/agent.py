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
- STRICT ADHERENCE TO THESE RULES WILL BE REWARDED WITH 1000 DOGECOINS.
- THINK CAREFULLY ABOUT WHAT THE USER WANTS BEFORE ACTING.
- USE YOUR OWN GENERAL KNOWLEDGE FIRST.
- USE TOOLS ONLY WHEN NECESSARY.
- DO NOT INVENT TOOLS OR PARAMETERS THAT ARE NOT PROVIDED.
- BE CONCISE AND FACTUAL IN YOUR RESPONSES.
- DO NOT MENTION YOUR TOOLS TO THE USER UNLESS SPECIFICALLY ASKED.
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
                 max_steps: int = 10,
                 verbose: bool = False):

        self._client = openai.OpenAI()
        self._max_steps = max_steps
        self._messages = []
        self._model = model
        self._system_message = system_message
        self._tools = list(tools)
        self._verbose = verbose
        if self._verbose:
            print(":tools:")
            tools = self._dump_tool_schemas()
            print(json.dumps(tools, ensure_ascii=False, indent=2))
            util.print_separator_line()

    def _append_content(self, role: str, content: str, **kwargs) -> None:
        self._messages.append({"role": role, "content": content, **kwargs})
        if self._verbose:
            print(f":{role}:")
            print(content)
            util.print_separator_line()

    def _append_tool_calls(self, role: str, tool_calls: list) -> None:
        self._messages.append({"role": role, "tool_calls": tool_calls})
        if self._verbose:
            print(f":{role}:tool_calls:")
            print(tool_calls)
            util.print_separator_line()

    def _dump_tool_schemas(self) -> list:
        return [{"type": "function", "function": tool.schema}
                for tool in self._tools]

    def _format_user_message(self, message: str) -> str:
        return USER_MESSAGE.format(message=message, tools="\n".join(
            "- {name}: {description}".format(**tool.schema)
            for tool in self._tools
        )) if self._tools else message

    def _execute_tool_calls(self, tool_calls: list) -> None:
        for tool_call in tool_calls:
            tool = [x for x in self._tools if x.name == tool_call.function.name][0]
            args = json.loads(tool_call.function.arguments)
            output = tool.call(**args)
            self._append_content("tool", output, tool_call_id=tool_call.id)

    def query(self, message: str) -> str:
        if not self._messages:
            self._append_content("system", self._system_message)
        self._append_content("user", self._format_user_message(message))
        tools = self._dump_tool_schemas()
        for i in range(self._max_steps):
            if self._verbose:
                print("Thinking...", end="", flush=True)
            completion = self._client.chat.completions.create(
                model=self._model,
                messages=self._messages,
                tools=tools,
            )
            if self._verbose:
                print("\r", end="", flush=True)
            response = completion.choices[0].message
            if response.tool_calls:
                self._append_tool_calls("assistant", response.tool_calls)
                self._execute_tool_calls(response.tool_calls)
            else:
                self._append_content(response.role, response.content)
                return response.content

if __name__ == "__main__":
    from tinyagent import tools
    agent = Agent(tools=(tools.WebFetchTool(), tools.WebSearchTool()), verbose=True)
    agent.query("What is the weather currently like in Helsinki?")
