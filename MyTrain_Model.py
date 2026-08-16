import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor
import joblib


# ---------------- LOAD DATA ----------------
print("🚀 STEP 4: Loading dataset")

try:
    df = pd.read_csv("cf_training_data.csv")
except FileNotFoundError:
    print("❌ Dataset not found. Run dataset_builder.py first.")
    exit()


# ---------------- PREPROCESS ----------------
print("🚀 STEP 5: Preprocessing")

# Remove any non-numeric columns if present
df = df.select_dtypes(include=[np.number])

# Handle missing values
df = df.fillna(0)

X = df.drop(columns=["target"])
y = df["target"]


# ---------------- TRAIN-TEST SPLIT ----------------
print("🚀 STEP 6: Train-test split")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ---------------- MODEL ----------------
print("🚀 STEP 7: Training model")

model = XGBRegressor(
    n_estimators=1200,
    learning_rate=0.01,
    max_depth=6,
    subsample=0.9,
    colsample_bytree=0.9,
    reg_lambda=1.5,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# ---------------- EVALUATION ----------------
print("🚀 STEP 8: Evaluating")

preds = model.predict(X_test)

r2 = r2_score(y_test, preds)
mae = mean_absolute_error(y_test, preds)

print(f"✅ R2 Score: {r2:.4f}")
print(f"✅ MAE: {mae * 100:.2f} rating points")


# ---------------- SAVE MODEL ----------------
joblib.dump(model, "cf_model.pkl")

print("🎉 MODEL READY → cf_model.pkl")


# ---------------- FEATURE IMPORTANCE ----------------
print("\n📊 Top Features:")

importances = model.feature_importances_
feat_names = X.columns

imp_df = pd.DataFrame({
    "feature": feat_names,
    "importance": importances
}).sort_values(by="importance", ascending=False)

print(imp_df.head(10).to_string(index=False))