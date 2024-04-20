import streamlit as st
import pandas as pd
import os
import openai
from pathlib import Path

def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    if 'openai' in st.secrets:
        return st.secrets['openai']['api_key']
    return st.secrets.get('OPENAI_API_KEY', 'Your-OpenAI-API-Key') # Replace 'Your-OpenAI-API-Key' with your actual key

# Set up the directory path
DIR_PATH = Path(__file__).parent.resolve() / "docs"

# Load the Excel file
excel_file = "UOG Vessels Defects List.xlsx"
file_path = DIR_PATH / excel_file
df = pd.read_excel(file_path)

# Set up the OpenAI API
openai.api_key = get_api_key()

# Streamlit app
st.title("Defect Sheet Chat Assistant")

user_query = st.text_input("Ask a question about the defect sheet data:")

if st.button("Analyze"):
    if user_query:
        try:
            # Prepare the prompt for the LLM
            prompt = f"The following is a defect sheet data for a fleet of vessels:\n\n{df.to_string(index=False)}\n\n"
            prompt += f"Based on the provided data, answer the following question: {user_query}\n"
            prompt += "Please provide a detailed and accurate answer, considering the following points:\n"
            prompt += "- Identify the most critical defects for each vessel\n"
            prompt += "- Provide the count of defects for specific vessels or components if requested\n"
            prompt += "- Analyze trends or patterns in the defect data\n"
            prompt += "- Offer insights and recommendations based on the defect information\n"
            prompt += "If the question cannot be answered based on the given data, provide a relevant response indicating the lack of sufficient information."

            # Send the prompt to the OpenAI ChatCompletion API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant analyzing defect sheet data."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.7,
            )

            # Extract and display the generated answer
            answer = response.choices[0].message['content'].strip()
            st.write(answer)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
