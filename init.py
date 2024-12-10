import logging
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
import os
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentParser(BaseModel):
    """
    This class represents a document parser model. It is used to structure the output of the document parsing process.
    
    The class contains the following fields:
    - document_type: a string indicating the type of the document
    - metadata: a dictionary containing general metadata about the document
    - sections: a list of dictionaries, where each dictionary represents a section in the document
    - images: a list of dictionaries, where each dictionary represents an image found in the document
    """
    document_type: str = Field(description="The type of the document, e.g., 'resume', 'invoice', 'contract', etc.")
    metadata: Dict[str, str] = Field(description="A JSON containing general metadata about the document, such as document number, date, etc.")
    sections: List[Dict[str, Any]] = Field(description="A list of sections in the document, each containing a title and content. The content can be a string, list, or nested dictionary depending on the section.")
    images: List[Dict[str, Any]] = Field(description="A list of images found in the document. Each image entry contains its appearance order and a description.", default=[])

document_parser = JsonOutputParser(pydantic_object=DocumentParser)

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

llm = ChatGroq(
    model = 'llama-3.3-70b-versatile'
)