import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Expansion Alignment Checker", layout="centered")

st.title("🔥 Expansion Alignment Checker")
st.markdown("**Does this multiply your life or maintain shrinkage?**")

DATA_FILE = "data.csv"

# --- INPUT SECTION ---

description = st.text_input("What is this about? (short description)", max_chars=150)

category = st.selectbox(
    "Category",
    ["Romantic", "Friend", "Work", "Family", "Social Event", "Solo", "Opportunity", "Other"]
)

person = st.text_input("Person involved (if any)")

mode = st.radio("Mode:", ["General Expansion", "Relationship"])

baseline = st.slider("How do I feel right now (before scoring)?", 0, 2, 1,
                     help="0 = calm, 1 = slightly reactive, 2 = irritated/triggered")

spark = st.slider("🔥 Spark", 0, 2, 1)
growth = st.slider("🌱 Growth", 0, 2, 1)
energy = st.slider("⚡ Energy", 0, 2, 1)
agency = st.slider("🧭 Agency", 0, 2, 1)
trajectory = st.slider("🚀 Trajectory Alignment", 0, 2, 1)

over_functioning = st.checkbox("Am I over-functioning here?")

notes = st.text_area("Notes (optional)")

if st.button("Save Entry"):

    if description == "":
        st.warning("Please add a short description.")
    else:
        total = spark + growth + energy + agency + trajectory

        entry = {
            "date": datetime.datetime.now(),
            "description": description,
            "category": category,
            "person": person,
            "mode": mode,
            "baseline": baseline,
            "spark": spark,
            "growth": growth,
            "energy": energy,
            "agency": agency,
            "trajectory": trajectory,
            "total": total,
            "over_functioning": over_functioning,
            "notes": notes
        }

        df = pd.DataFrame([entry])

        if os.path.exists(DATA_FILE):
            df.to_csv(DATA_FILE, mode='a', header=False, index=False)
        else:
            df.to_csv(DATA_FILE, index=False)

        st.success("Entry saved!")

# --- ANALYTICS SECTION ---

st.header("📊 Trend Dashboard")

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])

    # Overall trend
    st.subheader("Overall Expansion Score Over Time")
    st.line_chart(df.set_index("date")["total"])

    avg_score = round(df["total"].mean(), 2)
    st.write(f"**Average Score:** {avg_score}")

    # Category analysis
    st.subheader("Average Score by Category")
    cat_avg = df.groupby("category")["total"].mean().sort_values(ascending=False)
    st.bar_chart(cat_avg)

    # Person analysis
    if df["person"].str.strip().any():
        st.subheader("Average Score by Person")
        person_avg = df[df["person"] != ""].groupby("person")["total"].mean().sort_values(ascending=False)
        st.bar_chart(person_avg)

    # Over-functioning frequency
    st.subheader("Over-Functioning Frequency")
    of_rate = df["over_functioning"].mean() * 100
    st.write(f"{round(of_rate, 1)}% of entries involve over-functioning.")

    # Pattern alerts
    if avg_score <= 4:
        st.warning("⚠ Pattern of depletion detected.")
    elif avg_score >= 7:
        st.success("🔥 Strong expansion trend.")

else:
    st.info("No entries yet.")
