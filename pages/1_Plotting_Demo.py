import streamlit as st
import pandas as pd
import os
from pathlib import Path
import openai
from pandasai import SmartDataframe

def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    if 'openai' in st.secrets:
        return st.secrets['openai']['api_key']
    return os.getenv('OPENAI_API_KEY', 'Your-OpenAI-API-Key')

# Set up the OpenAI API
openai.api_key = get_api_key()

# Set up the directory path
DIR_PATH = Path(__file__).parent / "docs"

# Load the Excel files from the directory
xlsx_files = []
for file_path in DIR_PATH.glob("*.xlsx"):
    xlsx_data = pd.read_excel(file_path)
    xlsx_files.append(xlsx_data)

# Combine the Excel data into a single DataFrame
combined_data = pd.concat(xlsx_files, ignore_index=True)

# Create a SmartDataframe object with LLM configuration
smart_df = SmartDataframe(combined_data)

# Streamlit app setup
st.title("Vessel Data Chat Assistant")
user_query = st.text_input("Ask a question about the vessel data:")

def process_and_display_data(data_string, query):
    """Pass the data and query to LLM for enhanced response."""
    chunk_size = 30000  # Adjust based on token limits for the model
    data_chunks = [data_string[i:i + chunk_size] for i in range(0, len(data_string), chunk_size)]
    
    answer_chunks = []
    for chunk in data_chunks:
        prompt = f"Based on the following information:\n{chunk}\n\nPlease enhance and structure a response for the query: {query}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an intelligent assistant trained to analyze and reframe data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        answer_chunk = response.choices[0].message['content'].strip()
        answer_chunks.append(answer_chunk)
    
    return "\n".join(answer_chunks)

if st.button("Analyze") and user_query:
    # Use PandasAI to answer the user query
    extracted_info = smart_df.chat(user_query)

    if isinstance(extracted_info, pd.DataFrame) and not extracted_info.empty:
        # Convert DataFrame to string for LLM processing
        data_string = extracted_info.to_string(index=False)
        processed_answer = process_and_display_data(data_string, user_query)
        st.write(processed_answer)
    else:
        st.write("No data found based on your query.")
