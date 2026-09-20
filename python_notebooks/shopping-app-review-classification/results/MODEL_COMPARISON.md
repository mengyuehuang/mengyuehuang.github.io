# Transformer model comparison

Evaluation used the same held-out test split and a shared metric pipeline for all seven architectures.

| Model | Validation Accuracy | Validation Macro-F1 | Test Accuracy | Test Macro-F1 | Test Weighted-F1 | Top-2 Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| DeBERTa-v3-base | 0.7722 | 0.7740 | 0.7716 | 0.7725 | 0.7725 | 0.8893 |
| RoBERTa-base | 0.7660 | 0.7684 | 0.7682 | 0.7688 | 0.7686 | 0.8877 |
| BERT-large | 0.7639 | 0.7663 | 0.7636 | 0.7649 | 0.7641 | 0.8835 |
| ELECTRA-base | 0.7613 | 0.7636 | 0.7637 | 0.7635 | 0.7645 | 0.8820 |
| BERT-base | 0.7604 | 0.7631 | 0.7597 | 0.7610 | 0.7602 | 0.8820 |
| DistilBERT-base | 0.7531 | 0.7548 | 0.7541 | 0.7556 | 0.7548 | 0.8793 |
| ALBERT-base | 0.7482 | 0.7498 | 0.7509 | 0.7522 | 0.7516 | 0.8737 |

All machine-specific paths, execution logs, and contributor identifiers have been removed from this summary.
