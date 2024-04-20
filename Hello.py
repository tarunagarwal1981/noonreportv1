import streamlit as st
import pandas as pd
import os
from pathlib import Path
import openai
from pandasai import SmartDataframe  # Assuming it exists, or you might need to adjust this part

def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    if 'openai' in st.secrets:
        return st.secrets['openai']['api_key']
    return os.getenv('OPENAI_API_KEY', 'Your-OpenAI-API-Key')  # Ensure this is set in your environment

# Set up the directory path
DIR_PATH = Path(__file__).parent.resolve() / "docs"

# Load the Excel file
excel_file = "UOG Vessels Defects List.xlsx"
file_path = DIR_PATH / excel_file
df = pd.read_excel(file_path)

# Set up the OpenAI API
openai.api_key = get_api_key()

# Initialize the SmartDataframe
smart_df = SmartDataframe(df)  # Adjust parameters if SmartDataframe requires specific initialization

# Streamlit app
st.title("Defect Sheet Chat Assistant")
user_query = st.text_input("Ask a question about the defect sheet data:")

if st.button("Analyze"):
    if user_query:
        try:
            # Use SmartDataframe to extract relevant data based on the user's query
            extracted_data = smart_df.chat(user_query)  # Check if the .chat() method is appropriate

            # Check if relevant data is found
            if extracted_data.empty:
                st.write("No relevant data found for the given query.")
            else:
                # Split the extracted data into chunks for processing
                chunk_size = 30000  # Adjust chunk size according to your needs
                data_chunks = [extracted_data.iloc[i:i+chunk_size].to_string(index=False) for i in range(0, len(extracted_data), chunk_size)]

                # Process each chunk and get the response from the OpenAI API
                answer_chunks = []
                for chunk in data_chunks:
                    prompt = f"The following is the relevant defect sheet data based on the user's query:\n\n{chunk}\n\n"
                    prompt += f"Based on the provided data, answer the following question: {user_query}\n"
                    prompt += "Please provide a detailed and accurate answer, considering the following points:\n"
                    prompt += "- Identify the most critical defects for each vessel\n"
                    prompt += "- Provide the count of defects for specific vessels or components if requested\n"
                    prompt += "- Analyze trends or patterns in the defect data\n"
                    prompt += "- Offer insights and recommendations based on the defect information\n"
                    prompt += "If the question cannot be answered based on the given data, provide a relevant response indicating the lack of sufficient information."

                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant analyzing defect sheet data."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=500
                    )

                    answer_chunk = response.choices[0].message['content'].strip()
                    answer_chunks.append(answer_chunk)

                # Combine the answer chunks and display the result
                answer = "\n".join(answer_chunks)
                st.write(answer)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
