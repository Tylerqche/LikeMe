from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from PyPDF2 import PdfReader
import requests
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
            description="Search the web using DuckDuckGo"
        )
        self.base_url = "https://api.duckduckgo.com/"
    
    def execute(self, query: str) -> Dict[str, Any]:
        try:
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            results = response.json()
            
            return {
                "success": True,
                "abstract": results.get("Abstract", ""),
                "related_topics": results.get("RelatedTopics", []),
                "source": results.get("AbstractSource", ""),
                "query": query
            }
            
        except requests.RequestException as e:
            return {"error": f"Search failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Error: {str(e)}"}

class PDFParserTool(Tool):
    def __init__(self):
        super().__init__(
            name="pdf_parser",
            description="Extract and analyze text content from PDF files"
        )
    
    def execute(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a PDF file and extract its content.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}
            
            reader = PdfReader(file_path)
            
            result = {
                "success": True,
                "text": [],
                "metadata": reader.metadata,
                "num_pages": len(reader.pages)
            }
            
            for page in reader.pages:
                result["text"].append(page.extract_text())
            
            return result
            
        except Exception as e:
            return {"error": f"Error processing PDF: {str(e)}"}

if __name__ == "__main__":
    pdf_tool = PDFParserTool()
    pdf_result = pdf_tool.execute(file_path=r"C:\Users\tyler\OneDrive\Documents\Design and Description Final.pdf") 

    output_file = r"src\user_data\pdf_output.txt"
    
    # Write the result to a text file
    with open(output_file, 'w') as file:
        file.write(str(pdf_result))  # Write the result as a string

    print(f"PDFParserTool Result has been written to: {output_file}")

    search = WebSearchTool()
    results = search.execute("What is Netflix?")
    print(results)