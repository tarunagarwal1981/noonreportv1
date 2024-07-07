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
            st.text_input("Vessel Name", value=generate_random_vessel_name(), key="vessel_name")
        with col2:
            st.text_input("Vessel IMO", value=generate_random_imo(), key="vessel_imo")

    with st.expander("Voyage Data", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.date_input("Local Date", key="local_date")
        with col2:
            st.time_input("Local Time", key="local_time")
        with col3:
            st.selectbox("UTC Offset", [f"{i:+d}" for i in range(-12, 13)], key="utc_offset")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Voyage ID", key="voyage_id")
        with col2:
            st.text_input("Segment ID", key="segment_id")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("From Port", key="from_port")
        with col2:
            st.text_input("To Port", key="to_port")

    with st.expander("Event Data", expanded=False):
        st.write(f"Event Type: {st.session_state.current_report_type}")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.number_input("Time Elapsed (hrs)", min_value=0.0, step=0.1, format="%.1f", key="time_elapsed")
        with col2:
            st.number_input("Sailing Time (hrs)", min_value=0.0, step=0.1, format="%.1f", key="sailing_time")
        with col3:
            st.number_input("Anchor Time (hrs)", min_value=0.0, step=0.1, format="%.1f", key="anchor_time")
        with col4:
            st.number_input("Maneuvering (hrs)", min_value=0.0, step=0.1, format="%.1f", key="maneuvering_time")

    with st.expander("Position", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Latitude", min_value=-90.0, max_value=90.0, step=0.000001, format="%.6f", key="latitude")
        with col2:
            st.number_input("Longitude", min_value=-180.0, max_value=180.0, step=0.000001, format="%.6f", key="longitude")

    with st.expander("Cargo", expanded=False):
        st.number_input("Cargo Weight (mt)", min_value=0.0, step=0.1, format="%.1f", key="cargo_weight")

    with st.expander("Fuel Consumption", expanded=False):
        for engine in ["ME", "AE", "Boiler"]:
            st.subheader(f"{engine} Consumption")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.number_input(f"{engine} LFO (mt)", min_value=0.0, step=0.1, format="%.1f", key=f"{engine.lower()}_lfo")
            with col2:
                st.number_input(f"{engine} MGO (mt)", min_value=0.0, step=0.1, format="%.1f", key=f"{engine.lower()}_mgo")
            with col3:
                st.number_input(f"{engine} LNG (mt)", min_value=0.0, step=0.1, format="%.1f", key=f"{engine.lower()}_lng")
            with col4:
                st.number_input(f"{engine} Other (mt)", min_value=0.0, step=0.1, format="%.1f", key=f"{engine.lower()}_other")

    with st.expander("Remaining on Board (ROB)", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.number_input("LFO ROB (mt)", min_value=0.0, step=0.1, format="%.1f", key="rob_lfo")
        with col2:
            st.number_input("MGO ROB (mt)", min_value=0.0, step=0.1, format="%.1f", key="rob_mgo")
        with col3:
            st.number_input("LNG ROB (mt)", min_value=0.0, step=0.1, format="%.1f", key="rob_lng")
        with col4:
            st.number_input("Other ROB (mt)", min_value=0.0, step=0.1, format="%.1f", key="rob_other")

    with st.expander("Fuel Allocation", expanded=False):
        st.subheader("Cargo Heating")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Cargo Heating LFO (mt)", min_value=0.0, step=0.1, format="%.1f", key="cargo_heating_lfo")
        with col2:
            st.number_input("Cargo Heating MGO (mt)", min_value=0.0, step=0.1, format="%.1f", key="cargo_heating_mgo")
        with col3:
            st.number_input("Cargo Heating LNG (mt)", min_value=0.0, step=0.1, format="%.1f", key="cargo_heating_lng")

    with st.expander("Machinery", expanded=False):
        st.subheader("Main Engine")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("ME Load (kW)", min_value=0.0, step=0.1, format="%.1f", key="me_load")
        with col2:
            st.number_input("ME Load Percentage (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key="me_load_percentage")
        with col3:
            st.number_input("ME Speed (RPM)", min_value=0.0, step=0.1, format="%.1f", key="me_speed")

        st.subheader("Auxiliary Engines")
        for i in range(1, 4):
            st.subheader(f"AE {i}")
            col1, col2 = st.columns(2)
            with col1:
                st.number_input(f"AE{i} Load (kW)", min_value=0.0, step=0.1, format="%.1f", key=f"ae{i}_load")
            with col2:
                st.number_input(f"AE{i} Load Percentage (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key=f"ae{i}_load_percentage")

    with st.expander("Weather", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Wind Direction (°)", min_value=0, max_value=360, step=1, key="wind_direction")
        with col2:
            st.number_input("Wind Speed (knots)", min_value=0.0, step=0.1, format="%.1f", key="wind_speed")
        with col3:
            st.number_input("Wind Force (Beaufort)", min_value=0, max_value=12, step=1, key="wind_force")

    with st.expander("Draft", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Forward Draft (m)", min_value=0.0, step=0.01, format="%.2f", key="forward_draft")
        with col2:
            st.number_input("Aft Draft (m)", min_value=0.0, step=0.01, format="%.2f", key="aft_draft")

    if st.button("Submit Report"):
        st.success(f"{st.session_state.current_report_type} report submitted successfully!")
        st.session_state.show_form = False
        st.experimental_rerun()

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

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.show_form = False
        st.session_state.current_report_type = None
        st.experimental_rerun()

    if st.button("Clear Chat"):
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
