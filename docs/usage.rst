=========
Usage
=========

The system can be used in two ways: As a CLI, and as a library.

CLI
------

The CLI currently has 4 active commands:

* raw
* xml
* ntexts
* par

**raw** loads raw texts, and performs a number of operations on it. It will always convert the result to a TC-XML file.
**xml** loads TC-xml files, and performs a number of operations on it.
**ntexts** loads TC-xml files, and reports how many text-objects exist in the file.
**par** parses parallel corpora.

All file inputs in the commands accepts "-" as input, which specifies that the input should be read from stdin.
The examples in :ref:`combined_examples` gives some examples of this.

raw
________________

The **raw** command always loads raw text, and always outputs TC-XML files.


.. code-block:: console

    Usage: tpy raw [OPTIONS] [INPUT]...

    Options:
      --sent-tokenize / --no-sent-tokenize
                                      Will sentence tokenize if true.
      --tokenize / --no-tokenize      Will tokenize if true.
      --tag / --no-tag                Will tag if true.
      --tagger TEXT                   The tagger to use.
      --title TEXT                    Title to attach to generated texts.
      --language TEXT                 The language of the input text(s).
      --meta <TEXT TEXT>...           Metadata to attach to generated text(s)
      --tagset TEXT                   If set, the tags in the output will be
                                      converted into this tagset.
      -o, --output PATH               If given, the output will be written to this
                                      file, instead of stdout.
      --help                          Show this message and exit.

By default, the command will perform

* Sentence-tokenization
* Tokenization
* Tagging using NLTK
* All the above assuming the language is English.

Examples
..................

Load a raw file, tokenize and tag it, and output xml (to stdout):

.. code-block:: console

    $ tpy raw your_file.txt

To save to a file

.. code-block:: console

    $ tpy raw your_file.txt -o output.xml
    # or
    $ tpy raw your_file.txt > output.xml

To tag using a specific tagger:

.. code-block:: console

    $ tpy raw your_file.txt --tagger=tree  # Tags using the tree tagger

Attach "Annotator" metadata:

.. code-block:: console

    $ tpy raw your_file.txt --meta Annotator "Tormod Haugland"

Tags a german text

.. code-block:: console

    $ tpy raw your_file.txt --language=de

Tags a german text using the TreeTagger and converts all tags to the Typecraft tagset:

.. code-block:: console

    $ tpy raw your_file.txt --tagger=tree --tagset=tc --language=de


Suppose you have the file *input.txt* with the following contents:

.. code-block:: text

    Ich bin glucklich.

You now run the command

.. code-block:: console

    $ tpy raw input.txt --tagger=tree --language=de --tagset=tc

Your output (after prettifying) will be:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <typecraft xmlns="http://typecraft.org/typecraft" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://typecraft.org/typecraft.xsd">
       <text lang="de">
          <title>Automatically generated text from tpy</title>
          <titleTranslation />
          <body />
          <phrase valid="EMPTY">
             <original>Ich bin glucklich.</original>
             <translation />
             <translation2 />
             <globaltags id="1" tagset="DEFAULT" />
             <description />
             <word head="false" text="Ich">
                <pos>PN</pos>
                <morpheme baseform="ich" meaning="" text="Ich" />
             </word>
             <word head="false" text="bin">
                <pos>AUX</pos>
                <morpheme baseform="sein" meaning="" text="bin" />
             </word>
             <word head="false" text="glücklich">
                <pos>ADJ</pos>
                <morpheme baseform="glücklich" meaning="" text="glücklich" />
             </word>
             <word head="false" text=".">
                <pos>PUN</pos>
                <morpheme baseform="." meaning="" text="." />
             </word>
          </phrase>
       </text>
    </typecraft>

xml
________________

The **xml** command loads a TC-XML file, and performs a number of specified operations on it.

