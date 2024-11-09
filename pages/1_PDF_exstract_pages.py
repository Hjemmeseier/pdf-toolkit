import streamlit as st
from pdf_utils import extract_pages
from PyPDF2 import PdfReader

st.title("Extract Pages from PDF")

uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf", key="extract")

if uploaded_pdf:
    reader = PdfReader(uploaded_pdf)
    num_pages = len(reader.pages)
    st.write(f"The PDF has {num_pages} pages.")
    
    start_page = st.number_input("Start page", min_value=1, max_value=num_pages, value=1)
    end_page = st.number_input("End page", min_value=1, max_value=num_pages, value=num_pages)
    
    if st.button("Extract Pages"):
        extracted_pdf = extract_pages(uploaded_pdf, start_page, end_page)
        
        st.download_button(
            label="Download Extracted Pages",
            data=extracted_pdf,
            file_name="extracted_pages.pdf",
            mime="application/pdf"
        )
