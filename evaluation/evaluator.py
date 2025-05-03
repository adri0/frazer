import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score


def calculate_metrics(baseline_path, new_path):
    # Load the CSV files
    baseline = pd.read_csv(baseline_path)
    new = pd.read_csv(new_path)

    # Ensure both files have the same structure
    assert list(baseline.columns) == list(new.columns), "CSV column mismatch"

    # Exclude 'sentence_id' from evaluation
    columns_to_evaluate = [col for col in baseline.columns if col != "sentence_id"]

    # Initialize results dictionary
    results = {}

    for column in columns_to_evaluate:
        # Calculate precision, recall, and F1 score for the column
        baseline[column] = baseline[column].fillna("none")
        new[column] = new[column].fillna("none")
        precision = precision_score(
            baseline[column], new[column], average="micro", zero_division=0
        )
        recall = recall_score(
            baseline[column], new[column], average="micro", zero_division=0
        )
        f1 = f1_score(baseline[column], new[column], average="micro", zero_division=0)

        # Store the results
        results[column] = {"precision": precision, "recall": recall, "f1": f1}

    return results


if __name__ == "__main__":
    # Define file paths
    baseline_path = "evaluation/output/baseline.csv"
    new_path = "evaluation/output/new.csv"

    # Calculate metrics
    metrics = calculate_metrics(baseline_path, new_path)

    # Print the results
    for column, scores in metrics.items():
        print(f"Column: {column}")
        print(f"  Precision: {scores['precision']:.2f}")
        print(f"  Recall: {scores['recall']:.2f}")
        print(f"  F1 Score: {scores['f1']:.2f}")
        print()
