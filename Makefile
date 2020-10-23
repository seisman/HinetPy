# Build, test, docs, and clean

BLACK_FILES=HinetPy docs tests setup.py
FLAKE8_FILES=HinetPy docs tests setup.py


help:
	@echo "Commands:"
	@echo ""
	@echo "  test       run the test suite and report coverage"
	@echo "  format     run black to automatically format the code"
	@echo "  check      run code style and quality checks (black and flake8)"
	@echo "  doc        build the documentation"
	@echo "  clean      clean up build and generated files"
	@echo ""

test:
	pytest tests

doc:
	make -C docs docs

format:
	black ${BLACK_FILES}

check:
	black --check ${BLACK_FILES}
	flake8 ${FLAKE8_FILES}

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	rm -rvf *.egg-info build dist sdist \
		*/__pycache__ .cache .pytest_cache \
		.coverage coverage.xml
