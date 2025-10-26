# Makefile for Sentinel AI Project

.PHONY: all build run test clean

all: build

build:
	docker build -t sentinel-ai .

run:
	docker-compose up

test:
	pytest tests/

clean:
	docker-compose down
	rm -rf data/synthetic/*.csv
	rm -rf __pycache__/
