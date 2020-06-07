# Build, pacakge, test, and clean

help:
	@echo "Commands:"
	@echo ""
	@echo "  test       run the test suite and report coverage"
	@echo "  format     run black to automatically format the code"
	@echo "  check      run code style and quality checks (black and flake8)"

test:
	pytest --cov-report=term-missing --cov-report=xml --cov=HinetPy -vs tests/

doc:
	make -C docs docs

format:
	black .

check:
	black --check .
	flake8 .

publish:
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*
	rm -fr build dist HinetPy.egg-info

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	rm -rvf build dist MANIFEST *.egg-info __pycache__ .coverage .cache coverage.xml
