import streamlit as st
import pandas as pd

# Load processed reviews
@st.cache_data
def load_reviews():
    return pd.read_csv("disney_reviews_processed.csv")  # or use read_pickle()

df = load_reviews()

st.title("📝 Disneyland Review Summarizer")

# Dropdown to pick a review
selected_index = st.selectbox("Select review to summarize:", df.index)
review = df.loc[selected_index, "Review_Text"]
summary = df.loc[selected_index, "Summary"]

# Display
st.markdown("### Original Review")
st.write(review)

st.markdown("### ✂️ Extractive Summary")
st.success(summary)
