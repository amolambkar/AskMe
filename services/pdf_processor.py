"""
Purpose: Process pdf
"""

from PyPDF2 import PdfReader


def read_data_from_pdf(pdf_path: str) -> str:
    """
    Function to read pdf and return its text.
    """
    text = ""
    pdf_reader = PdfReader(pdf_path)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
