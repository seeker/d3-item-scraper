#!/usr/bin/env python

from setuptools import setup, find_packages

requirements = [
    'beautifulsoup4',
	'requests',
	'simplejson'
]

test_requirements = [
    'betamax'
]

setup(name='d3-item-scraper',
 version='0.1',
 description='Diablo 3 item scraper',
 author='Nicholas Wright',
 author_email='dozedoffagain@gmail.com',
 packages=find_packages(),
 test_suite="test",
 install_requires = requirements,
 tests_require=test_requirements,
 extras_require={
	'dev': test_requirements
}
)
