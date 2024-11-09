from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import io

def extract_pages(pdf_file, start_page, end_page):
    """
    Extracts a range of pages from a PDF file.
    
    Parameters:
    pdf_file (BytesIO): Uploaded PDF file as a BytesIO object.
    start_page (int): Start page number (1-based index).
    end_page (int): End page number (1-based index).
    
    Returns:
    BytesIO: A BytesIO object with the extracted PDF content.
    """
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

def merge_pdfs(files):
    """
    Merges multiple PDF files into a single PDF.
    
    Parameters:
    files (list): List of BytesIO objects for each PDF file to be merged.
    
    Returns:
    BytesIO: A BytesIO object with the merged PDF content.
    """
    merger = PdfMerger()
    for file in files:
        merger.append(file)
    
    merged_pdf = io.BytesIO()
    merger.write(merged_pdf)
    merger.close()
    merged_pdf.seek(0)
    
    return merged_pdf
