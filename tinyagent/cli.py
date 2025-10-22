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
    # A verbose agent will print all messages!
    _setup_readline()
    while True:
        try:
            message = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("Bye!")
            break
        if message := message.strip():
            agent.query(message)

if __name__ == "__main__":
    from tinyagent import tools
    chat(Agent(tools=(tools.WebFetchTool(), tools.WebSearchTool()), verbose=True))
