import streamlit as st
import fitz  # PyMuPDF
from io import BytesIO

def add_header_footer(pdf_data, header_text, footer_text, header_align, footer_align, header_font_size, footer_font_size, pages, add_page_numbers, page_number_prefix):
    # Open the PDF file from BytesIO
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    num_pages = pdf_document.page_count
    
    # Process each page based on user selection
    for i in range(num_pages):
        if i not in pages:
            continue  # Skip pages not in the selected range
        
        page = pdf_document[i]
        page_width = page.rect.width
        page_height = page.rect.height

        # Add header with alignment
        if header_text:
            header_position = get_text_position(page_width, header_align, header_font_size, 30)
            page.insert_text(header_position, header_text, fontsize=header_font_size, fontname="helv")

        # Add footer with alignment and optional page number
        footer_content = footer_text
        if add_page_numbers:
            page_number_text = f"{page_number_prefix} {i + 1}"
            footer_content += f" - {page_number_text}" if footer_content else page_number_text

        if footer_content:
            footer_position = get_text_position(page_width, footer_align, footer_font_size, page_height - 40)
            page.insert_text(footer_position, footer_content, fontsize=footer_font_size, fontname="helv")

    # Save the updated PDF to a BytesIO buffer
    output_pdf = BytesIO()
    pdf_document.save(output_pdf)
    pdf_document.close()
    output_pdf.seek(0)
    return output_pdf

def get_text_position(page_width, align, font_size, y_position):
    """Helper function to determine the x-position based on alignment, keeping text within page bounds."""
    # Text positioning based on alignment
    if align == "left":
        x_position = 40
    elif align == "center":
        x_position = page_width / 2
    return fitz.Point(x_position, y_position)

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
st.title("Headers and footers 🙆🦶")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Header and Footer inputs
header_text = st.text_input("Header Text", "")
footer_text = st.text_input("Footer Text", "")

# Alignment options
st.subheader("Header and Footer Alignment")
header_align = st.selectbox("Header Alignment", ["left", "center"])
footer_align = st.selectbox("Footer Alignment", ["left", "center"])

# Font size options
st.subheader("Font Size")
header_font_size = st.slider("Header Font Size", min_value=8, max_value=24, value=12)
footer_font_size = st.slider("Footer Font Size", min_value=8, max_value=24, value=12)

# Page selection input
page_ranges = st.text_input("Enter pages to apply header/footer (e.g., 1,2,3,4-6)", value="")

# Page number options
add_page_numbers = st.checkbox("Include Page Numbers in Footer")
page_number_prefix = st.text_input("Page Number Prefix (e.g., Page, Pg, P.)", value="Page")

# Button to add header and footer
if st.button("Add Header and Footer"):
    if uploaded_file is not None:
        # Read the file only once
        pdf_data = BytesIO(uploaded_file.read())
        
        # Parse pages and apply header/footer
        num_pages = fitz.open(stream=pdf_data, filetype="pdf").page_count
        pdf_data.seek(0)  # Reset the pointer after checking the number of pages
        pages_to_apply_set = parse_page_ranges(page_ranges, num_pages)
        
        # Generate updated PDF
        output_pdf = add_header_footer(pdf_data, header_text, footer_text, header_align, footer_align, header_font_size, footer_font_size, pages_to_apply_set, add_page_numbers, page_number_prefix)

        # Determine the original file name and modify it
        original_filename = uploaded_file.name
        new_filename = f"{original_filename.split('.pdf')[0]}_modified.pdf"

        # Provide download button
        if output_pdf:
            st.download_button(
                label="Download PDF with Header and Footer",
                data=output_pdf,
                file_name=new_filename,
                mime="application/pdf"
            )
    else:
        st.warning("Please upload a PDF file.")