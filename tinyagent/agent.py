# -*- coding: utf-8 -*-

import functools
import openai

class Agent:

    def __init__(self, *, model="gpt-5-nano", system_message=None, tools=()):
        self._client = openai.OpenAI()
        self._messages = []
        self._model = model
        self._system_message = system_message or "You are a helpful assistant."
        self._tools = list(tools)

    def _append_message(self, role, content):
        self._messages.append({"role": role, "content": content})

    @functools.cache
    def _setup_readline(self):
        import atexit
        import readline
        from pathlib import Path
        histfile = Path.cwd() / ".history"
        if histfile.exists():
            readline.read_history_file(histfile)
        atexit.register(readline.write_history_file, histfile)
        readline.set_history_length(1000)

    def chat(self):
        self._setup_readline()
        while True:
            try:
                message = input("> ")
            except (EOFError, KeyboardInterrupt):
                print("\rBye!")
                break
            if message := message.strip():
                print("Thinking...", end="", flush=True)
                response = self.query(message)
                print("\r" + "―" * 72)
                print(response)
                print("―" * 72)

    def query(self, message):
        if not self._messages:
            self._append_message("system", self._system_message)
        self._append_message("user", message)
        completion = self._client.chat.completions.create(
            model=self._model, messages=self._messages)
        response = completion.choices[0].message
        self._append_message(response.role, response.content)
        return response.content

if __name__ == "__main__":
    agent = Agent()
    agent.chat()
