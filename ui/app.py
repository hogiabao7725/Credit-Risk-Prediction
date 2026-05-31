from pathlib import Path
import sys

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ui.credit_dashboard.pages.eda import render_eda_page
from ui.credit_dashboard.pages.home import render_home_page
from ui.credit_dashboard.pages.modeling import render_modeling_page
from ui.credit_dashboard.pages.predict import render_predict_page
from ui.credit_dashboard.styles import apply_global_styles


st.set_page_config(
    page_title="Credit Risk Prediction",
    page_icon=":credit_card:",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_styles()

PAGES = {
    "Home": render_home_page,
    "EDA": render_eda_page,
    "ML Model": render_modeling_page,
    "Prediction": render_predict_page,
}

with st.sidebar:
    st.markdown("## Credit Risk")
    st.caption("Presentation dashboard")
    page = st.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
    st.divider()
    st.caption("Project flow")
    st.markdown("Home -> EDA -> ML Model -> Prediction")
    st.caption("Metric priority")
    st.markdown("Use **F1-score** and **Recall** because defaults are the minority class.")

PAGES[page]()
