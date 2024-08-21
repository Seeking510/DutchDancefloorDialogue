import streamlit as st
from src import home, demographics, talking_behaviour, impact_analysis, quiet_importance, yapping_factor

st.set_page_config(page_title="Rave Data Analysis Dashboard", layout="wide")

PAGES = {
    "Home": home,
    "Demographics": demographics,
    "Talking Behavior": talking_behaviour,
    "Impact Analysis": impact_analysis,
    "Quiet Importance": quiet_importance,
    "Yapping Factor": yapping_factor
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
page.app()
