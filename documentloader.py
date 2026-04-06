import os
from langchain_community.document_loaders import Docx2txtLoader,PyMuPDFLoader

def fileloader(file_path):
    loaders = {
        ".pdf": PyMuPDFLoader,
        ".docx": Docx2txtLoader,
    }

    _,ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext not in loaders:
        raise ValueError(f"Unsupported file type: {ext}")
    
    loader = loaders[ext](file_path)
    documents = loader.load()

    return documents


