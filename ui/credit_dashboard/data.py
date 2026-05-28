from dataclasses import dataclass

import numpy as np
import pandas as pd
import streamlit as st

from ui.credit_dashboard.config import (
    BILL_COLS,
    DATA_PATH,
    MONEY_COLS,
    PAY_AMT_COLS,
    PAY_COLS,
    TARGET_COL,
)


@dataclass(frozen=True)
class PreparationMetadata:
    duplicate_rows_removed: int
    high_skew_cols: tuple[str, ...]
    money_caps: dict[str, tuple[float, float]]
    original_shape: tuple[int, int]
    cleaned_shape: tuple[int, int]


@st.cache_data(show_spinner=False)
def load_raw_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    if "ID" in df.columns:
        df = df.drop(columns=["ID"])
    return df


def _add_behavior_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["AVG_BILL"] = out[BILL_COLS].mean(axis=1)
    out["AVG_PAY_AMT"] = out[PAY_AMT_COLS].mean(axis=1)
    out["UTIL_RATIO"] = out["AVG_BILL"] / out["LIMIT_BAL"].replace(0, np.nan)
    out["PAY_TO_BILL_RATIO"] = out["AVG_PAY_AMT"] / out["AVG_BILL"].replace(0, np.nan)
    out["AVG_PAY_DELAY"] = out[PAY_COLS].mean(axis=1)
    out["MAX_PAY_DELAY"] = out[PAY_COLS].max(axis=1)
    out["PAY_DELAY_VOLATILITY"] = out[PAY_COLS].std(axis=1)
    return out


@st.cache_data(show_spinner=False)
def prepare_clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, PreparationMetadata]:
    clean_df = df.copy()
    clean_df["EDUCATION"] = clean_df["EDUCATION"].replace({0: 4, 5: 4, 6: 4})
    clean_df["MARRIAGE"] = clean_df["MARRIAGE"].replace({0: 3})

    before_drop = clean_df.shape[0]
    clean_df = clean_df.drop_duplicates().reset_index(drop=True)

    money_caps: dict[str, tuple[float, float]] = {}
    for col in MONEY_COLS:
        lower = float(clean_df[col].quantile(0.01))
        upper = float(clean_df[col].quantile(0.99))
        money_caps[col] = (lower, upper)
        clean_df[col] = clean_df[col].clip(lower, upper)

    clean_df = _add_behavior_features(clean_df)

    skew_report = clean_df[MONEY_COLS].skew().sort_values(ascending=False)
    high_skew_cols = tuple(skew_report[skew_report > 1.5].index.tolist())
    for col in high_skew_cols:
        clean_df[f"LOG_{col}"] = np.log1p(clean_df[col].clip(lower=0))

    clean_df = clean_df.replace([np.inf, -np.inf], np.nan)
    metadata = PreparationMetadata(
        duplicate_rows_removed=before_drop - clean_df.shape[0],
        high_skew_cols=high_skew_cols,
        money_caps=money_caps,
        original_shape=df.shape,
        cleaned_shape=clean_df.shape,
    )
    return clean_df, metadata


def build_customer_frame(raw_values: dict, feature_columns: list[str], metadata: PreparationMetadata) -> pd.DataFrame:
    row = pd.DataFrame([raw_values])
    row["EDUCATION"] = row["EDUCATION"].replace({0: 4, 5: 4, 6: 4})
    row["MARRIAGE"] = row["MARRIAGE"].replace({0: 3})

    for col, (lower, upper) in metadata.money_caps.items():
        if col in row.columns:
            row[col] = row[col].clip(lower, upper)

    row = _add_behavior_features(row)
    for col in metadata.high_skew_cols:
        row[f"LOG_{col}"] = np.log1p(row[col].clip(lower=0))

    row = row.replace([np.inf, -np.inf], np.nan)
    return row.reindex(columns=feature_columns)