.. code-block:: console

    Usage: tpy xml [OPTIONS] [INPUT]...

    Options:
      --tokenize / --no-tokenize  Will re-tokenize all phrases if true.
      --tag / --no-tag            Will tag if true.
      --tagger TEXT               The tagger to use.
      --split INTEGER             If greater than 1, the output will be split into
                                  the given value number of texts.
      --merge / --no-merge        If true, will merge all files.
      --title TEXT                Title to attach to generated texts.
      --override-language TEXT    If set, will override the language used in all
                                  calculations and set the language for all texts.
      --meta <TEXT TEXT>...       Metadata to attach to generated text(s)
      --tagset TEXT               If set, the tags in the output will be converted
                                  into this tagset.
      -o, --output PATH           If given, the output will be written to this
                                  file, instead of stdout.
      --help                      Show this message and exit.


By default the command will do nothing but re-output the input. The "-o" flag behaves identically to the
one in **raw**.

Notes
...................

* Split will split into the given number of files, even if the given number is larger than the number of phrases.

Examples
....................

Load a text and splits it into 10 smaller texts (all contained in one file):

.. code-block:: console

    $ tpy xml your_file.xml --split 10

Load a text and convert the tagset:

.. code-block:: console

    $ tpy xml your_file.xml --tagset=tc

Tag or re-tag a text:

.. code-block:: console

    $ tpy xml your_file.xml --tag --tagger=tree

Change language and set some metadata:

.. code-block:: console

    $ tpy xml --override-language=nob \
        --meta Annotator "Tormod Haugland" \
        --meta "Content description" "This is some cool content"

par
___________________

**par** will parse parallel corpora files. Currently there is only one supported format,
named `continuous` or `linear`. The output is always Typecraft XML. This format requires there to
to be `n` consecutive lines in the file, one per language, for each phrase that is to be translated.

Note that the Typecraft XML format only supports two translation tiers.

.. code-block:: console

    Usage: tpy par [OPTIONS] [INPUT]...                                                                                                    │
                                                                                                                                           │
      The `par` command attempts to parse raw text as parallel corpora.                                                                    │
                                                                                                                                           │
      The input is one or more files containing raw text, in some parallel                                                                 │
      format.                                                                                                                              │
                                                                                                                                           │
    Options:                                                                                                                               │
      -f, --format TEXT        The format of the parallel file.                                                                            │
      -n, --num-langs INTEGER  The number of languages present.                                                                            │
      -o, --output PATH        If given, the output will be written to this file,                                                          │
                               instead of stdout.                                                                                          │
      --help                   Show this message and exit.

Examples
.......................

Given the file `input.txt` with the contents below:

.. code-block:: text

    Hi this is a nice sentence.
    Hei dette er en fin setning.
    This is sentence number two.
    Dette er setning nummber to.

Which is a parallel corpus file with two languages (Norwegian and English).
We can call the command

.. code-block:: console

    $ tpy par -n 2 input.txt

The resulting output will be Typecraft XML with a single text with two phrases. The phrases will not
be tokenized, with the appropriate amount of free translations tiers set.


ntexts
_________________

**ntexts** will output the number of texts in a TC-XML file.

Examples
......................

.. code-block:: console

    Usage: tpy ntexts [OPTIONS] INPUT

      This command lists the number of texts in a TCXml file. :param input:
      :return:

    Options:
      --help  Show this message and exit.


Examples
......................

.. code-block:: console

    $ tpy ntexts input_with_10_texts.xml
    10



.. _combined_examples:

Combined examples
_____________________

Load and treat a raw file, then split it into 10 texts:

.. code-block:: console

    # The "-" in the xml command reads the piped input
    $ tpy raw input.txt | tpy xml - --split 10

Load and treat a raw file, then merge it with an existing files texts.

.. code-block:: console

    $ tpy raw append_this.txt | tpy xml - to_this.xml --merge

Make sure ntexts behaves correctly:

.. code-block:: console

    $ tpy raw input.txt | tpy xml - --split 50 | tpy ntexts -
    100

Merge files then re-split:

.. code-block::  console

    $ tpy xml corpus{1..100}.xml --merge | tpy xml - -split 1000

