import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as tm
import json

# Custom imports
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space

# Initialize session state
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Function to update progress
def update_progress():
    total_fields = 100  # Estimate of total fields
    filled_fields = sum(1 for value in st.session_state.form_data.values() if value)
    st.session_state.progress = min(filled_fields / total_fields, 1.0)

# Function to save form data
def save_form_data():
    st.session_state.form_data.update({k: v for k, v in st.session_state.items() if not k.startswith('_')})
    with open('form_data.json', 'w') as f:
        json.dump(st.session_state.form_data, f)
    st.success("Form data saved successfully!")

# Function to load form data
def load_form_data():
    try:
        with open('form_data.json', 'r') as f:
            st.session_state.form_data = json.load(f)
        st.success("Form data loaded successfully!")
    except FileNotFoundError:
        st.warning("No saved form data found.")

# Main app
def main():
    st.set_page_config(layout="wide", page_title="Maritime Report")
    
    # Dark mode toggle
    if st.sidebar.checkbox("Dark Mode"):
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("Maritime Report")

    # Progress indicator
    st.progress(st.session_state.progress)

    # Quick Fill and Save buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Quick Fill from Previous Report"):
            load_form_data()
    with col2:
        if st.button("Save Current Report"):
            save_form_data()
    with col3:
        if st.button("Review Summary"):
            switch_page("summary")

    # Search function
    search_term = st.sidebar.text_input("Search fields")

    tabs = st.tabs(["Deck", "Engine"])

    with tabs[0]:
        deck_tab(search_term)

    with tabs[1]:
        engine_tab(search_term)

    if st.button("Submit Report", type="primary"):
        st.success("Report submitted successfully!")

    # Auto-save every 5 minutes
    if tm.time() % 300 < 1:  # Every 5 minutes
        save_form_data()

def deck_tab(search_term):
    st.header("Deck Information")

    sections = [
        ("General Information", general_info_section),
        ("Speed and Consumption", speed_consumption_section),
        ("Position and Navigation", position_navigation_section),
        ("Weather", weather_section),
        ("Special Areas", special_areas_section),
        ("Breaching International Navigating Limits", inl_section),
        ("Drifting", drifting_section)
    ]

    for section_name, section_function in sections:
        with st.expander(section_name, expanded=True):
            section_function(search_term)

def engine_tab(search_term):
    st.header("Engine Information")

    sections = [
        ("Main Engine", main_engine_section),
        ("Auxiliary Engines", auxiliary_engines_section),
        ("Lube Oil Consumptions", lube_oil_section),
        ("Fresh Water", fresh_water_section),
        ("Fuel Consumption", fuel_consumption_section),
        ("Detailed Fuel Consumption", detailed_fuel_consumption_section)
    ]

    for section_name, section_function in sections:
        with st.expander(section_name, expanded=True):
            section_function(search_term)

# Section functions
def general_info_section(search_term):
    col1, col2, col3 = st.columns(3)
    with col1:
        input_field("Vessel Name", "text", search_term, help="Enter the name of the vessel")
        input_field("Voyage No", "text", search_term, help="Enter the voyage number")
        input_field("Cargo No", "text", search_term, help="Enter the cargo number")
        input_field("Vessel's Status", "selectbox", search_term, options=["At Sea", "In Port"], help="Select the current status of the vessel")
        input_field("Current Port", "text", search_term, help="Enter the current port if in port")
        input_field("Last Port", "text", search_term, help="Enter the last port visited")
        input_field("Berth / Location", "text", search_term, help="Enter the specific berth or location")
    with col2:
        input_field("Report Date (LT)", "date", search_term, help="Enter the local date of the report")
        input_field("Report Time (LT)", "time", search_term, help="Enter the local time of the report")
        input_field("Report Date (UTC)", "date", search_term, help="Enter the UTC date of the report")
        input_field("Report Time (UTC)", "time", search_term, help="Enter the UTC time of the report")
        input_field("IDL Crossing", "text", search_term, help="Enter International Date Line crossing information if applicable")
        input_field("IDL Direction", "selectbox", search_term, options=["--Select--", "East", "West"], help="Select the direction of IDL crossing")
        input_field("Off Port Limits", "checkbox", search_term, help="Check if the vessel is at off port limits")
    with col3:
        input_field("Next Port", "text", search_term, help="Enter the next port of call")
        input_field("ETA Date", "date", search_term, help="Enter the estimated date of arrival at the next port")
        input_field("ETA Time", "time", search_term, help="Enter the estimated time of arrival at the next port")
        input_field("Speed required to achieve Scheduled ETA (kts)", "number", search_term, min_value=0.0, step=0.1, help="Enter the required speed to meet the scheduled ETA")
        input_field("ETB", "date", search_term, help="Enter the Estimated Time of Berthing")
        input_field("ETC/D", "date", search_term, help="Enter the Estimated Time of Completion/Departure")
        input_field("Ballast/Laden", "radio", search_term, options=["Ballast", "Laden"], help="Select whether the vessel is in ballast or laden condition")

