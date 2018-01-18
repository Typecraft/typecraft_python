from typecraft_python.parsing.convenience import detokenize


class TestDetokenize(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_detokenize_phrase_without_punctuation(self):
        tokens = [
            'This', 'is', 'cool'
        ]
        assert detokenize(tokens) == 'This is cool'

    def test_detokenize_phrase_with_end_punctuation(self):
        tokens = [
            'This', 'is', 'cool', '.'
        ]
        assert detokenize(tokens) == 'This is cool.'

    def test_detokenize_phrase_with_multiple_punctuation(self):
        tokens = [
            'And', 'so', 'he', 'said', ':', 'Give', 'me', 'milk', '!'
        ]
        assert detokenize(tokens) == 'And so he said: Give me milk!'

    def test_detokenize_with_single_quotation(self):
        tokens = [
            'I', '\'ve', 'sort', 'of', 'fallen', 'out', '.'
        ]
        assert detokenize(tokens) == 'I\'ve sort of fallen out.'

