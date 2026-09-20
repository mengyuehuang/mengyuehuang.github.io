#!/usr/bin/env python3
"""
Extension: TF-IDF + Borderline-SMOTE for Class Imbalance

This extension uses Borderline-SMOTE, which focuses on generating synthetic samples
near the decision boundary, making it more effective than standard SMOTE.

Borderline-SMOTE Algorithm:
1. Identify borderline minority samples (those near the decision boundary)
2. Generate synthetic samples only for these borderline samples
3. This focuses oversampling on the most critical regions

Reference:
- Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002).
  SMOTE: Synthetic Minority Over-sampling Technique.
  Journal of Artificial Intelligence Research (JAIR), 16, 321-357.
  https://doi.org/10.1613/jair.953

- Han, H., Wang, W. Y., & Mao, B. H. (2005). Borderline-SMOTE: A New Over-Sampling
  Method in Imbalanced Data Sets Learning. Advances in Intelligent Computing, 878-887.

Usage:
    python extension-borderline-smote.py <train_file> <dev_file> <test_file> <output_file> [options]
"""

import argparse
import pickle
import sys
from typing import List, Set

import numpy as np
import pandas as pd
from imblearn.over_sampling import BorderlineSMOTE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC

from utils import preprocess_text


def load_data(train_file, dev_file, test_file):
    """Load training, development, and test data."""
    print("Loading data...")
    train = pd.read_csv(train_file)
    dev = pd.read_csv(dev_file)
    test = pd.read_csv(test_file)

    print(f"Training set: {len(train)} samples")
    print(f"Development set: {len(dev)} samples")
    print(f"Test set: {len(test)} samples")

    return train, dev, test


