from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import joblib
import streamlit as st

from ui.credit_dashboard.config import DATA_PATH, MODEL_BUNDLE_PATH
from ui.credit_dashboard.data import PreparationMetadata
from ui.credit_dashboard.modeling import TrainingBundle


@dataclass
class TrainingPackage:
    bundle: TrainingBundle
    metadata: PreparationMetadata
    created_at: str
    data_path: str


def artifact_exists(path: Path = MODEL_BUNDLE_PATH) -> bool:
    return path.exists()


def save_training_package(
    bundle: TrainingBundle,
    metadata: PreparationMetadata,
    path: Path = MODEL_BUNDLE_PATH,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    package = TrainingPackage(
        bundle=bundle,
        metadata=metadata,
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        data_path=str(DATA_PATH),
    )
    joblib.dump(package, path)


@st.cache_resource(show_spinner=False)
def load_training_package(path: Path = MODEL_BUNDLE_PATH) -> TrainingPackage:
    if not path.exists():
        raise FileNotFoundError(path)
    return joblib.load(path)


def render_missing_artifact_message() -> None:
    st.error("Model artifact is missing. Train it once before opening ML Model or Prediction.")
    st.code("venv/bin/python scripts/train_artifacts.py", language="bash")
