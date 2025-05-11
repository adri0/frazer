from pathlib import Path

import pandas as pd
from sklearn.metrics import classification_report

EVALUTION_DIMENSIONS = [
    "word_root",
    "word_original_value_translation",
    "word_syntactic_category",
    "word_aspect",
    "word_conjugation",
    "word_object",
    "word_declension_case",
    "word_verb_causing_declension",
]


def calculate_metrics(baseline_path: Path, new_path: Path) -> dict[str, dict]:
    """
    Calculate evaluation metrics for comparing two datasets. The result
    is consists of precision, recall, F1-score and support.

    Args:
        baseline_path (Path): Path to the baseline CSV file.
        new_path (Path): Path to the new CSV file.

    Returns:
        dict[str, dict]: A dictionary where each key corresponds to an evaluation
    """
    baseline = pd.read_csv(baseline_path)
    new = pd.read_csv(new_path)

    assert list(baseline.columns) == list(new.columns), "CSV column mismatch"
    results = {}
    for column in EVALUTION_DIMENSIONS:
        baseline[column] = baseline[column].fillna("none")
        new[column] = new[column].fillna("none")
        report = classification_report(
            baseline[column], new[column], output_dict=True, zero_division=0
        )

        results[column] = {
            "precision": report["weighted avg"]["precision"],
            "recall": report["weighted avg"]["recall"],
            "f1": report["weighted avg"]["f1-score"],
            "support": report["weighted avg"]["support"],
        }

    return results


if __name__ == "__main__":
    baseline_path = Path("evaluation/output/baseline.csv")
    new_path = Path("evaluation/output/new.csv")
    metrics = calculate_metrics(baseline_path, new_path)
    metrics_df = pd.DataFrame.from_dict(metrics, orient="index")
    print(metrics_df)
