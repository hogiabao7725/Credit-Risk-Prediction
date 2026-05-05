# Credit Risk Prediction

A clear, student-friendly machine learning project for predicting credit default risk using the UCI credit card dataset.

## Project Goal

- Build a reproducible credit risk workflow.
- Focus on data understanding and preprocessing quality.
- Compare common classification models with imbalance-aware metrics.

## Dataset

- **Name:** Default of Credit Card Clients
- **Source:** [UCI Repository](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) (also available on Kaggle mirrors)
- **Size:** 30,000 rows, 24 columns
- **Target:** `default.payment.next.month` (`1` = default, `0` = non-default)

## Main Notebook

- `credit_risk_prediction.ipynb`

## Workflow in Notebook

1. Load data and review columns
2. Data quality audit (missing, duplicates, category checks, imbalance)
3. EDA (numerical, categorical, payment behavior)
4. Simple feature engineering for credit behavior
5. Train models one-by-one and print separate results
6. Compare models with `Accuracy`, `Precision`, `Recall`, `F1-score`, `ROC-AUC`
7. Final recommendation and practical risk note

## Quick Start

```bash
pip install -r requirements.txt
jupyter notebook
```

Then open `credit_risk_prediction.ipynb` and run cells from top to bottom.

## Notes

- Preprocessing is handled inside a pipeline to reduce leakage risk.
- Since the data is imbalanced, model selection should prioritize **F1-score** and **Recall**, not only Accuracy.
