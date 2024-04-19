import streamlit as st
import pandas as pd
import os
import time
from openai import OpenAI

def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    if 'openai' in st.secrets:
        return st.secrets['openai']['api_key']
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is None:
        st.error("API key not found. Set OPENAI_API_KEY as an environment variable.")
        raise ValueError("API key not found. Set OPENAI_API_KEY as an environment variable.")
    return api_key

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=get_api_key())

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

def create_assistant():
    """Create an assistant if not already created and return its ID."""
    try:
        assistant = client.beta.assistants.create(
            name="Data Analysis Assistant",
            instructions="Analyze the Excel data and answer questions.",
            model="gpt-4-1106-preview",
            tools=[{"type": "code_interpreter"}]
        )
        return assistant.id
    except Exception as e:
        st.error(f"Failed to create assistant: {str(e)}")
        raise

# Check if assistant already exists and use it, or create a new one
assistant_id = st.secrets["openai"]["assistant_id"]
if not assistant_id:
    assistant_id = create_assistant()

st.title('Data Analysis with OpenAI Assistant')
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
            """Polling function to wait for the run to complete."""
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

    except Exception as e:
        st.error(f"Failed to analyze data: {str(e)}")
