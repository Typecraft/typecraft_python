import copy

import click

from typecraft_python.parsing.parser import Parser
from typecraft_python.models import Phrase, Text
from typecraft_python.integrations.nltk_integration import raw_text_to_tokenized_phrases, raw_text_to_phrases, \
    raw_phrase_to_tokenized_phrase, tokenize_phrase
from typecraft_python.util import get_tagger_by_name, split as split_into_sublists


@click.group()
def main():
    pass


@main.command()
@click.argument('input', type=click.File('r'))
@click.option('--sent-tokenize/--no-sent-tokenize', default=True)
@click.option('--tokenize/--no-tokenize', default=True)
@click.option('--tag/--no-tag', default=True)
@click.option('--tagger', default='TreeTagger')
@click.option('--title', default='Automatically generated text from tpy')
@click.option('--language', default='en')
@click.option('--meta', nargs=2, type=click.Tuple([str, str]), multiple=True)
def raw(
    input,
    sent_tokenize,
    tokenize,
    tag,
    tagger,
    title,
    language,
    meta
):
    contents = input.read()
    if sent_tokenize and tokenize:
        phrases = raw_text_to_tokenized_phrases(contents)
    elif sent_tokenize:
        phrases = raw_text_to_phrases(contents)
    elif tokenize:
        phrases = [raw_phrase_to_tokenized_phrase(contents)]
    else:
        phrases = [Phrase(contents)]

    if tag:
        tagger = get_tagger_by_name(tagger)()
        phrases = tagger.tag_phrases(phrases, language)

    text = Text(
        phrases=phrases,
        title=title,
        metadata=dict(meta)
    )
    click.echo(Parser.write([text]))


@main.command()
@click.argument('input', type=click.File('r'))
@click.option('--tokenize/--no-tokenize', default=True)
@click.option('--tag/--no-tag', default=False)
@click.option('--tagger', default='TreeTagger')
@click.option('--split', default=1, type=int)
@click.option('--merge/--no-merge', default=False)
@click.option('--title', default=None)
@click.option('--override-language', default=None)
@click.option('--meta', nargs=2, type=click.Tuple([str, str]), multiple=True)
def xml(
    input,
    tokenize,
    tag,
    tagger,
    split,
    merge,
    title,
    override_language,
    meta
):
    if split > 1 and merge:
        raise ValueError("Error running tpy xml: Both merge and split cannot be set to true")

    texts = Parser.parse(input.read())
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

    root_text = new_texts[0]
    if merge:
        for text in new_texts[1:]:
            root_text.merge(text)
        new_texts = [root_text]

    click.echo(Parser.write(new_texts))


@main.command()
def convert():
    click.echo("Hello")


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
