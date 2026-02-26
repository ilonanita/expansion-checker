import streamlit as st
import pandas as pd
import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Expansion Alignment Checker", layout="centered")

st.title("Expansion Alignment Checker")
st.markdown("Does this multiply your life or maintain shrinkage?")

# -------------------------------
# GOOGLE SHEETS CONNECTION
# -------------------------------

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope,
)

client = gspread.authorize(creds)

# Open your sheet
sheet = client.open("Expansion Checker Data").sheet1

# -------------------------------
# INPUT SECTION
# -------------------------------

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
    st.markdown(f"**{label}**")
    st.markdown(f"<span style='font-size:14px;color:#555;'>{help_text}</span>", unsafe_allow_html=True)

    value = st.radio(
        "",
        [1,2,3,4,5],
        index=2,
        horizontal=True,
        key=key_name
    )

    st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)

    return value

baseline = rating_block(
    "Baseline",
    "How do I feel right now? (1 = reactive | 5 = energised)",
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
    "Do I feel energised (not drained)?",
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

# -------------------------------
# SAVE ENTRY TO GOOGLE SHEETS
# -------------------------------

if st.button("Save Entry"):
    if description == "":
        st.warning("Please add a short description.")
    else:
        total = spark + growth + energy + agency + trajectory

        row = [
            str(datetime.datetime.now()),
            mode,
            description,
            category,
            person,
            baseline,
            spark,
            growth,
            energy,
            agency,
            trajectory,
            total,
            over_functioning,
            notes
        ]

        sheet.append_row(row)

        st.success("Entry saved to Google Sheets.")