def speed_consumption_section(search_term):
    col1, col2, col3 = st.columns(3)
    with col1:
        input_field("Full Speed (hrs)", "number", search_term, min_value=0.0, step=0.1, help="Enter the time spent at full speed")
        input_field("Full Speed (nm)", "number", search_term, min_value=0.0, step=0.1, help="Enter the distance covered at full speed")
        input_field("Reduced Speed/Slow Steaming (hrs)", "number", search_term, min_value=0.0, step=0.1, help="Enter the time spent at reduced speed")
        input_field("Reduced Speed/Slow Steaming (nm)", "number", search_term, min_value=0.0, step=0.1, help="Enter the distance covered at reduced speed")
        input_field("Stopped (hrs)", "number", search_term, min_value=0.0, step=0.1, help="Enter the time spent stopped")
        input_field("Distance Observed (nm)", "number", search_term, min_value=0.0, step=0.1, help="Enter the total distance observed")
    with col2:
        input_field("Obs Speed (SOG) (kts)", "number", search_term, min_value=0.0, step=0.1, help="Enter the observed speed over ground")
        input_field("EM Log Speed (LOG) (kts)", "number", search_term, min_value=0.0, step=0.1, help="Enter the speed from the electromagnetic log")
        input_field("Voyage Average Speed (kts)", "number", search_term, min_value=0.0, step=0.1, help="Enter the average speed for the voyage")
        input_field("Distance To Go (nm)", "number", search_term, min_value=0.0, step=0.1, help="Enter the remaining distance to the destination")
        input_field("Distance since COSP (nm)", "number", search_term, min_value=0.0, step=0.1, help="Enter the distance traveled since Commencement of Sea Passage")
    with col3:
        input_field("Voyage Order Speed (kts)", "number", search_term, min_value=0.0, step=0.1, help="Enter the ordered speed for the voyage")
        input_field("Voyage Order ME FO Cons (mt)", "number", search_term, min_value=0.0, step=0.1, help="Enter the ordered Main Engine Fuel Oil consumption")
        input_field("Voyage Order ME DO Cons (mt)", "number", search_term, min_value=0.0, step=0.1, help="Enter the ordered Main Engine Diesel Oil consumption")
        input_field("Course (°)", "number", search_term, min_value=0.0, max_value=360.0, step=1.0, help="Enter the current course in degrees")
        input_field("Draft F (m)", "number", search_term, min_value=0.0, step=0.01, help="Enter the forward draft in meters")
        input_field("Draft A (m)", "number", search_term, min_value=0.0, step=0.01, help="Enter the aft draft in meters")
        input_field("Displacement (mt)", "number", search_term, min_value=0.0, step=0.1, help="Enter the current displacement in metric tons")

