# -*- coding: utf-8-unix -*-

check:
	uv run flake8 .
	uv run mypy .

clean:
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf */*/__pycache__

.PHONY: check clean
