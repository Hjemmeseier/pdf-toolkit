import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def rotate_pdf(file, rotation_angle, pages_to_rotate):
    # Initialize PDF reader and writer
    reader = PdfReader(file)
    writer = PdfWriter()

    # Rotate specified pages and add all pages to writer
    for i, page in enumerate(reader.pages):
        if i in pages_to_rotate:
            page.rotate(rotation_angle)
        writer.add_page(page)

    # Save the rotated PDF to a BytesIO object
    output_pdf = BytesIO()
    writer.write(output_pdf)
    output_pdf.seek(0)
    return output_pdf

def parse_page_ranges(page_ranges, num_pages):
    """
    Parse a string specifying page ranges into a set of page indices.
    Supports ranges (e.g., "1-3"), individual pages (e.g., "5"), open-ended
    ranges (e.g., "4-" for 4 to end or "-4" for start to 4).
    """
    if not page_ranges:
        return set(range(num_pages))  # Rotate all pages if no input

    pages_to_rotate = set()
    for part in page_ranges.split(','):
        if '-' in part:
            start, end = part.split('-')
            start = int(start) - 1 if start else 0
            end = int(end) - 1 if end else num_pages - 1
            pages_to_rotate.update(range(start, end + 1))
        else:
            pages_to_rotate.add(int(part) - 1)
    
    return pages_to_rotate

# Streamlit app interface
st.title("Rotate PDF Pages with Selected Pages Option")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Rotation angle selection
rotation_angle = st.selectbox("Select rotation angle", [90, 180, 270])

# Page selection input
pages_to_rotate = st.text_input("Enter pages to rotate (e.g., 1,2,3,4-6)", value="")

# Button to start rotation
if st.button("Rotate PDF"):
    if uploaded_file is not None:
        # Parse page range input and rotate PDF with specified pages
        num_pages = len(PdfReader(uploaded_file).pages)
        pages_to_rotate_set = parse_page_ranges(pages_to_rotate, num_pages)
        
        rotated_pdf = rotate_pdf(uploaded_file, rotation_angle, pages_to_rotate_set)

        # Provide download button for the rotated PDF
        st.download_button(
            label="Download Rotated PDF",
            data=rotated_pdf,
            file_name="rotated_output.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Please upload a PDF file to proceed.")
