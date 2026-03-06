import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
from xgboost import XGBClassifier
import joblib
import os

# --- Load SMOTE-balanced data ---
df = pd.read_csv("Dataset/smote_balanced.csv")

# Separate features and target
X = df.drop("Churn", axis=1)
y = df["Churn"]

feature_names = X.columns.tolist()

# --- Train-test split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- Scale features ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- Train XGBoost model ---
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.06,
    subsample=0.9,
    colsample_bytree=0.9,
    min_child_weight=1,
    gamma=0,
    reg_alpha=0.1,
    reg_lambda=0.5,
    random_state=42,
    eval_metric="logloss",
)

model.fit(X_train_scaled, y_train)

# --- Evaluate ---
y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)[:, 1]

print("=== XGBoost Model Evaluation (SMOTE-balanced) ===")
print(f"Accuracy : {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall   : {recall_score(y_test, y_pred):.4f}")
print(f"F1-Score : {f1_score(y_test, y_pred):.4f}")
print(f"ROC-AUC  : {roc_auc_score(y_test, y_prob):.4f}")
print()
print(classification_report(y_test, y_pred, target_names=["No Churn", "Churn"]))

# --- Save artifacts ---
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/xgboost_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
joblib.dump(feature_names, "models/feature_names.pkl")

print("Saved: models/xgboost_model.pkl, models/scaler.pkl, models/feature_names.pkl")
