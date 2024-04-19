import streamlit as st
import pandas as pd
import os
import time
from openai import OpenAI

# Setup the OpenAI API key
def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    if 'openai' in st.secrets:
        return st.secrets['openai']['api_key']
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is None:
        st.error("API key not found. Set OPENAI_API_KEY as an environment variable.")
        raise ValueError("API key not found. Set OPENAI_API_KEY as an environment variable.")
    return api_key

client = OpenAI(api_key=get_api_key())

# Function to list and load Excel files from a specified folder
def list_excel_files(folder_path='docs'):
    file_list = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]
    if not file_list:
        raise FileNotFoundError(f"No Excel files found in folder '{folder_path}'.")
    return file_list

def load_excel(file_name, folder_path='docs'):
    file_path = os.path.join(folder_path, file_name)
    df = pd.read_excel(file_path)
    return df

# Assistant ID
assistant_id = "your-assistant-id"  # Replace with your actual assistant ID

# Streamlit user interface setup
st.title('Data Analysis with OpenAI Assistant')
folder_path = 'docs'
try:
    excel_files = list_excel_files(folder_path)
    selected_file = st.selectbox("Choose an Excel file to analyze:", excel_files)
    df = load_excel(selected_file, folder_path)
except FileNotFoundError as e:
    st.error(str(e))
    df = None

user_query = st.text_input("Enter your query about the data:")

if st.button('Analyze') and df is not None:
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_query
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    def wait_on_run(run, thread):
        while run.status in ["queued", "in_progress"]:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run

    run = wait_on_run(run, thread)
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for message in messages.data:
        if message.role == "assistant":
            st.write(message.content[0].text['value'])

# Note: No need for st.mainloop() or equivalent
