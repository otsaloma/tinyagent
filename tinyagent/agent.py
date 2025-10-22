# -*- coding: utf-8 -*-

import openai

from collections.abc import Iterable

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

# TODO: Abstract out the provider.
# https://github.com/BerriAI/litellm ?
class Agent:

    def __init__(self, *,
                 model: str = "gpt-5-nano",
                 system_message: str = SYSTEM_MESSAGE,
                 tools: Iterable = ()):

        self._client = openai.OpenAI()
        self._messages = []
        self._model = model
        self._system_message = system_message
        self._tools = list(tools)

    def _append_message(self, role: str, content: str) -> None:
        self._messages.append({"role": role, "content": content})

    def query(self, message: str) -> str:
        if not self._messages:
            self._append_message("system", self._system_message)
        self._append_message("user", message)
        completion = self._client.chat.completions.create(
            model=self._model, messages=self._messages)
        response = completion.choices[0].message
        self._append_message(response.role, response.content)
        return response.content

if __name__ == "__main__":
    print(Agent().query("What is the capital of Vanuatu?"))
