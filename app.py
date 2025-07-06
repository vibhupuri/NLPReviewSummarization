import streamlit as st
import pandas as pd
import gdown
import os
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

@st.cache_data
def load_large_csv():
    file_id = "14kn_5J-Obqqbd_vFzxmeTsTrjXkXwE3J"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "disneyland_reviews_with_summary1.csv"

    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    
    return pd.read_csv(output, encoding='latin1')

# -------------------------------------------
# Extractive summarization function
def get_summary(text, sentence_count=2):
    try:
        if len(text.split('.')) < sentence_count + 1:
            return text  # too short to summarize

        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentence_count)
        summary_text = " ".join(str(sentence) for sentence in summary)

        return summary_text if summary_text.strip() else text
    except Exception:
        return text

# -------------------------------------------
# Streamlit UI
st.set_page_config(page_title="Disneyland Review Summarizer", layout="wide")
st.title("🎢 Disneyland Review Summarizer")

df = load_large_csv()

option = st.radio("Choose an option:", ["Pick from pre-processed dataset", "Summarize your own review"])

if option == "Pick from pre-processed dataset":
    st.markdown("#### Browse existing reviews")
    index = st.selectbox("Select a review:", df.index, format_func=lambda i: f"Review #{i}")
    
    review = df.loc[index, 'Review_Text']
    summary = df.loc[index, 'Summary']
    
    st.markdown("**📝 Original Review:**")
    st.info(review)

    st.markdown("**✂️ Summary:**")
    st.success(summary)

else:
    st.markdown("#### Paste your own review below")
    user_review = st.text_area("Enter your Disneyland review here")

    if st.button("Summarize"):
        if user_review.strip():
            generated_summary = get_summary(user_review)
            st.markdown("**✂️ Generated Summary:**")
            st.success(generated_summary)
        else:
            st.warning("Please enter some text to summarize.")
