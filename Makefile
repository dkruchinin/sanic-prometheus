.PHONY := bootstrap clean test install lint

bootstrap:
	pip install -r requirements.txt

bootstrap-dev:
	pip install -r requirements-dev.txt

install: clean
	python setup.py install

lint:
	flake8 sanic_prometheus

test: lint integration-test
	python -m unittest discover tests

integration-test:
	./tests/run_multiproc_it.sh

release:
	python setup.py sdist bdist_wheel
	twine upload dist/*

clean:
	rm -rf dist *.egg.info *.egg-info build

