import copy

import click
import nltk

from typecraft_python.parsing.parallell import parse_continuous_parallel_text_to_phrases
from typecraft_python.cli.util import write_to_stdout_or_file
from typecraft_python.parsing.parser import Parser
from typecraft_python.core.models import Phrase, Text
from typecraft_python.integrations.nltk.tokenization import raw_phrase_to_tokenized_phrase, raw_text_to_phrases, \
    raw_text_to_tokenized_phrases, tokenize_phrase
from typecraft_python.util import get_tagger_by_name, split as split_into_sublists


@click.group()
def main():
    pass


@main.command()
@click.option('--sent-tokenize/--no-sent-tokenize', default=True, help='Will sentence tokenize if true.')
@click.option('--tokenize/--no-tokenize', default=True, help='Will tokenize if true.')
@click.option('--tag/--no-tag', default=True, help='Will tag if true.')
@click.option('--tagger', default='nltk', help='The tagger to use.')
@click.option('--title', default='Automatically generated text from tpy', help='Title to attach to generated texts.')
@click.option('--language', default='en', help='The language of the input text(s).')
@click.option('--meta', nargs=2, type=click.Tuple([str, str]), multiple=True, help="Metadata to attach to generated text(s)")
@click.option('--tagset', type=str, default='', help='If set, the tags in the output will be converted into this tagset.')
@click.option('-o', '--output', type=click.Path(), help='If given, the output will be written to this file, instead of stdout.')
@click.argument('input', type=click.File('r'), nargs=-1)
def raw(
    input,
    sent_tokenize,
    tokenize,
    tag,
    tagger,
    title,
    language,
    meta,
    tagset,
    output
):
    # Perform input validation
    if tag and (not sent_tokenize or not tokenize):
        raise ValueError("Cannot tag untokenized text. Please set both `sent_tokenize` "
                         "and `tokenize` to true")

    contents = ""
    for _input in input:
        _contents = _input.read()
        if _contents[-1] != "\n":
            _contents += "\n"
        contents += _contents

    _tagger = None
    if tag:
        _tagger = get_tagger_by_name(tagger)()

    if _tagger and _tagger.has_automatic_word_tokenization_support(language) and \
       _tagger.has_automatic_sentence_tokenization_support(language):
        # The tagger has everything we need to get full tokenization
        phrases = _tagger.tag_raw(contents, language)
    elif _tagger and _tagger.has_automatic_word_tokenization_support(language):
        # Sentence tokenize, then tag.
        phrases = nltk.sent_tokenize(contents, language)
        _phrases = []
        for phrase in phrases:
            _phrases.extend(_tagger.tag_raw(phrase, language))
    else:
        if sent_tokenize and tokenize:
            phrases = raw_text_to_tokenized_phrases(contents)
        elif sent_tokenize:
            phrases = raw_text_to_phrases(contents)
        elif tokenize:
            phrases = [raw_phrase_to_tokenized_phrase(contents)]
        else:
            phrases = [Phrase(contents)]

        if tag:
            phrases = _tagger.tag_phrases(phrases, language)

    text = Text(
        phrases=phrases,
        title=title,
        metadata=dict(meta),
        language=language
    )

    if tagset != '':
        text.map_tags(tagset)

    write_to_stdout_or_file(Parser.write([text]), output)


@main.command()
@click.option('--tokenize/--no-tokenize', default=False, help='Will re-tokenize all phrases if true.')
@click.option('--tag/--no-tag', default=False, help='Will tag if true.')
@click.option('--tagger', default='nltk', help='The tagger to use.')
@click.option('--split', default=1, type=int, help='If greater than 1, the output will be split into the given value number of texts.')
@click.option('--merge/--no-merge', default=False, help='If true, will merge all files.')
@click.option('--title', default=None, help='Title to attach to generated texts.')
@click.option('--override-language', default=None, help='If set, will override the language used in all calculations and set the language for all texts.')
@click.option('--meta', nargs=2, type=click.Tuple([str, str]), multiple=True, help="Metadata to attach to generated text(s)")
@click.option('--tagset', type=str, default='', help='If set, the tags in the output will be converted into this tagset.')
@click.option('-o', '--output', type=click.Path(), help='If given, the output will be written to this file, instead of stdout.')
@click.argument('input', type=click.File('r'), nargs=-1)
def xml(
    input,
    tokenize,
    tag,
    tagger,
    split,
    merge,
    title,
    override_language,
    meta,
    tagset,
    output
):
    if split > 1 and merge:
        raise ValueError("Error running tpy xml: Both merge and split cannot be set to true")

    texts = []
    for _input in input:
        texts.extend(Parser.parse(_input.read()))
    new_texts = []
    for text in texts:
        if override_language:
            text.language = override_language

        if tokenize:
            for phrase in text:
                tokenize_phrase(phrase)

        if tag:
            _tagger = get_tagger_by_name(tagger)()
            _tagger.tag_text(text, text.language)

        if title:
            text.title = title

        for key, value in meta:
            text.add_metadata(key, value)

        if split > 1:
            batched_phrases = split_into_sublists(text.phrases, split)
            for phrase_batch in batched_phrases:
                new_text = copy.copy(text)
                new_text.phrases = list(phrase_batch)
                new_texts.append(new_text)
        else:
            new_texts.append(text)

    if merge:
        root_text = new_texts[0]
        for text in new_texts[1:]:
            root_text.merge(text)
        new_texts = [root_text]

    if tagset != '':
        for text in new_texts:
            text.map_tags(tagset)

    write_to_stdout_or_file(Parser.write(new_texts), output)


@main.command()
def convert():
    raise NotImplementedError("Convert command not implemented yet.")


@main.command()
@click.argument('input', type=click.File('r'))
def ntexts(
    input
):
    """
    This command lists the number of texts in a TCXml file.
    :param input:
    :return:
    """
    texts = Parser.parse(input.read())
    click.echo(len(texts))


@main.command()
@click.option('-f', '--format', type=str, default='continuous', help='The format of the parallel file.')
@click.option('-n', '--num-langs', type=int, default=2, help='The number of languages present.')
@click.option('-o', '--output', type=click.Path(), help='If given, the output will be written to this file, instead of stdout.')
@click.argument('input', type=click.File('r'), nargs=-1)
def par(
    format,
    num_langs,
    output,
    input
):
    """
    The `par` command attempts to parse raw text as parallel corpora.

    The input is one or more files containing raw text, in some parallel format.
    """
    contents = ""
    for _input in input:
        _contents = _input.read()
        if _contents[-1] != "\n":
            _contents += "\n"
        contents += _contents

    phrases = parse_continuous_parallel_text_to_phrases(contents, num_langs)
    text = Text(title="Automatically generated parallel corpus", phrases=phrases)

    write_to_stdout_or_file(Parser.write([text]), output)


if __name__ == '__main__':
    main()
