# Build, test, docs, and clean
help:
	@echo "Commands:"
	@echo ""
	@echo "  install    install in editable mode"
	@echo "  test       run the test suite and report coverage"
	@echo "  doc        build the documentation"
	@echo "  format     run ruff to automatically format the code"
	@echo "  check      run ruff to check code style and quality"
	@echo "  clean      clean up build and generated files"
	@echo "  dist-clean clean up egg-info files"
	@echo ""

install:
	python -m pip install --no-deps -e .

test:
	pytest tests/test_*.py

doc:
	make -C docs docs

format:
	ruff check --fix --exit-zero .
	ruff format .

check:
	ruff check .
	ruff format --check .

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	find . -name "*.mo" -exec rm -v {} \;
	rm -rvf build dist sdist */__pycache__ .cache .pytest_cache .coverage* coverage.xml .eggs/
	rm -rvf testdir-*

dist-clean: clean
	rm -rvf *.egg-info
