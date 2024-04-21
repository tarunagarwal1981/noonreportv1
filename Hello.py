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

# Set up the directory path
DIR_PATH = Path(__file__).parent.resolve() / "docs"

# Load all Excel files from the directory
xlsx_files = []
for file_path in DIR_PATH.glob("*.xlsx"):
    try:
        df = pd.read_excel(file_path)
        if df is not None:
            xlsx_files.append(df)
    except Exception as e:
        st.error(f"Failed to load {file_path}: {str(e)}")

if not xlsx_files:
    st.error("No Excel files found or they could not be loaded.")
else:
    # Combine all Excel files into a single DataFrame
    combined_df = pd.concat(xlsx_files, ignore_index=True)

    # Set up the OpenAI API
    openai.api_key = get_api_key()

    # Initialize the SmartDataframe
    if combined_df is not None and not combined_df.empty:
        smart_df = SmartDataframe(combined_df)

        # Streamlit app
        st.title("Defect Sheet Chat Assistant")
        user_query = st.text_input("Ask a question about the defect sheet data:")

        if st.button("Analyze") and user_query:
            try:
                # Use SmartDataframe to extract relevant data based on the user's query
                extracted_data = smart_df.chat(user_query)

                # Check the type of extracted_data and handle accordingly
                if extracted_data is not None:
                    if isinstance(extracted_data, pd.DataFrame):
                        if not extracted_data.empty:
                            # Process and display the DataFrame data
                            st.dataframe(extracted_data)
                        else:
                            st.write("No relevant data found for the given query.")
                    elif isinstance(extracted_data, str):
                        st.write(extracted_data)
                    else:
                        st.write("Unexpected data type received.")
                else:
                    st.write("The extraction returned no data.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Failed to combine Excel data or no data to display.")
