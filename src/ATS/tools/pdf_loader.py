from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import fitz # PyMuPDF

class PDFLoaderInput(BaseModel):
    file_path: str = Field(..., description="Path to the PDF file")

class PDFLoaderTool(BaseTool):
    name: str = "Load PDF Content"
    description: str = """Useful to load and extract text content from a PDF file. "
    "Input should be a path to the local PDF file."""
    args_schema: type[BaseModel] = PDFLoaderInput
    def _run(self, file_path: str) -> str:
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
                return text.strip()
        except Exception as e:
            return f"Failed to load PDF: {str(e)}"

async def _arun(self, file_path: str) -> str:
    raise NotImplementedError("Async not implemented")