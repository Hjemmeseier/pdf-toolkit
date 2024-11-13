import streamlit as st
import fitz  # PyMuPDF
from io import BytesIO

def add_header_footer(pdf_file, header_text, footer_text, pages):
    # Open the PDF file
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    num_pages = pdf_document.page_count
    
    # Process each page based on user selection
    for i in range(num_pages):
        if i not in pages:
            continue  # Skip pages not in the selected range
        
        page = pdf_document[i]
        page_width = page.rect.width
        page_height = page.rect.height

        # Add header
        if header_text:
            header_position = fitz.Point(40, 30)  # Top-left position for header
            page.insert_text(header_position, header_text, fontsize=12)

        # Add footer
        if footer_text:
            footer_position = fitz.Point(40, page_height - 30)  # Bottom-left position for footer
            page.insert_text(footer_position, footer_text, fontsize=12)

    # Save the updated PDF to a BytesIO buffer
    output_pdf = BytesIO()
    pdf_document.save(output_pdf)
    pdf_document.close()
    output_pdf.seek(0)
    return output_pdf

def parse_page_ranges(page_ranges, num_pages):
    """Parse string page ranges to a set of zero-based page indices."""
    if not page_ranges:
        return set(range(num_pages))  # Apply to all pages if no input

    pages_to_apply = set()
    for part in page_ranges.split(','):
        if '-' in part:
            start, end = part.split('-')
            start = int(start) - 1 if start else 0
            end = int(end) - 1 if end else num_pages - 1
            pages_to_apply.update(range(start, end + 1))
        else:
            pages_to_apply.add(int(part) - 1)
    
    return pages_to_apply

# Streamlit app interface
st.title("Add Header and Footer to Selected Pages in PDF")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Header and Footer inputs
header_text = st.text_input("Header Text", "")
footer_text = st.text_input("Footer Text", "")

# Page selection input
page_ranges = st.text_input("Enter pages to apply header/footer (e.g., 1,2,3,4-6)", value="")

# Button to add header and footer
if st.button("Add Header and Footer"):
    if uploaded_file is not None:
        # Parse pages and apply header/footer
        num_pages = fitz.open(stream=uploaded_file.read(), filetype="pdf").page_count
        pages_to_apply_set = parse_page_ranges(page_ranges, num_pages)
        
        # Generate updated PDF
        output_pdf = add_header_footer(uploaded_file, header_text, footer_text, pages_to_apply_set)

        # Provide download button
        if output_pdf:
            st.download_button(
                label="Download PDF with Header and Footer",
                data=output_pdf,
                file_name="pdf_with_header_footer.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Please upload a PDF file.")