import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, roc_auc_score, average_precision_score,
    precision_score, recall_score, confusion_matrix, ConfusionMatrixDisplay
)
from sklearn.preprocessing import label_binarize

# ML models
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
import seaborn as sns


def load_data(file_path):
    return pd.read_csv(file_path)


def prepare_data(df, target_col="Classificatie_MMZ", id_col="Identifier", categorical_cols=None):
    y = df[target_col].astype("category")
    y_encoded = y.cat.codes
    X = df.drop(columns=[target_col, id_col])
    if categorical_cols:
        for col in categorical_cols:
            if col in X.columns:
                X[col] = X[col].astype("category")
    return X, y_encoded, y


def split_data(X, y, test_ids_file=None, df_full=None, id_col="Identifier", test_size=0.2, random_state=42):
    if test_ids_file and df_full is not None:
        test_ids = pd.read_csv(test_ids_file)["Identifier"]
        is_test = df_full[id_col].isin(test_ids)
        return X[~is_test], X[is_test], y[~is_test], y[is_test]
    else:
        return train_test_split(X, y, stratify=y, test_size=test_size, random_state=random_state)


def get_model(name, num_class):
    name = name.lower()
    if name == "xgboost":
        return XGBClassifier(
            objective="multi:softprob",
            num_class=num_class,
            eval_metric="mlogloss",
            enable_categorical=True
        )
    elif name == "lightgbm":
        return LGBMClassifier(objective="multiclass", num_class=num_class)
    elif name == "catboost":
        return CatBoostClassifier(loss_function="MultiClass", verbose=False)
    elif name == "histgb":
        return HistGradientBoostingClassifier()
    else:
        raise ValueError(f"Unsupported model: {name}")



def evaluate_model(model, X_test, y_test, y_labels, model_name, dataset_name):
    # Get predictions and probabilities
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)

    # Classification report
    report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    accuracy = report_dict["accuracy"]
    macro_f1 = report_dict["macro avg"]["f1-score"]
    weighted_f1 = report_dict["weighted avg"]["f1-score"]
    macro_precision = report_dict["macro avg"]["precision"]
    macro_recall = report_dict["macro avg"]["recall"]

    # AUC/PR-AUC: Binarize y_test using full label space
    all_classes = np.arange(len(y_labels.cat.categories))
    y_test_bin = label_binarize(y_test, classes=all_classes)

    # Align predicted probabilities
    if y_proba.shape[1] != y_test_bin.shape[1]:
        padded_proba = np.zeros_like(y_test_bin, dtype=float)
        for i, cls in enumerate(model.classes_):
            padded_proba[:, cls] = y_proba[:, i]
        y_proba = padded_proba

    # Compute AUC and PR-AUC
    macro_auc = roc_auc_score(y_test_bin, y_proba, average="macro", multi_class="ovr")
    macro_pr_auc = average_precision_score(y_test_bin, y_proba, average="macro")

    # Confusion matrix plot
    cm = confusion_matrix(y_test, y_pred, labels=all_classes)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=all_classes, yticklabels=all_classes)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title(f"Confusion Matrix: {model_name} on {dataset_name}")
    plt.tight_layout()
    cm_filename = f"{model_name}_{dataset_name}_confmat.png".replace(".csv", "")
    plt.savefig(cm_filename, dpi=300)
    plt.close()

    return {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "macro_auc": macro_auc,
        "macro_pr_auc": macro_pr_auc,
        "confusion_matrix_image": cm_filename,
        "macro_recall": macro_recall,
        "macro_precision": macro_precision,
    }


def main():
    parser = argparse.ArgumentParser(description="Train a tabular classifier on MMA data")
    parser.add_argument("--data", type=str, default="primary_columns_impute_missing.csv", help="Path to input CSV")
    parser.add_argument("--test_ids", type=str, default="test_ids_20pct.csv", help="Path to test ID CSV")
    parser.add_argument("--model", type=str, default="xgboost", help="Model: xgboost, lightgbm, catboost, histgb")
    parser.add_argument("--target", type=str, default="Classificatie_MMZ", help="Target column")
    parser.add_argument("--id_col", type=str, default="Identifier", help="Unique ID column")
    parser.add_argument("--categorical", nargs="*", default=["Sex", "Kidney_problem", "Vitamin_B12_Problem_Label", "Anemie"],
                        help="Categorical columns")
    parser.add_argument("--test_size", type=float, default=0.2, help="Test size if not using test_ids")
    args = parser.parse_args()

    df = load_data(args.data)
    # Remove rare classes with <10 samples
    target_counts = df[args.target].value_counts()
    valid_classes = target_counts[target_counts >= 10].index
    df = df[df[args.target].isin(valid_classes)]


    X, y, y_labels = prepare_data(df, target_col=args.target, id_col=args.id_col, categorical_cols=args.categorical)
    X_train, X_test, y_train, y_test = split_data(X, y,
                                                  test_ids_file=args.test_ids,
                                                  df_full=df,
                                                  id_col=args.id_col,
                                                  test_size=args.test_size)

    model = get_model(args.model, num_class=y.nunique())
    model.fit(X_train, y_train)

    # Save feature importance
    try:
        importances = model.feature_importances_
        pd.Series(importances, index=X_train.columns).sort_values().plot(kind="barh", figsize=(8, 6))
        plt.title("Feature Importances")
        plt.tight_layout()
        plt.savefig(f"{args.model}_{args.data.rstrip('.csv')}_feature_importance.png", dpi=300)
        plt.close()
    except AttributeError:
        pass  # model may not support .feature_importances_

    return {
        "dataset": args.data,
        "model": args.model,
        **evaluate_model(model, X_test, y_test, y_labels, args.model, args.data.rstrip(".csv"))
    }


if __name__ == "__main__":
    import json
    print(json.dumps(main(), indent=2))
