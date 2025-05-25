"""
Mock server for testing the webapp.

Replies always with the same analysed sentence.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from frazer.analyser import (
    Adjective,
    AnalysedSentence,
    Aspect,
    Gender,
    Mood,
    Noun,
    Number,
    Other,
    SyntacticCategory,
    Verb,
    VerbConjugation,
)
from frazer.api import InputPayload, OutputPayload

logger = logging.getLogger(__name__)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mock_analysed_sentence = AnalysedSentence(
    text="Nie mogę znaleźć mojego telefonu.",
    translation="I can't find my phone.",
    words=[
        Other(
            original_value="Nie",
            root="nie",
            original_value_translation="not",
            syntatic_category=SyntacticCategory.adverb,
        ),
        Verb(
            original_value="mogę",
            root="móc",
            original_value_translation="can",
            syntatic_category=SyntacticCategory.verb,
            aspect=Aspect.imperfective,
            conjugation=VerbConjugation(
                person=1,
                number=Number.singular,
                gender=None,
                tense=None,
                mood=Mood.indicative,
            ),
            object=None,
        ),
        Verb(
            original_value="znaleźć",
            root="znaleźć",
            original_value_translation="to find",
            syntatic_category=SyntacticCategory.verb,
            aspect=Aspect.perfective,
            conjugation=VerbConjugation(
                person=None, number=None, gender=None, tense=None, mood=Mood.infinitive
            ),
            object=None,
        ),
        Adjective(
            original_value="mojego",
            root="mój",
            original_value_translation="my",
            syntatic_category=SyntacticCategory.adjective,
            declension_case="genitive",
            word_causing_declension="znaleźć",
            gender=Gender.masculine,
            number=Number.singular,
        ),
        Noun(
            original_value="telefonu",
            root="telefon",
            original_value_translation="phone",
            syntatic_category=SyntacticCategory.noun,
            declension_case="genitive",
            word_causing_declension="mojego",
            gender=Gender.masculine,
            number=Number.singular,
        ),
    ],
    grammatically_correct=True,
)


@app.post("/sentence", response_model=OutputPayload)
async def process_payload(payload: InputPayload):
    logger.info(f"Incoming sentence: {payload.sentence}")
    response = OutputPayload(sentence=mock_analysed_sentence)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("mock_server:app", host="127.0.0.1", port=8011, reload=True)
