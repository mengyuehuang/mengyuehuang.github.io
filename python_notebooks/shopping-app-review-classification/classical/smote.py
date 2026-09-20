#!/usr/bin/env python3
"""
Extension: TF-IDF + Logistic Regression/SVM with SMOTE for Class Imbalance

This extension addresses class imbalance using SMOTE (Synthetic Minority Oversampling Technique):
1. Text preprocessing with brand name masking
2. TF-IDF feature extraction
3. SMOTE oversampling to balance classes
4. Logistic Regression or SVM classifier

SMOTE creates synthetic samples for minority classes by interpolating between existing samples,
helping the model learn better representations for underrepresented classes.

Reference:
- Chawla, N. V., et al. (2002). SMOTE: synthetic minority over-sampling technique.
  Journal of artificial intelligence research, 16, 321-357.

Usage:
    python extension-smote.py <train_file> <dev_file> <test_file> <output_file> [--model MODEL] [--mask] [--smote-strategy STRATEGY]

Arguments:
    train_file: Path to training CSV file
    dev_file: Path to development CSV file (for validation)
    test_file: Path to test CSV file
    output_file: Path to output CSV file with predictions
    --model: Model to use ('lr' for Logistic Regression, 'svm' for SVM, default: 'lr')
    --mask: Enable brand name masking to prevent data leakage
    --smote-strategy: SMOTE sampling strategy ('auto', 'minority', or float, default: 'auto')
"""

import argparse
import pickle
import re
import sys
from difflib import SequenceMatcher
from typing import List, Set

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC


# Import masking functions from strong-baseline-mask.py
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
    smote_strategy="auto",
):
    """Train TF-IDF + SMOTE + classifier model"""
    print("\n" + "=" * 60)
    print("Training Model with SMOTE")
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

    # Show class distribution before SMOTE
    print("\nClass distribution before SMOTE:")
    unique, counts = np.unique(y_train, return_counts=True)
    for cls_idx, count in zip(unique, counts):
        cls_name = label_encoder.inverse_transform([cls_idx])[0]
        print(f"  {cls_name}: {count:,}")

    # Apply SMOTE
    print(f"\nApplying SMOTE (strategy={smote_strategy})...")
    smote = SMOTE(
        sampling_strategy=smote_strategy,
        random_state=42,
        k_neighbors=5,
    )

    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    print(f"Training samples after SMOTE: {X_train_resampled.shape[0]:,}")
    print("\nClass distribution after SMOTE:")
    unique, counts = np.unique(y_train_resampled, return_counts=True)
    for cls_idx, count in zip(unique, counts):
        cls_name = label_encoder.inverse_transform([cls_idx])[0]
        print(f"  {cls_name}: {count:,}")

    # Train classifier
    print(f"\nTraining {model_type.upper()} model...")
    if model_type == "svm":
        model = LinearSVC(
            max_iter=max_iter,
            random_state=42,
            C=1.0,
            dual=False,
        )
    else:
        model = LogisticRegression(
            max_iter=max_iter,
            random_state=42,
            n_jobs=-1,
            multi_class="ovr",
            C=1.0,
        )

    model.fit(X_train_resampled, y_train_resampled)

    # Evaluate on development set
    print("\nEvaluating on development set...")
    train_acc = model.score(X_train_resampled, y_train_resampled)
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
        description="Extension: TF-IDF + SMOTE + Logistic Regression/SVM"
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

    args = parser.parse_args()

    # Parse smote_strategy
    if args.smote_strategy == "auto":
        smote_strategy = "auto"
    elif args.smote_strategy == "minority":
        smote_strategy = "minority"
    else:
        try:
            smote_strategy = float(args.smote_strategy)
        except ValueError:
            print(f"Invalid smote-strategy: {args.smote_strategy}", file=sys.stderr)
            sys.exit(1)

    try:
        train, dev, test = load_data(args.train_file, args.dev_file, args.test_file)

        # Optionally sample data for faster training
        if args.sample_size and args.sample_size < len(train):
            print(f"\nSampling {args.sample_size:,} samples for faster training...")
            # Sample equal number from each class
            samples_per_class = args.sample_size // 11
            train_sampled = []
            for app_name in train["appName"].unique():
                class_data = train[train["appName"] == app_name]
                n_samples = min(len(class_data), samples_per_class)
                train_sampled.append(class_data.sample(n=n_samples, random_state=42))
            train = pd.concat(train_sampled, ignore_index=True)
            print(f"Sampled training set: {len(train):,} samples")

        vectorizer, label_encoder, model = train_model(
            train,
            dev,
            model_type=args.model,
            mask_brands=args.mask,
            smote_strategy=smote_strategy,
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
                    "smote_strategy": smote_strategy,
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
