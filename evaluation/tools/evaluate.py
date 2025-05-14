from datetime import datetime, timezone
from pathlib import Path

import click
import pandas as pd

from evaluation.tools.batch_analyse import batch_analyse
from evaluation.tools.metrics import calculate_metrics, diff_datasets


def generate_report(
    input_sentences: Path,
    baseline: Path,
    run_name: str = "",
) -> None:
    """
    Generate a CSV report by analyzing input sentences, calculating metrics,
    saving the results, and saving the diff between baseline and analysed datasets.

    Args:
        input_sentences (Path): Path to the input CSV file.
        run_name (str): Name of the run to create a subfolder under output.
        baseline (Path): Path to the baseline CSV file.
    """
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
    suffix = f"_{run_name}" if run_name else ""
    output_dir = Path(f"evaluation/output/{timestamp}{suffix}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_analysed = output_dir / "analysed.csv"
    output_metrics = output_dir / "words_metrics.csv"
    output_diff = output_dir / "diff.csv"

    batch_analyse(input=input_sentences, output=output_analysed)

    metrics = calculate_metrics(baseline, output_analysed)
    metrics_df = pd.DataFrame.from_dict(metrics, orient="index")
    metrics_df.to_csv(output_metrics, index_label="dimension")

    # Save the diff between baseline and analysed
    diff_df = diff_datasets(baseline, output_analysed)
    diff_df.to_csv(output_diff, index=False)


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
    default="",
    help="Name of the run to create a subfolder under output.",
)
@click.option(
    "--baseline",
    type=click.Path(path_type=Path),
    default="evaluation/output/baseline.csv",
    help="Path to the baseline CSV file.",
)
def generate_report_cli(input_sentences: Path, run_name: str, baseline: Path) -> None:
    """
    CLI command to generate a CSV report by analyzing input
    sentences, calculating metrics, and saving the results.
    """
    generate_report(
        input_sentences=input_sentences,
        run_name=run_name,
        baseline=baseline,
    )


if __name__ == "__main__":
    generate_report_cli()
