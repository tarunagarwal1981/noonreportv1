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

def dataframe_to_narrative(df):
    """Convert DataFrame to a narrative string format."""
    if df.empty:
        return "No data found."
    narratives = []
    for _, row in df.iterrows():
        narrative = ', '.join([f"{col} is {row[col]}" for col in df.columns])
        narratives.append(f"Record: {narrative}.")
    return ' '.join(narratives)

# Set up the directory path for loading Excel files.
DIR_PATH = Path(__file__).parent.resolve() / "docs"

# Load Excel files from the specified directory into a list of DataFrames.
xlsx_files = []
for file_path in DIR_PATH.glob("*.xlsx"):
    xlsx_data = pd.read_excel(file_path)
    xlsx_files.append(xlsx_data)

# Combine all loaded DataFrames into a single DataFrame.
combined_data = pd.concat(xlsx_files, ignore_index=True)

# Initialize OpenAI with the retrieved API key.
openai.api_key = get_api_key()

# Create a SmartDataFrame which integrates large language model capabilities.
smart_df = SmartDataframe(combined_data)

# Streamlit UI for user interaction.
st.title("Defect Sheet Chat Assistant")
user_query = st.text_input("Ask a question about the defect sheet data:")

if st.button('Analyze'):
    if user_query:
        # Use PandasAI to answer the user query
        extracted_info = smart_df.chat(user_query)

        # Convert DataFrame to a suitable string format if necessary
        info_string = dataframe_to_narrative(extracted_info) if isinstance(extracted_info, pd.DataFrame) else str(extracted_info)

        # Check if information was extracted and is not empty
        if info_string and info_string != "No data found.":
            # Pass the formatted string to LLM for further processing using ChatCompletion
            chat_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant, trained to summarize and enhance information."},
                    {"role": "user", "content": info_string}
                ],
                max_tokens=150
            )
            processed_answer = chat_response.choices[0].message['content'].strip()
            st.write(processed_answer)
        else:
            st.write("No data found based on your query.")
