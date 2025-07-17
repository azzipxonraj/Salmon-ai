# Salmon-ai


---

## How to Run

### 1. Prepare Datasets

Place `labeled_MMA_data.csv` in the project root.

Then run all cells in:

```bash
DataPreparation.ipynb
```

This will generate all required CSVs for model training.

---

### 2. Train & Evaluate Models

To run all experiments:

```bash
python run_all_experiments.py
```

This script applies multiple models on all datasets and saves results to `ml_experiment_results.csv`.

---

### 3. Visualize Evaluation

To visualize the evaluation results (F1, Accuracy):

```bash
EvaluationResultsVisualization.ipynb
```

This will generate comparison plots and LaTeX-style tables for reporting.


## 📊 Metric Comparison Table

![Metric Comparison Table 1](table1_accuracy_f1.png)
![Metric Comparison Table 2](table2_auc_precision_recall.png)


## 🔍 XGBoost Confusion Matrices

![XGBoost - Primary Columns Impute Missing](xgboost_primary_columns_impute_missing_confmat.png)
![XGBoost - Drop Missing](xgboost_primary_columns_drop_missing_confmat.png)
![XGBoost - MICE <10](xgboost_mice_with_columns_missing_lt_10_confmat.png)

## 🧠 XGBoost Feature Importances

![XGBoost - Feature Importance Impute](xgboost_primary_columns_impute_missing_feature_importance.png)
![XGBoost - Feature Importance MICE <65](xgboost_mice_with_columns_missing_lt_65_feature_importance.png)

## 🔍 HistGB Confusion Matrices

![HistGB - Impute](histgb_primary_columns_impute_missing_confmat.png)
![HistGB - Drop Missing](histgb_primary_columns_drop_missing_confmat.png)
