import pandas as pd
import streamlit as st

from ui.credit_dashboard.charts import (
    AMBER,
    BLUE,
    GREEN,
    box_chart,
    category_rate_chart,
    class_amount_chart,
    correlation_heatmap,
    late_payment_chart,
    median_trend_chart,
    pay_status_default_chart,
    default_count_chart,
    target_ratio_chart,
)
from ui.credit_dashboard.components import insight, page_hero, section_header, story_card
from ui.credit_dashboard.config import BILL_COLS, PAY_AMT_COLS, TARGET_COL
from ui.credit_dashboard.data import load_raw_data


def render_eda_page() -> None:
    df = load_raw_data()

    page_hero(
        "Exploratory Data Analysis",
        "Find the strongest risk signals",
        "EDA is split into small groups so the presentation can move from data quality to customer profile, "
        "payment behavior, and final predictor evidence.",
        "Subpages: audit, numerical, categorical, payment, key predictors",
    )

    audit_tab, numerical_tab, categorical_tab, payment_tab, predictor_tab = st.tabs(
        ["Audit & target", "Numerical", "Categorical", "Payment behavior", "Key predictors"]
    )

    with audit_tab:
        section_header("Data Quality And Target", "Start with whether the dataset is usable and how hard the target is.")
        c1, c2, c3 = st.columns(3)
        with c1:
            story_card("Missing values", f"{int(df.isna().sum().sum()):,} total missing values.", "green")
        with c2:
            duplicate_count = int(df.duplicated().sum())
            story_card("Duplicate rows", f"{duplicate_count:,} duplicate rows are removed before modeling.", "amber")
        with c3:
            story_card("Class imbalance", f"{df[TARGET_COL].mean() * 100:.2f}% customers default next month.", "blue")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(target_ratio_chart(df), width="stretch")
        with c2:
            st.plotly_chart(default_count_chart(df), width="stretch")
        insight("This is why the model comparison does not rely on Accuracy alone.")

    with numerical_tab:
        section_header("Numerical Variables", "AGE and LIMIT_BAL are checked first, then compared with payment signals.")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(box_chart(df, "AGE", "Age distribution by default status"), width="stretch")
        with c2:
            st.plotly_chart(box_chart(df, "LIMIT_BAL", "Credit limit by default status"), width="stretch")
        st.plotly_chart(correlation_heatmap(df), width="stretch")
        insight("PAY_0, PAY_2, and PAY_3 show stronger default relationship than basic profile variables.")

    with categorical_tab:
        section_header("Categorical Variables", "These columns are labels, so the numbers are treated as categories.")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.plotly_chart(category_rate_chart(df, "SEX", "Default rate by SEX", BLUE), width="stretch")
        with c2:
            st.plotly_chart(category_rate_chart(df, "EDUCATION", "Default rate by EDUCATION", GREEN), width="stretch")
        with c3:
            st.plotly_chart(category_rate_chart(df, "MARRIAGE", "Default rate by MARRIAGE", AMBER), width="stretch")

        gap_summary = pd.DataFrame(
            {
                "Group": ["SEX", "EDUCATION", "MARRIAGE"],
                "Default rate gap (%)": [
                    (df.groupby("SEX")[TARGET_COL].mean().max() - df.groupby("SEX")[TARGET_COL].mean().min()) * 100,
                    (df.groupby("EDUCATION")[TARGET_COL].mean().max() - df.groupby("EDUCATION")[TARGET_COL].mean().min()) * 100,
                    (df.groupby("MARRIAGE")[TARGET_COL].mean().max() - df.groupby("MARRIAGE")[TARGET_COL].mean().min()) * 100,
                ],
            }
        )
        st.dataframe(gap_summary, width="stretch", hide_index=True)

    with payment_tab:
        section_header("Payment Behavior", "The most important risk story: delay, bill pressure, and repayment amount.")
        st.plotly_chart(late_payment_chart(df), width="stretch")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(class_amount_chart(df, BILL_COLS, "Average BILL_AMT by class"), width="stretch")
        with c2:
            st.plotly_chart(class_amount_chart(df, PAY_AMT_COLS, "Average PAY_AMT by class"), width="stretch")
        insight("If bill amounts stay high while payments stay low, repayment pressure may increase.")

    with predictor_tab:
        section_header("Key Predictor Summary", "These charts connect EDA directly to feature engineering.")
        st.plotly_chart(pay_status_default_chart(df), width="stretch")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(median_trend_chart(df, BILL_COLS, "Median BILL_AMT trend by class"), width="stretch")
        with c2:
            st.plotly_chart(median_trend_chart(df, PAY_AMT_COLS, "Median PAY_AMT trend by class"), width="stretch")

        insight(
            "Higher PAY_* status usually means higher default risk. This supports AVG_BILL, AVG_PAY_AMT, "
            "UTIL_RATIO, PAY_TO_BILL_RATIO, AVG_PAY_DELAY, MAX_PAY_DELAY, and PAY_DELAY_VOLATILITY."
        )
