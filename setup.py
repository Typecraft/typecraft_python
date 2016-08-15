#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='tc_xml_python',
    version='0.1.3',
    description="Lightweight implementation of the Typecraft XML format in python.",
    long_description=readme + '\n\n' + history,
    author="Tormod Haugland",
    author_email='tormod.haugland@gmail.com',
    url='https://github.com/Typecraft/tc_xml_python',
    packages=find_packages(),
    package_dir={'tc_xml_python':
                 'tc_xml_python'},
    entry_points={
        'console_scripts': [
            'tc_xml_python=tc_xml_python.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='tc_xml_python',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
