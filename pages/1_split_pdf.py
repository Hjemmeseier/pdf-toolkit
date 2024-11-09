import streamlit as st
import PyPDF2
from io import BytesIO

def split_pdf(pdf_file, start_page, end_page):
    """
    Splits a PDF file by extracting pages from start_page to end_page (inclusive).
    
    Parameters:
    pdf_file (BytesIO): Uploaded PDF file as a BytesIO object.
    start_page (int): Start page number (1-based index).
    end_page (int): End page number (1-based index).
    
    Returns:
    BytesIO: A BytesIO object with the split PDF content.
    """
    # Open the PDF file
    reader = PyPDF2.PdfReader(pdf_file)
    writer = PyPDF2.PdfWriter()
    
    # Ensure page indices are within range
    num_pages = len(reader.pages)
    start_page = max(1, start_page)
    end_page = min(end_page, num_pages)
    
    # Extract the specified pages and add them to the writer
    for page_num in range(start_page - 1, end_page):
        page = reader.pages[page_num]
        writer.add_page(page)
    
    # Save the output to a BytesIO object
    output_pdf = BytesIO()
    writer.write(output_pdf)
    output_pdf.seek(0)
    
    return output_pdf

# Streamlit app layout
st.title("PDF Splitter")

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    # Display total number of pages
    reader = PyPDF2.PdfReader(uploaded_file)
    num_pages = len(reader.pages)
    st.write(f"The PDF has {num_pages} pages.")
    
    # Input page range
    start_page = st.number_input("Start page", min_value=1, max_value=num_pages, value=1)
    end_page = st.number_input("End page", min_value=1, max_value=num_pages, value=num_pages)
    
    # Split PDF button
    if st.button("Split PDF"):
        output_pdf = split_pdf(uploaded_file, start_page, end_page)
        
        # Download button for the split PDF
        st.download_button(
            label="Download Split PDF",
            data=output_pdf,
            file_name="split_pdf.pdf",
            mime="application/pdf"
        )
