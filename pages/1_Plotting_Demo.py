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
DIR_PATH = Path(__file__).parent.parent.resolve() / "docs"

# Load the Excel files from the directory
excel_files = {}
for file_path in DIR_PATH.glob("*.xlsx"):
    file_name = file_path.stem
    excel_files[file_name] = pd.read_excel(file_path)

# Streamlit app setup
st.title("Vessel Data Chat Assistant")
user_query = st.text_input("Ask a question about the vessel data:")

def process_and_display_data(data, query):
    # Assuming the need to process and display DataFrame data in chunks
    chunk_size = 30000  # Adjust based on token limits for the model
    data_chunks = [data.iloc[i:i + chunk_size].to_string(index=False) for i in range(0, len(data), chunk_size)]
    
    # Process each chunk and get the response from the OpenAI API
    answer_chunks = []
    for chunk in data_chunks:
        prompt = f"{chunk}\n\nBased on the provided vessel data, can you provide insights and analysis related to the following query: {query}? Please frame your response with relevant context to the query."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an intelligent assistant trained to analyze and provide insights from vessel data. Frame your responses with context relevant to the given query."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        answer_chunk = response.choices[0].message['content'].strip()
        answer_chunks.append(answer_chunk)
    
    # Combine the answer chunks and display the result
    return "\n".join(answer_chunks)

if st.button("Analyze") and user_query:
    # Provide information about the Excel files to PandasAI
    excel_file_info = "The available Excel files are:\n"
    excel_file_info += "1. UOG vessels defect list.xlsx: Contains details of all the defects like their name, actions taken, vessel name, status, cost, etc.\n"
    excel_file_info += "2. UOG - AE Status Excel.xlsx: Contains various KPIs with different aux engines (AEs) of different vessels.\n"
    excel_file_info += "3. UOM - AE Health Status Excel.xlsx: Contains the rating of the different aux engines of the vessels."

    # Use OpenAI API to find the relevant Excel sheet and answer the user query
    excel_file_query = f"{excel_file_info}\n\nBased on the user's query: '{user_query}', which Excel file among {list(excel_files.keys())} is most likely to contain the relevant information to answer the query?"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an intelligent assistant trained to analyze and provide insights from vessel data. Frame your responses with context relevant to the given query."},
            {"role": "user", "content": excel_file_query}
        ],
        max_tokens=100
    )
    relevant_file = response.choices[0].message['content'].strip()
    
    if relevant_file in excel_files:
        relevant_data = excel_files[relevant_file]
        smart_df = SmartDataframe(relevant_data)
        
        # Use PandasAI to answer the user query with context
        prompt = f"{excel_file_info}\n\nBased on the data in '{relevant_file}', provide an insightful answer to the following question: {user_query}. Ensure your response includes relevant context related to the query."
        extracted_info = smart_df.chat(prompt)
        
        if not extracted_info.empty:
            # Create a de-fragmented copy of the DataFrame
            extracted_df = extracted_info.copy()
            
            # Process and display the de-fragmented DataFrame
            processed_answer = process_and_display_data(extracted_df, user_query)
            st.write(processed_answer)
        else:
            st.write("No data found based on your query.")
    else:
        st.write(f"No relevant Excel file found for the query: {user_query}")
