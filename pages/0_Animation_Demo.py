import streamlit as st
import openai
from datetime import datetime, time
import pytz
import json
import os
import re
import random
import string

# Set page config
st.set_page_config(layout="wide", page_title="AI-Enhanced Maritime Reporting System")

# Custom CSS for compact layout and history panel
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
    .history-panel {
        background-color: #f1f1f1;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        max-width: 300px;
    }
    .history-panel h3 {
        margin-top: 0;
        margin-bottom: 10px;
    }
    .history-select {
        margin-bottom: 5px;
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

# Define report types
REPORT_TYPES = [
    "Arrival", "Departure", "Begin of offhire", "End of offhire", "Arrival STS",
    "Departure STS", "STS", "Begin canal passage", "End canal passage",
    "Begin of sea passage", "End of sea passage", "Begin Anchoring/Drifting",
    "End Anchoring/Drifting", "Noon (Position) - Sea passage", "Noon (Position) - Port",
    "Noon (Position) - River", "Noon (Position) - Stoppage", "ETA update",
    "Begin fuel change over", "End fuel change over", "Change destination (Deviation)",
    "Begin of deviation", "End of deviation", "Entering special area", "Leaving special area"
]

# Define sections for each report type
REPORT_SECTIONS = {
    "Arrival": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Departure": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Begin of offhire": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "End of offhire": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Arrival STS": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Departure STS": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "STS": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Begin canal passage": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "End canal passage": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Begin of sea passage": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "End of sea passage": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Begin Anchoring/Drifting": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "End Anchoring/Drifting": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Noon (Position) - Sea passage": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Noon (Position) - Port": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Noon (Position) - River": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Noon (Position) - Stoppage": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "ETA update": ["Vessel Data", "Voyage Data", "Position"],
    "Begin fuel change over": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "End fuel change over": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Change destination (Deviation)": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Begin of deviation": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "End of deviation": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Entering special area": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"],
    "Leaving special area": ["Vessel Data", "Voyage Data", "Event Data", "Position", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"]
}

# Prepare the training data as a string
TRAINING_DATA = f"""
You are an AI assistant for an advanced maritime reporting system. Your role is to guide users through creating various types of maritime reports, ensuring compliance with industry standards and regulations.

Key features:
1. Error reduction and data completion assistance
2. Insights generation based on reported data
3. Streamlined reporting process
4. Enhanced accuracy in maritime operational reporting

The valid report types are: {', '.join(REPORT_TYPES)}

When suggesting follow-up reports, consider the history of the last 3-4 reports. Only suggest reports from the list provided above. Do not suggest any reports that are not in this list.

When a user agrees to create a specific report, inform them that the form will appear on the left side of the page with the relevant sections for that report type.

Provide concise and helpful guidance throughout the report creation process.
"""

def generate_random_vessel_name():
    adjectives = ['Swift', 'Majestic', 'Brave', 'Stellar', 'Royal']
    nouns = ['Voyager', 'Explorer', 'Mariner', 'Adventurer', 'Navigator']
    return f"{random.choice(adjectives)} {random.choice(nouns)}"

def generate_random_imo():
    return ''.join(random.choices(string.digits, k=7))

def get_ai_response(user_input, last_reports):
    current_time = datetime.now(pytz.utc).strftime("%H:%M:%S")
    
    context = f"""
    The current UTC time is {current_time}. 
    The last reports submitted were: {' -> '.join(last_reports)}
    
    Please provide guidance based on this context and the user's input.
    Remember to only suggest reports from the provided list.
    """
    
    messages = [
        {"role": "system", "content": TRAINING_DATA},
        {"role": "system", "content": context},
        {"role": "user", "content": user_input}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"I'm sorry, but I encountered an error while processing your request: {str(e)}. Please try again later."

def create_form(report_type):
    st.header(f"New {report_type}")
    
    sections = REPORT_SECTIONS.get(report_type, [])
    
    for section in sections:
        with st.expander(section, expanded=False):
            if section == "Vessel Data":
                st.text_input("Vessel Name", value=generate_random_vessel_name(), key=f"{report_type}_vessel_name")
                st.text_input("IMO Number", value=generate_random_imo(), key=f"{report_type}_imo_number")
            elif section == "Voyage Data":
                st.date_input("Local Date", key=f"{report_type}_local_date")
                st.time_input("Local Time", key=f"{report_type}_local_time")
                st.selectbox("UTC Offset", options=[f"{i:+d}" for i in range(-12, 13)], key=f"{report_type}_utc_offset")
                st.text_input("Voyage ID", key=f"{report_type}_voyage_id")
                st.text_input("Segment ID", key=f"{report_type}_segment_id")
                st.text_input("From Port", key=f"{report_type}_from_port")
                st.text_input("To Port", key=f"{report_type}_to_port")
            # Add more sections with their respective fields
            # ...

    if st.button("Submit Report"):
        st.success(f"{report_type} submitted successfully!")
        return True
    return False

def create_collapsible_history_panel():
    with st.expander("Report History (for testing)", expanded=False):
        st.markdown('<div class="history-panel">', unsafe_allow_html=True)
        st.markdown("<h3>Recent Reports</h3>", unsafe_allow_html=True)
        
        if "report_history" not in st.session_state:
            st.session_state.report_history = ["None"] * 4

        for i in range(4):
            st.session_state.report_history[i] = st.selectbox(
                f"Report {i+1}:",
                ["None"] + REPORT_TYPES,
                key=f"history_{i}",
                index=REPORT_TYPES.index(st.session_state.report_history[i]) + 1 if st.session_state.report_history[i] in REPORT_TYPES else 0
            )

        st.markdown('</div>', unsafe_allow_html=True)

def create_chatbot(last_reports):
    st.header("AI Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I assist you with your maritime reporting?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_ai_response(prompt, last_reports)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Check if a specific report type is mentioned
        for report_type in REPORT_TYPES:
            if report_type.lower() in prompt.lower():
                st.session_state.current_report_type = report_type
                st.session_state.show_form = True
                break
        
        st.experimental_rerun()

def main():
    st.title("AI-Enhanced Maritime Reporting System")
    
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        st.markdown('<div class="reportSection">', unsafe_allow_html=True)
        if 'show_form' in st.session_state and st.session_state.show_form:
            if create_form(st.session_state.current_report_type):
                st.session_state.show_form = False
                st.experimental_rerun()
        else:
            st.write("Please use the AI Assistant to initiate a report.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        create_collapsible_history_panel()
        st.markdown('<div class="chatSection">', unsafe_allow_html=True)
        create_chatbot([report for report in st.session_state.report_history if report != "None"])
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.show_form = False
            st.session_state.current_report_type = None
            st.session_state.report_history = ["None"] * 4
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
