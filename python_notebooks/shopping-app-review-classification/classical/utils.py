#!/usr/bin/env python3
"""
Utility functions for text preprocessing and masking brand names
"""

import re
from typing import List, Set


def get_app_name_variants(app_name: str) -> Set[str]:
    """
    Generate variants of app name for masking.
    Returns a set of lowercase variants that should be masked.
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

    # Add common variations
    if "shopping" in app_lower:
        variants.add("shopping")
    if "online" in app_lower:
        variants.add("online")

    return variants


def mask_brand_names(
    text: str, app_names: List[str], mask_token: str = "[MASK]"
) -> str:
    """
    Mask brand names and app names in text to prevent data leakage.

    Args:
        text: Input text
        app_names: List of all app names to mask
        mask_token: Token to replace brand names with (default: "[MASK]")

    Returns:
        Text with brand names masked
    """
    import pandas as pd

    if not isinstance(text, str) or pd.isna(text):
        return ""

    text_lower = text.lower()

    # Collect all variants to mask
    all_variants = set()
    for app_name in app_names:
        all_variants.update(get_app_name_variants(app_name))

    # Sort by length (longest first) to avoid partial matches
    sorted_variants = sorted(all_variants, key=len, reverse=True)

    # Mask each variant
    masked_text = text
    for variant in sorted_variants:
        # Use word boundary to match whole words only
        pattern = r"\b" + re.escape(variant) + r"\b"
        masked_text = re.sub(pattern, mask_token, masked_text, flags=re.IGNORECASE)

    return masked_text


def preprocess_text(
    text: str, mask_brands: bool = False, app_names: List[str] = None
) -> str:
    """
    Preprocess text: lowercase, remove extra whitespace, optionally mask brands.

    Args:
        text: Input text
        mask_brands: Whether to mask brand names
        app_names: List of app names to mask (required if mask_brands=True)

    Returns:
        Preprocessed text
    """
    import pandas as pd

    if pd.isna(text):
        return ""

    # Convert to string and lowercase
    text = str(text).lower()

    # Mask brand names if requested
    if mask_brands and app_names:
        text = mask_brand_names(text, app_names)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()
