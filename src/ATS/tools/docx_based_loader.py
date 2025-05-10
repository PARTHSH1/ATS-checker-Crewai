from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import pdfplumber
import docx
from bs4 import BeautifulSoup
import os

class InputLoader(BaseTool):
    name: str = "Input Loader Tool"
    description: str = "Loads and parses content from different file formats such as PDF, DOCX, and HTML."
    
    # Define the input schema for the file path (you can also accept file objects if needed)
    class Input(BaseModel):
        file_path: str = Field(..., description="The file path to the resume (PDF, DOCX, HTML).")
    
    def _run(self, file_path: str) -> str:
        """
        This method handles loading and parsing of PDF, DOCX, and HTML files.
        Returns the extracted text content from the provided file.
        """
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            # Load and extract text based on file extension
            if file_extension == '.pdf':
                return self._parse_pdf(file_path)
            elif file_extension == '.docx':
                return self._parse_docx(file_path)
            else:
                return self._parse_html(file_path)
        
        except Exception as e:
            return f"Error occurred while loading the file: {str(e)}"

    def _parse_pdf(self, file_path: str) -> str:
        """
        Extracts text from a PDF file using pdfplumber.
        """
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error parsing PDF: {str(e)}"
    
    def _parse_docx(self, file_path: str) -> str:
        """
        Extracts text from a DOCX file using python-docx.
        """
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Error parsing DOCX: {str(e)}"
    
    def _parse_html(self, file_path: str) -> str:
        """
        Extracts text from an HTML file using BeautifulSoup.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
                text = soup.get_text()
            return text
        except Exception as e:
            return f"Error parsing HTML: {str(e)}"
