#!/usr/bin/env python3
"""
Extension: TF-IDF + Logistic Regression/SVM with Class Weights for Imbalance

This extension addresses class imbalance using class weights instead of SMOTE.
This is simpler and often more effective for high-dimensional sparse features like TF-IDF.

Class weights automatically adjust the loss function to penalize misclassifying
minority classes more heavily, without needing to generate synthetic samples.

Usage:
    python extension-classweight.py <train_file> <dev_file> <test_file> <output_file> [--model MODEL] [--mask]

Arguments:
    train_file: Path to training CSV file
    dev_file: Path to development CSV file
    test_file: Path to test CSV file
    output_file: Path to output CSV file with predictions
    --model: Model to use ('lr' for Logistic Regression, 'svm' for SVM, default: 'lr')
    --mask: Enable brand name masking to prevent data leakage
"""

import argparse
import pickle
import re
import sys
from difflib import SequenceMatcher
from typing import List, Set

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC


# Import masking functions
def get_app_name_variants(app_name: str) -> Set[str]:
    """Generate variants of app name for masking."""
    variants = set()
    app_lower = app_name.lower()
    variants.add(app_lower)
    words = app_lower.split()
    for word in words:
        if len(word) > 2:
            variants.add(word)
    return variants


def is_typo_variant(word: str, target: str, threshold: float = 0.85) -> bool:
    """Check if word is a typo variant of target."""
    if len(word) < 4 or len(target) < 4:
        return False
    similarity = SequenceMatcher(None, word, target).ratio()
    return similarity >= threshold


def mask_brand_names(
    text: str,
    app_names: List[str],
    mask_token: str = "[MASK]",
    enable_fuzzy: bool = True,
    fuzzy_threshold: float = 0.85,
) -> str:
    """Mask brand names and app names in text."""
    if not isinstance(text, str) or pd.isna(text):
        return ""

    text_lower = text.lower()
    all_variants = set()
    for app_name in app_names:
        all_variants.update(get_app_name_variants(app_name))

    sorted_variants = sorted(all_variants, key=len, reverse=True)
    masked_text = text

    for variant in sorted_variants:
        pattern = r"\b" + re.escape(variant) + r"\b"
        masked_text = re.sub(pattern, mask_token, masked_text, flags=re.IGNORECASE)

    if enable_fuzzy:
        words = masked_text.split()
        for i, word in enumerate(words):
            word_clean = re.sub(r"[^\w]", "", word.lower())
            for app_name in app_names:
                for variant in get_app_name_variants(app_name):
                    if is_typo_variant(word_clean, variant, fuzzy_threshold):
                        words[i] = mask_token
                        break
        masked_text = " ".join(words)

    return masked_text


def preprocess_text(
    text: str,
    mask_brands: bool = False,
    app_names: List[str] = None,
    fuzzy_threshold: float = 0.85,
) -> str:
    """Preprocess text: lowercase, remove extra whitespace, optionally mask brands."""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    if mask_brands and app_names:
        text = mask_brand_names(
            text, app_names, enable_fuzzy=True, fuzzy_threshold=fuzzy_threshold
        )
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_data(train_file, dev_file, test_file):
    """Load data"""
    print("Loading data...")
    train = pd.read_csv(train_file)
    dev = pd.read_csv(dev_file)
    test = pd.read_csv(test_file)

    print(f"Training set: {len(train):,} samples")
    print(f"Development set: {len(dev):,} samples")
    print(f"Test set: {len(test):,} samples")

    for df, name in [
        (train, "Training set"),
        (dev, "Development set"),
        (test, "Test set"),
    ]:
        if "content" not in df.columns or "appName" not in df.columns:
            raise ValueError(f"{name} must contain 'content' and 'appName' columns")

    return train, dev, test


def train_model(
    train,
    dev,
    model_type="lr",
    max_features=10000,
    max_iter=1000,
    mask_brands=False,
):
    """Train TF-IDF + classifier model with class weights"""
    print("\n" + "=" * 60)
    print("Training Model with Class Weights")
    print("=" * 60)

    all_app_names = sorted(train["appName"].unique().tolist())

    print("Preprocessing text...")
    if mask_brands:
        print("  Masking brand names to prevent data leakage...")
    train_texts = train["content"].apply(
        lambda x: preprocess_text(x, mask_brands=mask_brands, app_names=all_app_names)
    )
    dev_texts = dev["content"].apply(
        lambda x: preprocess_text(x, mask_brands=mask_brands, app_names=all_app_names)
    )

    print(f"Extracting TF-IDF features (max_features={max_features})...")
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        sublinear_tf=True,
    )

    X_train = vectorizer.fit_transform(train_texts)
    X_dev = vectorizer.transform(dev_texts)

    print(f"Feature dimension: {X_train.shape[1]:,}")

    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(train["appName"])
    y_dev = label_encoder.transform(dev["appName"])

    print(f"Number of classes: {len(label_encoder.classes_)}")
    print(f"Classes: {list(label_encoder.classes_)}")

    # Show class distribution
    print("\nClass distribution:")
    unique, counts = np.unique(y_train, return_counts=True)
    class_weights_dict = {}
    for cls_idx, count in zip(unique, counts):
        cls_name = label_encoder.inverse_transform([cls_idx])[0]
        # Calculate weight: total_samples / (n_classes * class_count)
        weight = len(y_train) / (len(unique) * count)
        class_weights_dict[cls_idx] = weight
        print(f"  {cls_name}: {count:,} (weight: {weight:.3f})")

    # Train classifier with class weights
    print(f"\nTraining {model_type.upper()} model with class weights...")
    if model_type == "svm":
        model = LinearSVC(
            max_iter=max_iter,
            random_state=42,
            C=1.0,
            dual=False,
            class_weight="balanced",  # Automatically balance class weights
        )
    else:
        model = LogisticRegression(
            max_iter=max_iter,
            random_state=42,
            n_jobs=-1,
            multi_class="ovr",
            C=1.0,
            class_weight="balanced",  # Automatically balance class weights
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

    all_app_names = sorted(test["appName"].unique().tolist())

    test_texts = test["content"].apply(
        lambda x: preprocess_text(x, mask_brands=mask_brands, app_names=all_app_names)
    )

    X_test = vectorizer.transform(test_texts)

    print("Making predictions...")
    y_pred = model.predict(X_test)

    pred_labels = label_encoder.inverse_transform(y_pred)

    predictions = pd.DataFrame({"reviewId": test["reviewId"], "appName": pred_labels})

    return predictions


def main():
    parser = argparse.ArgumentParser(
        description="Extension: TF-IDF + Class Weights + Logistic Regression/SVM"
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
        train, dev, test = load_data(args.train_file, args.dev_file, args.test_file)

        vectorizer, label_encoder, model = train_model(
            train,
            dev,
            model_type=args.model,
            mask_brands=args.mask,
        )

        predictions = predict(
            model, vectorizer, label_encoder, test, mask_brands=args.mask
        )

        predictions.to_csv(args.output_file, index=False)
        print(f"\nPredictions saved to: {args.output_file}")

        model_file = args.output_file.replace(".csv", "_model.pkl")
        with open(model_file, "wb") as f:
            pickle.dump(
                {
                    "vectorizer": vectorizer,
                    "label_encoder": label_encoder,
                    "model": model,
                    "model_type": args.model,
                    "mask_brands": args.mask,
                    "method": "class_weight",
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
