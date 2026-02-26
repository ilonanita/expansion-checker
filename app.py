import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Expansion Alignment Checker", layout="centered")

# --- Calm Green Theme Override ---
st.markdown("""
<style>
.stApp {
    background-color: #f4fbf4;
}

/* Radio button color override */
div[role="radiogroup"] input:checked + div {
    background-color: #2e7d32 !important;
    border-color: #2e7d32 !important;
}

/* Remove default red focus */
div[role="radiogroup"] input:focus + div {
    box-shadow: none !important;
}

/* Make radio layout horizontal */
div[data-baseweb="radio"] > div {
    flex-direction: row;
}

/* Enlarge dot display */
div[role="radiogroup"] > label {
    font-size: 28px;
    padding: 0 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("Expansion Alignment Checker")
st.markdown("**Does this multiply your life or maintain shrinkage?**")

DATA_FILE = "data.csv"

# --- MODE FIRST (default to General Expansion) ---
mode = st.radio(
    "Mode",
    ["General Expansion", "Relationship"],
    horizontal=True,
    index=0
)

# --- CONTEXT ---
description = st.text_input("What is this about?", max_chars=150)

category = st.selectbox(
    "Category",
    ["Romantic", "Friend", "Work", "Family", "Social Event", "Solo", "Opportunity", "Other"]
)

person = st.text_input("Person involved (if any)")

st.divider()

# --- SINGLE DOT RATING FUNCTION ---
def dot_rating(label, help_text):
    st.markdown(f"**{label}**")
    st.caption(help_text)

    value = st.radio(
        "",
        [1,2,3,4,5],
        index=2,  # default = 3 (neutral)
        horizontal=True,
        format_func=lambda x: "●" if x == 3 else "○",
        key=label
    )

    return value

# --- BASELINE ---
baseline = dot_rating(
    "Baseline",
    "How do I feel right now? (1 = reactive | 5 = calm and clear)"
)

spark = dot_rating(
    "🔥 Spark",
    "Does this ignite intellectual, emotional, or sensual aliveness?"
)

growth = dot_rating(
    "🌱 Growth",
    "Does this stretch me or move me forward?"
)

energy = dot_rating(
    "⚡ Energy",
    "Do I feel energised (not drained) thinking about engaging?"
)

agency = dot_rating(
    "🧭 Agency",
    "Am I choosing this freely — not from guilt or pressure?"
)

trajectory = dot_rating(
    "🚀 Trajectory Alignment",
    "Does this align with the woman I am becoming?"
)

over_functioning = st.checkbox("Am I over-functioning here?")

notes = st.text_area("Notes (optional)")

st.divider()

# --- SAVE ---
if st.button("Save Entry"):
    if description == "":
        st.warning("Please add a short description.")
    else:
        total = spark + growth + energy + agency + trajectory

        entry = {
            "date": datetime.datetime.now(),
            "mode": mode,
            "description": description,
            "category": category,
            "person": person,
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

        st.success("Entry saved.")

# --- ANALYTICS ---
st.header("Trend Overview")

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])

    st.line_chart(df.set_index("date")["total"])

    avg_score = round(df["total"].mean(), 2)
    st.write(f"Average Expansion Score: {avg_score}")

    st.subheader("By Category")
    cat_avg = df.groupby("category")["total"].mean().sort_values(ascending=False)
    st.bar_chart(cat_avg)

    if df["person"].str.strip().any():
        st.subheader("By Person")
        person_avg = df[df["person"] != ""].groupby("person")["total"].mean().sort_values(ascending=False)
        st.bar_chart(person_avg)

    of_rate = df["over_functioning"].mean() * 100
    st.write(f"Over-functioning appears in {round(of_rate,1)}% of entries.")

else:
    st.info("No entries yet.")
