import streamlit as st
import pandas as pd
from datetime import datetime, time
import random
import string
import pytz
import re
import openai
import json
import os

# Set page config
st.set_page_config(layout="wide", page_title="Maritime Reporting System")

# Custom CSS for compact layout
st.markdown("""
<style>
    .reportSection { padding-right: 1rem; }
    .chatSection { padding-left: 1rem; border-left: 1px solid #e0e0e0; }
    .stButton > button { width: 100%; }
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 100%; }
    h1, h2, h3 { margin-top: 0; font-size: 1.2em; }
    .stAlert { margin-top: 1rem; }
    .stNumberInput, .stTextInput, .stSelectbox { 
        padding-bottom: 0.5rem !important; 
    }
    .stNumberInput input, .stTextInput input, .stSelectbox select {
        padding: 0.3rem !important;
        font-size: 0.9em !important;
    }
    .stExpander { 
        border: none !important; 
        box-shadow: none !important;
        margin-bottom: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Set up OpenAI API key
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("OpenAI API key not found. Please set it in Streamlit secrets or as an environment variable.")
    st.stop()

# Define report types and their sequences
REPORT_TYPES = [
    "Arrival", "Departure", "Begin of sea passage", "End of sea passage",
    "Noon (Position) - Sea passage", "Drifting", "Anchor Arrival / FWE",
    "Noon Port / Anchor", "Anchor/STS Departure / SBE", "Berth Arrival / FWE",
    "Berth Departure / SBE", "Begin fuel change over", "End fuel change over",
    "Entering special area", "Leaving special area", "Begin offhire", "End offhire",
    "Begin canal passage", "End canal passage", "Begin Anchoring/Drifting",
    "End Anchoring/Drifting", "Noon (Position) - Port", "Noon (Position) - River",
    "Noon (Position) - Stoppage", "ETA update", "Change destination (Deviation)",
    "Begin of deviation", "End of deviation", "Other event"
]

FOLLOW_UP_REPORTS = {
    "Arrival": ["Departure", "Noon (Position) - Port", "Begin fuel change over", "End fuel change over", "Bunkering", "Off hire"],
    "Departure": ["Begin of sea passage", "Noon (Position) - Port", "ArrivalSTS", "DepartureSTS", "Begin canal passage", "End canal passage", "Begin Anchoring/Drifting", "End Anchoring/Drifting", "Noon (Position) - River", "Noon (Position) - Stoppage", "Begin fuel change over", "End fuel change over", "Entering special area", "Leaving special area"],
    "Begin of sea passage": ["Noon (Position) - Sea passage", "End of sea passage", "Begin fuel change over", "End fuel change over", "Entering special area", "Leaving special area"],
    "End of sea passage": ["Anchor Arrival / FWE", "Berth Arrival / FWE", "Begin Anchoring/Drifting"],
    "Noon (Position) - Sea passage": ["Noon (Position) - Sea passage", "End of sea passage", "Begin fuel change over", "End fuel change over", "Entering special area", "Leaving special area"],
    "Drifting": ["End Anchoring/Drifting", "Begin of sea passage"],
    "Anchor Arrival / FWE": ["Noon Port / Anchor", "Anchor/STS Departure / SBE", "Begin fuel change over", "End fuel change over"],
    "Noon Port / Anchor": ["Noon Port / Anchor", "Anchor/STS Departure / SBE", "Begin fuel change over", "End fuel change over"],
    "Anchor/STS Departure / SBE": ["Begin of sea passage", "Berth Arrival / FWE"],
    "Berth Arrival / FWE": ["Noon (Position) - Port", "Berth Departure / SBE", "Begin fuel change over", "End fuel change over"],
    "Berth Departure / SBE": ["Begin of sea passage", "Anchor Arrival / FWE"]
}

REQUIRED_FOLLOW_UPS = {
    "Begin fuel change over": "End fuel change over",
    "Entering special area": "Leaving special area",
    "Begin offhire": "End offhire",
    "Begin canal passage": "End canal passage",
    "Begin Anchoring/Drifting": "End Anchoring/Drifting",
    "Begin of deviation": "End of deviation"
}

# Prepare the training data as a string
TRAINING_DATA = f"""
You are an AI assistant for a maritime reporting system. Your role is to guide users through creating various types of maritime reports, ensuring they follow the correct sequence and rules.

Report Types: {json.dumps(REPORT_TYPES)}
Follow-up Reports: {json.dumps(FOLLOW_UP_REPORTS)}
Required Follow-ups: {json.dumps(REQUIRED_FOLLOW_UPS)}

Rules:
1. Check if there are any pending reports before allowing new report creation.
2. Validate the sequence of reports based on the FOLLOW_UP_REPORTS dictionary.
3. Noon reports can only be created between 11:00 and 13:00 LT.
4. When a valid report type is requested, inform the user that the report can be initiated.
5. Provide guidance on which reports can be created based on the last report.
6. If an invalid report sequence is requested, inform the user and suggest valid options.

Always maintain a professional and helpful tone. If you're unsure about something, it's okay to say so and offer to provide the information you do have.
"""

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
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"I'm sorry, but I encountered an error while processing your request: {str(e)}. Please try again later."

def generate_random_vessel_name():
    adjectives = ['Swift', 'Majestic', 'Brave', 'Stellar', 'Royal']
    nouns = ['Voyager', 'Explorer', 'Mariner', 'Adventurer', 'Navigator']
    return f"{random.choice(adjectives)} {random.choice(nouns)}"

def generate_random_imo():
    return ''.join(random.choices(string.digits, k=7))

def create_form():
    st.header(f"New {st.session_state.current_report_type} Report")
    
    with st.expander("Vessel Data", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Vessel Name", value=generate_random_vessel_name(), key="vessel_name_input")
        with col2:
            st.text_input("Vessel IMO", value=generate_random_imo(), key="vessel_imo_input")

    with st.expander("Voyage Data", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.date_input("Local Date", key="local_date_input")
        with col2:
            st.time_input("Local Time", key="local_time_input")
        with col3:
            st.selectbox("UTC Offset", [f"{i:+d}" for i in range(-12, 13)], key="utc_offset_input")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Voyage ID", key="voyage_id_input")
        with col2:
            st.text_input("Segment ID", key="segment_id_input")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("From Port", key="from_port_input")
        with col2:
            st.text_input("To Port", key="to_port_input")

    # Add more sections as needed, ensuring unique keys for each input

    if st.button("Submit Report", key="submit_report_button"):
        st.success(f"{st.session_state.current_report_type} report submitted successfully!")
        st.session_state.show_form = False
        st.experimental_rerun()

def create_chatbot():
    st.header("AI Assistant")
    
    if "last_report" not in st.session_state:
        st.session_state.last_report = REPORT_TYPES[0]

    last_report = st.selectbox("Select last report", REPORT_TYPES, key="last_report_select")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I assist you with your maritime reporting?", key="chat_input"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_ai_response(prompt, last_report)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Check if the user's input matches any report type
        mentioned_report = next((report for report in REPORT_TYPES if report.lower() in prompt.lower()), None)
        
        if mentioned_report:
            st.session_state.current_report_type = mentioned_report
            st.session_state.show_form = True
            st.info(f"Initiating {mentioned_report} report. Please fill out the form on the left.")
        elif "Initiating" in response and "report" in response:
            report_type = re.search(r"Initiating (.*?) report", response)
            if report_type:
                st.session_state.current_report_type = report_type.group(1)
                st.session_state.show_form = True
                st.info(f"Initiating {report_type.group(1)} report. Please fill out the form on the left.")
        
        st.experimental_rerun()

    if st.button("Clear Chat", key="clear_chat_button"):
        st.session_state.messages = []
        st.session_state.show_form = False
        st.session_state.current_report_type = None
        st.experimental_rerun()

def main():
    st.title("AI-Enhanced Maritime Reporting System")
    
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        st.markdown('<div class="reportSection">', unsafe_allow_html=True)
        if 'show_form' in st.session_state and st.session_state.show_form:
            create_form()
        else:
            st.write("Please use the chatbot to initiate a report.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chatSection">', unsafe_allow_html=True)
        create_chatbot()
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
