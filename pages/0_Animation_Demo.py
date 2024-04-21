import streamlit as st
import pandas as pd
import os
from pathlib import Path
import openai
from pandasai import PandasAI

def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    if 'openai' in st.secrets:
        return st.secrets['openai']['api_key']
    return os.getenv('OPENAI_API_KEY', 'Your-OpenAI-API-Key')

# Set up the OpenAI API
openai.api_key = get_api_key()

# Initialize PandasAI with the OpenAI API token
pandas_ai = PandasAI(api_token=openai.api_key)

# Set up the directory path
DIR_PATH = Path(__file__).parent.resolve() / "docs"

# Load the Excel files from the directory
xlsx_files = []
for file_path in DIR_PATH.glob("*.xlsx"):
    xlsx_data = pd.read_excel(file_path)
    xlsx_files.append(xlsx_data)

# Combine the Excel data into a single DataFrame
combined_data = pd.concat(xlsx_files, ignore_index=True)

# Streamlit app setup
st.title("Defect Sheet Chat Assistant")
user_query = st.text_input("Ask a question about the defect sheet data:")

def process_and_display_data(data, query):
    # Assuming the need to process and display DataFrame data in chunks
    chunk_size = 30000  # Adjust based on token limits for the model
    data_chunks = [data.iloc[i:i + chunk_size].to_string(index=False) for i in range(0, len(data), chunk_size)]
    
    # Process each chunk and get the response from PandasAI
    answer_chunks = []
    for chunk in data_chunks:
        prompt = f"{chunk}\n\nCan you provide further insights based on this data regarding the query: {query}?"
        answer_chunk = pandas_ai.ask(combined_data, prompt)
        answer_chunks.append(answer_chunk)
    
    # Combine the answer chunks and display the result
    return "\n".join(answer_chunks)

if st.button("Analyze") and user_query:
    # Use PandasAI to answer the user query
    extracted_info = pandas_ai.ask(combined_data, user_query)
    
    if extracted_info:
        # If the info is too large, process in chunks and display
        processed_answer = process_and_display_data(pd.DataFrame([extracted_info]), user_query)  # Assuming the output can be a single row DataFrame
        st.write(processed_answer)
    else:
        st.write("No data found based on your query.")
