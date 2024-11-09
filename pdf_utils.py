from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import io

def extract_pages(pdf_file, start_page, end_page):
    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    
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
    merger = PdfMerger()
    for file in files:
        merger.append(file)
    
    merged_pdf = io.BytesIO()
    merger.write(merged_pdf)
    merger.close()
    merged_pdf.seek(0)
    
    return merged_pdf
