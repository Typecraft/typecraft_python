import nltk

from typecraft_python.integrations.nltk.util import _parse_entity_tree_for_named_entities


def find_named_entities_for_phrase(phrase, binary=False):
    """
    Finds all the named entities of a phrase, and adds them to the
    phrases comment.

    :param phrase: A Phrase.
    :param binary: Should the returned named entity tags be of binary type?
    :return: The Phrase. Note that the alteration is done in-place.
             Thus this return value need not be used.
    """
    words = [word.word for word in phrase]
    tagged = nltk.pos_tag(words)
    entities = nltk.chunk.ne_chunk(tagged, binary)
    parsed = _parse_entity_tree_for_named_entities(entities)

    if len(parsed) == 0:
        return phrase

    phrase.comment += "\nNamed entities:\n%s" % ("\n".join(
        [("%s: %s" % (ne[0], ne[1])) for ne in parsed]
    ))
    return phrase
