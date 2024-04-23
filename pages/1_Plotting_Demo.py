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

openai.api_key = get_api_key()

# Set up the directory path
DIR_PATH = Path(__file__).parent.resolve() / "docs"

# Load the Excel files from the directory
excel_files = []
for file_path in DIR_PATH.glob("*.xlsx"):
    data = pd.read_excel(file_path)
    excel_files.append(data)

st.title("Vessel Data Chat Assistant")
user_query = st.text_input("Ask a question about the vessel data:")

def process_and_display_data(data_text, query):
    # Here data_text is a single string of all responses collected
    prompt = f"{data_text}\n\nCan you provide further insights based on this data regarding the query: {query}?"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an intelligent assistant trained to analyze and summarize data."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message['content'].strip()

if st.button("Analyze") and user_query:
    all_responses = []
    for data_frame in excel_files:
        smart_df = SmartDataframe(data_frame)
        extracted_info = smart_df.chat(user_query)
        # Check if extracted_info is not empty
        if extracted_info:
            if isinstance(extracted_info, pd.DataFrame) and not extracted_info.empty:
                all_responses.append(extracted_info.to_string(index=False))
            elif isinstance(extracted_info, str):
                all_responses.append(extracted_info)

    if all_responses:
        combined_responses = "\n".join(all_responses)
        processed_answer = process_and_display_data(combined_responses, user_query)
        st.write(processed_answer)
    else:
        st.write("No data found based on your query.")
