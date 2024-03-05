from PyPDF2 import PdfMerger
import io

def merge_pdfs(files):
    # Create a PDF merger object
    merger = PdfMerger()

    # Loop through selected files and merge them
    for file in files:
        merger.append(file)

    # Save the merged PDF to a BytesIO object
    merged_pdf = io.BytesIO()
    merger.write(merged_pdf)
    merger.close()

    return merged_pdf