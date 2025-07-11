from enum import Enum
from typing import Literal

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field


class Gender(str, Enum):
    masculine = "masculine"
    feminine = "feminine"
    neuter = "neuter"


class Tense(str, Enum):
    present = "present"
    past = "past"
    future = "future"


class Mood(str, Enum):
    indicative = "indicative"
    conditional = "conditional"
    imperative = "imperative"
    infinitive = "infinitive"
    active_participle = "active_participle"
    passive_participle = "passive_participle"


class Number(str, Enum):
    singular = "singular"
    plural = "plural"


class VerbConjugation(BaseModel):
    person: int | None = Field(
        description="The person of the verb (1, 2, or 3)",
        ge=1,
        le=3,
        default=None,
    )
    number: Number | None = Field(
        description="The number of the verb (singular or plural)",
        default=None,
    )
    gender: Gender | None = Field(
        description="The gender of the verb form, if applicable",
        default=None,
    )
    tense: Tense | None = Field(
        description="The tense of the verb, if applicable",
        default=None,
    )
    mood: Mood = Field(
        description="The mood of the verb, if applicable",
    )

    def __str__(self) -> str:
        """Convert the conjugation to a string representation."""
        parts = []
        if self.person and self.number:
            parts.append(f"{self.person}person_{self.number.value}")
        if self.gender:
            parts.append(self.gender.value)
        if self.tense:
            parts.append(self.tense.value)
        parts.append(self.mood.value)
        return "_".join(parts)


class SyntacticCategory(str, Enum):
    noun = "noun"
    pronoun = "pronoun"
    verb = "verb"
    adjective = "adjective"
    adverb = "adverb"
    preposition = "preposition"
    conjunction = "conjunction"
    interjection = "interjection"
    particle = "particle"
    numeral = "numeral"
    other = "other"


class Word(BaseModel):
    original_value: str
    root: str
    original_value_translation: str
    syntatic_category: SyntacticCategory
    other_syntatic_category: str | None = Field(
        description=(
            "If the word is of a different syntatical function, label "
            "the word's syntatic category as 'other' and provide its syntactical "
            "function."
        ),
        default=None,
    )


class Aspect(str, Enum):
    perfective = "perfective"
    imperfective = "imperfective"


class Verb(Word):
    syntatic_category: Literal[SyntacticCategory.verb]
    aspect: Aspect
    conjugation: VerbConjugation
    object: str | None = Field(
        description=("Object in the original sentence which this verbs acts upon."),
        default=None,
    )


class Adjective(Word):
    syntatic_category: Literal[SyntacticCategory.adjective]
    declension_case: str
    word_causing_declension: str
    gender: Gender
    number: Number


class Noun(Word):
    syntatic_category: Literal[SyntacticCategory.noun]
    declension_case: str
    word_causing_declension: str
    gender: Gender
    number: Number


class Preposition(Word):
    syntatic_category: Literal[SyntacticCategory.preposition]


class NumeralSubtype(str, Enum):
    cardinal = "cardinal"  # Główne
    ordinal = "ordinal"  # Porządkowe
    collective = "collective"  # Zbiorowe
    fractional = "fractional"  # Ułamkowe
    multiplicative = "multiplicative"  # Wielokrotne
    indefinite = "indefinite"  # Nieokreślone


class Numeral(Word):
    syntatic_category: Literal[SyntacticCategory.numeral]
    declension_case: str
    word_causing_declension: str
    subtype: NumeralSubtype


class Other(Word):
    pass


class AnalysedSentence(BaseModel):
    text: str
    translation: str
    words: list[Noun | Verb | Preposition | Adjective | Numeral | Other]
    grammatically_correct: bool
    remarks: str | None = Field(
        description=(
            "Any remarks about the sentence that could be relevant to the student. "
            "For example, if the sentence contains a mispelling or grammar mistake."
        ),
        default=None,
    )


client = instructor.from_openai(OpenAI())

categories = ",".join(SyntacticCategory.__members__.keys())


def analyse_sentence(input_sentence: str) -> AnalysedSentence:
    input_clean = input_sentence.strip()
    if not input_clean:
        raise ValueError("Sentence cannot be empty")
    # noqa: E501
    sentence: AnalysedSentence = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=AnalysedSentence,
        temperature=0.0,
        top_p=1,
        messages=[
            {
                "role": "system",
                "content": "You're a Polish language teacher with the goal of explaining a sentence word by word.",  # noqa: E501
            },
            {
                "role": "user",
                "content": (  # noqa: E501
                    f"Do a syntatical analysis of the sentence '{input_clean}'. "
                    "Choose a syntactical category for each word amonth the options: "
                    f"{categories}\n"
                    "Provide the sentence translation to English. "
                    "If a word is a verb, indicate the verb's aspect and what declension case it enforces (if any). "  # noqa: E501
                    "If a word is a noun, numeral or adjective, provide its declension case. "  # noqa: E501
                    "If the word is of a different syntatical function, label "
                    "the word as 'other' and provide its syntactical function. "
                    "Any remarks about the sentence that could be relevant to "
                    "the student: for example, point out a potential mispelling "
                    "or grammar mistake."
                ),
            },
        ],
    )
    return sentence
