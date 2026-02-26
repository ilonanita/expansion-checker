import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Expansion Alignment Checker", layout="centered")

st.title("🔥 Expansion Alignment Checker")

st.markdown("Does this multiply your life or maintain shrinkage?")

# Mode Toggle
mode = st.radio("Mode:", ["General Expansion", "Relationship"])

person = ""
if mode == "Relationship":
    person = st.text_input("Person involved (optional):")

spark = st.slider("🔥 Spark", 0, 2, 1)
growth = st.slider("🌱 Growth", 0, 2, 1)
energy = st.slider("⚡ Energy", 0, 2, 1)
agency = st.slider("🧭 Agency", 0, 2, 1)
trajectory = st.slider("🚀 Trajectory Alignment", 0, 2, 1)

over_functioning = st.checkbox("Am I over-functioning here?")

notes = st.text_area("Notes (optional)")

if st.button("Save Entry"):

    total = spark + growth + energy + agency + trajectory

    entry = {
        "date": datetime.datetime.now(),
        "mode": mode,
        "person": person,
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

    if os.path.exists("data.csv"):
        df.to_csv("data.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("data.csv", index=False)

    st.success("Entry saved!")

# --- Trend Analysis ---

st.header("📊 Trends")

if os.path.exists("data.csv"):
    df = pd.read_csv("data.csv")
    df["date"] = pd.to_datetime(df["date"])

    st.line_chart(df.set_index("date")["total"])

    avg_score = round(df["total"].mean(), 2)
    st.write(f"Average Score: {avg_score}")

    if avg_score <= 4:
        st.warning("⚠ Pattern of depletion detected.")
    elif avg_score >= 7:
        st.success("🔥 Strong expansion trend.")
else:
    st.info("No entries yet.")
