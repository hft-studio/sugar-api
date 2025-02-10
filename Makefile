.PHONY: test format lint install run

install:
	pip install -r requirements.txt

test:
	pytest

format:
	black sugar_api tests

lint:
	flake8 sugar_api tests

run:
	python run.py
