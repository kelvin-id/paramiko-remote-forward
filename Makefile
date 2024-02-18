PYTHON=poetry run python

include .env
export $(shell sed 's/=.*//' .env)

bin-start:
	@make -j bin-server bin-forward

start:
	@make -j 2 server forward

bin-forward:
	./forward.bin

bin-server:
	./server.bin

server:
	${PYTHON} server.py

forward:
	${PYTHON} forward.py

server:
	${PYTHON} server.py

build:
	make -j build-forward build-server

# New targets for compiling with Nuitka
build-forward:
	${PYTHON} -m nuitka --output-dir=build --standalone --onefile forward.py

build-server:
	${PYTHON} -m nuitka --output-dir=build --standalone --onefile server.py

# Optional: clean up the build directories created by Nuitka
clean:
	rm -rf forward.build server.build forward.dist server.dist forward.exe server.exe
