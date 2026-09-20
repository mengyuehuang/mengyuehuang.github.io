# eval_pipeline.py

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
    top_k_accuracy_score,
)

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
)
from datasets import Dataset


def softmax(x, axis=-1):
    x = x - np.max(x, axis=axis, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x, axis=axis, keepdims=True)


def get_label_name(id2label, i: int):
    """
    id2label in HF config may use string keys ("0", "1", ...) or int keys.
    This helper makes it robust.
    """
    if not id2label:
        return str(i)
    keys = list(id2label.keys())
    if isinstance(keys[0], str):
        return id2label.get(str(i), str(i))
    else:
        return id2label.get(i, str(i))

def load_and_prepare_eval_data(train_path: str, test_path: str, label2id: dict):
    """
    Load train & test CSVs, map appName -> labels using label2id
    from the *model config*, to guarantee consistency with training.
    """
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    train_df = train_df[["content", "appName"]].dropna()
    test_df = test_df[["content", "appName"]].dropna()

    train_df["labels"] = train_df["appName"].map(label2id)
    test_df["labels"] = test_df["appName"].map(label2id)

    if train_df["labels"].isna().any():
        unknown = sorted(
            train_df.loc[train_df["labels"].isna(), "appName"].unique().tolist()
        )
        raise ValueError(
            f"Train set contains labels not found in model label2id mapping: {unknown}"
        )

    if test_df["labels"].isna().any():
        unknown = sorted(
            test_df.loc[test_df["labels"].isna(), "appName"].unique().tolist()
        )
        raise ValueError(
            f"Test set contains labels not found in model label2id mapping: {unknown}"
        )

    return train_df, test_df


def make_tokenized_eval_datasets(train_df, test_df, tokenizer, max_length: int = 128):
    """
    For evaluation we build a fresh val split from the training data
    and keep the full test set for final metrics.
    """
    train_df, val_df = train_test_split(
        train_df,
        test_size=0.1,
        random_state=42,
        stratify=train_df["labels"],
    )

    train_dataset = Dataset.from_pandas(train_df, preserve_index=False)
    val_dataset = Dataset.from_pandas(val_df, preserve_index=False)
    test_dataset = Dataset.from_pandas(test_df, preserve_index=False)

    def tokenize_function(examples):
        return tokenizer(
            examples["content"],
            padding="max_length",
            truncation=True,
            max_length=max_length,
        )

    remove_cols = ["content", "appName"]

    tokenized_train = train_dataset.map(
        tokenize_function, batched=True, remove_columns=remove_cols
    )
    tokenized_val = val_dataset.map(
        tokenize_function, batched=True, remove_columns=remove_cols
    )
    tokenized_test = test_dataset.map(
        tokenize_function, batched=True, remove_columns=remove_cols
    )

    return tokenized_train, tokenized_val, tokenized_test

def trainer_compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1_macro": f1_score(labels, preds, average="macro"),
    }

