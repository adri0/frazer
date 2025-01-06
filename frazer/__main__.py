import click

from frazer.analyser import analyse_sentence


@click.command()
@click.argument("sentence")
def analyse_cmd(sentence: str) -> None:
    """Analyse a given sentence using OpenAI API."""

    try:
        result = analyse_sentence(sentence)
        click.echo(f"Analysis: {result}")
    except Exception as e:
        click.echo(f"Error: {e}")


if __name__ == "__main__":
    analyse_cmd()
