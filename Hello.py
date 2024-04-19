import streamlit as st
import pandas as pd
import os
import anthropic

def get_api_key():
    """Retrieve the API key from Streamlit secrets or environment variables."""
    if 'claude' in st.secrets:
        return st.secrets['claude']['api_key']
    api_key = os.getenv('CLAUDE_API_KEY')
    if api_key is None:
        st.error("API key not found. Set CLAUDE_API_KEY as an environment variable.")
        raise ValueError("API key not found. Set CLAUDE_API_KEY as an environment variable.")
    return api_key

# Initialize the Anthropic client with the API key
client = anthropic.Anthropic(api_key=get_api_key())

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

def chunk_csv_data(csv_data, chunk_size=10000):
    """Split the CSV data into smaller chunks."""
    chunks = []
    for i in range(0, len(csv_data), chunk_size):
        chunk = csv_data[i:i+chunk_size]
        chunks.append(chunk)
    return chunks

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

        # Split the CSV data into chunks
        csv_chunks = chunk_csv_data(csv_data)

        # Process each chunk and get the response from Claude
        response_chunks = []
        for chunk in csv_chunks:
            # Construct the prompt for Claude
            prompt = f"Here is a chunk of the data in CSV format:\n\n{chunk}\n\nUser's query: {user_query}\n\nPlease analyze the data and provide a response to the user's query."

            # Send the prompt to Claude and get the response
            response = client.messages.create(
                model="claude-1.3",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                system="You are a data analysis assistant.",
                temperature=0.7
            )

            response_chunks.append(response.content[0].text)

        # Combine the response chunks and display the result
        combined_response = "\n".join(response_chunks)
        st.write(combined_response)

    except Exception as e:
        st.error(f"Failed to analyze data: {str(e)}")