def train_model_borderline_smote(
    train,
    dev,
    test,
    model_type="lr",
    max_features=10000,
    max_iter=1000,
    mask_brands=False,
    smote_strategy="auto",
    sample_size=None,
):
    """
    Train model with TF-IDF + Borderline-SMOTE.

    Args:
        train: Training DataFrame
        dev: Development DataFrame
        test: Test DataFrame
        model_type: 'lr' or 'svm'
        max_features: Maximum TF-IDF features
        max_iter: Maximum iterations for classifier
        mask_brands: Whether to mask brand names
        smote_strategy: SMOTE sampling strategy
        sample_size: Sample size for faster training (None = use all data)
    """
    print("\n" + "=" * 60)
    print("TF-IDF + Borderline-SMOTE Extension")
    print("=" * 60)

    # Sample data if requested
    if sample_size and sample_size < len(train):
        print(f"\nSampling {sample_size} samples from training set...")
        train = (
            train.groupby("appName", group_keys=False)
            .apply(
                lambda x: x.sample(min(len(x), sample_size // 11), random_state=42),
                include_groups=False,
            )
            .reset_index(drop=True)
        )
        print(f"Sampled training set: {len(train)} samples")

    # Get app names for masking
    app_names = train["appName"].unique().tolist() if mask_brands else None

    # Preprocess text
    print("\nPreprocessing text...")
    train_texts = (
        train["content"]
        .apply(
            lambda x: preprocess_text(x, mask_brands=mask_brands, app_names=app_names)
        )
        .tolist()
    )
    dev_texts = (
        dev["content"]
        .apply(
            lambda x: preprocess_text(x, mask_brands=mask_brands, app_names=app_names)
        )
        .tolist()
    )
    test_texts = (
        test["content"]
        .apply(
            lambda x: preprocess_text(x, mask_brands=mask_brands, app_names=app_names)
        )
        .tolist()
    )

    # TF-IDF vectorization
    print(f"\nExtracting TF-IDF features (max_features={max_features})...")
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        sublinear_tf=True,
    )

    X_train = vectorizer.fit_transform(train_texts)
    X_dev = vectorizer.transform(dev_texts)
    X_test = vectorizer.transform(test_texts)

    print(f"Training set shape: {X_train.shape}")
    print(f"Development set shape: {X_dev.shape}")
    print(f"Test set shape: {X_test.shape}")

    # Encode labels
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(train["appName"])
    y_dev = label_encoder.transform(dev["appName"])

    # Check class distribution before Borderline-SMOTE
    print("\nClass distribution before Borderline-SMOTE:")
    unique, counts = np.unique(y_train, return_counts=True)
    for label, count in zip(unique, counts):
        print(f"  Class {label_encoder.inverse_transform([label])[0]}: {count} samples")

    # Apply Borderline-SMOTE
    print(f"\nApplying Borderline-SMOTE (strategy={smote_strategy})...")
    borderline_smote = BorderlineSMOTE(
        random_state=42,
        sampling_strategy=smote_strategy,
        k_neighbors=5,
        kind="borderline-1",  # or 'borderline-2'
    )
    X_train_resampled, y_train_resampled = borderline_smote.fit_resample(
        X_train, y_train
    )

    print(f"Training set after Borderline-SMOTE: {X_train_resampled.shape[0]} samples")
    print("\nClass distribution after Borderline-SMOTE:")
    unique, counts = np.unique(y_train_resampled, return_counts=True)
    for label, count in zip(unique, counts):
        print(f"  Class {label_encoder.inverse_transform([label])[0]}: {count} samples")

    # Train classifier
    print(f"\nTraining {model_type.upper()} classifier...")
    if model_type == "lr":
        classifier = LogisticRegression(
            max_iter=max_iter, random_state=42, n_jobs=-1, verbose=1
        )
    elif model_type == "svm":
        classifier = LinearSVC(
            max_iter=max_iter, random_state=42, verbose=1, dual=False
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")

    classifier.fit(X_train_resampled, y_train_resampled)
    print("Training completed!")

    # Evaluate on development set
    print("\nEvaluating on development set...")
    y_dev_pred = classifier.predict(X_dev)
    dev_accuracy = np.mean(y_dev_pred == y_dev)
    print(f"Development accuracy: {dev_accuracy:.4f}")

    # Predict on test set
    print("\nPredicting on test set...")
    y_test_pred = classifier.predict(X_test)
    test_predictions = label_encoder.inverse_transform(y_test_pred)

    # Save model
    model_file = "extension-borderline-smote-predictions_model.pkl"
    print(f"\nSaving model to {model_file}...")
    with open(model_file, "wb") as f:
        pickle.dump(
            {
                "classifier": classifier,
                "vectorizer": vectorizer,
                "label_encoder": label_encoder,
                "mask_brands": mask_brands,
            },
            f,
        )

    return test_predictions, classifier, label_encoder


def main():
    parser = argparse.ArgumentParser(
        description="TF-IDF + Borderline-SMOTE Extension for Class Imbalance"
    )
    parser.add_argument("train_file", help="Path to training CSV file")
    parser.add_argument("dev_file", help="Path to development CSV file")
    parser.add_argument("test_file", help="Path to test CSV file")
    parser.add_argument("output_file", help="Path to output CSV file with predictions")
    parser.add_argument(
        "--model",
        choices=["lr", "svm"],
        default="lr",
        help="Model to use (default: lr)",
    )
    parser.add_argument(
        "--mask",
        action="store_true",
        help="Enable brand name masking to prevent data leakage",
    )
    parser.add_argument(
        "--smote-strategy",
        default="auto",
        help="SMOTE sampling strategy: 'auto', 'minority', or float (default: auto)",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=None,
        help="Sample size for faster training (default: None, use all data)",
    )
    parser.add_argument(
        "--max-features",
        type=int,
        default=10000,
        help="Maximum TF-IDF features (default: 10000)",
    )
    parser.add_argument(
        "--max-iter",
        type=int,
        default=1000,
        help="Maximum iterations for classifier (default: 1000)",
    )

    args = parser.parse_args()

    # Load data
    train, dev, test = load_data(args.train_file, args.dev_file, args.test_file)

    # Train model
    predictions, model, label_encoder = train_model_borderline_smote(
        train=train,
        dev=dev,
        test=test,
        model_type=args.model,
        max_features=args.max_features,
        max_iter=args.max_iter,
        mask_brands=args.mask,
        smote_strategy=args.smote_strategy,
        sample_size=args.sample_size,
    )

    # Save predictions
    output_df = pd.DataFrame({"reviewId": test["reviewId"], "appName": predictions})
    output_df.to_csv(args.output_file, index=False)
    print(f"\nPredictions saved to {args.output_file}")

    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
