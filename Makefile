# Build, test, docs, and clean
help:
	@echo "Commands:"
	@echo ""
	@echo "  install    install in editable mode"
	@echo "  test       run the test suite and report coverage"
	@echo "  doc        build the documentation"
	@echo "  format     run black to automatically format the code"
	@echo "  check      run code style and quality checks (black and flake8)"
	@echo "  lint       run pylint for a deeper quality check"
	@echo "  clean      clean up build and generated files"
	@echo "  dist-clean clean up egg-info files"
	@echo ""

install:
	pip install --no-deps -e .

test:
	pytest tests/test_*.py

doc:
	make -C docs docs

format:
	isort .
	black .
	blackdoc .

check:
	isort --check .
	black --check .
	blackdoc --check .
	flake8 .

lint:
	pylint HinetPy docs tests

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	find . -name "*.mo" -exec rm -v {} \;
	rm -rvf build dist sdist */__pycache__ .cache .pytest_cache .coverage* coverage.xml .eggs/
	rm -rvf testdir-*

dist-clean: clean
	rm -rvf *.egg-info
