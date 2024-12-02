import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path


def has_meaningful_text(text: str) -> bool:
    """Check if the text has meaningful, non-garbage content."""
    return bool(text.strip() and any(char.isalnum() for char in text))


def extract_text_with_pymupdf(pdf_path: str, start_page: int = 0, end_page: int = 10) -> str:
    """Extract text using PyMuPDF for a user-specified range of pages."""
    extracted_text = ""
    try:
        with fitz.open(pdf_path) as doc:
            total_pages = len(doc)
            end_page = min(end_page, total_pages, start_page + 10)
            for page_number in range(start_page, end_page):
                page = doc[page_number]
                page_text = page.get_text("text")
                if has_meaningful_text(page_text):
                    extracted_text += page_text
    except fitz.exceptions.FSError as e:
        print(f"[PyMuPDF] Error reading PDF: {e}")
    return extracted_text


def extract_text_with_ocr(pdf_path: str, start_page: int = 0, end_page: int = 10) -> str:
    """Extract text using OCR for a user-specified range of pages."""
    extracted_text = ""
    try:
        pages = convert_from_path(pdf_path, 500)
        total_pages = len(pages)
        end_page = min(end_page, total_pages, start_page + 10)
        for page_number, page in enumerate(pages[start_page:end_page], start=start_page + 1):
            ocr_text = pytesseract.image_to_string(page)
            if has_meaningful_text(ocr_text):
                extracted_text += ocr_text + "\n"
    except Exception as e:
        print(f"[OCR] Error during OCR processing: {e}")
    return extracted_text
