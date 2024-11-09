import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def rotate_pdf(file, rotation_angle):
    # Initialize PDF reader and writer
    reader = PdfReader(file)
    writer = PdfWriter()

    # Rotate each page and add to writer
    for page in reader.pages:
        page.rotate_clockwise(rotation_angle)
        writer.add_page(page)

    # Save the rotated PDF to a BytesIO object
    output_pdf = BytesIO()
    writer.write(output_pdf)
    output_pdf.seek(0)
    return output_pdf

# Streamlit app interface
st.title("Rotate PDF Pages")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Rotation angle selection
rotation_angle = st.selectbox("Select rotation angle", [90, 180, 270])

if uploaded_file is not None:
    # Rotate PDF and generate output
    rotated_pdf = rotate_pdf(uploaded_file, rotation_angle)

    # Provide download button for the rotated PDF
    st.download_button(
        label="Download Rotated PDF",
        data=rotated_pdf,
        file_name="rotated_output.pdf",
        mime="application/pdf"
    )
