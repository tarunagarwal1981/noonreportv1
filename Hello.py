import streamlit as st
import pandas as pd
import os
from pathlib import Path
import openai
from pandasai import SmartDataframe  # Ensure this is correctly imported or adjust as needed

def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    if 'openai' in st.secrets:
        return st.secrets['openai']['api_key']
    return os.getenv('OPENAI_API_KEY', 'Your-OpenAI-API-Key')

# Set up the OpenAI API
openai.api_key = get_api_key()

# Set up the directory path
DIR_PATH = Path(__file__).parent.resolve() / "docs"

# Load all Excel files from the directory into a list of DataFrames
xlsx_files = []
for file_path in DIR_PATH.glob("*.xlsx"):
    try:
        df = pd.read_excel(file_path)
        xlsx_files.append(df)
    except Exception as e:
        st.error(f"Failed to load {file_path}: {str(e)}")

# Combine all Excel files into a single DataFrame
if xlsx_files:
    combined_df = pd.concat(xlsx_files, ignore_index=True)
else:
    combined_df = pd.DataFrame()  # Create an empty DataFrame to prevent further errors
    st.error("No Excel files found or they are empty.")

# Initialize the SmartDataframe
smart_df = SmartDataframe(combined_df)

# Streamlit UI setup
st.title("Defect Sheet Chat Assistant")
user_query = st.text_input("Ask a question about the defect sheet data:")

def process_and_display_data(extracted_data, user_query):
    # Assuming the need to process and display DataFrame data in chunks
    chunk_size = 30000  # Adjust based on token limits
    data_chunks = [extracted_data.iloc[i:i + chunk_size].to_string(index=False) for i in range(0, len(extracted_data), chunk_size)]

    # Process each chunk and get the response from the OpenAI API
    answer_chunks = []
    for chunk in data_chunks:
        prompt = f"The following data needs analysis based on the user's query: {user_query}\n\n{chunk}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        answer_chunk = response.choices[0].message['content'].strip()
        answer_chunks.append(answer_chunk)

    # Combine the answer chunks and display the result
    answer = "\n".join(answer_chunks)
    return answer

if st.button("Analyze") and user_query:
    if combined_df.empty:
        st.write("The combined data is empty. Please check the data files.")
    else:
        try:
            # Use SmartDataframe to extract relevant data based on the user's query
            extracted_data = smart_df.chat(user_query)

            # Check if relevant data is found and process it
            if isinstance(extracted_data, pd.DataFrame) and not extracted_data.empty:
                final_answer = process_and_display_data(extracted_data, user_query)
                st.write(final_answer)
            else:
                st.write("No relevant data found for the given query.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
