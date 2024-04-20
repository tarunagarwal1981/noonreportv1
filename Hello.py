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

def convert_df_to_string(df):
    """Convert DataFrame to a readable string format."""
    if not df.empty:
        return df.to_string(index=False)
    return "No data found."

def dataframe_to_narrative(df):
    """Convert DataFrame to a narrative string format."""
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

        # Check if extracted_info is DataFrame and convert accordingly
        if isinstance(extracted_info, pd.DataFrame):
            # Convert DataFrame to a suitable string format
            info_string = dataframe_to_narrative(extracted_info)
        elif isinstance(extracted_info, (int, float)):
            info_string = str(extracted_info)
        else:
            info_string = str(extracted_info)  # Assuming it is already in a string or similar format

        if info_string:
            # Pass the formatted string to LLM for further processing
            response = openai.Completion.create(
                engine="davinci",
                prompt=f"Summarize or enhance the following information: {info_string}",
                max_tokens=150
            )
            processed_answer = response.choices[0].text.strip()
            st.write(processed_answer)
        else:
            st.write("No data found based on your query.")
