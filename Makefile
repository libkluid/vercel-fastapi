.PHONY: install

install:
	poetry install

dev:
	poetry run fastapi dev api/index.py
