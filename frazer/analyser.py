from typing import Literal, Optional

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field


class Word(BaseModel):
    original_value: str
    root: str
    original_value_translation: str


class Verb(Word):
    aspect: Literal["perfective", "imperfective"]
    conjugation: str
    object: Optional[str] = Field(
        description=("Object in the original sentence which this verbs acts upon."),
        default=None,
    )


class Adjective(Word):
    declension_case: str
    verb_causing_declension: str


class Noun(Word):
    declension_case: str
    verb_causing_declension: str


class Preposition(Word):
    pass


class Other(Word):
    function: str


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


def analyse_sentence(input_sentence: str) -> Sentence:
    sentence: Sentence = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=Sentence,
        temperature=0.1,
        messages=[
            {"role": "system", "content": "You're a Polish language teacher."},
            {
                "role": "user",
                "content": (
                    f"Do a syntatical analysis of the sentence '{input_sentence}'. "
                    "Provide a syntatical response for each word in the sentence (consider that some words might consist of 1 letter). "
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
