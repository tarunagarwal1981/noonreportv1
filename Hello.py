import streamlit as st
import pandas as pd
import os
import openai
from pathlib import Path
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    if 'openai' in st.secrets:
        return st.secrets['openai']['api_key']
    return st.secrets.get('OPENAI_API_KEY', 'Your-OpenAI-API-Key') # Replace 'Your-OpenAI-API-Key' with your actual key

# Set up the directory path
DIR_PATH = Path(__file__).parent.resolve() / "UOG"

# Load the Excel files from the directory
xlsx_files = []
for file_path in DIR_PATH.glob("*.xlsx"):
    xlsx_data = pd.read_excel(file_path)
    xlsx_files.append(xlsx_data)

# Set up the OpenAI API
openai.api_key = get_api_key()
llm = OpenAI(api_token=openai.api_key)

# Combine the Excel data into a single DataFrame
combined_data = pd.concat(xlsx_files, ignore_index=True)

# Create a SmartDataframe object
smart_df = SmartDataframe(combined_data, config={"llm": llm})

# Streamlit app
st.title("Defect Sheet Chat Assistant")

user_query = st.text_input("Ask a question about the defect sheet data:")

if st.button("Analyze"):
    if user_query:
        try:
            # Use PandasAI to extract data from the Excel file
            answer = smart_df.chat(user_query)
            
            # Check the type of the answer and format it accordingly
            if isinstance(answer, pd.DataFrame):
                extracted_data = answer.to_string(index=False)
            elif isinstance(answer, str):
                extracted_data = answer
            elif isinstance(answer, (int, float)):
                extracted_data = str(answer)
            else:
                st.write("Unsupported data type extracted from the Excel file.")
                extracted_data = None
            
            if extracted_data:
                # Pass the extracted data to the LLM for further processing
                prompt = f"User's query: {user_query}\n\nExtracted data:\n{extracted_data}\n\nPlease provide a summarized and enhanced answer to the user's query based on the extracted data."
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant, trained to summarize and enhance information."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150
                )
                
                processed_answer = response['choices'][0]['message']['content'].strip()
                st.write(processed_answer)
        except Exception as e:
            st.write(f"An error occurred: {str(e)}")
