================
Typecraft Python
================


.. image:: https://img.shields.io/pypi/v/typecraft_python.svg
        :target: https://pypi.python.org/pypi/typecraft_python

.. image:: https://img.shields.io/travis/Typecraft/typecraft_python.svg
        :target: https://travis-ci.org/Typecraft/typecraft_python

.. image:: https://readthedocs.org/projects/typecraft_python/badge/?version=latest
        :target: https://typecraft_python.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/Typecraft/typecraft_python/shield.svg
     :target: https://pyup.io/repos/github/Typecraft/typecraft_python/
     :alt: Updates


This repository contains an IGT model based on the Typecraft IGT format. It also contains a simple CLI for
performing various NLP tasks, interfacing with both NLTK and other tools such as the TreeTagger.

* Free software: MIT license
* Full Documentation: https://typecraft_python.readthedocs.io.

Installation
------------
    pip install typecraft_python


Features
--------
* Parsing of the Typecraft XML format.
* Manipulation of the Typecraft IGT model format.
   * Integrating with NLTK
   * Integrating with TreeTagger
* Provides a CLI that can be used to load, convert and manipulate raw text and Typecraft XML files.


Usage
-----

.. code-block:: console

    Usage: tpy [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      convert
      ntexts   This command lists the number of texts in a...
      raw
      xml


Examples
_____________

Load a raw file, tokenize and tag it, and output xml (to stdout):

.. code-block:: console

    $ tpy raw your_file.txt

To save to a file

.. code-block:: console

    $ tpy raw your_file.txt -o output.xml
    # or
    $ tpy raw your_file.txt > output.xml

To tag using a specific tagger:

.. code-block:: console

    $ tpy raw your_file.txt --tagger=tree  # Tags using the tree tagger

To load a Typecraft xml file and tag it:

.. code-block:: console

    $ tpy xml your_file.xml --tag --tagger=nltk -o tagged_output.xml


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

