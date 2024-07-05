import streamlit as st
import pandas as pd
from datetime import datetime, time
import pytz
import re

# Set page config
st.set_page_config(layout="wide", page_title="Maritime Reporting System")

# Custom CSS for compact layout
st.markdown("""
<style>
    .reportSection { padding-right: 1rem; }
    .chatSection { padding-left: 1rem; border-left: 1px solid #e0e0e0; }
    .stButton > button { width: 100%; }
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 100%; }
    .stAlert { margin-top: 1rem; }
    h1, h2, h3 { margin-top: 0; }
</style>
""", unsafe_allow_html=True)

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

def is_valid_sequence(last_report, new_report):
    if last_report in FOLLOW_UP_REPORTS:
        return new_report in FOLLOW_UP_REPORTS[last_report]
    return True

def is_noon_report_time():
    now = datetime.now(pytz.utc)
    return 11 <= now.hour <= 13

def get_pending_reports(last_report):
    return [REQUIRED_FOLLOW_UPS[last_report]] if last_report in REQUIRED_FOLLOW_UPS else []

def get_chatbot_response(last_report, user_input):
    user_input = user_input.lower()
    pending_reports = get_pending_reports(last_report)
    
    if pending_reports:
        return f"Before creating a new report, you need to complete the following report: {pending_reports[0]}"
    
    if re.search(r'\b(create|make|start|begin|new)\b.*\breport\b', user_input):
        valid_reports = FOLLOW_UP_REPORTS.get(last_report, REPORT_TYPES)
        
        if "noon" in last_report.lower() and not is_noon_report_time():
            valid_reports = [report for report in valid_reports if "noon" not in report.lower()]
        
        report_options = "\n".join([f"- {report}" for report in valid_reports])
        return f"Your last report was '{last_report}'. You can create one of the following reports:\n{report_options}\nWhich report would you like to create?"
    
    for report_type in REPORT_TYPES:
        if report_type.lower() in user_input:
            if is_valid_sequence(last_report, report_type):
                if "noon" in report_type.lower() and not is_noon_report_time():
                    return "Noon reports can only be created between 11:00 and 13:00 LT."
                if "fuel change over" in report_type.lower():
                    return f"Initiating {report_type}. This can be done during any state. Please provide the necessary details."
                return f"Initiating {report_type}. Please provide the necessary details."
            else:
                return f"Invalid report sequence. The {report_type} report cannot follow the {last_report} report. Please choose a valid report type from the list provided earlier."
    
    return "I'm not sure what specific action you want to take. You can say things like:\n" \
           "- 'Create a new report'\n" \
           "- Or specify a report type like 'Create a Departure report'\n" \
           "How can I assist you with your maritime reporting?"

def main():
    st.title("AI-Enhanced Maritime Reporting System")
    
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        st.markdown('<div class="reportSection">', unsafe_allow_html=True)
        create_form()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chatSection">', unsafe_allow_html=True)
        create_chatbot()
        st.markdown('</div>', unsafe_allow_html=True)

def create_form():
    st.header("Maritime Report Form")
    
    with st.form(key='report_form'):
        st.subheader("Vessel Data Section")
        st.text_input("Vessel Name")
        st.text_input("IMO Number")
        
        st.subheader("Voyage Data Section")
        st.text_input("Voyage ID")
        st.text_input("Segment ID")
        
        st.subheader("Event Data Section")
        st.selectbox("Event Type", REPORT_TYPES)
        st.text_input("Loading/Unloading Hours")
        st.text_input("Drifting Hours")
        st.text_input("Maneuvering Hours")
        st.text_input("Anchor Time")
        
        st.subheader("Position Section")
        st.text_input("Latitude")
        st.text_input("Longitude")
        
        st.subheader("Cargo Section")
        st.text_input("Cargo Type")
        st.text_input("Cargo Weight")
        
        st.subheader("Fuel Consumption Section")
        st.text_input("Fuel Type")
        st.text_input("Fuel Consumption")
        
        st.subheader("ROB Section")
        st.text_input("Fuel ROB")
        
        st.subheader("Fuel Allocation Section")
        st.text_input("DP Part")
        
        st.subheader("Machinery Section")
        st.text_input("Main Engine Data")
        st.text_input("Auxiliary Engine Data")
        
        st.subheader("Weather Section")
        st.text_input("Wind Direction")
        st.text_input("Wind Speed")
        st.text_input("Sea State")
        
        st.subheader("Draft Section")
        st.text_input("Draft")
        
        st.form_submit_button(label='Submit Report')

def clear_chat_history():
    st.session_state.messages = []
    # Removed the line that tries to reset last_report

def create_chatbot():
    st.header("AI Assistant")
    
    if "last_report" not in st.session_state:
        st.session_state.last_report = REPORT_TYPES[0]

    last_report = st.selectbox("Select last report (for testing)", REPORT_TYPES, key="last_report")

    if st.button("Clear Chat"):
        clear_chat_history()
        st.experimental_rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I assist you with your maritime reporting?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_chatbot_response(last_report, prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.experimental_rerun()

if __name__ == "__main__":
    main()
