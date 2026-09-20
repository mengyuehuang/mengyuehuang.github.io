#!/usr/bin/env python3
"""
Evaluation script: Compute evaluation metrics for multi-class classification task

Usage:
    python score.py <gold_file> <pred_file>

Arguments:
    gold_file: CSV file containing gold standard labels (must have reviewId and appName columns)
    pred_file: CSV file containing predicted labels (must have reviewId and appName columns)

Output:
    Prints accuracy, macro-averaged and micro-averaged precision, recall, and F1 score
"""

import sys

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def load_labels(file_path):
    """Load labels from CSV file"""
    df = pd.read_csv(file_path)
    if "reviewId" not in df.columns or "appName" not in df.columns:
        raise ValueError(
            f"File {file_path} must contain 'reviewId' and 'appName' columns"
        )
    return df.set_index("reviewId")["appName"]


def evaluate(gold_file, pred_file):
    """Evaluate predictions"""
    # Load gold and predicted labels
    gold_labels = load_labels(gold_file)
    pred_labels = load_labels(pred_file)

    # Ensure both files have the same reviewIds
    common_ids = gold_labels.index.intersection(pred_labels.index)
    if len(common_ids) != len(gold_labels):
        print(
            f"Warning: Only {len(common_ids)}/{len(gold_labels)} samples have predictions",
            file=sys.stderr,
        )

    gold_labels = gold_labels.loc[common_ids]
    pred_labels = pred_labels.loc[common_ids]

    # Get all labels
    all_labels = sorted(set(gold_labels) | set(pred_labels))

    # Compute metrics
    accuracy = accuracy_score(gold_labels, pred_labels)
    precision_macro = precision_score(
        gold_labels, pred_labels, average="macro", zero_division=0
    )
    recall_macro = recall_score(
        gold_labels, pred_labels, average="macro", zero_division=0
    )
    f1_macro = f1_score(gold_labels, pred_labels, average="macro", zero_division=0)

    precision_micro = precision_score(
        gold_labels, pred_labels, average="micro", zero_division=0
    )
    recall_micro = recall_score(
        gold_labels, pred_labels, average="micro", zero_division=0
    )
    f1_micro = f1_score(gold_labels, pred_labels, average="micro", zero_division=0)

    # Print results
    print("=" * 60)
    print("Evaluation Results")
    print("=" * 60)
    print(f"Accuracy: {accuracy:.4f}")
    print()
    print("Macro Average:")
    print(f"  Precision: {precision_macro:.4f}")
    print(f"  Recall:    {recall_macro:.4f}")
    print(f"  F1 Score:  {f1_macro:.4f}")
    print()
    print("Micro Average:")
    print(f"  Precision: {precision_micro:.4f}")
    print(f"  Recall:    {recall_micro:.4f}")
    print(f"  F1 Score:  {f1_micro:.4f}")
    print()
    print("=" * 60)
    print("Classification Report:")
    print("=" * 60)
    print(classification_report(gold_labels, pred_labels, zero_division=0))

    return {
        "accuracy": accuracy,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "f1_macro": f1_macro,
        "precision_micro": precision_micro,
        "recall_micro": recall_micro,
        "f1_micro": f1_micro,
    }


def main():
    if len(sys.argv) != 3:
        print("Usage: python score.py <gold_file> <pred_file>", file=sys.stderr)
        print(
            "Example: python score.py data/new_data/test.csv predictions.csv",
            file=sys.stderr,
        )
        sys.exit(1)

    gold_file = sys.argv[1]
    pred_file = sys.argv[2]

    try:
        evaluate(gold_file, pred_file)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
