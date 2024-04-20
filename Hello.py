import streamlit as st
import pandas as pd
import os
from pathlib import Path
import openai
from pandasai import SmartDataframe

def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    return st.secrets.get('openai', {}).get('api_key', os.getenv('OPENAI_API_KEY', 'Your-OpenAI-API-Key'))

# Set up the directory path for loading Excel files.
DIR_PATH = Path(__file__).resolve().parent / "docs"

# Load Excel files from the specified directory into a list of DataFrames.
xlsx_files = []
for file_path in DIR_PATH.glob("*.xlsx"):
    xlsx_data = pd.read_excel(file_path)
    if xlsx_data is not None:
        xlsx_files.append(xlsx_data)

# Ensure there are files loaded
if not xlsx_files:
    st.error("No Excel files found or they are empty.")
else:
    # Combine all loaded DataFrames into a single DataFrame.
    combined_data = pd.concat(xlsx_files, ignore_index=True)

    # Initialize OpenAI with the retrieved API key.
    openai.api_key = get_api_key()

    # Create a SmartDataFrame which integrates large language model capabilities.
    smart_df = SmartDataframe(combined_data)

    # Streamlit UI for user interaction.
    st.title("Defect Sheet Chat Assistant")
    user_query = st.text_input("Ask a question about the defect sheet data:")

    if st.button('Analyze') and user_query:
        # Use PandasAI to answer the user query
        extracted_info = smart_df.chat(user_query)

        # Validate the extracted_info before proceeding
        if extracted_info is not None and not extracted_info.empty:
            info_string = extracted_info.to_string(index=False) if isinstance(extracted_info, pd.DataFrame) else str(extracted_info)

            # Use OpenAI's LLM to process the information
            if info_string:
                chat_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant, trained to summarize and enhance information."},
                        {"role": "user", "content": info_string}
                    ],
                    max_tokens=150
                )
                processed_answer = chat_response.choices[0].message['content'].strip() if chat_response.choices else "No response from LLM."
                st.write(processed_answer)
            else:
                st.write("Unable to process the data into a suitable format.")
        else:
            st.write("No relevant data extracted from your query.")
