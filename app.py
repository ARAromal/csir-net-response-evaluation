import streamlit as st
import tempfile
from csir_net_evaluation import (
    parse_response_sheet,
    parse_answer_key,
    calculate_score
)

st.set_page_config(page_title="CSIR NET Marks Calculator")

st.title("CSIR-UGC NET Marks Calculator")
st.write("⚠️ Unofficial tool. Files are processed temporarily and not stored.")

response_file = st.file_uploader("Upload Response Sheet (PDF)", type=["pdf"])
answer_key_file = st.file_uploader("Upload Answer Key (HTML / ASPX)", type=["html", "aspx"])

if response_file and answer_key_file:
    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as rp, \
         tempfile.NamedTemporaryFile(delete=True, suffix=".html") as ak:

        rp.write(response_file.read())
        ak.write(answer_key_file.read())
        rp.flush()
        ak.flush()

        responses = parse_response_sheet(rp.name)
        answer_key = parse_answer_key(ak.name)

        c1, w1, c2, w2, score = calculate_score(responses, answer_key)

        st.subheader("Results")
        st.write(f"Correct (Q1–70): {c1}")
        st.write(f"Wrong (Q1–70): {w1}")
        st.write(f"Correct (Q71–145): {c2}")
        st.write(f"Wrong (Q71–145): {w2}")
        st.success(f"Total Score: {score:.2f} / 200")
