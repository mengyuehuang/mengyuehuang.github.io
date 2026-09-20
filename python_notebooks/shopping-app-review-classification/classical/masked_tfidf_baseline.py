#!/usr/bin/env python3
"""
Masked Baseline: TF-IDF + Logistic Regression/SVM with Brand Name Masking

This method uses traditional text classification with enhanced brand name masking:
1. Text preprocessing with typo-aware brand name masking
2. TF-IDF feature extraction
3. Logistic Regression or SVM classifier

The masking feature prevents data leakage by:
- Masking exact app name matches
- Masking app name word components
- Fuzzy matching to catch typo variations (e.g., "amzon" → "amazon")

Reference paper:
- McIlroy et al. (2015): Used TF-IDF + SVM for app review classification
- We implement both Logistic Regression and SVM for comparison

Usage:
    python masked-baseline.py <train_file> <dev_file> <test_file> <output_file> [--model MODEL] [--mask] [--fuzzy-threshold THRESHOLD]

Arguments:
    train_file: Path to training CSV file
    dev_file: Path to development CSV file (for validation)
    test_file: Path to test CSV file
    output_file: Path to output CSV file with predictions
    --model: Model to use ('lr' for Logistic Regression, 'svm' for SVM, default: 'lr')
    --mask: Enable brand name masking to prevent data leakage
    --fuzzy-threshold: Similarity threshold for typo matching (default: 0.85, range: 0.0-1.0)
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

def get_app_name_variants(app_name: str) -> Set[str]:
    """
    Generate variants of app name for masking.
    
    Args:
        app_name: Original app name
    
    Returns:
        Set of lowercase variants that should be masked
    """
    variants = set()
    app_lower = app_name.lower()

    # Add full app name
    variants.add(app_lower)

    # Split into words and add individual words (if length > 2)
    words = app_lower.split()
    for word in words:
        if len(word) > 2:  # Ignore short words like "app", "the", etc.
            variants.add(word)

    return variants


def is_typo_variant(word: str, target: str, threshold: float = 0.85) -> bool:
    """
    Check if word is a typo variant of target using fuzzy string matching.
    
    Args:
        word: Word to check
        target: Target app name or word
        threshold: Similarity threshold (0-1), higher = more strict
    
    Returns:
        True if word is likely a typo of target
    """
    # Skip very short words to avoid false positives
    if len(word) < 4 or len(target) < 4:
        return False
    
    # Calculate similarity ratio using SequenceMatcher
    similarity = SequenceMatcher(None, word, target).ratio()
    
    return similarity >= threshold


def mask_brand_names(
    text: str,
    app_names: List[str],
    mask_token: str = "[MASK]",
    enable_fuzzy: bool = True,
    fuzzy_threshold: float = 0.85,
) -> str:
    """
    Mask brand names and app names in text to prevent data leakage.
    Uses two-pass approach: exact matching first, then fuzzy matching for typos.

    Args:
        text: Input text
        app_names: List of all app names to mask
        mask_token: Token to replace brand names with
        enable_fuzzy: Whether to enable fuzzy matching for typos
        fuzzy_threshold: Similarity threshold for fuzzy matching (0-1)

    Returns:
        Text with brand names masked
    """
    if not isinstance(text, str) or pd.isna(text):
        return ""

    # Collect all variants to mask
    all_variants = set()
    for app_name in app_names:
        all_variants.update(get_app_name_variants(app_name))

    # Sort by length (longest first) to avoid partial matches
    sorted_variants = sorted(all_variants, key=len, reverse=True)

    # First pass: Exact matching with word boundaries
    masked_text = text
    for variant in sorted_variants:
        pattern = r"\b" + re.escape(variant) + r"\b"
        masked_text = re.sub(pattern, mask_token, masked_text, flags=re.IGNORECASE)

    # Second pass: Fuzzy matching for typos (if enabled)
    if enable_fuzzy:
        words = masked_text.split()
        masked_words = []

        for word in words:
            # Skip if already masked
            if word == mask_token:
                masked_words.append(word)
                continue

            # Clean word (remove punctuation for matching)
            clean_word = re.sub(r"[^\w]", "", word.lower())

            # Check for typo variants
            is_typo = False
            for variant in sorted_variants:
                if is_typo_variant(clean_word, variant, fuzzy_threshold):
                    masked_words.append(mask_token)
                    is_typo = True
                    break

            if not is_typo:
                masked_words.append(word)

        masked_text = " ".join(masked_words)

    return masked_text


def preprocess_text(
    text: str,
    mask_brands: bool = False,
    app_names: List[str] = None,
    fuzzy_threshold: float = 0.85,
) -> str:
    """
    Preprocess text: lowercase, remove extra whitespace, optionally mask brands.

    Args:
        text: Input text
        mask_brands: Whether to mask brand names
        app_names: List of app names to mask (required if mask_brands=True)
        fuzzy_threshold: Similarity threshold for typo matching

    Returns:
        Preprocessed text
    """
    if pd.isna(text):
        return ""

    # Convert to string and lowercase
    text = str(text).lower()

    # Mask brand names if requested
    if mask_brands and app_names:
        text = mask_brand_names(
            text, app_names, enable_fuzzy=True, fuzzy_threshold=fuzzy_threshold
        )

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def load_data(train_file, dev_file, test_file):
    """Load training, development, and test data from CSV files"""
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
    train,
    dev,
    model_type="lr",
    max_features=10000,
    max_iter=1000,
    mask_brands=False,
    fuzzy_threshold=0.85,
):
    """
    Train TF-IDF + classifier model with optional brand name masking.
    
    Args:
        train: Training DataFrame
        dev: Development DataFrame
        model_type: 'lr' for Logistic Regression or 'svm' for SVM
        max_features: Maximum number of TF-IDF features
        max_iter: Maximum iterations for classifier training
        mask_brands: Whether to mask brand names
        fuzzy_threshold: Similarity threshold for typo matching
    
    Returns:
        Tuple of (vectorizer, label_encoder, model)
    """
    print("\n" + "=" * 60)
    print("Training Model")
    print("=" * 60)

    # Get all app names for masking
    all_app_names = sorted(train["appName"].unique().tolist())

    # Text preprocessing
    print("Preprocessing text...")
    if mask_brands:
        print(f"  Masking brand names (fuzzy threshold: {fuzzy_threshold})...")
    train_texts = train["content"].apply(
        lambda x: preprocess_text(
            x,
            mask_brands=mask_brands,
            app_names=all_app_names,
            fuzzy_threshold=fuzzy_threshold,
        )
    )
    dev_texts = dev["content"].apply(
        lambda x: preprocess_text(
            x,
            mask_brands=mask_brands,
            app_names=all_app_names,
            fuzzy_threshold=fuzzy_threshold,
        )
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


def predict(
    model, vectorizer, label_encoder, test, mask_brands=False, fuzzy_threshold=0.85
):
    """
    Make predictions on test set.
    
    Args:
        model: Trained classifier
        vectorizer: Fitted TF-IDF vectorizer
        label_encoder: Fitted label encoder
        test: Test DataFrame
        mask_brands: Whether to mask brand names
        fuzzy_threshold: Similarity threshold for typo matching
    
    Returns:
        DataFrame with predictions
    """
    print("\n" + "=" * 60)
    print("Generating Predictions")
    print("=" * 60)

    # Get all app names for masking
    all_app_names = sorted(test["appName"].unique().tolist())

    # Preprocess test set text
    test_texts = test["content"].apply(
        lambda x: preprocess_text(
            x,
            mask_brands=mask_brands,
            app_names=all_app_names,
            fuzzy_threshold=fuzzy_threshold,
        )
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
        description="Masked baseline: TF-IDF + Logistic Regression/SVM with brand name masking"
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
        "--fuzzy-threshold",
        type=float,
        default=0.85,
        help="Similarity threshold for fuzzy typo matching (default: 0.85, range: 0.0-1.0)",
    )

    args = parser.parse_args()

    # Validate fuzzy threshold
    if not 0.0 <= args.fuzzy_threshold <= 1.0:
        print("Error: --fuzzy-threshold must be between 0.0 and 1.0", file=sys.stderr)
        sys.exit(1)

    try:
        # Load data
        train, dev, test = load_data(args.train_file, args.dev_file, args.test_file)

        # Train model
        vectorizer, label_encoder, model = train_model(
            train,
            dev,
            model_type=args.model,
            mask_brands=args.mask,
            fuzzy_threshold=args.fuzzy_threshold,
        )

        # Make predictions
        predictions = predict(
            model,
            vectorizer,
            label_encoder,
            test,
            mask_brands=args.mask,
            fuzzy_threshold=args.fuzzy_threshold,
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
                    "fuzzy_threshold": args.fuzzy_threshold,
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