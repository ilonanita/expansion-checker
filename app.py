import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Expansion Alignment Checker", layout="centered")

# --- Clean Styling + Precise Spacing ---
st.markdown("""
<style>

/* Remove radio circle */
div[role="radiogroup"] input {
    display: none;
}

/* Horizontal radio */
div[data-baseweb="radio"] > div {
    flex-direction: row;
}

/* Remove extra spacing from markdown */
div[data-testid="stMarkdownContainer"] p {
    margin-bottom: 0.2rem;
}

/* Remove extra spacing from captions */
div[data-testid="stCaptionContainer"] {
    margin-bottom: 0.3rem;
}

/* Tight radio spacing */
div[role="radiogroup"] {
    margin-top: 0rem;
    margin-bottom: 0rem;
}

/* Larger spacing AFTER each rating block */
.block-spacer {
    height: 1.8rem;
}

/* Clean radio labels */
div[role="radiogroup"] label {
    background-color: transparent !important;
}

div[role="radiogroup"] label span {
    font-size: 20px;
    padding: 0 10px;
    color: black !important;
}

</style>
""", unsafe_allow_html=True)

st.title("Expansion Alignment Checker")
st.markdown("**Does this multiply your life or maintain shrinkage?**")

DATA_FILE = "data.csv"

mode = st.radio(
    "Mode",
    ["General Expansion", "Relationship"],
    horizontal=True,
    index=0,
    key="mode"
)

description = st.text_input("What is this about?", max_chars=150)

category = st.selectbox(
    "Category",
    ["Romantic", "Friend", "Work", "Family", "Social Event", "Solo", "Opportunity", "Other"]
)

person = st.text_input("Person involved (if any)")

st.divider()

def rating_block(label, help_text, key_name):
    st.markdown(f"### {label}")
    st.caption(help_text)

    value = st.radio(
        "",
        [1,2,3,4,5],
        index=2,
        horizontal=True,
        key=key_name
    )

    # Spacer AFTER full block
    st.markdown('<div class="block-spacer"></div>', unsafe_allow_html=True)

    return value

baseline = rating_block(
    "Baseline",
    "How do I feel right now? (1 = reactive | 5 = calm and clear)",
    "baseline"
)

spark = rating_block(
    "🔥 Spark",
    "Does this ignite intellectual, emotional, or sensual aliveness?",
    "spark"
)

growth = rating_block(
    "🌱 Growth",
    "Does this stretch me or move me forward?",
    "growth"
)

energy = rating_block(
    "⚡ Energy",
    "Do I feel energised (not drained) thinking about engaging?",
    "energy"
)

agency = rating_block(
    "🧭 Agency",
    "Am I choosing this freely — not from guilt or pressure?",
    "agency"
)

trajectory = rating_block(
    "🚀 Trajectory Alignment",
    "Does this align with the woman I am becoming?",
    "trajectory"
)

over_functioning = st.checkbox("Am I over-functioning here?")

notes = st.text_area("Notes (optional)")

st.divider()

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

st.header("Trend Overview")

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])

    st.line_chart(df.set_index("date")["total"])

    avg_score = round(df["total"].mean(), 2)
    st.write(f"Average Expansion Score: {avg_score}")
else:
    st.info("No entries yet.")
