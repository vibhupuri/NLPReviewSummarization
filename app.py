import pandas as pd
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import streamlit as st

# Function to summarize text
def get_summary(text, sentence_count=2):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentence_count)
        return " ".join(str(sentence) for sentence in summary)
    except Exception:
        return text

st.title("📝 Disneyland Review Summarizer")

review = st.text_area("Paste a Disneyland review:")

if st.button("Summarize"):
    if review.strip():
        summary = get_summary(review)
        st.markdown("### ✂️ Extractive Summary")
        st.success(summary)
    else:
        st.warning("Please enter some review text.")
