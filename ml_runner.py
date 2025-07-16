import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ML models
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import HistGradientBoostingClassifier


def load_data(file_path):
    return pd.read_csv(file_path)


def prepare_data(df, target_col="Classificatie_MMZ", id_col="Identifier", categorical_cols=None):
    y = df[target_col].astype("category").cat.codes
    X = df.drop(columns=[target_col, id_col])
    if categorical_cols:
        for col in categorical_cols:
            if col in X.columns:
                X[col] = X[col].astype("category")
    return X, y


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



def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    accuracy = report_dict["accuracy"]
    macro_f1 = report_dict["macro avg"]["f1-score"]
    weighted_f1 = report_dict["weighted avg"]["f1-score"]
    return {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1
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
    X, y = prepare_data(df, target_col=args.target, id_col=args.id_col, categorical_cols=args.categorical)

    X_train, X_test, y_train, y_test = split_data(X, y,
                                                  test_ids_file=args.test_ids,
                                                  df_full=df,
                                                  id_col=args.id_col,
                                                  test_size=args.test_size)

    model = get_model(args.model, num_class=y.nunique())
    model.fit(X_train, y_train)
    return {
    "dataset": args.data,
    "model": args.model,
    **evaluate_model(model, X_test, y_test)
    }


if __name__ == "__main__":
    import json
    print(json.dumps(main()))
