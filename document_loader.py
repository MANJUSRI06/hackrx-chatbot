from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests
import tempfile
import os

def load_pdf_from_url(url):
    """Download a PDF from a URL and split into text chunks."""
    response = requests.get(url)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name
    return split_pdf(tmp_path)

def load_pdf_from_file(file_path):
    """Load a local PDF file and split into text chunks."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF not found at: {file_path}")
    return split_pdf(file_path)

def split_pdf(file_path):
    """Split PDF into smaller chunks for embeddings."""
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(pages)
    
    return chunks
