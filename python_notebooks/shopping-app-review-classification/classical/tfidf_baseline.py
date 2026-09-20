#!/usr/bin/env python3
"""
Strong Baseline: TF-IDF + Logistic Regression or SVM

This method uses traditional but effective text classification:
1. TF-IDF feature extraction
2. Logistic Regression or SVM classifier

Reference paper:
- McIlroy et al. (2015): Used TF-IDF + SVM for app review classification
- We implement both Logistic Regression and SVM for comparison

Usage:
    python strong-baseline.py <train_file> <dev_file> <test_file> <output_file> [--model MODEL] [--mask]

Arguments:
    train_file: Path to training CSV file
    dev_file: Path to development CSV file (for validation)
    test_file: Path to test CSV file
    output_file: Path to output CSV file with predictions
    --model: Model to use ('lr' for Logistic Regression, 'svm' for SVM, default: 'lr')
    --mask: Mask brand names in text to prevent data leakage
"""

import argparse
import pickle
import re
import sys

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC

from utils import preprocess_text


def load_data(train_file, dev_file, test_file):
    """Load data"""
    print("Loading data...")
    train = pd.read_csv(train_file)
    dev = pd.read_csv(dev_file)
    test = pd.read_csv(test_file)

    print(f"Training set: {len(train):,} samples")
    print(f"Development set: {len(dev):,} samples")
    print(f"Test set: {len(test):,} samples")

    # Check required columns
    for df, name in [
        (train, "Training set"),
        (dev, "Development set"),
        (test, "Test set"),
    ]:
        if "content" not in df.columns or "appName" not in df.columns:
            raise ValueError(f"{name} must contain 'content' and 'appName' columns")

    return train, dev, test


def train_model(
    train, dev, model_type="lr", max_features=10000, max_iter=1000, mask_brands=False
):
    """Train TF-IDF + classifier model"""
    print("\n" + "=" * 60)
    print("Training Model")
    print("=" * 60)

    # Get all app names for masking
    all_app_names = sorted(train["appName"].unique().tolist())

    # Text preprocessing
    print("Preprocessing text...")
    if mask_brands:
        print("  Masking brand names to prevent data leakage...")
    train_texts = train["content"].apply(
        lambda x: preprocess_text(x, mask_brands=mask_brands, app_names=all_app_names)
    )
    dev_texts = dev["content"].apply(
        lambda x: preprocess_text(x, mask_brands=mask_brands, app_names=all_app_names)
    )

    # TF-IDF feature extraction
    print(f"Extracting TF-IDF features (max_features={max_features})...")
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),  # Use unigrams and bigrams
        min_df=2,  # Word must appear in at least 2 documents
        max_df=0.95,  # Word can appear in at most 95% of documents
        sublinear_tf=True,  # Use logarithmic TF
    )

    X_train = vectorizer.fit_transform(train_texts)
    X_dev = vectorizer.transform(dev_texts)

    print(f"Feature dimension: {X_train.shape[1]:,}")

    # Label encoding
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(train["appName"])
    y_dev = label_encoder.transform(dev["appName"])

    print(f"Number of classes: {len(label_encoder.classes_)}")
    print(f"Classes: {list(label_encoder.classes_)}")

    # Train classifier
    print(f"\nTraining {model_type.upper()} model...")
    if model_type == "svm":
        model = LinearSVC(
            max_iter=max_iter,
            random_state=42,
            C=1.0,  # Regularization parameter
            dual=False,  # Use primal formulation for large datasets
        )
    else:  # default to logistic regression
        model = LogisticRegression(
            max_iter=max_iter,
            random_state=42,
            n_jobs=-1,  # Use all CPU cores
            multi_class="ovr",  # One-vs-rest strategy
            C=1.0,  # Regularization parameter
        )

    model.fit(X_train, y_train)

    # Evaluate on development set
    print("\nEvaluating on development set...")
    train_acc = model.score(X_train, y_train)
    dev_acc = model.score(X_dev, y_dev)

    print(f"Training set accuracy: {train_acc:.4f}")
    print(f"Development set accuracy: {dev_acc:.4f}")

    return vectorizer, label_encoder, model


def predict(model, vectorizer, label_encoder, test, mask_brands=False):
    """Make predictions on test set"""
    print("\n" + "=" * 60)
    print("Generating Predictions")
    print("=" * 60)

    # Get all app names for masking
    all_app_names = sorted(test["appName"].unique().tolist())

    # Preprocess test set text
    test_texts = test["content"].apply(
        lambda x: preprocess_text(x, mask_brands=mask_brands, app_names=all_app_names)
    )

    # Extract features
    X_test = vectorizer.transform(test_texts)

    # Make predictions
    print("Making predictions...")
    y_pred = model.predict(X_test)

    # Convert back to class names
    pred_labels = label_encoder.inverse_transform(y_pred)

    # Create predictions DataFrame
    predictions = pd.DataFrame({"reviewId": test["reviewId"], "appName": pred_labels})

    return predictions


def main():
    parser = argparse.ArgumentParser(
        description="Strong baseline: TF-IDF + Logistic Regression or SVM"
    )
    parser.add_argument("train_file", help="Path to training CSV file")
    parser.add_argument("dev_file", help="Path to development CSV file")
    parser.add_argument("test_file", help="Path to test CSV file")
    parser.add_argument("output_file", help="Path to output CSV file")
    parser.add_argument(
        "--model",
        choices=["lr", "svm"],
        default="lr",
        help="Model to use: 'lr' for Logistic Regression, 'svm' for SVM (default: lr)",
    )
    parser.add_argument(
        "--mask",
        action="store_true",
        help="Mask brand names in text to prevent data leakage",
    )

    args = parser.parse_args()

    try:
        # Load data
        train, dev, test = load_data(args.train_file, args.dev_file, args.test_file)

        # Train model
        vectorizer, label_encoder, model = train_model(
            train, dev, model_type=args.model, mask_brands=args.mask
        )

        # Make predictions
        predictions = predict(
            model, vectorizer, label_encoder, test, mask_brands=args.mask
        )

        # Save predictions
        predictions.to_csv(args.output_file, index=False)
        print(f"\nPredictions saved to: {args.output_file}")

        # Save model (optional)
        model_file = args.output_file.replace(".csv", "_model.pkl")
        with open(model_file, "wb") as f:
            pickle.dump(
                {
                    "vectorizer": vectorizer,
                    "label_encoder": label_encoder,
                    "model": model,
                    "model_type": args.model,
                    "mask_brands": args.mask,
                },
                f,
            )
        print(f"Model saved to: {model_file}")

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
