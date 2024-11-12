import streamlit as st
import fitz  # PyMuPDF
from io import BytesIO

def add_header_to_first_page(pdf_file, header_text):
    # Open the PDF file
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    
    # Process the first page
    first_page = pdf_document[0]
    first_page.insert_text(fitz.Point(40, 30), header_text, fontsize=12)  # Insert header at the top-left

    # Save the updated PDF to a BytesIO buffer
    output_pdf = BytesIO()
    pdf_document.save(output_pdf)
    pdf_document.close()
    output_pdf.seek(0)
    return output_pdf

# Streamlit app interface
st.title("Add Header to First Page of PDF")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Header input
header_text = st.text_input("Header Text", "")

# Button to add header
if st.button("Add Header"):
    if uploaded_file is not None and header_text:
        # Add header to first page
        output_pdf = add_header_to_first_page(uploaded_file, header_text)

        # Provide download button
        st.download_button(
            label="Download PDF with Header",
            data=output_pdf,
            file_name="pdf_with_header.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Please upload a PDF file and enter header text.")