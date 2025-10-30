#!/bin/sh
export PYTHONPATH=.
exec uv run tinyagent/cli.py "$@"
