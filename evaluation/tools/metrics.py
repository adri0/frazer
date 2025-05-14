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
        baseline[column] = baseline[column].fillna("N/A")
        new[column] = new[column].fillna("N/A")
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


def diff_datasets(baseline_path: Path, new_path: Path) -> pd.DataFrame:
    """
    Generate a diff DataFrame for each column and row between baseline and new datasets.
    For each cell, output only values that don't match.

    Args:
        baseline_path (Path): Path to the baseline CSV file.
        new_path (Path): Path to the new CSV file.

    Returns:
        pd.DataFrame: DataFrame with '-' for matches and new value for differences.
    """
    baseline = pd.read_csv(baseline_path)
    new = pd.read_csv(new_path)
    assert list(baseline.columns) == list(new.columns), "CSV column mismatch"
    assert len(baseline) == len(new), "CSV row count mismatch"
    diff = new.copy()
    for col in EVALUTION_DIMENSIONS:
        diff[col] = [
            None if baseline.at[i, col] == new.at[i, col] else new.at[i, col]
            for i in range(len(baseline))
        ]
    return diff
