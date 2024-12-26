from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from PyPDF2 import PdfReader
from typing import Optional, Dict, Any
import os


@dataclass
class Tool:
    name: str
    description: str
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        pass

class WebSearchTool(Tool):
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information about a given query"
        )
    
    def execute(self, query: str) -> str:
        # Simulate web search for demo purposes
        return f"Found information about: {query}"

class PDFParserTool(Tool):
    def __init__(self):
        super().__init__(
            name="pdf_parser",
            description="Extract and analyze text content from PDF files"
        )
    
    def execute(self, file_path: str, pages: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        Parse a PDF file and extract its content.
        
        Args:
            file_path: Path to the PDF file
            pages: Optional list of specific pages to parse. If None, parses all pages.
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}
                
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            
            # Initialize results
            result = {
                "total_pages": total_pages,
                "extracted_text": "",
                "metadata": reader.metadata if reader.metadata else {},
                "pages_parsed": []
            }
            
            # Determine which pages to parse
            pages_to_parse = pages if pages else range(total_pages)
            
            # Extract text from specified pages
            for page_num in pages_to_parse:
                if 0 <= page_num < total_pages:
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    result["extracted_text"] += f"\n--- Page {page_num + 1} ---\n{text}"
                    result["pages_parsed"].append(page_num + 1)
            
            return result