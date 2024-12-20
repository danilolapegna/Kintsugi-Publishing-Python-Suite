import os
import logging
from typing import List

def ensure_directory(path: str):
    """Ensure that a directory exists, create if not."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def find_documents(directory: str, extensions: List[str]) -> List[str]:
    """
    Recursively find all documents in given directory 
    that have one of the specified extensions.
    """
    docs = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if any(f.lower().endswith(ext) for ext in extensions):
                docs.append(os.path.join(root, f))
    return docs

def load_text_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
