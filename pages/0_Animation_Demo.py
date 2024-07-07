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

# Define sections and fields for each report type
REPORT_SECTIONS = {
    "Vessel Data": ["Vessel Name", "Vessel IMO"],
    "Voyage Data": ["Local Date", "Local Time", "UTC Offset", "Voyage ID", "Segment ID", "From Port", "To Port"],
    "Event Data": ["Event Type", "Time Elapsed (hours)", "Sailing Time (hours)", "Anchor Time (hours)", "DP Time (hours)", "Ice Time (hours)", "Maneuvering (hours)", "Loading/Unloading (hours)", "Drifting (hours)"],
    "Position": ["Latitude Degrees", "Latitude Minutes", "Latitude Direction", "Longitude Degrees", "Longitude Minutes", "Longitude Direction"],
    "Cargo": ["Cargo Weight (mt)"],
    "Fuel Consumption": ["ME LFO (mt)", "ME MGO (mt)", "ME LNG (mt)", "ME Other (mt)", "ME Other Fuel Type", "AE LFO (mt)", "AE MGO (mt)", "AE LNG (mt)", "AE Other (mt)", "AE Other Fuel Type", "Boiler LFO (mt)", "Boiler MGO (mt)", "Boiler LNG (mt)", "Boiler Other (mt)", "Boiler Other Fuel Type"],
    "ROB": ["LFO ROB (mt)", "MGO ROB (mt)", "LNG ROB (mt)", "Other ROB (mt)", "Other Fuel Type ROB", "Total Fuel ROB (mt)"],
    "Fuel Allocation": ["Cargo Heating LFO (mt)", "Cargo Heating MGO (mt)", "Cargo Heating LNG (mt)", "Cargo Heating Other (mt)", "Cargo Heating Other Fuel Type"],
    "Machinery": ["ME Load (kW)", "ME Load Percentage (%)", "ME Speed (RPM)", "ME Propeller Pitch (m)", "ME Propeller Pitch Ratio", "ME Shaft Generator Power (kW)", "ME Charge Air Inlet Temp (°C)", "ME Scav. Air Pressure (bar)", "ME SFOC (g/kWh)", "ME SFOC ISO Corrected (g/kWh)", "AE1 Load (kW)", "AE1 Charge Air Inlet Temp (°C)", "AE1 Charge Air Pressure (bar)", "AE1 SFOC (g/kWh)", "AE1 SFOC ISO Corrected (g/kWh)", "AE2 Load (kW)", "AE2 Charge Air Inlet Temp (°C)", "AE2 Charge Air Pressure (bar)", "AE2 SFOC (g/kWh)", "AE2 SFOC ISO Corrected (g/kWh)", "AE3 Load (kW)", "AE3 Charge Air Inlet Temp (°C)", "AE3 Charge Air Pressure (bar)", "AE3 SFOC (g/kWh)", "AE3 SFOC ISO Corrected (g/kWh)"],
    "Weather": ["Wind Direction (degrees)", "Wind Speed (knots)", "Wind Force (Beaufort)", "Sea State Direction (degrees)", "Sea State Force (Douglas scale)", "Sea State Period (seconds)", "Swell Direction (degrees)", "Swell Height (meters)", "Swell Period (seconds)", "Current Direction (degrees)", "Current Speed (knots)", "Air Temperature (°C)", "Sea Temperature (°C)"],
    "Draft": ["Actual Forward Draft (m)", "Actual Aft Draft (m)", "Displacement (mt)", "Water Depth (m)"]
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
    
    for section, fields in REPORT_SECTIONS.items():
        with st.expander(section, expanded=False):
            for field in fields:
                if section == "Vessel Data" and field == "Vessel Name":
                    st.text_input(field, value=generate_random_vessel_name(), key=f"{report_type}_{field.lower().replace(' ', '_')}")
                elif section == "Vessel Data" and field == "Vessel IMO":
                    st.text_input(field, value=generate_random_imo(), key=f"{report_type}_{field.lower().replace(' ', '_')}")
                elif "Date" in field:
                    st.date_input(field, key=f"{report_type}_{field.lower().replace(' ', '_')}")
                elif "Time" in field:
                    st.time_input(field, key=f"{report_type}_{field.lower().replace(' ', '_')}")
                elif any(unit in field for unit in ["(%)", "(mt)", "(kW)", "(°C)", "(bar)", "(g/kWh)", "(knots)", "(meters)", "(seconds)", "(degrees)"]):
                    st.number_input(field, key=f"{report_type}_{field.lower().replace(' ', '_')}")
                elif "Direction" in field:
                    st.selectbox(field, options=["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=f"{report_type}_{field.lower().replace(' ', '_')}")
                else:
                    st.text_input(field, key=f"{report_type}_{field.lower().replace(' ', '_')}")

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
        
        # Check if a specific report type is mentioned and agreed upon
        for report_type in REPORT_TYPES:
            if report_type.lower() in prompt.lower() and "agree" in prompt.lower():
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
