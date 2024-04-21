import streamlit as st
import pandas as pd
import os
from pathlib import Path
import openai
from pandasai import SmartDataframe  # Assuming SmartDataframe is the correct class

def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    if 'openai' in st.secrets:
        return st.secrets['openai']['api_key']
    return os.getenv('OPENAI_API_KEY', 'Your-OpenAI-API-Key')

# Set up the directory path
DIR_PATH = Path(__file__).parent.resolve() / "docs"

# Load all Excel files from the directory
xlsx_files = []
for file_path in DIR_PATH.glob("*.xlsx"):
    try:
        df = pd.read_excel(file_path)
        xlsx_files.append(df)
    except Exception as e:
        st.error(f"Failed to load {file_path}: {str(e)}")

# Combine all Excel files into a single DataFrame if any files were loaded
if xlsx_files:
    combined_df = pd.concat(xlsx_files, ignore_index=True)
else:
    st.error("No Excel files found in the directory.")
    combined_df = pd.DataFrame()  # Create an empty DataFrame to prevent further errors

# Set up the OpenAI API
openai.api_key = get_api_key()

# Initialize the SmartDataframe with the combined DataFrame
smart_df = SmartDataframe(combined_df)

# Streamlit app
st.title("Defect Sheet Chat Assistant")
user_query = st.text_input("Ask a question about the defect sheet data:")

if st.button("Analyze"):
    if user_query:
        try:
            # Use SmartDataframe to extract relevant data based on the user's query
            extracted_data = smart_df.chat(user_query)

            # Check the type of extracted_data and handle accordingly
            if isinstance(extracted_data, pd.DataFrame):
                if extracted_data.empty:
                    st.write("No relevant data found for the given query.")
                else:
                    # Process and display the DataFrame data
                    process_and_display_data(extracted_data)
            elif isinstance(extracted_data, str):
                # Handle string responses
                st.write(extracted_data)
            else:
                st.write("Unexpected data type received.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def process_and_display_data(data):
    # Assuming the need to process and display DataFrame data
    chunk_size = 30000  # Adjust based on token limits
    data_chunks = [data.iloc[i:i + chunk_size].to_string(index=False) for i in range(0, len(data), chunk_size)]

    # Process each chunk and get the response from the OpenAI API
    answer_chunks = []
    for chunk in data_chunks:
        prompt = f"The following is the relevant defect sheet data based on the user's query:\n\n{chunk}\n\n"
        prompt += f"Based on the provided data, answer the following question: {user_query}\n"
        prompt += "Please provide a detailed and accurate answer."
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
