from pathlib import Path
import logging
import sys
import warnings

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

logging.getLogger("streamlit.runtime.caching.cache_data_api").setLevel(logging.ERROR)
warnings.filterwarnings(
    "ignore",
    message="`sklearn.utils.parallel.delayed` should be used.*",
    category=UserWarning,
)

from ui.credit_dashboard.artifacts import save_training_package
from ui.credit_dashboard.config import MODEL_BUNDLE_PATH
from ui.credit_dashboard.data import prepare_dataset, read_raw_data
from ui.credit_dashboard.modeling import build_training_bundle


def main() -> None:
    raw_df = read_raw_data()
    clean_df, metadata = prepare_dataset(raw_df)
    bundle = build_training_bundle(clean_df)
    save_training_package(bundle, metadata)

    best = bundle.results.iloc[0]
    print(f"Saved artifact: {MODEL_BUNDLE_PATH}")
    print(f"Best model: {best['Model']}")
    print(f"F1-score: {best['F1-score']:.4f}")
    print(f"Recall: {best['Recall']:.4f}")
    print(f"ROC-AUC: {best['ROC-AUC']:.4f}")


if __name__ == "__main__":
    main()
