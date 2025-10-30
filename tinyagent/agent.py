# -*- coding: utf-8 -*-

import dataclasses
import json
import litellm
import multiprocessing

from collections.abc import Iterable
from dataclasses import dataclass
from tinyagent import Tool
from tinyagent import util
from typing import Any

SYSTEM_MESSAGE = """
You are an intelligent, reliable and helpful AI agent. Your goal is to help the
user by reasoning carefully. You have access to a list of tools, each defined
by name, description and an input parameter specification. When a tool is
needed, respond with a `tool_calls` object. Otherwise, reply directly to the
user in natural language. If a tool call fails or returns an error, explain
what went wrong and suggest alternatives if possible.

When looking for information on the web, never settle for just search result
summaries. Always check the referenced pages. Never rely on a single source.
Always try to find at least two sources that agree on a matter.

General rules:
- Think carefully about what the user wants before acting.
- Use your own general knowledge first.
- Use tools only when necessary.
- Do not invent tools or parameters that are not provided.
- Be concise and factual in your responses.
- Do not mention your tools to the user unless specifically asked.
""".strip()

USER_MESSAGE = """
User query:
{message}

Available tools:
{tools}

Respond directly or use one of the tools.
Tools are your hidden superpower, not something to advertise or overuse.
""".strip()

@dataclass
class Message:
    role: str
    content: str
    def __str__(self):
        return f":{self.role}:\n{self.content}"

@dataclass
class ToolCallMessage:
    role: str
    tool_calls: list
    def __str__(self):
        return "\n".join(
            [f":{self.role}:tool-calls:"] +
            [f"{i+1}. {x.function.name} {x.function.arguments}"
             for i, x in enumerate(self.tool_calls)])

@dataclass
class ToolOutputMessage:
    role: str
    tool_call_id: str
    content: str
    def __str__(self):
        max_lines = 1000 if self.content.startswith("Traceback") else 20
        return "\n".join(
            [f":{self.role}:output:"] +
            self.content.splitlines()[:max_lines] +
            [f"... {len(self.content)} characters total"])

# Outside Agent, since multiprocessing uses pickle
# and works better with top-level functions without self.
def _execute_tool_call(tools: list[Tool], tool_call: Any) -> ToolOutputMessage:
    tool = {x.name: x for x in tools}[tool_call.function.name]
    args = json.loads(tool_call.function.arguments)
    output = tool.call_or_traceback(**args)
    return ToolOutputMessage("tool", tool_call.id, output)

class Agent:

    def __init__(self, *,
                 model: str = "openai/gpt-5-mini",
                 system_message: str = SYSTEM_MESSAGE,
                 tools: Iterable = (),
                 max_steps: int = 10,
                 verbose: bool = False):

        self._max_steps = max_steps
        self._messages = [] # type: ignore[var-annotated]
        self._model = model
        self._system_message = system_message
        self._tools = list(tools)
        self._verbose = verbose
        if self._verbose:
            print(f"Using {self._model}")
            print(":tools:")
            for tool in self._tools:
                print(tool.schema_json)
            print(util.SEPARATOR_LINE)

    def _format_user_message(self, message: str) -> str:
        return USER_MESSAGE.format(message=message, tools="\n".join(
            "- {name}: {description}".format(**tool.schema)
            for tool in self._tools
        )) if self._tools else message

    def _push(self, message: Message|ToolCallMessage|ToolOutputMessage) -> None:
        self._messages.append(dataclasses.asdict(message))
        if self._verbose:
            print(message)
            print(util.SEPARATOR_LINE)

    @property
    def _tool_schemas(self) -> list:
        # Follow the OpenAI function/tool JSON schema.
        # https://platform.openai.com/docs/guides/function-calling
        return [{"type": "function", "function": tool.schema}
                for tool in self._tools]

    def _complete(self) -> Any:
        if self._verbose:
            print("Thinking...", end="", flush=True)
        completion = litellm.completion(
            model=self._model,
            messages=self._messages,
            tools=self._tool_schemas,
            timeout=60,
        )
        if self._verbose:
            print("\r", end="", flush=True)
        return completion.choices[0].message

    def query(self, message: str) -> str:
        if not self._messages:
            self._push(Message("system", self._system_message))
        self._push(Message("user", self._format_user_message(message)))
        for i in range(self._max_steps):
            if self._verbose:
                print(f":step:{i+1}/{self._max_steps}:")
            response = self._complete()
            if response.tool_calls:
                # LLM wants to use tools to answer the user.
                # Execute tool calls in parallel and append output to messages.
                self._push(ToolCallMessage("assistant", response.tool_calls))
                with multiprocessing.Pool() as pool:
                    args = [(self._tools, x) for x in response.tool_calls]
                    for result in pool.starmap(_execute_tool_call, args):
                        self._push(result)
            else:
                # LLM can answer based on general knowledge from its training
                # data and previous messages, including output from tool calls.
                # Relay that as-is to the user.
                self._push(Message(response.role, response.content))
                return response.content
        content = f"Maximum steps ({self._max_steps}) reached with no answer :-("
        self._push(Message("assistant", content))
        return content

if __name__ == "__main__":
    import sys
    from tinyagent import tools
    agent = Agent(tools=(tools.WebFetchTool(), tools.WebSearchTool()), verbose=True)
    query = sys.argv[1] if sys.argv[1:] else "What is the weather currently like in Helsinki?"
    agent.query(query)
