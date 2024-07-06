import streamlit as st
import openai
from datetime import datetime
import pytz
import json
import os

# Set page config
st.set_page_config(layout="wide", page_title="Maritime Reporting Chatbot")

# Set up OpenAI API key
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    # If the secret is not found, try to get it from an environment variable
    openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("OpenAI API key not found. Please set it in Streamlit secrets or as an environment variable.")
    st.stop()

# Rest of the code remains the same...

def get_ai_response(user_input, last_report):
    current_time = datetime.now(pytz.utc).strftime("%H:%M:%S")
    
    messages = [
        {"role": "system", "content": TRAINING_DATA},
        {"role": "system", "content": f"The current UTC time is {current_time}. The last report submitted was: {last_report}"},
        {"role": "user", "content": user_input}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        st.error(f"An error occurred while getting AI response: {str(e)}")
        return "I'm sorry, but I encountered an error while processing your request. Please try again later."

def main():
    st.title("Maritime Reporting Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "last_report" not in st.session_state:
        st.session_state.last_report = REPORT_TYPES[0]

    last_report = st.selectbox("Select last report (for testing)", REPORT_TYPES, key="last_report")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I assist you with your maritime reporting?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_ai_response(prompt, last_report)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.experimental_rerun()

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

if __name__ == "__main__":
    main()
