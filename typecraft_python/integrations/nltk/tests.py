# coding: utf-8
import pytest

from typecraft_python.integrations.nltk.lemmatization import lemmatize_word, lemmatize_phrase
from typecraft_python.integrations.nltk.ne import find_named_entities_for_phrase
from typecraft_python.integrations.nltk.tokenization import raw_phrase_to_tokenized_phrase, raw_text_to_phrases, \
    raw_text_to_tokenized_phrases, tokenize_phrase
from typecraft_python.models import Phrase, Word, Morpheme, Text

# Ensure base modules is downloaded
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('wordnet')


class TestTokenize(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_simple_phrase(self):
        phrase = Phrase("This is a nice phrase.")
        tokenize_phrase(phrase)

        assert len(phrase.words) == 6
        assert phrase.words[0].word == "This"
        assert phrase.words[1].word == "is"
        assert phrase.words[2].word == "a"
        assert phrase.words[3].word == "nice"
        assert phrase.words[4].word == "phrase"
        assert phrase.words[5].word == "."

    def test_bad_phrase_should_throw(self):
        phrase = "This is a nice phrase."
        with pytest.raises(Exception):
            tokenize_phrase(phrase)

    def test_tokenize_raw_phrase(self):
        raw_phrase = "This is a nice phrase."
        phrase = raw_phrase_to_tokenized_phrase(raw_phrase)

        assert isinstance(phrase, Phrase)
        assert phrase.phrase == "This is a nice phrase."

        assert len(phrase.words) == 6
        assert phrase.words[0].word == "This"
        assert phrase.words[1].word == "is"
        assert phrase.words[2].word == "a"
        assert phrase.words[3].word == "nice"
        assert phrase.words[4].word == "phrase"
        assert phrase.words[5].word == "."


class TestNamedEntities(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_sentence_without_named_entities_adds_nothing(self):
        phrase = raw_phrase_to_tokenized_phrase("This has no named entities.")
        find_named_entities_for_phrase(phrase)

        assert 'Named entities' not in phrase.comment

    def test_sentence_with_named_entity_binary(self):
        phrase = raw_phrase_to_tokenized_phrase("Mike is a named entity")
        find_named_entities_for_phrase(phrase, binary=True)

        assert 'Named entities' in phrase.comment
        assert 'NE: Mike' in phrase.comment

    def test_sentence_with_named_entity_non_binary(self):
        phrase = raw_phrase_to_tokenized_phrase("Mike is a named entity")
        find_named_entities_for_phrase(phrase)
        assert 'Named entities' in phrase.comment
        assert 'PERSON: Mike' in phrase.comment

    def test_sentence_with_multiple_entities(self):
        phrase = raw_phrase_to_tokenized_phrase("Mike went travelling to Australia.")
        find_named_entities_for_phrase(phrase, binary=True)
        assert 'Named entities' in phrase.comment
        assert 'NE: Mike' in phrase.comment
        assert 'NE: Australia' in phrase.comment


class TestSentTokenize(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_raw_text_to_phrases(self):
        text = """
            This text contains two sentences. They are both very nice indeed.
        """
        phrases = raw_text_to_phrases(text)
        assert len(phrases) == 2
        assert isinstance(phrases[0], Phrase)
        assert isinstance(phrases[1], Phrase)
        assert len(phrases[0].words) == 0
        assert len(phrases[1].words) == 0

    def test_raw_text_to_tokenized_phrases(self):
        text = """
            This text contains two sentences. They are both very nice indeed.
        """
        phrases = raw_text_to_tokenized_phrases(text)
        assert len(phrases) == 2
        assert isinstance(phrases[0], Phrase)
        assert isinstance(phrases[1], Phrase)
        assert len(phrases[0].words) == 6
        assert len(phrases[1].words) == 7

    def test_longer_text(self):
        text = u"""
        Die wortschlaue Prinzessinn.
Es war einmal ein König, der hatte eine Tochter, die war so schlau und
spitzfindig in Worten, daß Keiner sie zum Schweigen bringen konnte.Da setzte der König einen Preis aus und ließ bekannt machen, daß Der,
welcher es könnte, die Prinzessinn und das halbe Reich haben sollte.Drei Brüder, welche dies hörten, beschlossen, ihr Glück zu versuchen.Zuerst machten sich die beiden ältesten auf, die sich am klügsten
dünkten; aber sie konnten Nichts bei der Prinzessinn ausrichten und
mußten noch dazu mit blauer Haut wieder abziehen. Darnach machte sich Aschenbrödel auch auf. Als er eine Strecke weit gegangen war, fand er am Wege ein Weidenreis, das nahm er auf. Eine Strecke weiter fand er eine Scherbe von einer alten Schüssel, die nahm er auch auf. Als er noch etwas weiter gegangen war, fand er einen todten Staar, und etwas darnach
ein krummes Bockshorn; ein wenig später fand er noch ein krummes
Bockshorn, und als er über das Feld zum Königshof gehen wollte, wo
Dünger ausgestreu't lag, fand er darunter eine ausgegangene Schuhsohle.
Alle diese Dinge nahm er mit sich zum Königsschloß, und damit trat er zu
der Prinzessinn ein. »Guten Tag!« sagte er. »Guten Tag!« sagte sie und
verzog das Gesicht. »Kann ich nicht meinen Staar gebraten kriegen?«
fragte er. »Ich bin bange, er birstet,« antwortete die Prinzessinn. »O,
das hat keine Noth, ich binde dieses Weidenreis um,« sagte der Bursch
und nahm das Reis hervor. »Aber das Fett läuft heraus,« sagte die
Prinzessinn. »Ich halte dies unter,« sagte der Bursch und zeigte ihr die
Scherbe von der Schüssel. »Du machst es mir so krumm, Du!« sagte die
Prinzessinn. »Ich mach es nicht krumm, sondern es ist schon krumm,«
sagte der Bursch und nahm das eine Horn hervor. »Nein, etwas Ähnliches
hab' ich noch mein Lebtag nicht gesehn!« rief die Prinzessinn. »Hier
siehst Du was Ähnliches,« sagte der Bursch und nahm das andre Bockshorn
hervor. »Ich glaube, Du bist ausgegangen, um mich zum Schweigen zu
bringen,« sagte die Prinzessinn. »Nein, ich bin nicht ausgegangen,
aber diese hier ist ausgegangen,« sagte der Bursch und zeigte ihr die
Schuhsohle. Hierauf wußte die Prinzessinn Nichts mehr zu antworten. »Nun
bist Du mein!« sagte der Bursch, und darauf erhielt er die Prinzessinn
und das halbe Königreich.
        """
        phrases = raw_text_to_tokenized_phrases(text)
        assert len(phrases) == 22


class TestLemmatize(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_lemmatize_word_morpheme_exists(self):
        morpheme = Morpheme('Cars')
        word = Word('Cars', morphemes=[morpheme])
        lemmatize_word(word)

        assert morpheme.baseform == 'car'

    def test_lemmatize_word_morpheme_does_not_exist(self):
        word = Word('Cars')
        lemmatize_word(word)

        assert len(word.morphemes) == 1

        morpheme = word.morphemes[0]
        assert morpheme.baseform == 'car'

    def test_lemmatize_phrase(self):
        phrase = raw_phrase_to_tokenized_phrase('Robert has many cars in his three houses.')
        lemmatize_phrase(phrase)

        for word in phrase:
            morpheme = word.morphemes[0]
            assert morpheme.baseform is not ''
