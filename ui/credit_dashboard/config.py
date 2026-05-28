from pathlib import Path

RANDOM_STATE = 42
TARGET_COL = "default.payment.next.month"
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT_DIR / "UCI_Credit_Card.csv"

PAY_COLS = ["PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]
BILL_COLS = [f"BILL_AMT{i}" for i in range(1, 7)]
PAY_AMT_COLS = [f"PAY_AMT{i}" for i in range(1, 7)]
MONEY_COLS = ["LIMIT_BAL"] + BILL_COLS + PAY_AMT_COLS

SEX_LABELS = {1: "Male", 2: "Female"}
EDUCATION_LABELS = {
    1: "Graduate school",
    2: "University",
    3: "High school",
    4: "Other / unknown",
}
MARRIAGE_LABELS = {1: "Married", 2: "Single", 3: "Other / unknown"}

MODEL_EXPLANATIONS = {
    "Logistic Regression": "Balanced linear baseline, easy to explain.",
    "KNN": "Distance-based benchmark using similar customers.",
    "Naive Bayes": "Fast probabilistic baseline.",
    "Decision Tree": "Interpretable rule-based model with balanced classes.",
    "Random Forest": "Stronger tabular model using many balanced trees.",
}
