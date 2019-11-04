.PHONY := bootstrap clean test install lint

bootstrap:
	pip install -r requirements.txt

install: clean
	python setup.py install

lint:
	flake8 --ignore=E731 --ignore=F401 prometheus_sanic

test: lint integration-test
	python -m unittest discover tests

integration-test:
	./tests/run_multiproc_it.sh

clean:
	rm -rf dist *.egg.info *.egg-info build
