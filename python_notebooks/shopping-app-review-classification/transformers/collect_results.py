#!/usr/bin/env python3
"""
Evaluate all saved models under milestone4/models and produce a comparison summary.

Repo layout assumed:
milestone4/
  collect_results.py
  eval_pipeline.py          (must expose evaluate_model(...))
  new_data/
    train.csv
    test.csv
    dev.csv (optional)
  models/
    <model_name>/
      config.json
      model.safetensors OR pytorch_model.bin
      (tokenizer files...)
  eval/                     (will be created)
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Import evaluation function from your existing pipeline
# (eval_pipeline.py should be in the same folder as this script)
from eval_pipeline import evaluate_model


def pick_data_files(base_dir: Path) -> Dict[str, Optional[Path]]:
    """
    Find dataset files under milestone4/new_data.

    Returns:
        {"train": Path, "test": Path, "dev": Optional[Path]}
    """
    new_data = base_dir / "new_data"
    train_path = new_data / "train.csv"
    test_path = new_data / "test.csv"
    dev_path = new_data / "dev.csv"

    if not train_path.exists():
        raise FileNotFoundError(f"Missing required file: {train_path}")
    if not test_path.exists():
        raise FileNotFoundError(f"Missing required file: {test_path}")

    return {
        "train": train_path,
        "test": test_path,
        "dev": dev_path if dev_path.exists() else None,
    }


def is_hf_model_dir(p: Path) -> bool:
    """
    Heuristic: a Hugging Face saved model folder usually has:
      - config.json
      - model.safetensors OR pytorch_model.bin
    """
    if not p.is_dir():
        return False
    config_ok = (p / "config.json").exists()
    weights_ok = (p / "model.safetensors").exists() or (p / "pytorch_model.bin").exists()
    return config_ok and weights_ok


def safe_get(d: Dict[str, Any], *keys: str, default=None):
    cur: Any = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def fmt(x: Optional[float]) -> str:
    return "-" if x is None else f"{x:.4f}"


def pretty_text_dump(obj: Any, indent: int = 0) -> list[str]:
    """
    Recursively format nested dicts/lists into readable plain text.
    This avoids JSON serialization issues (ndarray, tensors, etc.).
    """
    lines: list[str] = []
    pad = "  " * indent

    if isinstance(obj, dict):
        for k, v in obj.items():
            lines.append(f"{pad}{k}:")
            lines.extend(pretty_text_dump(v, indent + 1))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            lines.append(f"{pad}- [{i}]")
            lines.extend(pretty_text_dump(v, indent + 1))
    else:
        try:
            lines.append(f"{pad}{obj}")
        except Exception:
            lines.append(f"{pad}{repr(obj)}")

    return lines


def main():
    base_dir = Path(__file__).resolve().parent  # milestone4/
    models_dir = base_dir / "models"
    out_dir = base_dir / "eval"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Locate data
    data = pick_data_files(base_dir)
    train_path = str(data["train"])
    test_path = str(data["test"])

    # model folders
    if not models_dir.exists():
        raise FileNotFoundError(f"Missing models folder: {models_dir}")

    model_folders = sorted([p for p in models_dir.iterdir() if is_hf_model_dir(p)])

    results: Dict[str, Any] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "base_dir": str(base_dir),
        "data_paths": {
            "train": train_path,
            "test": test_path,
            "dev": str(data["dev"]) if data["dev"] else None,
        },
        "models_dir": str(models_dir),
        "models": {},
    }

    print("=== Data ===")
    print("train:", train_path)
    print("test :", test_path)
    if data["dev"]:
        print("dev  :", data["dev"])
    print()

    if not model_folders:
        print(f"No valid HF model folders found under: {models_dir}")
        print("Expected each model folder to contain config.json and model weights.")
        return

    print("=== Models discovered ===")
    for p in model_folders:
        print("-", p.name)
    print()

    # Evaluate each model
    for model_dir in model_folders:
        model_name = model_dir.name
        print("=" * 70)
        print(f"Evaluating: {model_name}")
        print("=" * 70)

        try:
            metrics = evaluate_model(
                model_path=str(model_dir),
                tokenizer_name=None,
                train_path=train_path,
                test_path=test_path,
                max_length=128,
            )

            results["models"][model_name] = {
                "status": "success",
                "model_path": str(model_dir),
                "metrics": metrics,
            }

            test_f1 = safe_get(metrics, "test", "f1_macro", default=None)
            print(f"✓ Done: {model_name} | test f1_macro={test_f1}")

        except Exception as e:
            results["models"][model_name] = {
                "status": "failed",
                "model_path": str(model_dir),
                "error": str(e),
            }
            print(f"✗ Failed: {model_name}\n  Error: {e}")

    # --------------------------
    # Save TXT (safe for anything)
    # --------------------------
    txt_path = out_dir / "all_model_metrics.txt"
    text_lines = [
        "ALL MODEL EVALUATION RESULTS",
        "=" * 80,
        f"Generated at: {results['generated_at']}",
        f"Train: {results['data_paths']['train']}",
        f"Test : {results['data_paths']['test']}",
        f"Dev  : {results['data_paths']['dev']}",
        f"Models dir: {results['models_dir']}",
        "",
    ]
    text_lines.extend(pretty_text_dump(results))
    txt_path.write_text("\n".join(text_lines), encoding="utf-8")
    print(f"\nSaved TXT results: {txt_path}")

    # --------------------------
    # Build Markdown leaderboard
    # --------------------------
    rows = []
    for name, rec in results["models"].items():
        if rec.get("status") != "success":
            rows.append({
                "name": name,
                "status": "failed",
                "val_acc": None, "val_f1": None,
                "test_acc": None, "test_f1_macro": None, "test_f1_weighted": None,
                "top2": None,
            })
            continue

        m = rec["metrics"]
        rows.append({
            "name": name,
            "status": "ok",
            "val_acc": safe_get(m, "val", "accuracy"),
            "val_f1": safe_get(m, "val", "f1_macro"),
            "test_acc": safe_get(m, "test", "accuracy"),
            "test_f1_macro": safe_get(m, "test", "f1_macro"),
            "test_f1_weighted": safe_get(m, "test", "f1_weighted"),
            "top2": safe_get(m, "test", "top2_accuracy", default=0.0),
        })

    # Sort by test macro-F1 descending; failures last
    rows.sort(key=lambda r: (r["test_f1_macro"] is None, -(r["test_f1_macro"] or 0.0)))

    md_lines = []
    md_lines.append("# Model Comparison Summary (Milestone 4)")
    md_lines.append("")
    md_lines.append(f"- Generated at: `{results['generated_at']}`")
    md_lines.append(f"- Train: `{results['data_paths']['train']}`")
    md_lines.append(f"- Test: `{results['data_paths']['test']}`")
    md_lines.append("")
    md_lines.append("## Leaderboard (sorted by Test F1-macro)")
    md_lines.append("")
    md_lines.append("| Model | Val Acc | Val F1(macro) | Test Acc | Test F1(macro) | Test F1(weighted) | Top-2 Acc | Status |")
    md_lines.append("|---|---:|---:|---:|---:|---:|---:|---|")

    for r in rows:
        md_lines.append(
            f"| {r['name']} | {fmt(r['val_acc'])} | {fmt(r['val_f1'])} | {fmt(r['test_acc'])} | "
            f"{fmt(r['test_f1_macro'])} | {fmt(r['test_f1_weighted'])} | {fmt(r['top2'])} | {r['status']} |"
        )

    md_lines.append("")
    md_lines.append("## Notes")
    md_lines.append("- Models are auto-discovered from `milestone4/models/*`.")
    md_lines.append("- A folder is considered a model if it contains `config.json` and weights.")
    md_lines.append("- Detailed per-model outputs (including any confusion matrices printed by eval_pipeline) are in the TXT file.")
    md_lines.append("")

    md_path = out_dir / "MODEL_COMPARISON.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Saved report: {md_path}")

    # Console top-5
    top_ok = [r for r in rows if r["status"] == "ok"]
    if top_ok:
        print("\n=== Top models (by test f1_macro) ===")
        for i, r in enumerate(top_ok[:5], 1):
            print(f"{i}. {r['name']}  f1_macro={r['test_f1_macro']:.4f}  acc={r['test_acc']:.4f}")


if __name__ == "__main__":
    main()
