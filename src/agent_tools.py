from dataclasses import dataclass
from abc import abstractmethod
from typing import Dict, Any
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import re
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
        """
        Search a web query and return its result.
        
        Args:
            Query: Search prompt to enter into engine
            
        Returns:
            Dictionary containing an abstract and relevant topics
        """
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
            
            result = {
                "success": True if results.get("Abstract", "") else False,
                "abstract": results.get("Abstract", ""),
                "related_topics": results.get("RelatedTopics", []),
                "source": results.get("AbstractSource", ""),
                "query": query
            }

            return result
            
        except requests.RequestException as e:
            return {"error": f"Search failed: {str(e)}"}

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
        
class WebParserTool(Tool):
    def __init__(self):
        super().__init__(
            name="web_parser",
            description="Extract content from any website"
        )
    
    def clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        return text.strip()
    
    def execute(self, url: str) -> Dict[str, Any]:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for tag in ['script', 'style', 'meta', 'link', 'header', 'footer', 'nav']:
                for element in soup.find_all(tag):
                    element.decompose()
            
            # Find main content
            content = None
            for selector in ['article', 'main', '[role="main"]', '#content', '.content', '.post', '.article']:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text(separator='\n')
                    break
            
            # Fallback to body if no main content found
            if not content:
                content = soup.body.get_text(separator='\n')
            
            return {
                "success": True,
                "title": soup.title.string if soup.title else "",
                "content": self.clean_text(content),
                "url": url
            }
            
        except Exception as e:
            return {"error": f"Parsing error: {str(e)}"}
        


if __name__ == "__main__":
    #pdf_tool = PDFParserTool()
    #pdf_result = pdf_tool.execute(file_path=r"src\user_data\Resume.pdf") 
    #print(pdf_result)

    #search = WebSearchTool()
    #results = search.execute("What is SAP Company?")
    #print(results["abstract"])

    search = WebParserTool()
    results = search.execute("https://job-boards.greenhouse.io/andurilindustries/jobs/4552470007?gh_jid=4552470007&gh_src=6a93de687us")
    print(results)