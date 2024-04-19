import streamlit as st
import pandas as pd
import os
import time
from anthropic import Claude

def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    if 'claude' in st.secrets:
        return st.secrets['claude']['api_key']
    api_key = os.getenv('CLAUDE_API_KEY')
    if api_key is None:
        st.error("API key not found. Set CLAUDE_API_KEY as an environment variable.")
        raise ValueError("API key not found. Set CLAUDE_API_KEY as an environment variable.")
    return api_key

# Initialize the Claude client with the API key
client = Claude(api_key=get_api_key())

def list_excel_files(folder_path='docs'):
    """List .xlsx files in the specified folder."""
    file_list = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]
    if not file_list:
        raise FileNotFoundError(f"No Excel files found in folder '{folder_path}'.")
    return file_list

def load_excel(file_name, folder_path='docs'):
    """Load an Excel file into a pandas DataFrame."""
    file_path = os.path.join(folder_path, file_name)
    df = pd.read_excel(file_path)
    return df

st.title('Data Analysis with Claude')

folder_path = 'docs'
try:
    excel_files = list_excel_files(folder_path)
    selected_file = st.selectbox("Choose an Excel file to analyze:", excel_files)
    df = load_excel(selected_file, folder_path)
except Exception as e:
    st.error(str(e))
    df = None

user_query = st.text_input("Enter your query about the data:")

if st.button('Analyze') and df is not None:
    try:
        # Convert DataFrame to CSV string
        csv_data = df.to_csv(index=False)

        # Construct the prompt for Claude
        prompt = f"Here is the data in CSV format:\n\n{csv_data}\n\nUser's query: {user_query}\n\nPlease analyze the data and provide a response to the user's query."

        # Send the prompt to Claude and get the response
        response = client.completion(
            prompt=prompt,
            model="claude-v1",
            max_tokens_to_sample=500,
            temperature=0.7,
        )

        # Display Claude's response
        st.write(response.completion)

    except Exception as e:
        st.error(f"Failed to analyze data: {str(e)}")
