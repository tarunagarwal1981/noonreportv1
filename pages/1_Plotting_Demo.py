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

DIR_PATH = Path(__file__).parent / "docs"
xlsx_files = {}
for file_path in DIR_PATH.glob("*.xlsx"):
    file_name = file_path.stem
    xlsx_files[file_name] = pd.read_excel(file_path)

st.title("Vessel Data Chat Assistant")
user_query = st.text_input("Ask a question about the vessel data:")

def process_and_display_data(data_string, query):
    chunk_size = 30000
    data_chunks = [data_string[i:i + chunk_size] for i in range(0, len(data_string), chunk_size)]
    answer_chunks = []
    for chunk in data_chunks:
        prompt = f"{chunk}\n\nCan you provide further insights based on this data regarding the query: {query}?"
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
    all_responses = []
    for file_name, data in xlsx_files.items():
        smart_df = SmartDataframe(data)
        extracted_info = smart_df.chat(user_query)
        if extracted_info:
            all_responses.append(str(extracted_info))

    if all_responses:
        combined_info = " ".join(all_responses)
        processed_answer = process_and_display_data(combined_info, user_query)
        st.write(processed_answer)
    else:
        st.write("No data found based on your query.")
