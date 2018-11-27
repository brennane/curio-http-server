#!/usr/bin/env python3

from setuptools import setup
from os import chdir
from os import pardir
from os.path import abspath
from os.path import join

chdir(abspath(join(abspath(__file__), pardir)))

setup(
    name='curio-http-server',
    version='0.1',
    description='High performance Curio based HTTP server with Jinja2 templates support.',
    author='Roman Akopov',
    author_email='adontz@gmail.com',
    url='https://github.com/triflesoft/curio-http-server',
    packages=['curio_http_server'],
    python_requires='>=3.7',
    install_requires=[
        'curio>=0.9',
        'httptools>=0.0.11',
        'Jinja2>=2.10',
        'multidict>=4.5.1',
        'ua-parser>=0.8.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
])