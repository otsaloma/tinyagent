# -*- coding: utf-8 -*-

import atexit
import functools
import readline

from pathlib import Path
from tinyagent import Agent
from tinyagent import util

@functools.cache
def _setup_readline() -> None:
    path = Path.cwd() / ".history"
    if path.exists():
        readline.read_history_file(path)
    readline.set_history_length(1000)
    atexit.register(readline.write_history_file, path)

def chat(agent: Agent) -> None:
    # A verbose agent will print all messages,
    # no need to print separately here!
    agent._verbose = True
    _setup_readline()
    print("How can I help you today?")
    while True:
        try:
            message = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\rBye!")
            break
        if message := message.strip():
            print(util.SEPARATOR_LINE)
            agent.query(message)

if __name__ == "__main__":
    import sys
    from tinyagent import tools
    use_tools = [tools.WebFetchTool(), tools.WebSearchTool()]
    kwargs = {"model": sys.argv[1]} if sys.argv[1:] else {}
    chat(Agent(tools=use_tools, verbose=True, **kwargs)) # type: ignore[arg-type]
