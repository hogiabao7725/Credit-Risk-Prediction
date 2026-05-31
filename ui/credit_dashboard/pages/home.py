import pandas as pd
import streamlit as st

from ui.credit_dashboard.charts import default_count_chart, target_ratio_chart
from ui.credit_dashboard.components import insight, metric_card, page_hero, section_header, story_card, workflow_step
from ui.credit_dashboard.config import TARGET_COL
from ui.credit_dashboard.data import load_raw_data, prepare_clean_data


def render_home_page() -> None:
    df = load_raw_data()
    clean_df, metadata = prepare_clean_data(df)

    page_hero(
        "Machine Learning Presentation",
        "Credit Risk Prediction",
        "A clean dashboard for explaining the UCI credit card default project: data quality, EDA, "
        "feature engineering, model comparison, and a customer-level prediction demo.",
        "Dataset: Default of Credit Card Clients | Target: default.payment.next.month",
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Raw rows", f"{metadata.original_shape[0]:,}", "Original UCI dataset")
    with c2:
        metric_card("Features", f"{metadata.cleaned_shape[1] - 1:,}", "After feature engineering")
    with c3:
        metric_card("Default rate", f"{clean_df[TARGET_COL].mean() * 100:.2f}%", "Target = 1")
    with c4:
        metric_card("Duplicates removed", f"{metadata.duplicate_rows_removed:,}", "Cleaned before modeling")

    section_header("Project Story", "Use this page as the opening slide before moving into EDA and modeling.")
    s1, s2, s3 = st.columns(3)
    with s1:
        story_card(
            "Business question",
            "Can previous payment behavior help identify customers who may default next month?",
            "blue",
        )
    with s2:
        story_card(
            "Modeling challenge",
            "The default class is much smaller, so a high Accuracy score can still miss risky customers.",
            "amber",
        )
    with s3:
        story_card(
            "Evaluation focus",
            "Recall and F1-score are used to balance catching defaults with avoiding too many false alarms.",
            "green",
        )

    section_header("Workflow", "The dashboard follows the notebook in a presentation-friendly order.")
    w1, w2, w3, w4 = st.columns(4)
    with w1:
        workflow_step("01", "Audit", "Check shape, missing values, duplicates, categories, and target ratio.")
    with w2:
        workflow_step("02", "EDA", "Group charts by numerical, categorical, payment, and key predictor signals.")
    with w3:
        workflow_step("03", "Model", "Clean data, engineer behavior features, train five classification models.")
    with w4:
        workflow_step("04", "Demo", "Use the selected model to predict default probability for a customer.")

    left, right = st.columns([1.05, 1])
    with left:
        section_header("Target Balance", "The dataset is imbalanced, so accuracy is not enough.")
        st.plotly_chart(target_ratio_chart(df), width="stretch")
    with right:
        section_header("Class Count", "A default-catching model must be judged by Recall and F1.")
        st.plotly_chart(default_count_chart(df), width="stretch")

    insight(
        "About 22% of customers defaulted next month. A model can look accurate by predicting "
        "mostly non-defaults, so the dashboard prioritizes F1-score and Recall."
    )

    overview = []
    for col in df.columns:
        non_null = df[col].dropna()
        preview = sorted(non_null.unique().tolist()) if non_null.nunique() <= 12 else non_null.astype(str).unique()[:6].tolist()
        overview.append(
            {
                "column": col,
                "dtype": str(df[col].dtype),
                "missing": int(df[col].isna().sum()),
                "unique": int(non_null.nunique()),
                "examples": ", ".join(map(str, preview)),
            }
        )
    preview_tab, audit_tab = st.tabs(["Dataset preview", "Column audit"])
    with preview_tab:
        st.dataframe(df.head(12), width="stretch", hide_index=True)
    with audit_tab:
        st.dataframe(pd.DataFrame(overview), width="stretch", hide_index=True)
