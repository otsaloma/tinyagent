# -*- coding: utf-8-unix -*-

check:
	flake8 .

clean:
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf */*/__pycache__

.PHONY: check clean
