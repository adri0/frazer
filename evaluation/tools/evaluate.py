from datetime import datetime, timezone
from pathlib import Path

import click
import yaml

from evaluation.tools.batch_analyse import batch_analyse
from evaluation.tools.metrics import calculate_metrics


def generate_report(
    input_sentences: Path,
    run_name: str,
    baseline: Path,
):
    """
    Generate a YAML report by analyzing input sentences, calculating metrics, and saving the results.

    Args:
        input_sentences (Path): Path to the input CSV file.
        run_name (str): Name of the run to create a subfolder under output.
        baseline (Path): Path to the baseline CSV file.
    """
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"evaluation/output/{timestamp}_{run_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_analysed = output_dir / "analysed.csv"
    output_metrics = output_dir / "report.yaml"

    batch_analyse(input=input_sentences, output=output_analysed)

    metrics = calculate_metrics(baseline, output_analysed)
    with output_metrics.open("w", encoding="utf-8") as file:
        yaml.dump(metrics, file, default_flow_style=False)


@click.command()
@click.option(
    "--input-sentences",
    type=click.Path(exists=True, path_type=Path),
    default="evaluation/input_sentences.csv",
    help="Path to the input CSV file containing sentences.",
)
@click.option(
    "--run-name",
    type=str,
    required=True,
    help="Name of the run to create a subfolder under output.",
)
@click.option(
    "--baseline",
    type=click.Path(path_type=Path),
    default="evaluation/output/baseline.csv",
    help="Path to the baseline CSV file.",
)
def generate_report_cli(input_sentences: Path, run_name: str, baseline: Path):
    """
    CLI command to generate a YAML report by analyzing input sentences, calculating metrics, and saving the results.
    """
    generate_report(
        input_sentences=input_sentences,
        run_name=run_name,
        baseline=baseline,
    )


if __name__ == "__main__":
    generate_report_cli()
