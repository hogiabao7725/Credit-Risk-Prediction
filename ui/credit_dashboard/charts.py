import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ui.credit_dashboard.config import BILL_COLS, PAY_AMT_COLS, PAY_COLS, TARGET_COL

BLUE = "#2563EB"
GREEN = "#059669"
RED = "#DC2626"
AMBER = "#D97706"
INK = "#111827"


def _polish(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK),
        title=dict(font=dict(size=18), x=0.02, xanchor="left"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False, linecolor="#D0D7E2")
    fig.update_yaxes(gridcolor="#EEF2F7", linecolor="#D0D7E2")
    return fig


def target_ratio_chart(df: pd.DataFrame) -> go.Figure:
    counts = df[TARGET_COL].value_counts().sort_index()
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["No default", "Default"],
                values=counts.values,
                hole=0.58,
                marker={"colors": [GREEN, RED]},
                textinfo="percent+label",
            )
        ]
    )
    fig.update_layout(height=330, margin=dict(l=10, r=10, t=30, b=10), showlegend=False)
    return _polish(fig)


def default_count_chart(df: pd.DataFrame) -> go.Figure:
    counts = df[TARGET_COL].value_counts().sort_index().rename_axis("class").reset_index(name="count")
    counts["label"] = counts["class"].map({0: "No default", 1: "Default"})
    fig = px.bar(counts, x="label", y="count", color="label", color_discrete_sequence=[GREEN, RED])
    fig.update_layout(height=330, showlegend=False, margin=dict(l=10, r=10, t=30, b=10))
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Customers")
    return _polish(fig)


def box_chart(df: pd.DataFrame, y_col: str, title: str) -> go.Figure:
    plot_df = df.copy()
    plot_df["Default status"] = plot_df[TARGET_COL].map({0: "No default", 1: "Default"})
    fig = px.box(
        plot_df,
        x="Default status",
        y=y_col,
        color="Default status",
        color_discrete_sequence=[GREEN, RED],
        points=False,
        title=title,
    )
    fig.update_layout(height=380, showlegend=False, margin=dict(l=10, r=10, t=50, b=10))
    fig.update_xaxes(title="")
    return _polish(fig)


def correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    corr_cols = ["LIMIT_BAL", "AGE", "PAY_0", "PAY_2", "PAY_3", "BILL_AMT1", "PAY_AMT1", TARGET_COL]
    corr = df[[c for c in corr_cols if c in df.columns]].corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Correlation heatmap",
    )
    fig.update_layout(height=520, margin=dict(l=10, r=10, t=50, b=10))
    return _polish(fig)


def category_rate_chart(df: pd.DataFrame, col: str, title: str, color: str) -> go.Figure:
    rate = (df.groupby(col)[TARGET_COL].mean().sort_index() * 100).reset_index(name="Default rate")
    rate[col] = rate[col].astype(str)
    fig = px.bar(rate, x=col, y="Default rate", text="Default rate", title=title)
    fig.update_traces(marker_color=color, texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=50, b=10))
    fig.update_yaxes(title="Default rate (%)")
    return _polish(fig)


def late_payment_chart(df: pd.DataFrame) -> go.Figure:
    late_rate = ((df[PAY_COLS] > 0).mean().sort_index() * 100).reset_index()
    late_rate.columns = ["Month", "Late-payment rate"]
    fig = px.bar(late_rate, x="Month", y="Late-payment rate", text="Late-payment rate")
    fig.update_traces(marker_color=BLUE, texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=35, b=10))
    fig.update_yaxes(title="Rate (%)")
    return _polish(fig)


def class_amount_chart(df: pd.DataFrame, cols: list[str], title: str) -> go.Figure:
    compare = pd.DataFrame(
        {
            "No default": df[df[TARGET_COL] == 0][cols].mean(),
            "Default": df[df[TARGET_COL] == 1][cols].mean(),
        }
    ).reset_index(names="Feature")
    long_df = compare.melt(id_vars="Feature", var_name="Class", value_name="Average amount")
    fig = px.bar(
        long_df,
        x="Feature",
        y="Average amount",
        color="Class",
        barmode="group",
        color_discrete_map={"No default": GREEN, "Default": RED},
        title=title,
    )
    fig.update_layout(height=390, margin=dict(l=10, r=10, t=50, b=10))
    return _polish(fig)


