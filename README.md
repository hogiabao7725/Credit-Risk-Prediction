# Credit Risk Prediction

Du an du doan kha nang khach hang vo no trong ky tiep theo tren bo du lieu `UCI_Credit_Card`.

## Muc tieu

- Xay dung quy trinh du doan rui ro tin dung ro rang, de tai lap.
- So sanh nhieu mo hinh phan lop tren cung mot setup tien xu ly.
- Danh gia theo cac metric phu hop bai toan mat can bang lop (Recall, F1, ROC-AUC).

## Cau truc du an

```text
credit-risk-prediction/
├── data/
│   └── UCI_Credit_Card.csv
├── credit_risk_prediction.ipynb
├── requirements.txt
└── README.md
```

## Dataset

- Ten: Default of Credit Card Clients Dataset
- Nguon:
  - [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients)
  - [Kaggle mirror](https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset)
- Kich thuoc: 30,000 dong x 24 cot
- Target: `default.payment.next.month` (1 = vo no, 0 = khong vo no)

## Cai dat

Yeu cau:
- Python 3.9+
- Jupyter Notebook/JupyterLab

Cai thu vien:

```bash
pip install -r requirements.txt
```

## Cach chay notebook

1. Tai file `UCI_Credit_Card.csv` va dat vao thu muc `data/`.
2. Mo Jupyter:

```bash
jupyter notebook
```

3. Mo file `credit_risk_prediction.ipynb`.
4. Chay lan luot tat ca cells tu tren xuong.

## Logic trong notebook

Notebook da duoc to chuc theo flow sau:

1. Import thu vien va cau hinh
2. Load du lieu + dataset overview
3. EDA co ban (phan bo target, nhom bien thanh toan, bill, pay amount)
4. Chia train/test theo stratify
5. Tien xu ly bang `ColumnTransformer` + `Pipeline`
6. Train va so sanh 6 mo hinh:
   - Logistic Regression
   - KNN
   - Naive Bayes
   - SVM
   - Decision Tree
   - Random Forest
7. Danh gia bang:
   - Cross-validation metrics
   - Test Precision/Recall/F1/ROC-AUC
   - Confusion Matrix
8. Chon mo hinh tot nhat va phan tich feature importance (neu ho tro)

## Luu y hoc thuat

- De tranh data leakage, moi buoc impute/scale/encode deu nam trong pipeline va duoc fit tren train set.
- Bai toan credit risk thuong uu tien phat hien dung lop vo no, vi vay can theo doi Recall va F1 ben canh Accuracy.

## Huong cai thien

- Hyperparameter tuning (`GridSearchCV`, `RandomizedSearchCV`, `Optuna`)
- Thu mo hinh boosting (`XGBoost`, `LightGBM`, `CatBoost`)
- Threshold tuning theo business cost

## Tai lieu tham khao

- [Scikit-learn documentation](https://scikit-learn.org/stable/)
- [Pandas documentation](https://pandas.pydata.org/docs/)
- [Seaborn documentation](https://seaborn.pydata.org/)
