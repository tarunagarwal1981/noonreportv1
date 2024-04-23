import streamlit as st
import pandas as pd
import os
from pathlib import Path
import openai
from pandasai import SmartDataframe

def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    if 'openai' in st.secrets:
        return st.secrets['openai']['api_key']import streamlit as st
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
    return os.getenv('OPENAI_API_KEY', 'Your-OpenAI-API-Key')

openai.api_key = get_api_key()

# Initialize the LLM with the OpenAI API token
llm = OpenAI(api_token=openai.api_key)

# Set up the directory path and load Excel files
DIR_PATH = Path(__file__).parent.resolve() / "docs"
xlsx_files = []
for file_path in DIR_PATH.glob("*.xlsx"):
    xlsx_data = pd.read_excel(file_path)
    xlsx_files.append(xlsx_data)

# Combine the Excel data into a single DataFrame
combined_data = pd.concat(xlsx_files, ignore_index=True)

# Create a SmartDataframe object with LLM configuration
smart_df = SmartDataframe(combined_data, config={"llm": llm})

st.title("Defect Sheet Chat Assistant")
user_query = st.text_input("Ask a question about the defect sheet data:")

def process_and_display_data(data, query):
    chunk_size = 30000
    data_chunks = [data.iloc[i:i + chunk_size].to_string(index=False) for i in range(0, len(data), chunk_size)]
    answer_chunks = []
    for chunk in data_chunks:
        prompt = f"{chunk}\n\nBased on this data, can you provide further insights regarding the query: '{query}'?"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an intelligent assistant trained to analyze and summarize data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        answer_chunk = response.choices[0].message['content'].strip()
        answer_chunks.append(answer_chunk)
    return "\n".join(answer_chunks)

if st.button("Analyze") and user_query:
    extracted_info = smart_df.chat(user_query)

    # Ensure the extracted_info is a DataFrame before proceeding
    if isinstance(extracted_info, pd.DataFrame):
        if not extracted_info.empty:
            processed_answer = process_and_display_data(extracted_info, user_query)
            st.write(processed_answer)
        else:
            st.write("No data found based on your query.")
    elif isinstance(extracted_info, str):  # Handling the case where the output is a string
        st.write("Extracted Info:", extracted_info)  # Directly display the string response
        # Optionally, process this string further using ChatCompletion if needed
    else:
        st.write("Unexpected output type received from SmartDataframe.")
    return os.getenv('OPENAI_API_KEY', 'Your-OpenAI-API-Key')

openai.api_key = get_api_key()

# Adjust the directory path to match the relative path from your script location
DIR_PATH = Path(__file__).parent.parent / "docs"

# Load the Excel files from the directory
excel_files = {}
for file_path in DIR_PATH.glob("*.xlsx"):
    file_name = file_path.stem
    excel_files[file_name] = pd.read_excel(file_path)

st.title("Vessel Data Chat Assistant")
user_query = st.text_input("Ask a question about the vessel data:")

def process_and_display_data(data, query):
    chunk_size = 30000  # Adjust based on token limits for the model
    data_chunks = [data.iloc[i:i + chunk_size].to_string(index=False) for i in range(0, len(data), chunk_size)]
    
    answer_chunks = []
    for chunk in data_chunks:
        prompt = f"{chunk}\n\nBased on the provided vessel data, can you provide insights and analysis related to the following query: {query}?"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an intelligent assistant trained to analyze and provide insights from vessel data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        answer_chunk = response.choices[0].message['content'].strip()
        answer_chunks.append(answer_chunk)
    
    return "\n".join(answer_chunks)

if st.button("Analyze") and user_query:
    if user_query in excel_files:
        relevant_data = excel_files[user_query]
        smart_df = SmartDataframe(relevant_data)
        
        extracted_info = smart_df.chat(user_query)
        if not extracted_info.empty:
            processed_answer = process_and_display_data(extracted_info, user_query)
            st.write(processed_answer)
        else:
            st.write("No data found based on your query.")
    else:
        st.write("No relevant Excel file found for the query.")
