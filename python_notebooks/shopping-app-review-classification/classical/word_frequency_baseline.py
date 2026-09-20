#!/usr/bin/env python3
"""
Simple Baseline: Word Frequency Baseline

This baseline uses word frequency to make predictions:
1. For each class, find the most distinctive words (words that appear frequently in that class but not in others)
2. For each test sample, count how many distinctive words from each class appear in the review
3. Predict the class with the most matching distinctive words

This is still a simple baseline but uses text information, making it more meaningful than majority class baseline.

Usage:
    python simple-baseline.py <train_file> <test_file> <output_file> [--top-n N]

Arguments:
    train_file: Path to training CSV file
    test_file: Path to test CSV file
    output_file: Path to output CSV file with predictions
    --top-n: Number of top distinctive words per class (default: 20)
"""

import argparse
import re
import sys
from collections import Counter

import pandas as pd


def preprocess_text(text):
    """Simple text preprocessing"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"[^\w\s]", " ", text)  # Remove punctuation
    text = re.sub(r"\s+", " ", text)  # Normalize whitespace
    return text.strip()


def get_class_word_frequencies(df, top_n=20):
    """
    Get top distinctive words for each class.
    Distinctiveness is measured by: word frequency in class / word frequency overall
    """
    print("Computing word frequencies per class...")

    # Get all words for each class
    class_words = {}
    all_words = Counter()

    for app_name in df["appName"].unique():
        class_texts = df[df["appName"] == app_name]["content"].apply(preprocess_text)
        words = []
        for text in class_texts:
            words.extend(text.split())
        class_words[app_name] = Counter(words)
        all_words.update(words)

    # Find distinctive words for each class
    class_distinctive_words = {}

    for app_name, word_counts in class_words.items():
        class_total = sum(word_counts.values())
        overall_total = sum(all_words.values())

        # Calculate distinctiveness score: (freq in class / class total) / (freq overall / overall total)
        # Higher score means word is more distinctive to this class
        # Also require minimum frequency to avoid typos and rare words
        distinctive_scores = {}
        min_freq = max(
            10, class_total // 1000
        )  # Word must appear at least this many times in class

        for word, count in word_counts.items():
            if (
                word and len(word) > 3 and count >= min_freq
            ):  # Ignore short words and rare words
                class_freq = count / class_total if class_total > 0 else 0
                overall_freq = (
                    all_words[word] / overall_total if overall_total > 0 else 0
                )
                if (
                    overall_freq > 0 and overall_freq < 0.1
                ):  # Word should not be too common overall
                    distinctive_scores[word] = class_freq / overall_freq
                elif overall_freq == 0:
                    distinctive_scores[word] = class_freq

        # Get top N most distinctive words
        if distinctive_scores:
            top_words = sorted(
                distinctive_scores.items(), key=lambda x: x[1], reverse=True
            )[:top_n]
            class_distinctive_words[app_name] = [word for word, score in top_words]
        else:
            # Fallback: use most frequent words in this class
            class_distinctive_words[app_name] = [
                word for word, count in word_counts.most_common(top_n) if len(word) > 3
            ]

        print(
            f"  {app_name}: {len(class_distinctive_words[app_name])} distinctive words"
        )
        print(f"    Top 5: {', '.join(class_distinctive_words[app_name][:5])}")

    return class_distinctive_words


def predict_with_word_frequency(test_df, class_distinctive_words):
    """Predict class based on word frequency matching"""
    predictions = []

    for idx, row in test_df.iterrows():
        text = preprocess_text(row["content"])
        words = set(text.split())

        # Count matches for each class
        class_scores = {}
        for app_name, distinctive_words in class_distinctive_words.items():
            matches = len(words.intersection(set(distinctive_words)))
            class_scores[app_name] = matches

        # Predict class with most matches
        # If tie, use majority class as fallback
        max_score = max(class_scores.values())
        if max_score == 0:
            # No matches, use majority class (Aliexpress)
            predicted = "Aliexpress"
        else:
            predicted = max(class_scores.items(), key=lambda x: x[1])[0]

        predictions.append(predicted)

    return predictions


def main():
    parser = argparse.ArgumentParser(description="Simple baseline using word frequency")
    parser.add_argument("train_file", help="Path to training CSV file")
    parser.add_argument("test_file", help="Path to test CSV file")
    parser.add_argument("output_file", help="Path to output CSV file")
    parser.add_argument(
        "--top-n",
        type=int,
        default=20,
        help="Number of top distinctive words per class (default: 20)",
    )

    args = parser.parse_args()

    try:
        print("=" * 60)
        print("Simple Baseline: Word Frequency Baseline")
        print("=" * 60)

        # Load data
        print("\nLoading data...")
        train_df = pd.read_csv(args.train_file)
        test_df = pd.read_csv(args.test_file)

        print(f"Training set: {len(train_df):,} samples")
        print(f"Test set: {len(test_df):,} samples")

        # Get distinctive words for each class
        class_distinctive_words = get_class_word_frequencies(train_df, top_n=args.top_n)

        # Make predictions
        print("\n" + "=" * 60)
        print("Generating Predictions")
        print("=" * 60)
        predictions = predict_with_word_frequency(test_df, class_distinctive_words)

        # Create output DataFrame
        output_df = pd.DataFrame(
            {"reviewId": test_df["reviewId"], "appName": predictions}
        )
        output_df.to_csv(args.output_file, index=False)

        print(f"\nPredictions saved to: {args.output_file}")

        # Show prediction distribution
        pred_counts = Counter(predictions)
        print(f"\nPrediction distribution:")
        for app_name, count in pred_counts.most_common():
            print(f"  {app_name}: {count:,} ({count/len(predictions)*100:.2f}%)")

        print("\n" + "=" * 60)
        print("Complete!")
        print("=" * 60)
        print(f"\nYou can evaluate the results using:")
        print(f"  python score.py {args.test_file} {args.output_file}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
