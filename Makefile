# Build, test, docs, and clean

FLAKE8_FILES=HinetPy docs tests setup.py
LINT_FILES=HinetPy

help:
	@echo "Commands:"
	@echo ""
	@echo "  test       run the test suite and report coverage"
	@echo "  format     run black to automatically format the code"
	@echo "  check      run code style and quality checks (black and flake8)"
	@echo "  lint       run pylint for a deeper quality check"
	@echo "  doc        build the documentation"
	@echo "  clean      clean up build and generated files"
	@echo ""

install:
	pip install --no-deps -e .

test:
	pytest tests

doc:
	make -C docs docs

format:
	black .

check:
	black --check .
	flake8 $(FLAKE8_FILES)

lint:
	pylint $(LINT_FILES)

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	find . -name "*.mo" -exec rm -v {} \;
	rm -rvf *.egg-info build dist sdist */__pycache__ .cache .pytest_cache \
		    .coverage* coverage.xml
