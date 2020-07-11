#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements


install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]


setup(name='alg',
      version='0.1',
      description='Commonly used algorithms',
      author='Misaka-10032',
      author_email='longqic@andrew.cmu.edu',
      url='https://github.com/misaka-10032/alg',
      packages=find_packages(),
      install_requires=reqs,
      )
