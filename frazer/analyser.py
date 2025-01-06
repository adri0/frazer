from openai import OpenAI

open_ai = OpenAI()


def analyse_sentence(sentence: str) -> str:
    response = open_ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You're a language teacher."},
            {
                "role": "user",
                "content": f"Do a syntatical analysis the sentence '{sentence}'",
            },
        ],
    )
    analysis = response.choices[0]
    return analysis.message.content
