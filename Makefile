.PHONY: .venv
.SECONDARY: .venv
.venv:
	@python3 -m venv .venv
	@(. .venv/bin/activate; \
	pip install -q -r configs/requirements-dev.txt; \
	pip install -q -r configs/requirements-test.txt;)

.SECONDARY: build-dev
build-dev:
	@sudo docker build --pull --rm -f "configs/Dockerfile.dev" -t dev .

.SECONDARY: build-test
build-test:
	@sudo docker build --pull --rm -f "configs/Dockerfile.test" -t test .

.PHONY: clean
clean:
	@rm -rf */__pycache__ */*/__pycache__ */*/*/__pycache__ */*/*/*/__pycache__ src/*.sqlite .coverage \
	 */.*_cache coverage.xml .*_cache htmlcov/ site/ .report/

.PHONY: delete-containers
.SECONDARY: delete-containers
delete-containers:
	@sudo docker stop devcontainer || true && sudo docker rm devcontainer || true
	@sudo docker stop testcontainer || true && sudo docker rm testcontainer || true

drun: delete-containers build-dev
	@sudo docker run -it --name devcontainer -p 8000:8000 dev

run: .venv
	@(. .venv/bin/activate; \
		python3 src/main.py)

dtest: delete-containers build-test
	@sudo docker run -it --name testcontainer -p 8000:8000 test

test: .venv clean
	@(. .venv/bin/activate; \
	pytest -v -s --cov=src --cov-report=term --cov-config=configs/.coveragerc)

html-cov: .venv clean
	@(. .venv/bin/activate; \
	pytest -v -s --cov=src --cov-report=html --cov-config=configs/.coveragerc)
	@xdg-open htmlcov/index.html

report: .venv
	@mkdir -p .report
	@(. .venv/bin/activate; \
	pylint src/ > ./.report/pylint-report; \
	pyflakes src/ > ./.report/pyflakes-report; \
	mypy src/ > ./.report/mypy-report; \
	vulture src/ > ./.report/vulture-report)