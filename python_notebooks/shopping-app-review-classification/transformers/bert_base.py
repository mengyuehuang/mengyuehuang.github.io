# bert_base.py

import os
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
)
from datasets import Dataset

def load_and_prepare_data(train_path: str, test_path: str):
    """
    Load CSVs, keep required columns, drop missing,
    build label mappings from TRAIN ONLY, and map to numeric labels.
    """
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    train_df = train_df[["content", "appName"]].dropna()
    test_df = test_df[["content", "appName"]].dropna()

    label_list = sorted(train_df["appName"].unique().tolist())
    label2id = {label: i for i, label in enumerate(label_list)}
    id2label = {i: label for label, i in label2id.items()}

    train_df["labels"] = train_df["appName"].map(label2id)
    test_df["labels"] = test_df["appName"].map(label2id)

    if test_df["labels"].isna().any():
        unknown = sorted(
            test_df.loc[test_df["labels"].isna(), "appName"].unique().tolist()
        )
        raise ValueError(f"Test set contains unseen labels not in train: {unknown}")

    return train_df, test_df, label_list, label2id, id2label


def make_tokenized_datasets(train_df, test_df, tokenizer, max_length: int = 128):
    """
    Split train into train/val, convert to HF Datasets, and tokenize.
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


def train_shopping_app_model(
    model_name: str = "bert-base-uncased",
    train_path: str = "new_data/train.csv",
    test_path: str = "new_data/test.csv",
    output_dir: str = "models/bert-shopping-base",
    num_epochs: int = 3,
    max_length: int = 128,
):
    """
    Build + fine-tune a BERT (or other HF) model
    for shopping app review classification.

    Returns the directory where the model (and tokenizer) are saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    train_df, test_df, label_list, label2id, id2label = load_and_prepare_data(
        train_path, test_path
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenized_train, tokenized_val, tokenized_test = make_tokenized_datasets(
        train_df, test_df, tokenizer, max_length=max_length
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(label_list),
        id2label=id2label,
        label2id=label2id,
    )

    training_args = TrainingArguments(
        output_dir=os.path.join(output_dir, "results"),
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        fp16=False,  # MPS不支持fp16
        per_device_train_batch_size=32,
        per_device_eval_batch_size=32,
        num_train_epochs=num_epochs,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro",
        greater_is_better=True,
        logging_steps=50,
    )

    print("device:", training_args.device)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
        tokenizer=tokenizer,
        compute_metrics=trainer_compute_metrics,
    )

    trainer.train()

    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    print(f"\nTraining finished. Model saved to: {output_dir}")

    return output_dir


if __name__ == "__main__":
    model_dir = train_shopping_app_model()
    print(f"Model directory: {model_dir}")
