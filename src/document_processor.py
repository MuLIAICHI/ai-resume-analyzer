import pandas as pd
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os

@st.cache_data
def load_and_process_pdf(file):
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(file.getvalue())
            tmp_file_path = tmp_file.name

        # Use the temporary file path with PyPDFLoader
        loader = PyPDFLoader(tmp_file_path)
        documents = loader.load()
        
        # Create a DataFrame with the PDF content
        df = pd.DataFrame({
            'page_number': range(1, len(documents) + 1),
            'content': [doc.page_content for doc in documents]
        })
        
        return documents, df
    except Exception as e:
        st.error(f"Error loading PDF: {str(e)}")
        return None, None
    finally:
        # Clean up the temporary file
        if 'tmp_file_path' in locals():
            os.unlink(tmp_file_path)