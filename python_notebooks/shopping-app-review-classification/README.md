# Shopping App Classification from User Reviews

This folder is a privacy-cleaned, portfolio-ready archive of an 11-class NLP project. It classifies the originating shopping app from review text using interpretable baselines, imbalance-aware models, and seven Transformer architectures.

The dataset contains 630,000 public reviews. A stratified 80/10/10 split produces 504,000 training, 63,000 development, and 63,000 held-out test examples. DeBERTa-v3-base achieved the strongest final result: 0.7725 test Macro-F1, 0.7716 accuracy, and 0.8893 Top-2 accuracy.

## Folder structure

- `data/prepare_splits.ipynb` — clean, portable data preparation notebook with no user metadata or machine-specific paths.
- `data/README.md` — dataset source, schema, and expected local layout.
- `classical/` — word-frequency, TF-IDF, brand-masking, SMOTE, Borderline-SMOTE, and class-weighted baselines.
- `transformers/` — training scripts for seven pretrained encoders plus the shared evaluation and result-collection pipelines.
- `results/MODEL_COMPARISON.md` — anonymized final leaderboard.
- `REPORT.md` — consolidated project report.

## Setup

Create a virtual environment, then install the dependencies:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Download the public dataset linked in `data/README.md`. Either run the notebook to create the splits or place prepared files at:

```text
new_data/train.csv
new_data/dev.csv
new_data/test.csv
```

Each CSV must include at least `content` and `appName`. The raw data and trained checkpoints are intentionally not committed because of their size.

## Example commands

Run the word-frequency baseline:

```bash
python classical/word_frequency_baseline.py new_data/train.csv new_data/test.csv predictions.csv --top-n 1000
python classical/score.py new_data/test.csv predictions.csv
```

Run the TF-IDF baseline:

```bash
python classical/tfidf_baseline.py new_data/train.csv new_data/test.csv predictions.csv
python classical/score.py new_data/test.csv predictions.csv
```

Train one Transformer model from the project root:

```bash
python transformers/deberta_v3_base.py
```

Evaluate a saved checkpoint:

```bash
python transformers/eval_pipeline.py --model_path models/deberta-v3-base --model_name deberta-v3-base
```

Transformer training is GPU-intensive. Model weights, raw logs, cached datasets, and per-machine output paths are excluded from this archive.

## Privacy note

Contributor names, email addresses, account identifiers, notebook authorship metadata, local absolute paths, and original reports containing identity information have been removed. The original working directory was not modified.
