import click
import yaml
from termcolor import colored

from frazer.analyser import analyse_sentence


def colorize_yaml(yaml_content: str) -> str:
    """Colorize YAML content with keys in blue and values in green."""
    colored_yaml = ""
    for line in yaml_content.splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            colored_yaml += f"{colored(key, 'blue')}: {colored(value, 'green')}\n"
        else:
            colored_yaml += f"{colored(line, 'blue')}\n"
    return colored_yaml


@click.command()
@click.argument("sentence")
def analyse_cmd(sentence: str) -> None:
    """Analyse a given sentence using OpenAI API."""

    try:
        analysed_sentence = analyse_sentence(sentence)
        result_dict = analysed_sentence.model_dump(mode="json")
        yaml_result = yaml.dump(result_dict, allow_unicode=True, indent=2)
        colored_yaml = colorize_yaml(yaml_result)
        click.echo(colored_yaml)

    except Exception as e:
        click.echo(f"Error: {e}")


if __name__ == "__main__":
    analyse_cmd()
