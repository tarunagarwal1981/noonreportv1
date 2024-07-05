import streamlit as st
import pandas as pd
from datetime import datetime, time
import pytz
import re

# Set page config
st.set_page_config(layout="wide", page_title="Maritime Reporting System")

# Custom CSS
st.markdown("""
<style>
    .reportSection { padding-right: 1rem; }
    .chatSection { padding-left: 1rem; border-left: 1px solid #e0e0e0; }
    .stButton > button { width: 100%; }
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 100%; }
    h1, h2, h3 { margin-top: 0; }
    .stAlert { margin-top: 1rem; }
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
                    st.session_state.current_report_type = report_type
                    return f"Initiating {report_type}. This can be done during any state. Please fill out the form on the left side of the screen with the necessary details."
                st.session_state.current_report_type = report_type
                return f"Initiating {report_type}. Please fill out the form on the left side of the screen with the necessary details."
            else:
                return f"Invalid report sequence. The {report_type} report cannot follow the {last_report} report. Please choose a valid report type from the list provided earlier."
    
    return "I'm not sure what specific action you want to take. You can say things like:\n" \
           "- 'Create a new report'\n" \
           "- Or specify a report type like 'Create a Departure report'\n" \
           "How can I assist you with your maritime reporting?"

def create_report_form(report_type):
    st.subheader(f"{report_type} Report")
    
    # Vessel data (Auto fill for all reports)
    st.subheader("Vessel Data")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Vessel Name", key="vessel_name")
    with col2:
        st.text_input("IMO Number", key="imo_number")
    
    # Voyage data
    st.subheader("Voyage Data")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Voyage ID", key="voyage_id")
    with col2:
        st.text_input("Segment ID", key="segment_id")
    
    # Event data
    st.subheader("Event Data")
    if "drifting" in report_type.lower():
        st.number_input("Drifting Hours", min_value=0.0, step=0.1, key="drifting_hours")
    if report_type in ["End of sea passage", "Begin of sea passage"]:
        st.number_input("Maneuvering Time (hours)", min_value=0.0, step=0.1, key="maneuvering_time")
    if "anchor" in report_type.lower():
        st.number_input("Anchor Time (hours)", min_value=0.0, step=0.1, key="anchor_time")
    
    # Position (All reports)
    st.subheader("Position")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Latitude", key="latitude")
    with col2:
        st.text_input("Longitude", key="longitude")
    
    # Cargo (All reports)
    st.subheader("Cargo")
    st.number_input("Cargo Quantity (MT)", min_value=0.0, step=0.1, key="cargo_quantity")
    
    # Fuel Consumption (All reports)
    st.subheader("Fuel Consumption")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("HFO Consumption (MT)", min_value=0.0, step=0.1, key="hfo_consumption")
    with col2:
        st.number_input("LFO Consumption (MT)", min_value=0.0, step=0.1, key="lfo_consumption")
    with col3:
        st.number_input("MGO Consumption (MT)", min_value=0.0, step=0.1, key="mgo_consumption")
    
    # ROB (All reports)
    st.subheader("Remaining On Board (ROB)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("HFO ROB (MT)", min_value=0.0, step=0.1, key="hfo_rob")
    with col2:
        st.number_input("LFO ROB (MT)", min_value=0.0, step=0.1, key="lfo_rob")
    with col3:
        st.number_input("MGO ROB (MT)", min_value=0.0, step=0.1, key="mgo_rob")
    
    # Fuel allocation (All reports)
    st.subheader("Fuel Allocation")
    st.text_area("Fuel Allocation Details", key="fuel_allocation")
    
    # Main Engine (Only for noon at sea reports and EOSP reports)
    if report_type in ["Noon (Position) - Sea passage", "End of sea passage"]:
        st.subheader("Main Engine")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Main Engine RPM", min_value=0, step=1, key="me_rpm")
        with col2:
            st.number_input("Main Engine Load (%)", min_value=0, max_value=100, step=1, key="me_load")
    
    # Aux Engines (All reports)
    st.subheader("Auxiliary Engines")
    st.text_area("Auxiliary Engines Details", key="aux_engines_details")
    
    # Weather (All reports)
    st.subheader("Weather")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Wind Speed (knots)", min_value=0, step=1, key="wind_speed")
        st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key="wind_direction")
    with col2:
        st.number_input("Sea State (Douglas Scale)", min_value=0, max_value=9, step=1, key="sea_state")
        st.number_input("Swell Height (m)", min_value=0.0, step=0.1, key="swell_height")
    
    # Draft (All reports)
    st.subheader("Draft")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Forward Draft (m)", min_value=0.0, step=0.1, key="forward_draft")
    with col2:
        st.number_input("Aft Draft (m)", min_value=0.0, step=0.1, key="aft_draft")
    
    if st.button("Submit Report"):
        st.success(f"{report_type} report submitted successfully!")

def clear_chat_history():
    st.session_state.messages = []
    # We're not clearing the current_report_type here

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

def main():
    st.title("AI-Enhanced Maritime Reporting System")
    
    # Initialize current_report_type if it doesn't exist
    if 'current_report_type' not in st.session_state:
        st.session_state.current_report_type = None
    
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        st.markdown('<div class="reportSection">', unsafe_allow_html=True)
        if st.session_state.current_report_type:
            create_report_form(st.session_state.current_report_type)
        else:
            st.write("Please use the chatbot to initiate a report.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chatSection">', unsafe_allow_html=True)
        create_chatbot()
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
