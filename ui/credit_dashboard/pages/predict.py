import pandas as pd
import streamlit as st

from ui.credit_dashboard.charts import probability_gauge
from ui.credit_dashboard.components import insight, metric_card, page_hero, section_header, story_card
from ui.credit_dashboard.config import (
    BILL_COLS,
    EDUCATION_LABELS,
    MARRIAGE_LABELS,
    PAY_AMT_COLS,
    PAY_COLS,
    SEX_LABELS,
)
from ui.credit_dashboard.data import build_customer_frame, load_raw_data, prepare_clean_data
from ui.credit_dashboard.modeling import train_models


def _label_to_code(label_map: dict[int, str], selected: str) -> int:
    reverse = {v: k for k, v in label_map.items()}
    return reverse[selected]


def render_predict_page() -> None:
    df = load_raw_data()
    clean_df, metadata = prepare_clean_data(df)
    bundle = train_models(clean_df)
    artifact = bundle.artifacts[bundle.best_name]

    page_hero(
        "Prediction Demo",
        "Customer-level risk estimate",
        "Enter a customer profile, repayment status, bill amount, and payment amount. "
        "The selected model returns a default probability and a clear risk label for presentation.",
        f"Active model: {bundle.best_name}",
    )

    left, right = st.columns([1.1, 0.9])
    with left:
        profile_tab, payment_tab = st.tabs(["Profile", "Payment history"])
        with profile_tab:
            section_header("Customer Profile")
            c1, c2 = st.columns(2)
            with c1:
                limit_bal = st.number_input("Credit limit (NT$)", min_value=0, value=120000, step=10000)
                age = st.number_input("Age", min_value=18, max_value=90, value=35, step=1)
                sex = st.selectbox("Sex", list(SEX_LABELS.values()), index=1)
            with c2:
                education = st.selectbox("Education", list(EDUCATION_LABELS.values()), index=1)
                marriage = st.selectbox("Marriage", list(MARRIAGE_LABELS.values()), index=1)

        with payment_tab:
            section_header("Repayment Status", "Positive PAY values mean delayed payment.")
            pay_values = {}
            cols = st.columns(6)
            defaults = [0, 0, 0, 0, 0, 0]
            for idx, col in enumerate(PAY_COLS):
                with cols[idx]:
                    pay_values[col] = st.number_input(col, min_value=-2, max_value=8, value=defaults[idx], step=1)

            section_header("Bills And Payments")
            bill_values = {}
            pay_amt_values = {}
            bill_cols = st.columns(6)
            pay_cols = st.columns(6)
            for idx, col in enumerate(BILL_COLS):
                with bill_cols[idx]:
                    bill_values[col] = st.number_input(col, min_value=0, value=30000, step=5000)
            for idx, col in enumerate(PAY_AMT_COLS):
                with pay_cols[idx]:
                    pay_amt_values[col] = st.number_input(col, min_value=0, value=3000, step=1000)

    raw_values = {
        "LIMIT_BAL": float(limit_bal),
        "SEX": _label_to_code(SEX_LABELS, sex),
        "EDUCATION": _label_to_code(EDUCATION_LABELS, education),
        "MARRIAGE": _label_to_code(MARRIAGE_LABELS, marriage),
        "AGE": int(age),
        **pay_values,
        **{k: float(v) for k, v in bill_values.items()},
        **{k: float(v) for k, v in pay_amt_values.items()},
    }

    customer_X = build_customer_frame(raw_values, bundle.feature_columns, metadata)
    probability = float(artifact.pipeline.predict_proba(customer_X)[:, 1][0])
    prediction = int(probability >= 0.5)

    with right:
        section_header("Prediction Result")
        st.plotly_chart(probability_gauge(probability), width="stretch")
        c1, c2 = st.columns(2)
        with c1:
            metric_card("Default probability", f"{probability * 100:.2f}%")
        with c2:
            metric_card("Predicted label", "Default" if prediction else "No default", f"Best model: {bundle.best_name}")

        if probability >= 0.65:
            insight("High risk: the profile has repayment pressure similar to default customers in the training data.")
        elif probability >= 0.35:
            insight("Medium risk: threshold tuning would matter depending on whether the bank wants fewer misses or fewer false alarms.")
        else:
            insight("Lower risk: the profile looks closer to non-default customers under the current model.")

        r1, r2, r3 = st.columns(3)
        with r1:
            story_card("Low", "0-35%: closer to non-default profile.", "green")
        with r2:
            story_card("Medium", "35-65%: threshold decision matters.", "amber")
        with r3:
            story_card("High", "65-100%: review repayment pressure.", "blue")

        section_header("Engineered Customer Features")
        feature_view = customer_X[
            [
                "AVG_BILL",
                "AVG_PAY_AMT",
                "UTIL_RATIO",
                "PAY_TO_BILL_RATIO",
                "AVG_PAY_DELAY",
                "MAX_PAY_DELAY",
                "PAY_DELAY_VOLATILITY",
            ]
        ].T.reset_index()
        feature_view.columns = ["Feature", "Value"]
        st.dataframe(feature_view, width="stretch", hide_index=True)

    section_header("Sample Predictions From Test Set")
    sample_X = clean_df.drop(columns=["default.payment.next.month"]).head(8)
    sample_prob = artifact.pipeline.predict_proba(sample_X)[:, 1]
    sample_pred = (sample_prob >= 0.5).astype(int)
    sample_out = pd.DataFrame(
        {
            "pred_prob_default": sample_prob,
            "pred_label": sample_pred,
            "actual": clean_df["default.payment.next.month"].head(8).values,
        }
    )
    st.dataframe(sample_out.style.format({"pred_prob_default": "{:.4f}"}), width="stretch", hide_index=True)
