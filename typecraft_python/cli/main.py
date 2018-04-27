import copy

import click
import nltk

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
@click.argument('input', type=click.File('r'), nargs=-1)
@click.option('--sent-tokenize/--no-sent-tokenize', default=True)
@click.option('--tokenize/--no-tokenize', default=True)
@click.option('--tag/--no-tag', default=True)
@click.option('--tagger', default='nltk')
@click.option('--title', default='Automatically generated text from tpy')
@click.option('--language', default='en')
@click.option('--meta', nargs=2, type=click.Tuple([str, str]), multiple=True)
@click.option('--tagset', type=str, default='')
@click.option('-o', '--output', type=click.Path())
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

    if tag:
        _tagger = get_tagger_by_name(tagger)()

    if _tagger and _tagger.has_automatic_word_tokenization_support() and \
       _tagger.has_automatic_sentence_tokenization_support():
        # The tagger has everything we need to get full tokenization
        phrases = _tagger.tag_raw(contents)
    elif _tagger and _tagger.has_automatic_word_tokenization_support():
        # Sentence tokenize, then tag.
        phrases = nltk.sent_tokenize(contents, language)
        _phrases = []
        for phrase in phrases:
            _phrases.extend(_tagger.tag_raw(phrase))
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
        metadata=dict(meta)
    )

    if tagset != '':
        text.map_tags(tagset)

    write_to_stdout_or_file(Parser.write([text]), output)


@main.command()
@click.argument('input', type=click.File('r'), nargs=-1)
@click.option('--tokenize/--no-tokenize', default=True)
@click.option('--tag/--no-tag', default=False)
@click.option('--tagger', default='nltk')
@click.option('--split', default=1, type=int)
@click.option('--merge/--no-merge', default=False)
@click.option('--title', default=None)
@click.option('--override-language', default=None)
@click.option('--meta', nargs=2, type=click.Tuple([str, str]), multiple=True)
@click.option('--tagset', type=str, default="")
@click.option('-o', '--output', type=click.Path())
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
        if tokenize:
            for phrase in text:
                tokenize_phrase(phrase)

        if tag:
            _tagger = get_tagger_by_name(tagger)()
            _tagger.tag_text(text, override_language or text.language)

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


if __name__ == '__main__':
    main()
