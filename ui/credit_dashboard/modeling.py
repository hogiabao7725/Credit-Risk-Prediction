from dataclasses import dataclass

import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from ui.credit_dashboard.config import RANDOM_STATE, TARGET_COL


@dataclass
class ModelArtifact:
    name: str
    pipeline: Pipeline
    y_test: pd.Series
    pred: pd.Series
    prob: pd.Series
    confusion: list[list[int]]


@dataclass
class TrainingBundle:
    results: pd.DataFrame
    artifacts: dict[str, ModelArtifact]
    best_name: str
    feature_columns: list[str]
    train_shape: tuple[int, int]
    test_shape: tuple[int, int]


def build_training_bundle(clean_df: pd.DataFrame) -> TrainingBundle:
    X = clean_df.drop(columns=[TARGET_COL])
    y = clean_df[TARGET_COL]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    num_cols = X_train.select_dtypes(include=["number"]).columns.tolist()
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                num_cols,
            )
        ]
    )
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    estimators = {
        "Logistic Regression": LogisticRegression(
            max_iter=2000, class_weight="balanced", random_state=RANDOM_STATE
        ),
        "KNN": KNeighborsClassifier(n_neighbors=15),
        "Naive Bayes": GaussianNB(),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=6, class_weight="balanced", random_state=RANDOM_STATE
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
    }

    rows = []
    artifacts: dict[str, ModelArtifact] = {}
    for name, estimator in estimators.items():
        pipe = Pipeline([("preprocessor", preprocessor), ("model", estimator)])
        cv_f1 = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="f1", n_jobs=1).mean()
        pipe.fit(X_train, y_train)
        pred = pd.Series(pipe.predict(X_test), index=y_test.index, name="pred")
        prob = pd.Series(pipe.predict_proba(X_test)[:, 1], index=y_test.index, name="prob")

        rows.append(
            {
                "Model": name,
                "Accuracy": accuracy_score(y_test, pred),
                "Precision": precision_score(y_test, pred),
                "Recall": recall_score(y_test, pred),
                "F1-score": f1_score(y_test, pred),
                "CV F1": cv_f1,
                "ROC-AUC": roc_auc_score(y_test, prob),
            }
        )
        artifacts[name] = ModelArtifact(
            name=name,
            pipeline=pipe,
            y_test=y_test,
            pred=pred,
            prob=prob,
            confusion=confusion_matrix(y_test, pred).tolist(),
        )

    results = pd.DataFrame(rows).sort_values("F1-score", ascending=False).reset_index(drop=True)
    best_name = str(results.iloc[0]["Model"])
    return TrainingBundle(
        results=results,
        artifacts=artifacts,
        best_name=best_name,
        feature_columns=X.columns.tolist(),
        train_shape=X_train.shape,
        test_shape=X_test.shape,
    )


@st.cache_resource(show_spinner="Training models from notebook pipeline...")
def train_models(clean_df: pd.DataFrame) -> TrainingBundle:
    return build_training_bundle(clean_df)
