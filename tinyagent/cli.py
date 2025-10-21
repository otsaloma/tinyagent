# -*- coding: utf-8 -*-

import atexit
import functools
import readline

from pathlib import Path
from tinyagent import Agent

@functools.cache
def _setup_readline() -> None:
    path = Path.cwd() / ".history"
    if path.exists():
        readline.read_history_file(path)
    readline.set_history_length(1000)
    atexit.register(readline.write_history_file, path)

def chat(agent: Agent) -> None:
    _setup_readline()
    while True:
        try:
            message = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\rBye!")
            break
        if message := message.strip():
            print("Thinking...", end="", flush=True)
            response = agent.query(message)
            print("\r" + "―" * 72)
            print(response)
            print("―" * 72)

if __name__ == "__main__":
    chat(Agent())
