from openai import OpenAI

open_ai = OpenAI()


def analyse_sentence(sentence: str) -> str | None:
    response = open_ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You're a Polish language teacher."},
            {
                "role": "user",
                "content": f"Do a syntatical analysis the sentence '{sentence}'. Provide also its translation to English. For every verb, indicate the verb's aspect and what declension case it enforces (if any). For nouns, adjects and adverbs, provide the declension case.",
            },
        ],
    )
    analysis = response.choices[0]
    return analysis.message.content
