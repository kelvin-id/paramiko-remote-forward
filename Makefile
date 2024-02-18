PYTHON=poetry run python

include .env
export $(shell sed 's/=.*//' .env)

start:
	@make -j 2 server forward

forward:
	${PYTHON} forward.py

server:
	${PYTHON} server.py
