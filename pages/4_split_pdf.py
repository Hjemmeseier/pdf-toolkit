import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import zipfile

# App title
st.title("PDF Splitter with Page Selection")
st.write("Upload a PDF, select specific pages (or leave blank to select all), and download them as individual files or a ZIP.")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    # Read the PDF
    reader = PdfReader(uploaded_file)
    num_pages = len(reader.pages)
    st.write(f"The uploaded PDF has **{num_pages}** pages.")

    # Input for page range
    page_range = st.text_input(
        "Enter pages to split (e.g., 1,2,4-7) or leave blank to select all:",
        value=""
    )

    # Parse the page range
    def parse_page_range(page_range, total_pages):
        if not page_range.strip():
            return list(range(total_pages))  # Default to all pages
        selected_pages = set()
        for part in page_range.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                selected_pages.update(range(start, end + 1))
            else:
                selected_pages.add(int(part))
        return sorted(p - 1 for p in selected_pages if 1 <= p <= total_pages)

    try:
        selected_pages = parse_page_range(page_range, num_pages)
    except ValueError:
        selected_pages = []
        st.error("Invalid page range. Please ensure the format is correct.")

    if selected_pages:
        if not page_range.strip():
            st.write("No specific pages selected. All pages will be included.")
        else:
            st.write(f"Selected pages: {', '.join(str(p + 1) for p in selected_pages)}")

        # Option for download type
        download_as_zip = st.checkbox("Download as ZIP file", value=True)

        if download_as_zip:
            # Prepare a ZIP file
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for i in selected_pages:
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])

                    # Save each page to a BytesIO buffer
                    pdf_buffer = BytesIO()
                    writer.write(pdf_buffer)
                    pdf_buffer.seek(0)

                    # Add the PDF page to the ZIP file
                    zip_file.writestr(f"Page_{i + 1}.pdf", pdf_buffer.read())

            # Move to the beginning of the ZIP buffer
            zip_buffer.seek(0)

            # Provide download link for the ZIP file
            st.download_button(
                label="Download Selected Pages as ZIP",
                data=zip_buffer,
                file_name="selected_pages.zip",
                mime="application/zip"
            )
        else:
            # Provide individual download buttons
            for i in selected_pages:
                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                # Save each page to a BytesIO buffer
                pdf_buffer = BytesIO()
                writer.write(pdf_buffer)
                pdf_buffer.seek(0)

                st.download_button(
                    label=f"Download Page {i + 1}",
                    data=pdf_buffer,
                    file_name=f"Page_{i + 1}.pdf",
                    mime="application/pdf"
                )
    else:
        st.error("No valid pages selected.")
