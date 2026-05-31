import streamlit as st

from ui.credit_dashboard.artifacts import load_training_package, render_missing_artifact_message
from ui.credit_dashboard.charts import confusion_matrix_chart, feature_importance_chart, model_metric_chart
from ui.credit_dashboard.components import insight, metric_card, page_hero, section_header, story_card, workflow_step
from ui.credit_dashboard.config import MODEL_EXPLANATIONS


def render_modeling_page() -> None:
    try:
        package = load_training_package()
    except FileNotFoundError:
        render_missing_artifact_message()
        st.stop()

    bundle = package.bundle
    metadata = package.metadata

    page_hero(
        "Machine Learning",
        "Train, compare, explain",
        "All models use the same preprocessing pipeline from the notebook, then they are compared with "
        "imbalance-aware metrics so the selected model is defensible.",
        f"Models loaded from artifact | Created at: {package.created_at}",
    )

    c1, c2, c3, c4 = st.columns(4)
    best = bundle.results.iloc[0]
    with c1:
        metric_card("Best model", str(best["Model"]), "Selected by F1-score")
    with c2:
        metric_card("Best F1", f"{best['F1-score']:.4f}", "Precision/Recall balance")
    with c3:
        metric_card("Best Recall", f"{best['Recall']:.4f}", "Defaults caught")
    with c4:
        metric_card("ROC-AUC", f"{best['ROC-AUC']:.4f}", "Ranking quality")

    pipeline_tab, results_tab, explain_tab, inspect_tab = st.tabs(
        ["Pipeline", "Model comparison", "Why this model", "Inspect"]
    )

    with pipeline_tab:
        section_header("Preprocessing Pipeline", "The same cleaning and feature engineering logic is used for every model.")
        p1, p2, p3, p4 = st.columns(4)
        with p1:
            workflow_step("01", "Clean categories", "Map uncommon EDUCATION and MARRIAGE codes into stable groups.")
        with p2:
            workflow_step("02", "Reduce noise", "Drop duplicates and cap monetary outliers at the 1st-99th percentiles.")
        with p3:
            workflow_step("03", "Engineer behavior", "Create bill, payment, utilization, and delay features.")
        with p4:
            workflow_step("04", "Evaluate", "Use stratified split and 5-fold stratified CV with F1 scoring.")

        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("Train shape", f"{bundle.train_shape[0]:,} x {bundle.train_shape[1]:,}")
        with c2:
            metric_card("Test shape", f"{bundle.test_shape[0]:,} x {bundle.test_shape[1]:,}")
        with c3:
            metric_card("Log transforms", f"{len(metadata.high_skew_cols):,}", "High-skew money columns")

    with results_tab:
        section_header("Model Comparison", "F1-score is the main ranking metric because defaults are the minority class.")
        st.plotly_chart(model_metric_chart(bundle.results), width="stretch")
        st.dataframe(
            bundle.results.style.format({c: "{:.4f}" for c in bundle.results.columns if c != "Model"}),
            width="stretch",
        )

    with explain_tab:
        section_header("Why This Model", "The selected model balances missed defaults and false alarms better than the others.")
        b1, b2, b3 = st.columns(3)
        with b1:
            story_card("Selection rule", "Choose the highest F1-score, then check Recall and ROC-AUC for practical risk.", "blue")
        with b2:
            story_card("Risk concern", "False negatives are costly because the model misses customers who actually default.", "amber")
        with b3:
            story_card("Recommendation", f"Use {bundle.best_name} as the demo model and tune threshold later if needed.", "green")

        best_artifact = bundle.artifacts[bundle.best_name]
        model = best_artifact.pipeline.named_steps["model"]
        if hasattr(model, "feature_importances_"):
            st.plotly_chart(
                feature_importance_chart(bundle.feature_columns, model.feature_importances_),
                width="stretch",
            )
        else:
            insight("The selected model does not expose tree-based feature importance.")

    with inspect_tab:
        section_header("Inspect A Model", "Use this section during Q&A to compare confusion matrices.")
        selected_model = st.selectbox("Model", bundle.results["Model"].tolist())
        artifact = bundle.artifacts[selected_model]
        st.plotly_chart(
            confusion_matrix_chart(artifact.confusion, f"Confusion matrix - {selected_model}"),
            width="stretch",
        )
        insight(MODEL_EXPLANATIONS[selected_model])
