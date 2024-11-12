import streamlit as st
import fitz  # PyMuPDF
from io import BytesIO

def add_header_footer(pdf_file, header_text, footer_text, page_number):
    # Open the PDF file
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    
    # Check if the specified page exists
    if page_number < 1 or page_number > pdf_document.page_count:
        st.error("Page number is out of range.")
        return None

    # Process the specified page
    page = pdf_document[page_number - 1]  # Convert to zero-based index
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

# Streamlit app interface
st.title("Add Header and Footer to a Specific Page in PDF")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Header and Footer inputs
header_text = st.text_input("Header Text", "")
footer_text = st.text_input("Footer Text", "")

# Page selection input
page_number = st.number_input("Page Number to Apply Header/Footer", min_value=1, step=1)

# Button to add header and footer
if st.button("Add Header and Footer"):
    if uploaded_file is not None:
        # Add header and footer to the specified page
        output_pdf = add_header_footer(uploaded_file, header_text, footer_text, page_number)

        if output_pdf:
            # Provide download button
            st.download_button(
                label="Download PDF with Header and Footer",
                data=output_pdf,
                file_name="pdf_with_header_footer.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Please upload a PDF file.")