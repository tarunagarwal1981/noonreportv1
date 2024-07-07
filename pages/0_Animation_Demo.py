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

# Custom CSS for compact layout (as before)
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

# Define report types and their sequences (as before)
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
    # (as before)
}

REQUIRED_FOLLOW_UPS = {
    # (as before)
}

# Define report sections and their applicability
REPORT_SECTIONS = {
    "Vessel data": {
        "applicable_to": "All reports",
        "note": "Auto fill"
    },
    "Voyage data": {
        "applicable_to": "All reports",
        "note": "Voyage ID will be same from one departure to arrival, segment ID can change"
    },
    "Event data": {
        "applicable_to": "All reports",
        "special_cases": {
            "loading_unloading_hrs": "Not for reports between arrival and departure",
            "drifting": "Only between begin and end drifting reports",
            "manoeuvering": "Only between EOSP and BOSP reports",
            "anchor_time": "Only between begin anchor and end anchor reports"
        }
    },
    "Position": {
        "applicable_to": "All reports"
    },
    "Cargo": {
        "applicable_to": "All reports"
    },
    "Fuel Consumption": {
        "applicable_to": "All reports"
    },
    "ROB": {
        "applicable_to": "All reports"
    },
    "Fuel allocation": {
        "applicable_to": "All reports",
        "note": "Grey out DP part"
    },
    "Machinery": {
        "Main Engine": {
            "applicable_to": ["Noon (Position) - Sea passage", "End of sea passage"]
        },
        "Auxiliary Engine": {
            "applicable_to": "All reports"
        }
    },
    "Weather": {
        "applicable_to": "All reports"
    },
    "Draft": {
        "applicable_to": "All reports"
    }
}

# Prepare the training data as a string
TRAINING_DATA = f"""
You are an AI assistant for a maritime reporting system. Your role is to guide users through creating various types of maritime reports, ensuring they follow the correct sequence and rules.

Report Types: {json.dumps(REPORT_TYPES)}
Follow-up Reports: {json.dumps(FOLLOW_UP_REPORTS)}
Required Follow-ups: {json.dumps(REQUIRED_FOLLOW_UPS)}
Report Sections and Applicability: {json.dumps(REPORT_SECTIONS, indent=2)}

Rules:
1. Check if there are any pending reports before allowing new report creation.
2. Validate the sequence of reports based on the FOLLOW_UP_REPORTS dictionary.
3. Noon reports can only be created between 11:00 and 13:00 LT.
4. When a valid report type is requested, inform the user that the report can be initiated.
5. Provide guidance on which reports can be created based on the last report.
6. If an invalid report sequence is requested, inform the user and suggest valid options.
7. When guiding users through report creation, refer to the REPORT_SECTIONS to know which sections are applicable for each report type.
8. Pay attention to special cases in the Event data section and Machinery section.

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

# Rest of the functions (main, create_form, etc.) remain the same

def create_chatbot():
    st.header("AI Assistant")
    
    if "last_report" not in st.session_state:
        st.session_state.last_report = REPORT_TYPES[0]

    last_report = st.selectbox("Select last report", REPORT_TYPES, key="last_report")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I assist you with your maritime reporting?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_ai_response(prompt, last_report)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Check if the AI suggests creating a report
        if "Initiating" in response and "report" in response:
            report_type = re.search(r"Initiating (.*?) report", response)
            if report_type:
                st.session_state.current_report_type = report_type.group(1)
                st.session_state.show_form = True
        
        st.experimental_rerun()

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.show_form = False
        st.session_state.current_report_type = None
        st.experimental_rerun()

if __name__ == "__main__":
    main()