def pay_status_default_chart(df: pd.DataFrame) -> go.Figure:
    rows = []
    for col in ["PAY_0", "PAY_2", "PAY_6"]:
        tmp = df.groupby(col)[TARGET_COL].mean().reset_index()
        tmp.columns = ["status_level", "default_rate"]
        tmp["pay_col"] = col
        rows.append(tmp)
    plot_df = pd.concat(rows, ignore_index=True)
    plot_df["default_rate_pct"] = plot_df["default_rate"] * 100
    fig = px.line(
        plot_df,
        x="status_level",
        y="default_rate_pct",
        color="pay_col",
        markers=True,
        title="Default rate by delinquency level",
    )
    fig.update_layout(height=410, margin=dict(l=10, r=10, t=50, b=10))
    fig.update_yaxes(title="Default rate (%)")
    fig.update_xaxes(title="PAY status level")
    return _polish(fig)


def median_trend_chart(df: pd.DataFrame, cols: list[str], title: str) -> go.Figure:
    med = pd.DataFrame(
        {
            "No default": df[df[TARGET_COL] == 0][cols].median(),
            "Default": df[df[TARGET_COL] == 1][cols].median(),
        }
    ).reset_index(names="Feature")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=med["Feature"], y=med["No default"], mode="lines+markers", name="No default"))
    fig.add_trace(go.Scatter(x=med["Feature"], y=med["Default"], mode="lines+markers", name="Default"))
    fig.update_traces(line=dict(width=3))
    fig.update_layout(height=390, title=title, margin=dict(l=10, r=10, t=50, b=10))
    fig.update_yaxes(title="Median amount")
    return _polish(fig)


def model_metric_chart(results: pd.DataFrame) -> go.Figure:
    metric_cols = ["Accuracy", "Precision", "Recall", "F1-score", "ROC-AUC"]
    long_df = results.melt(id_vars="Model", value_vars=metric_cols, var_name="Metric", value_name="Score")
    fig = px.bar(long_df, x="Model", y="Score", color="Metric", barmode="group", text="Score")
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig.update_layout(height=470, margin=dict(l=10, r=10, t=35, b=10))
    fig.update_yaxes(range=[0, 1.05])
    return _polish(fig)


def confusion_matrix_chart(confusion: list[list[int]], title: str) -> go.Figure:
    fig = px.imshow(
        confusion,
        text_auto=True,
        color_continuous_scale="Blues",
        labels=dict(x="Predicted", y="Actual", color="Count"),
        x=["No default", "Default"],
        y=["No default", "Default"],
        title=title,
    )
    fig.update_layout(height=390, margin=dict(l=10, r=10, t=50, b=10))
    return _polish(fig)


def feature_importance_chart(feature_names: list[str], importances, top_n: int = 14) -> go.Figure:
    importance_df = (
        pd.DataFrame({"Feature": feature_names, "Importance": importances})
        .sort_values("Importance", ascending=False)
        .head(top_n)
        .sort_values("Importance", ascending=True)
    )
    fig = px.bar(
        importance_df,
        x="Importance",
        y="Feature",
        orientation="h",
        text="Importance",
        title="Top model signals",
    )
    fig.update_traces(marker_color=BLUE, texttemplate="%{text:.3f}", textposition="outside")
    fig.update_layout(height=460, showlegend=False, margin=dict(l=10, r=10, t=50, b=10))
    fig.update_xaxes(title="Importance")
    fig.update_yaxes(title="")
    return _polish(fig)


def probability_gauge(probability: float) -> go.Figure:
    if probability < 0.35:
        color = GREEN
    elif probability < 0.65:
        color = AMBER
    else:
        color = RED
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            number={"suffix": "%", "font": {"size": 42}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 35], "color": "#DCFCE7"},
                    {"range": [35, 65], "color": "#FEF3C7"},
                    {"range": [65, 100], "color": "#FEE2E2"},
                ],
                "threshold": {"line": {"color": INK, "width": 3}, "value": 50},
            },
        )
    )
    fig.update_layout(height=310, margin=dict(l=20, r=20, t=20, b=10))
    return _polish(fig)
