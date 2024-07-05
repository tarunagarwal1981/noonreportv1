import streamlit as st
import pandas as pd
from datetime import datetime, time
import random
import string

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

def generate_random_vessel_name():
    adjectives = ['Swift', 'Majestic', 'Brave', 'Stellar', 'Royal']
    nouns = ['Voyager', 'Explorer', 'Mariner', 'Adventurer', 'Navigator']
    return f"{random.choice(adjectives)} {random.choice(nouns)}"

def generate_random_imo():
    return ''.join(random.choices(string.digits, k=6))

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
    st.header("New Report")
    
    with st.expander("Vessel Data", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Vessel Name", value=generate_random_vessel_name(), key="vessel_name")
        with col2:
            st.text_input("Vessel IMO", value=generate_random_imo(), key="vessel_imo")

    with st.expander("Voyage Data", expanded=True):
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

    with st.expander("Event Data", expanded=True):
        event_types = [
            "Arrival", "Departure", "Begin of sea passage", "End of sea passage",
            "Noon (Position) - Sea passage", "Noon (Position) - Port", "Noon (Position) - River",
            "Noon (Position) - Stoppage", "Begin Anchoring/Drifting", "End Anchoring/Drifting",
            "Begin canal passage", "End canal passage", "Begin fuel change over", "End fuel change over",
            "Entering special area", "Leaving special area", "Begin offhire", "End offhire",
            "ETA update", "Change destination (Deviation)", "Begin of deviation", "End of deviation"
        ]
        st.selectbox("Event Type", event_types, key="event_type")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.number_input("Time Elapsed (hrs)", min_value=0.0, step=0.1, format="%.1f", key="time_elapsed")
        with col2:
            st.number_input("Sailing Time (hrs)", min_value=0.0, step=0.1, format="%.1f", key="sailing_time")
        with col3:
            st.number_input("Anchor Time (hrs)", min_value=0.0, step=0.1, format="%.1f", key="anchor_time")
        with col4:
            st.number_input("Maneuvering (hrs)", min_value=0.0, step=0.1, format="%.1f", key="maneuvering_time")

    with st.expander("Position", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Latitude", min_value=-90.0, max_value=90.0, step=0.000001, format="%.6f", key="latitude")
        with col2:
            st.number_input("Longitude", min_value=-180.0, max_value=180.0, step=0.000001, format="%.6f", key="longitude")

    with st.expander("Cargo", expanded=True):
        st.number_input("Cargo Weight (mt)", min_value=0.0, step=0.1, format="%.1f", key="cargo_weight")

    with st.expander("Fuel Consumption", expanded=True):
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

    with st.expander("Remaining on Board (ROB)", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.number_input("LFO ROB (mt)", min_value=0.0, step=0.1, format="%.1f", key="rob_lfo")
        with col2:
            st.number_input("MGO ROB (mt)", min_value=0.0, step=0.1, format="%.1f", key="rob_mgo")
        with col3:
            st.number_input("LNG ROB (mt)", min_value=0.0, step=0.1, format="%.1f", key="rob_lng")
        with col4:
            st.number_input("Other ROB (mt)", min_value=0.0, step=0.1, format="%.1f", key="rob_other")

    with st.expander("Fuel Allocation", expanded=True):
        st.subheader("Cargo Heating")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Cargo Heating LFO (mt)", min_value=0.0, step=0.1, format="%.1f", key="cargo_heating_lfo")
        with col2:
            st.number_input("Cargo Heating MGO (mt)", min_value=0.0, step=0.1, format="%.1f", key="cargo_heating_mgo")
        with col3:
            st.number_input("Cargo Heating LNG (mt)", min_value=0.0, step=0.1, format="%.1f", key="cargo_heating_lng")

    with st.expander("Machinery", expanded=True):
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

    with st.expander("Weather", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Wind Direction (°)", min_value=0, max_value=360, step=1, key="wind_direction")
        with col2:
            st.number_input("Wind Speed (knots)", min_value=0.0, step=0.1, format="%.1f", key="wind_speed")
        with col3:
            st.number_input("Wind Force (Beaufort)", min_value=0, max_value=12, step=1, key="wind_force")

    with st.expander("Draft", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Forward Draft (m)", min_value=0.0, step=0.01, format="%.2f", key="forward_draft")
        with col2:
            st.number_input("Aft Draft (m)", min_value=0.0, step=0.01, format="%.2f", key="aft_draft")

    if st.button("Submit Report"):
        st.success("Report submitted successfully!")

def create_chatbot():
    st.header("AI Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I help you with your report?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = f"Thank you for your question. Here's a placeholder response to: {prompt}"
        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

if __name__ == "__main__":
    main()
