import os, numpy as np, pandas as pd, torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset

def load_data(train_path, test_path):
    train_df = pd.read_csv(train_path)[["content","appName"]].dropna()
    test_df  = pd.read_csv(test_path)[["content","appName"]].dropna()

    labels = sorted(train_df["appName"].unique().tolist())
    label2id = {l:i for i,l in enumerate(labels)}
    id2label = {i:l for l,i in label2id.items()}

    train_df["labels"] = train_df["appName"].map(label2id)
    test_df["labels"]  = test_df["appName"].map(label2id)

    if test_df["labels"].isna().any():
        bad = sorted(test_df.loc[test_df["labels"].isna(), "appName"].unique().tolist())
        raise ValueError(f"Unseen labels in test: {bad}")

    return train_df, labels, label2id, id2label

def tokenize_split(train_df, tokenizer, max_len=128):
    tr, va = train_test_split(train_df, test_size=0.1, random_state=42, stratify=train_df["labels"])
    tr_ds = Dataset.from_pandas(tr, preserve_index=False)
    va_ds = Dataset.from_pandas(va, preserve_index=False)

    def tok(b): 
        return tokenizer(b["content"], truncation=True, padding="max_length", max_length=max_len)

    remove_cols = ["content","appName"]
    return (
        tr_ds.map(tok, batched=True, remove_columns=remove_cols),
        va_ds.map(tok, batched=True, remove_columns=remove_cols),
    )

def metrics(eval_pred):
    logits, y = eval_pred
    p = np.argmax(logits, axis=-1)
    return {"accuracy": accuracy_score(y,p), "f1_macro": f1_score(y,p,average="macro")}

def main():
    model_name = "google/electra-base-discriminator"
    out_dir = "models/electra-base"
    os.makedirs(out_dir, exist_ok=True)

    train_df, label_list, label2id, id2label = load_data("new_data/train.csv", "new_data/test.csv")
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    train_tok, val_tok = tokenize_split(train_df, tokenizer, max_len=128)

    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=len(label_list), id2label=id2label, label2id=label2id
    )

    bf16_ok = torch.cuda.is_available() and torch.cuda.get_device_capability(0)[0] >= 8
    args = TrainingArguments(
        output_dir=os.path.join(out_dir, "results"),
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=32,
        per_device_eval_batch_size=64,
        num_train_epochs=3,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro",
        greater_is_better=True,
        fp16=False,  # MPS不支持fp16/bf16
        dataloader_num_workers=4,
        dataloader_pin_memory=True,
        logging_steps=200,
        report_to="none",
    )

    print("device:", args.device)

    trainer = Trainer(model=model, args=args, train_dataset=train_tok, eval_dataset=val_tok,
                      tokenizer=tokenizer, compute_metrics=metrics)
    print("Device:", args.device, "| bf16:", args.bf16, "| fp16:", args.fp16)
    trainer.train()
    trainer.save_model(out_dir); tokenizer.save_pretrained(out_dir)
    print("Saved:", out_dir)

if __name__ == "__main__":
    main()
