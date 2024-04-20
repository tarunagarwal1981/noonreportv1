import streamlit as st
import pandas as pd
import os
from pathlib import Path
import openai
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    if 'openai' in st.secrets:
        return st.secrets['openai']['api_key']
    return os.getenv('OPENAI_API_KEY', 'Your-OpenAI-API-Key')  # Suggested use of os.getenv for safety

# Set up the directory path
DIR_PATH = Path(__file__).parent.resolve() / "docs"

# Load the Excel files from the directory
xlsx_files = []
for file_path in DIR_PATH.glob("*.xlsx"):
    xlsx_data = pd.read_excel(file_path)
    xlsx_files.append(xlsx_data)

# Combine the Excel data into a single DataFrame
combined_data = pd.concat(xlsx_files, ignore_index=True)

# Set up the OpenAI API
openai.api_key = get_api_key()
llm = OpenAI(api_token=openai.api_key)

# Create a SmartDataframe object
smart_df = SmartDataframe(combined_data, config={"llm": llm})

# Streamlit app
st.title("Defect Sheet Chat Assistant")
user_query = st.text_input("Ask a question about the defect sheet data:")

if user_query:
    # Use PandasAI to answer the user query
    extracted_info = smart_df.chat(user_query)

    # Check if extracted_info needs further processing
    if extracted_info:
        # Pass the extracted info to LLM for summarization or further processing
        response = openai.Completion.create(
            engine="davinci",  # or another suitable model
            prompt=f"Summarize the following information: {extracted_info}",
            max_tokens=150  # Adjust based on needs
        )
        processed_answer = response.choices[0].text.strip()
        st.write(processed_answer)
    else:
        st.write("No data found based on your query.")
