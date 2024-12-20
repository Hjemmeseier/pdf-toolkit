import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import io

# Function to extract pages from PDF
def extract_pages(pdf_file, start_page, end_page):
    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    
    # Ensure page indices are within range
    num_pages = len(reader.pages)
    start_page = max(1, start_page)
    end_page = min(end_page, num_pages)
    
    for page_num in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_num])
    
    extracted_pdf = io.BytesIO()
    writer.write(extracted_pdf)
    extracted_pdf.seek(0)
    
    return extracted_pdf

# Streamlit UI
st.title("PDF Page Extractor")

# Allow user to upload a single PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf", label_visibility="visible")

# Check if a file is uploaded
if uploaded_file:
    # Display the number of pages in the uploaded PDF
    reader = PdfReader(uploaded_file)
    num_pages = len(reader.pages)
    st.write(f"The PDF has {num_pages} pages.")

    # Input fields for start and end pages
    start_page = st.number_input("Start page", min_value=1, max_value=num_pages, value=1)
    end_page = st.number_input("End page", min_value=1, max_value=num_pages, value=num_pages)

    # Extract Pages Button
    if st.button("Extract Pages"):
        # Validate page range
        if start_page <= end_page:
            # Extract the specified pages
            extracted_pdf = extract_pages(uploaded_file, start_page, end_page)
            
            # Display success message and download button
            st.success("Pages extracted successfully!")
            st.download_button(
                "Download Extracted Pages",
                extracted_pdf.getvalue(),
                file_name="extracted_pages.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("End page must be greater than or equal to start page.")
else:
    st.info("Please upload a PDF file to extract pages.")
