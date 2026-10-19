import os
import httpx
import streamlit as st

st.set_page_config(page_title="Sift", page_icon="🔎", layout="centered")
st.title("Sift")
st.caption("Research with a visible evidence check before synthesis.")

question = st.text_area("Research question", placeholder="When is RAG a better fit than fine-tuning for a support assistant?")
if st.button("Research", type="primary", disabled=not question.strip()):
    api_url = os.getenv("SIFT_API_URL", "http://localhost:8000")
    with st.spinner("Working through the evidence..."):
        response = httpx.post(f"{api_url}/research", json={"question": question}, timeout=120)
        response.raise_for_status()
        data = response.json()
    st.markdown(data["report"])
    with st.expander("Verification details"):
        st.json(data["verified_claims"])
