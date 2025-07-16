import subprocess
import json
import pandas as pd

# List of dataset files
datasets = [
    "primary_columns_drop_missing.csv",
    "primary_columns_impute_missing.csv",
    "primary_columns_hb_mcv_crp_drop_missing.csv",
    "primary_columns_hb_mcv_crp_impute_missing.csv",
    "primary_secondary_columns_drop_missing.csv",
    "mice_with_columns_missing_lt_10.csv",
    "mice_with_columns_missing_lt_65.csv"
]

# List of models to evaluate
models = ["xgboost", "histgb"]

# Test IDs file
test_ids_path = "test_ids_20pct.csv"
results = []

for data in datasets:
    for model in models:
        print(f"▶ Running {model} on {data}...")
        result = subprocess.run(
            ["python", "ml_runner.py", "--data", data, "--test_ids", test_ids_path, "--model", model],
            capture_output=True, text=True
        )
        try:
            metrics_str = result.stdout
            metrics = json.loads(metrics_str)
            results.append(metrics)
        except Exception as e:
            print(f"⚠ Failed parsing result: {e}")

# Save to CSV
df_results = pd.DataFrame(results)
df_results.to_csv("ml_experiment_results.csv", index=False)
