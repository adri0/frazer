import click

from evaluation.tools.batch_analyse import main as batch_analyse_main
from evaluation.tools.evaluate import generate_report_cli


@click.group()
def cli():
    """
    Evaluation tool for Frazer.
    """
    pass


cli.add_command(generate_report_cli, name="generate-report")
cli.add_command(batch_analyse_main, name="batch-analyse")


if __name__ == "__main__":
    cli()
