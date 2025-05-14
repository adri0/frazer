import pytest

from frazer.analyser import (
    AnalysedSentence,
    Noun,
    SyntacticCategory,
    Verb,
    analyse_sentence,
)


@pytest.fixture
def mock_openai_client(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock OpenAI client for testing."""

    def mock_create(*args, **kwargs):
        return AnalysedSentence(
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
                    syntatic_category=SyntacticCategory.verb,
                ),
                Noun(
                    original_value="książkę",
                    root="książka",
                    original_value_translation="book",
                    declension_case="accusative",
                    verb_causing_declension="czytać",
                    syntatic_category=SyntacticCategory.noun,
                ),
            ],
            grammatically_correct=True,
        )

    monkeypatch.setattr("frazer.analyser.client.chat.completions.create", mock_create)


def test_simple_sentence_analysis(mock_openai_client: None) -> None:
    sentence = analyse_sentence("Czytam książkę.")

    assert isinstance(sentence, AnalysedSentence)
    assert sentence.text == "Czytam książkę."
    assert sentence.translation == "I am reading a book."
    assert len(sentence.words) == 2
    assert isinstance(sentence.words[0], Verb)
    assert isinstance(sentence.words[1], Noun)


def test_sentence_structure(mock_openai_client: None) -> None:
    sentence = analyse_sentence("Czytam książkę.")

    verb = sentence.words[0]
    assert isinstance(verb, Verb)
    assert verb.original_value == "czytam"
    assert verb.aspect == "imperfective"
    assert verb.object == "książkę"

    noun = sentence.words[1]
    assert isinstance(noun, Noun)
    assert noun.original_value == "książkę"
    assert noun.declension_case == "accusative"
    assert noun.verb_causing_declension == "czytać"


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",
        "   ",
    ],
)
def test_invalid_input(invalid_input: str) -> None:
    with pytest.raises(ValueError):
        analyse_sentence(invalid_input)
