# Build, pacakge, test, and clean

help:
	@echo "Commands:"
	@echo ""
	@echo "  test    run the test suite and report coverage"

test:
	pytest --cov-report=term-missing --cov-report=xml --cov=HinetPy -vs tests/

coverage:
	codecov

doc:
	make -C docs docs

publish:
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*
	rm -fr build dist HinetPy.egg-info

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	rm -rvf build dist MANIFEST *.egg-info __pycache__ .coverage .cache coverage.xml
