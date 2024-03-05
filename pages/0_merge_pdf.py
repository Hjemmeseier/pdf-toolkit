import streamlit as st

import pdf_utils as pu

# Streamlit UI
st.title("PDF Merger")

# Allow user to upload multiple PDF files
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True,label_visibility= "collapsed")

if st.button("Merge PDFs"):
    if uploaded_files:
        # Merge PDF files
        merged_pdf = pu.merge_pdfs(uploaded_files)

        # Display download link for the merged PDF
        st.success("PDFs merged successfully!")
        st.download_button("Download Merged PDF", merged_pdf.getvalue(), file_name="merged_pdf.pdf", mime="application/pdf")
    else:
        st.warning("Please upload PDF files to merge")