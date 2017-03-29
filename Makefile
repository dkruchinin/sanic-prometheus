.PHONY := bootstrap clean test install lint

bootstrap:
	pip install -r requirements.txt

install: clean
	python setup.py install

lint:
	flake8 --ignore=E731 sanic_prometheus

test: lint
	python -m unittest discover tests

clean:
	rm -rf dist *.egg.info build

