import pytest

from frazer.analyser import (
    Noun,
    Sentence,
    Verb,
    analyse_sentence,
)


@pytest.fixture
def mock_openai_client(monkeypatch):
    """Mock OpenAI client for testing."""

    def mock_create(*args, **kwargs):
        return Sentence(
            text="Czytam książkę.",
            translation="I am reading a book.",
            words=[
                Verb(
                    original_value="czytam",
                    root="czytać",
                    original_value_translation="I read",
                    aspect="imperfective",
                    conjugation="first person singular",
                    object="książkę",
                ),
                Noun(
                    original_value="książkę",
                    root="książka",
                    original_value_translation="book",
                    declension_case="accusative",
                    verb_causing_declension="czytać",
                ),
            ],
        )

    monkeypatch.setattr("frazer.analyser.client.chat.completions.create", mock_create)


def test_simple_sentence_analysis(mock_openai_client):
    sentence = analyse_sentence("Czytam książkę.")

    assert isinstance(sentence, Sentence)
    assert sentence.text == "Czytam książkę."
    assert sentence.translation == "I am reading a book."
    assert len(sentence.words) == 2
    assert isinstance(sentence.words[0], Verb)
    assert isinstance(sentence.words[1], Noun)


def test_sentence_structure(mock_openai_client):
    sentence = analyse_sentence("Czytam książkę.")

    verb = sentence.words[0]
    assert verb.original_value == "czytam"
    assert verb.aspect == "imperfective"
    assert verb.object == "książkę"

    noun = sentence.words[1]
    assert noun.original_value == "książkę"
    assert noun.declension_case == "accusative"
    assert noun.verb_causing_declension == "czytać"


def test_empty_sentence():
    with pytest.raises(ValueError):
        analyse_sentence("")


def test_whitespace_only_sentence():
    with pytest.raises(ValueError):
        analyse_sentence("   ")