def position_navigation_section(search_term):
    col1, col2 = st.columns(2)
    with col1:
        input_field("Latitude", "text", search_term, help="Enter the current latitude")
        input_field("Longitude", "text", search_term, help="Enter the current longitude")
    with col2:
        input_field("Best ETA PBG (LT)", "date", search_term, help="Enter the best estimated time of arrival at Pilot Boarding Ground (Local Time)")
        input_field("Best ETA PBG Time (LT)", "time", search_term, help="Enter the best estimated time of arrival at Pilot Boarding Ground (Local Time)")
        input_field("Best ETA PBG (UTC)", "date", search_term, help="Enter the best estimated time of arrival at Pilot Boarding Ground (UTC)")
        input_field("Best ETA PBG Time (UTC)", "time", search_term, help="Enter the best estimated time of arrival at Pilot Boarding Ground (UTC)")

def weather_section(search_term):
    col1, col2 = st.columns(2)
    with col1:
        input_field("Wind Direction", "selectbox", search_term, options=["North", "East", "South", "West", "North East", "North West", "South East", "South West"], help="Select the wind direction")
        input_field("Wind Force", "number", search_term, min_value=0, max_value=12, help="Enter the wind force on the Beaufort scale")
        input_field("Visibility (nm)", "number", search_term, min_value=0.0, step=0.1, help="Enter the visibility in nautical miles")
        input_field("Sea Height (m)", "number", search_term, min_value=0.0, step=0.1, help="Enter the sea height in meters")
        input_field("Sea Direction", "selectbox", search_term, options=["North", "East", "South", "West", "North East", "North West", "South East", "South West"], help="Select the sea direction")
    with col2:
        input_field("Swell Height (m)", "number", search_term, min_value=0.0, step=0.1, help="Enter the swell height in meters")
        input_field("Swell Direction", "selectbox", search_term, options=["North", "East", "South", "West", "North East", "North West", "South East", "South West"], help="Select the swell direction")
        input_field("Current Set (kts)", "number", search_term, min_value=0.0, step=0.1, help="Enter the current set in knots")
        input_field("Current Drift", "selectbox", search_term, options=["North", "East", "South", "West", "North East", "North West", "South East", "South West"], help="Select the current drift direction")
        input_field("Air Temp (°C)", "number", search_term, min_value=-50.0, max_value=50.0, step=0.1, help="Enter the air temperature in Celsius")
        input_field("Icing on Deck?", "checkbox", search_term, help="Check if there is icing on the deck")
    input_field("Period of bad Weather (beyond BF scale 5, in Hours)", "number", search_term, min_value=0.0, step=0.1, help="Enter the duration of bad weather in hours")

def special_areas_section(search_term):
    col1, col2 = st.columns(2)
    with col1:
        input_field("Is vessel currently in Gulf of Aden / HRA or will be Transiting Gulf of Aden / HRA within next 14 days?", "radio", search_term, options=["Yes", "No"], help="Select if the vessel is in or approaching a High Risk Area")
        if st.session_state.get("Is vessel currently in Gulf of Aden / HRA or will be Transiting Gulf of Aden / HRA within next 14 days?") == "Yes":
            input_field("Entry into HRA Date", "date", search_term, help="Enter the date of entry into the High Risk Area")
            input_field("Entry into HRA Time", "time", search_term, help="Enter the time of entry into the High Risk Area")
            input_field("Exit from HRA Date", "date", search_term, help="Enter the date of exit from the High Risk Area")
            input_field("Exit from HRA Time", "time", search_term, help="Enter the time of exit from the High Risk Area")
    with col2:
        input_field("Is vessel in an ECA area or will enter ECA area within next 3 days?", "radio", search_term, options=["Yes", "No"], help="Select if the vessel is in or approaching an Emission Control Area")
        if st.session_state.get("Is vessel in an ECA area or will enter ECA area within next 3 days?") == "Yes":
            input_field("Entry into ECA Date", "date", search_term, help="Enter the date of entry into the Emission Control Area")
            input_field("Entry into ECA Time", "time", search_term, help="Enter the time of entry into the Emission Control Area")
            input_field("Exit from ECA Date", "date", search_term, help="Enter the date of exit from the
