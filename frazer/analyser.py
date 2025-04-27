from enum import Enum
from typing import Literal, Optional

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field


class SyntacticCategory(str, Enum):
    Noun = "Noun"
    Pronoun = "Pronoun"
    Verb = "Verb"
    Adjective = "Adjective"
    Adverb = "Adverb"
    Preposition = "Preposition"
    Conjunction = "Conjunction"
    Interjection = "Interjection"
    Particle = "Particle"


class Word(BaseModel):
    original_value: str
    root: str
    original_value_translation: str
    syntatic_category: SyntacticCategory


class Verb(Word):
    syntatic_category: Literal[SyntacticCategory.Verb]
    aspect: Literal["perfective", "imperfective"]
    conjugation: str
    object: Optional[str] = Field(
        description=("Object in the original sentence which this verbs acts upon."),
        default=None,
    )


class Adjective(Word):
    syntatic_category: Literal[SyntacticCategory.Adjective]
    declension_case: str
    verb_causing_declension: str


class Noun(Word):
    syntatic_category: Literal[SyntacticCategory.Noun]
    declension_case: str
    verb_causing_declension: str


class Preposition(Word):
    syntatic_category: Literal[SyntacticCategory.Preposition]


class Other(Word):
    pass


class Sentence(BaseModel):
    text: str
    translation: str
    words: list[Noun | Verb | Preposition | Adjective | Other]
    remarks: Optional[str] = Field(
        description=(
            "Any remarks about the sentence that could be relevant to the student. "
            "For example, if the sentence contains a mispelling or grammar mistake."
        ),
        default=None,
    )


client = instructor.from_openai(OpenAI())

categories = ",".join(SyntacticCategory.__members__.keys())


def analyse_sentence(input_sentence: str) -> Sentence:
    input_clean = input_sentence.strip()
    if not input_clean:
        raise ValueError("Sentence cannot be empty")
    sentence: Sentence = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=Sentence,
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": "You're a Polish language teacher with the goal of explaining a sentence word by word.",
            },
            {
                "role": "user",
                "content": (
                    f"Do a syntatical analysis of the sentence '{input_clean}'. "
                    f"Choose a syntactical category for each word amonth the options: {categories} \n"
                    "Provide the sentence translation to English. "
                    "If a word is a verb, indicate the verb's aspect and what declension case it enforces (if any). "
                    "If a word is a noun, numeral or adjective, provide its declension case. "
                    "If the word is of a different syntatical function, label the word as 'other' and provide its syntactical function. "
                    "Any remarks about the sentence that could be relevant to the student: "
                    "for example, point out a potential mispelling or grammar mistake."
                ),
            },
        ],
    )
    return sentence

    # "Provide a syntatical response for each word in the sentence (consider that some words might consist of 1 letter). "


#
