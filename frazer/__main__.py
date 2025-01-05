import click
from openai import OpenAI


@click.command()
@click.argument("sentence")
def analyse(sentence: str) -> None:
    """Analyse a given sentence using OpenAI API."""

    client = OpenAI()
    try:
        response = client.chat.completions.create(
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
        click.echo(f"Analysis: {analysis}")
    except Exception as e:
        click.echo(f"Error: {e}")


if __name__ == "__main__":
    analyse()
