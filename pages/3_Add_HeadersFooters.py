import streamlit as st
from pymupdf import fitz  # PyMuPDF
from io import BytesIO

def add_header_footer(pdf_file, header_text, footer_text, header_align, footer_align, pages):
    # Open the PDF file
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    num_pages = pdf_document.page_count
    
    # Prepare alignment options
    align_options = {
        "left": 0,
        "center": 1,
        "right": 2
    }
    
    # Process each page
    for i in range(num_pages):
        if i not in pages:
            continue  # Skip pages not in the selected range
        
        page = pdf_document[i]
        page_width = page.rect.width
        page_height = page.rect.height
        
        # Add header
        if header_text:
            header_position = fitz.Point(get_alignment_x(page_width, header_align), 30)
            page.insert_text(header_position, header_text, fontname="helv", fontsize=12, align=align_options[header_align])

        # Add footer
        if footer_text:
            footer_position = fitz.Point(get_alignment_x(page_width, footer_align), page_height - 30)
            page.insert_text(footer_position, footer_text, fontname="helv", fontsize=12, align=align_options[footer_align])
    
    # Save the updated PDF to a BytesIO buffer
    output_pdf = BytesIO()
    pdf_document.save(output_pdf)
    pdf_document.close()
    output_pdf.seek(0)
    return output_pdf

def get_alignment_x(page_width, align):
    """Helper function to determine the x-position based on alignment."""
    if align == "left":
        return 40
    elif align == "center":
        return page_width / 2
    elif align == "right":
        return page_width - 40

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
st.title("Add Headers and Footers to PDF")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Header and Footer inputs
header_text = st.text_input("Header Text", "")
footer_text = st.text_input("Footer Text", "")

# Alignment options
st.subheader("Header and Footer Alignment")
header_align = st.selectbox("Header Alignment", ["left", "center", "right"])
footer_align = st.selectbox("Footer Alignment", ["left", "center", "right"])

# Page selection
pages_to_apply = st.text_input("Enter pages to apply header/footer (e.g., 1,2,3,4-6)", value="")

# Button to add header and footer
if st.button("Add Header and Footer"):
    if uploaded_file is not None:
        # Parse pages and apply header/footer
        num_pages = fitz.open(stream=uploaded_file.read(), filetype="pdf").page_count
        pages_to_apply_set = parse_page_ranges(pages_to_apply, num_pages)
        
        # Generate updated PDF
        output_pdf = add_header_footer(uploaded_file, header_text, footer_text, header_align, footer_align, pages_to_apply_set)

        # Provide download button
        st.download_button(
            label="Download PDF with Header and Footer",
            data=output_pdf,
            file_name="updated_with_header_footer.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Please upload a PDF file to proceed.")
