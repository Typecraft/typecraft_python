import six

from typecraft_python.core.models import Phrase
from typecraft_python.util import batch


def parse_continuous_parallel_text_to_tuples(
    raw_text,
    num_of_langs,
    strip=True
):
    assert isinstance(raw_text, six.string_types)
    lines = raw_text.split("\n")
    # Strip
    if strip:
        lines = [line.strip() for line in lines]

    # Ignore empty lines
    lines = [line for line in lines if line != ""]

    lines_batched = batch(lines, num_of_langs)
    return lines_batched


def parse_continuous_parallel_text_to_phrases(
    raw_text,
    num_of_langs,
    strip=True
):
    tuples = parse_continuous_parallel_text_to_tuples(raw_text, num_of_langs, strip)
    phrases = []
    for _tuple in tuples:
        if len(_tuple) == 0:
            continue
        phrase = Phrase()
        phrase.phrase = _tuple[0]

        if len(_tuple) > 1:
            phrase.translation = _tuple[1]

        if len(_tuple) > 2:
            phrase.translation2 = _tuple[2]

        phrases.append(phrase)

    return phrases



