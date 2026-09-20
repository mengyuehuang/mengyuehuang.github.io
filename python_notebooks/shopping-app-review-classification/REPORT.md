# Shopping App Classification from User Reviews

## Objective

The project asks whether the source of a shopping-app review can be identified from its language alone. It is formulated as an 11-class text-classification task over 630,000 public reviews.

The work addresses two risks that make the benchmark harder than it first appears:

- Class sizes are unequal, with roughly a 7:1 ratio between the largest and smallest labels.
- About 29% of reviews explicitly mention an app or brand name, creating potential target leakage.

## Data design

Platform-specific CSV files were merged without changing the original eight fields. A stratified 80/10/10 split produced:

- 504,000 training examples
- 63,000 development examples
- 63,000 held-out test examples

The modeling target is `appName`, and the primary input is `content`. The split notebook verifies consistent columns, preserved label distributions, and disjoint review identifiers.

## Evaluation

Macro-F1 is the primary metric because it weights each platform equally despite class imbalance. Accuracy, Macro Precision, Macro Recall, weighted F1, and Top-2 accuracy provide complementary views.

## Interpretable baselines

The word-frequency baseline selects class-distinctive terms and predicts the label with the most matching terms. It reached 0.3484 Macro-F1.

A TF-IDF model with unigrams, bigrams, and Logistic Regression raised performance to 0.7021 Macro-F1 on raw review text. A masked version replaces detected platform and brand names with `[MASK]`; this more conservative setup reached 0.5514 Macro-F1.

## Class-imbalance experiments

Three approaches were evaluated over sparse TF-IDF features:

| Method | Accuracy | Macro-F1 |
|---|---:|---:|
| Masked baseline | 0.5676 | 0.5514 |
| Standard SMOTE | 0.5650 | 0.5482 |
| Borderline-SMOTE | 0.5714 | 0.5555 |
| Class-weighted Logistic Regression | **0.6034** | **0.5802** |

Class weighting performed best. It changes the optimization objective without creating interpolated examples in a sparse, high-dimensional feature space.

## Transformer benchmark

Seven pretrained encoders were fine-tuned with a shared evaluation pipeline. The workflow standardizes label mapping, data splits, tokenization, checkpoint discovery, test metrics, Top-2 accuracy, per-class reporting, and confusion-matrix generation.

| Model | Test Accuracy | Test Macro-F1 | Test Top-2 Accuracy |
|---|---:|---:|---:|
| DeBERTa-v3-base | **0.7716** | **0.7725** | **0.8893** |
| RoBERTa-base | 0.7682 | 0.7688 | 0.8877 |
| BERT-large | 0.7636 | 0.7649 | 0.8835 |
| ELECTRA-base | 0.7637 | 0.7635 | 0.8820 |
| BERT-base | 0.7597 | 0.7610 | 0.8820 |
| DistilBERT-base | 0.7541 | 0.7556 | 0.8793 |
| ALBERT-base | 0.7509 | 0.7522 | 0.8737 |

DeBERTa-v3-base led the benchmark. The seven models remained within a relatively narrow performance band, and the compact DistilBERT model finished only 0.0169 Macro-F1 behind the leader.

## Conclusions

1. Leakage-aware evaluation matters: raw and brand-masked scores answer different questions.
2. Class weights are better suited than synthetic oversampling to sparse TF-IDF representations in this experiment.
3. Larger architectures do not automatically perform better; BERT-large did not surpass DeBERTa-v3-base.
4. A stronger follow-up would repeat the Transformer benchmark on masked text, remove near-duplicate reviews across splits, and report repeated-seed confidence intervals.

## Reproducibility scope

This archive includes the data preparation notebook, classical models, Transformer training scripts, shared evaluation pipeline, consolidated report, and final metrics. Raw reviews, model weights, verbose logs, original course reports, and identity-bearing metadata are intentionally excluded.
