# Build, test, docs, and clean
help:
	@echo "Commands:"
	@echo ""
	@echo "  install    install in editable mode"
	@echo "  package    build source and wheel distributions"
	@echo "  test       run the test suite and report coverage"
	@echo "  doc        build the documentation"
	@echo "  format     run black to automatically format the code"
	@echo "  check      run code style and quality checks (black and flake8)"
	@echo "  lint       run pylint for a deeper quality check"
	@echo "  clean      clean up build and generated files"
	@echo ""

install:
	pip install --no-deps -e .

package:
	python setup.py sdist bdist_wheel

test:
	pytest tests

doc:
	make -C docs docs

format:
	isort .
	black .
	black .

check:
	isort --check .
	black --check .
	black --check .
	flake8 .

lint:
	pylint HinetPy docs tests

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	find . -name "*.mo" -exec rm -v {} \;
	rm -rvf *.egg-info build dist sdist */__pycache__ .cache .pytest_cache .coverage* coverage.xml
