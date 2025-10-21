# -*- coding: utf-8 -*-

import openai

from collections.abc import Iterable

# TODO: Abstract out the provider.
# https://github.com/BerriAI/litellm ?
class Agent:

    def __init__(self, *,
                 model: str = "gpt-5-nano",
                 system_message: str = "",
                 tools: Iterable = ()):

        self._client = openai.OpenAI()
        self._messages = []
        self._model = model
        self._system_message = system_message or "You are a helpful assistant."
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