def evaluate_model(
    model_path: str,
    tokenizer_name: str = None,
    train_path: str = "new_data/train.csv",
    test_path: str = "new_data/test.csv",
    max_length: int = 128,
):
    """
    Universal evaluation pipeline for shopping app review classifiers.

    Arguments:
        model_path: directory of a saved HF model (from any training script).
        tokenizer_name: HF checkpoint name for tokenizer. If None, loads tokenizer
                        from model_path.
        train_path: CSV with 'content' and 'appName' (used for val split).
        test_path: CSV with 'content' and 'appName' (final test evaluation).
        max_length: max sequence length for tokenization.

    Prints:
        - Overall metrics (accuracy, macro/micro/weighted F1) for val + test
        - Per-class precision/recall/F1
        - Confusion matrix
        - Top-2 accuracy
        - Most confused app pairs

    Returns:
        dict with key metrics + confusion matrix.
    """
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    print(f"\n[Eval] Using model from: {model_path}\n")
    config = model.config

    label2id = config.label2id
    id2label = config.id2label
    num_labels = config.num_labels
    class_ids = list(range(num_labels))

    if tokenizer_name is None:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
    else:
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    train_df, test_df = load_and_prepare_eval_data(train_path, test_path, label2id)
    _, tokenized_val, tokenized_test = make_tokenized_eval_datasets(
        train_df, test_df, tokenizer, max_length=max_length
    )

    eval_args = TrainingArguments(
        output_dir="./tmp_eval",
        per_device_eval_batch_size=32,
        do_train=False,
        do_eval=True,
        logging_steps=50,
    )

    trainer = Trainer(
        model=model,
        args=eval_args,
        eval_dataset=tokenized_val,
        tokenizer=tokenizer,
        compute_metrics=trainer_compute_metrics,
    )

    print("\n================ VALIDATION SET EVALUATION ================")
    val_output = trainer.predict(tokenized_val)
    val_logits = val_output.predictions
    val_labels = val_output.label_ids
    val_preds = np.argmax(val_logits, axis=-1)

    val_acc = accuracy_score(val_labels, val_preds)
    val_f1_macro = f1_score(val_labels, val_preds, average="macro")
    val_f1_micro = f1_score(val_labels, val_preds, average="micro")
    val_f1_weighted = f1_score(val_labels, val_preds, average="weighted")

    print(f"Validation Accuracy:       {val_acc:.4f}")
    print(f"Validation F1 (macro):     {val_f1_macro:.4f}")
    print(f"Validation F1 (micro):     {val_f1_micro:.4f}")
    print(f"Validation F1 (weighted):  {val_f1_weighted:.4f}")

    label_names = [get_label_name(id2label, i) for i in class_ids]
    print("\nValidation per-class metrics:")
    print(
        classification_report(
            val_labels,
            val_preds,
            target_names=label_names,
        )
    )
    print("\n=================== TEST SET EVALUATION ===================")
    test_output = trainer.predict(tokenized_test)
    test_logits = test_output.predictions
    test_labels = test_output.label_ids
    test_preds = np.argmax(test_logits, axis=-1)

    test_acc = accuracy_score(test_labels, test_preds)
    test_f1_macro = f1_score(test_labels, test_preds, average="macro")
    test_f1_micro = f1_score(test_labels, test_preds, average="micro")
    test_f1_weighted = f1_score(test_labels, test_preds, average="weighted")

    print(f"Test Accuracy:             {test_acc:.4f}")
    print(f"Test F1 (macro):           {test_f1_macro:.4f}")
    print(f"Test F1 (micro):           {test_f1_micro:.4f}")
    print(f"Test F1 (weighted):        {test_f1_weighted:.4f}")

    print("\nTest per-class metrics:")
    print(
        classification_report(
            test_labels,
            test_preds,
            target_names=label_names,
        )
    )

    print("\n==================== CONFUSION MATRIX =====================")
    cm = confusion_matrix(test_labels, test_preds, labels=class_ids)
    cm_df = pd.DataFrame(
        cm,
        index=[f"true_{name}" for name in label_names],
        columns=[f"pred_{name}" for name in label_names],
    )
    print(cm_df)

    print("\n==================== TOP-2 ACCURACY =======================")
    probs = softmax(test_logits, axis=-1)
    top2_acc = top_k_accuracy_score(test_labels, probs, k=2, labels=class_ids)
    print(f"Top-2 Accuracy:            {top2_acc:.4f}")
    print("\n============= MOST CONFUSED APP PAIRS (TEST) ==============")
    cm_no_diag = cm.copy()
    np.fill_diagonal(cm_no_diag, 0)

    num_pairs = min(10, cm_no_diag.size)
    flat_indices = np.argsort(cm_no_diag, axis=None)[::-1][:num_pairs]

    print("Format: true_app -> pred_app : count")
    for idx in flat_indices:
        count = cm_no_diag.flat[idx]
        if count == 0:
            break
        i = idx // num_labels
        j = idx % num_labels
        true_app = label_names[i]
        pred_app = label_names[j]
        print(f"{true_app} -> {pred_app} : {count}")

    return {
        "val": {
            "accuracy": val_acc,
            "f1_macro": val_f1_macro,
            "f1_micro": val_f1_micro,
            "f1_weighted": val_f1_weighted,
        },
        "test": {
            "accuracy": test_acc,
            "f1_macro": test_f1_macro,
            "f1_micro": test_f1_micro,
            "f1_weighted": test_f1_weighted,
            "top2_accuracy": top2_acc,
        },
        "confusion_matrix": cm,
    }


if __name__ == "__main__":
    import argparse
    import os
    import sys
    from pathlib import Path

    class Tee:
        """Write to both console and a file."""
        def __init__(self, *streams):
            self.streams = streams

        def write(self, data):
            for s in self.streams:
                s.write(data)
                s.flush()

        def flush(self):
            for s in self.streams:
                s.flush()

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", required=True, help="Path to saved HF model dir")
    parser.add_argument("--tokenizer_name", default=None)
    parser.add_argument("--train_path", default="new_data/train.csv")
    parser.add_argument("--test_path", default="new_data/test.csv")
    parser.add_argument("--max_length", type=int, default=128)

    # NEW: auto-save options
    parser.add_argument("--save_dir", default="eval", help="Directory to save eval txt")
    parser.add_argument("--save_name", default=None, help="Override output txt filename (optional)")
    args = parser.parse_args()

    model_dir_name = Path(args.model_path).name  # e.g. "bert-shopping-base"
    
    os.makedirs(args.save_dir, exist_ok=True)
    out_file = Path(args.save_dir) / (args.save_name or f"results_{model_dir_name}.txt")

    # Tee stdout/stderr to both console and file
    with open(out_file, "w", encoding="utf-8") as f:
        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout = Tee(old_out, f)
        sys.stderr = Tee(old_err, f)
        try:
            print(f"[EVAL] model_path = {args.model_path}")
            print(f"[EVAL] saving log to = {out_file}")

            metrics = evaluate_model(
                model_path=args.model_path,
                tokenizer_name=args.tokenizer_name,
                train_path=args.train_path,
                test_path=args.test_path,
                max_length=args.max_length,
            )

            print("\n[EVAL] Done. Key metrics:")
            print(metrics)
        finally:
            sys.stdout, sys.stderr = old_out, old_err

