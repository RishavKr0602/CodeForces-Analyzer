import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from utils import get_features

# Title
st.set_page_config(page_title="Codeforces AI Coach", layout="centered")
st.title("🚀 Codeforces AI Coach")

# Load model safely
@st.cache_resource
def load_model():
    return joblib.load("cf_model.pkl")

model = load_model()

# Input
user = st.text_input("Enter Codeforces Username")

if st.button("Analyze"):

    if not user.strip():
        st.warning("⚠️ Please enter a username")
        st.stop()

    st.write("🔄 Fetching user data...")

    feat = get_features(user)

    if not feat:
        st.error("❌ Invalid user or insufficient data")
        st.stop()

    st.success("✅ Data fetched")

    # Extract tags separately
    tags = feat.pop("tag_counts", {})

    # Convert to DataFrame
    df = pd.DataFrame([feat])

    # Align features with model
    try:
        df = df.reindex(columns=model.get_booster().feature_names, fill_value=0)
    except:
        st.error("⚠️ Model feature mismatch. Retrain or check model.")
        st.stop()

    st.write("🤖 Predicting...")

    pred = model.predict(df)[0] * 100

    st.success("✅ Prediction complete")

    # Show metric
    st.metric("📈 Monthly Gain", f"{pred:.0f}")

    # 🔴 Weak topics
    st.subheader("📚 Weak Topics")

    total = sum(tags.values()) if tags else 1

    for t in ["dp", "graphs", "greedy", "math"]:
        ratio = tags.get(t, 0) / total

        if ratio < 0.15:
            st.write(f"{t}: 🔴 weak → Solve ~20 problems (~10 hrs)")
        else:
            st.write(f"{t}: 🟢 good")

    # 📈 Growth curve
    st.subheader("📈 Expected Growth")

    r = feat["current"]
    curve = []

    for _ in range(12):
        r += pred * (1 - r / 3000)
        curve.append(r)

    fig, ax = plt.subplots()
    ax.plot(curve)
    ax.set_title("Expected Rating Growth (Next 12 Months)")
    ax.set_xlabel("Months")
    ax.set_ylabel("Rating")
    ax.grid()

    st.pyplot(fig)