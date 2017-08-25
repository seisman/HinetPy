test:
	py.test --cov-report term-missing --cov=HinetPy -vs tests/

coverage:
	codecov

doc:
	bash ci/build-docs.sh

publish:
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*
	rm -fr build dist HinetPy.egg-info

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	rm -rvf build dist MANIFEST *.egg-info __pycache__ .coverage .cache
