import streamlit as st
import pandas as pd
from datetime import datetime, time
import json

# Set page configuration
st.set_page_config(layout="wide", page_title="Maritime Report")

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
            st.session_state.show_summary = True

    # Search function
    search_term = st.sidebar.text_input("Search fields")

    tabs = st.tabs(["Deck", "Engine"])

    with tabs[0]:
        deck_tab(search_term)

    with tabs[1]:
        engine_tab(search_term)

    if st.button("Submit Report", type="primary"):
        save_report()
        st.success("Report submitted and saved successfully!")

    # Auto-save every 5 minutes
    if time.time() % 300 < 1:  # Every 5 minutes
        save_form_data()

    # Update progress
    update_progress()

    # Display summary if requested
    if st.session_state.get('show_summary', False):
        display_summary()
        if st.button("Close Summary"):
            st.session_state.show_summary = False


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
        input_field("Best ETA PBG (LT)", "date", search_term, help="Enter the best estimated time of arrival at Pilot Boarding Ground (Local Time)")
        input_field("Best ETA PBG Time (LT)", "time", search_term, help="Enter the best estimated time of arrival at Pilot Boarding Ground (Local Time)")
        input_field("Best ETA PBG (UTC)", "date", search_term, help="Enter the best estimated time of arrival at Pilot Boarding Ground (UTC)")
        input_field("Best ETA PBG Time (UTC)", "time", search_term, help="Enter the best estimated time of arrival at Pilot Boarding Ground (UTC)")

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
            input_field("Exit from ECA Date", "date", search_term, help="Enter the date of exit from the Emission Control Area")
            input_field("Exit from ECA Time", "time", search_term, help="Enter the time of exit from the Emission Control Area")
            input_field("Latitude (ECA)", "text", search_term, help="Enter the latitude when entering/exiting the ECA")
            input_field("Longitude (ECA)", "text", search_term, help="Enter the longitude when entering/exiting the ECA")
            input_field("Fuel used in ECA", "text", search_term, help="Enter the type of fuel used in the ECA")
            input_field("Fuel C/O Time", "time", search_term, help="Enter the time of fuel changeover for ECA compliance")

def inl_section(search_term):
    input_field("Is the vessel in IWL Breach area or will enter IWL Breach area within next 7 days?", "radio", search_term, options=["Yes", "No"], help="Select if the vessel is in or approaching an International Navigating Limits Breach area")
    if st.session_state.get("Is the vessel in IWL Breach area or will enter IWL Breach area within next 7 days?") == "Yes":
        col1, col2 = st.columns(2)
        with col1:
            input_field("Entry into IWL Breach Date", "date", search_term, help="Enter the date of entry into the IWL Breach area")
            input_field("Entry into IWL Breach Time", "time", search_term, help="Enter the time of entry into the IWL Breach area")
        with col2:
            input_field("Exit from IWL Breach Date", "date", search_term, help="Enter the date of exit from the IWL Breach area")
            input_field("Exit from IWL Breach Time", "time", search_term, help="Enter the time of exit from the IWL Breach area")

def drifting_section(search_term):
    col1, col2 = st.columns(2)
    with col1:
        input_field("Drifting Start Latitude", "text", search_term, help="Enter the latitude where drifting started")
        input_field("Drifting Start Longitude", "text", search_term, help="Enter the longitude where drifting started")
        input_field("Drifting Start Date", "date", search_term, help="Enter the date when drifting started")
        input_field("Drifting Start Time", "time", search_term, help="Enter the time when drifting started")
        input_field("Drifting Distance (nm)", "number", search_term, min_value=0.0, step=0.1, help="Enter the total distance drifted")
    with col2:
        input_field("Drifting End Latitude", "text", search_term, help="Enter the latitude where drifting ended")
        input_field("Drifting End Longitude", "text", search_term, help="Enter the longitude where drifting ended")
        input_field("Drifting End Date", "date", search_term, help="Enter the date when drifting ended")
        input_field("Drifting End Time", "time", search_term, help="Enter the time when drifting ended")
        input_field("Drifting Time (hrs)", "number", search_term, min_value=0.0, step=0.1, help="Enter the total time spent drifting")

def main_engine_section(search_term):
    col1, col2, col3 = st.columns(3)
    with col1:
        input_field("ME Rev Counter", "number", search_term, min_value=0, step=1, help="Enter the Main Engine revolution counter reading")
        input_field("Average RPM", "number", search_term, min_value=0.0, step=0.1, help="Enter the average RPM of the Main Engine")
        input_field("Avg RPM since COSP", "number", search_term, min_value=0.0, step=0.1, help="Enter the average RPM since Commencement of Sea Passage")
        input_field("Power Output", "radio", search_term, options=["BHP", "KW"], help="Select the unit of power output")
        input_field("Calculated BHP", "number", search_term, min_value=0, step=1, help="Enter the calculated Brake Horse Power")
    with col2:
        input_field("Governor Setting or Fuel rack Setting (%)", "number", search_term, min_value=0.0, max_value=100.0, step=0.1, help="Enter the governor setting or fuel rack setting as a percentage")
        input_field("Speed Setting", "number", search_term, min_value=0.0, step=0.1, help="Enter the speed setting")
        input_field("Scav Air Temp (°C)", "number", search_term, min_value=0.0, step=0.1, help="Enter the scavenging air temperature in Celsius")
        input_field("Scav Air Press (bar)", "number", search_term, min_value=0.0, step=0.1, help="Enter the scavenging air pressure in bar")
        input_field("FO Inlet Temp (°C)", "number", search_term, min_value=0.0, step=0.1, help="Enter the fuel oil inlet temperature in Celsius")
    with col3:
        input_field("FO Cat Fines (ppm)", "number", search_term, min_value=0.0, step=0.1, help="Enter the fuel oil catalyst fines content in parts per million")
        input_field("FO Press (bar)", "number", search_term, min_value=0.0, step=0.1, help="Enter the fuel oil pressure in bar")
        input_field("Exh Temp Max (°C)", "number", search_term, min_value=0.0, step=0.1, help="Enter the maximum exhaust temperature in Celsius")
        input_field("Exh Temp Min (°C)", "number", search_term, min_value=0.0, step=0.1, help="Enter the minimum exhaust temperature in Celsius")
        input_field("Exh Press (bar)", "number", search_term, min_value=0.0, step=0.1, help="Enter the exhaust pressure in bar")

def auxiliary_engines_section(search_term):
    col1, col2 = st.columns(2)
    with col1:
        input_field("A/E No.1 Generator Load (kw)", "number", search_term, min_value=0, step=1, help="Enter the load of Auxiliary Engine No.1 Generator in kilowatts")
        input_field("A/E No.2 Generator Load (kw)", "number", search_term, min_value=0, step=1, help="Enter the load of Auxiliary Engine No.2 Generator in kilowatts")
        input_field("A/E No.3 Generator Load (kw)", "number", search_term, min_value=0, step=1, help="Enter the load of Auxiliary Engine No.3 Generator in kilowatts")
        input_field("A/E No.4 Generator Load (kw)", "number", search_term, min_value=0, step=1, help="Enter the load of Auxiliary Engine No.4 Generator in kilowatts")
    with col2:
        input_field("A/E No.1 Generator Hours of Operation (hrs)", "number", search_term, min_value=0.0, step=0.1, help="Enter the hours of operation for Auxiliary Engine No.1 Generator")
        input_field("A/E No.2 Generator Hours of Operation (hrs)", "number", search_term, min_value=0.0, step=0.1, help="Enter the hours of operation for Auxiliary Engine No.2 Generator")
        input_field("A/E No.3 Generator Hours of Operation (hrs)", "number", search_term, min_value=0.0, step=0.1, help="Enter the hours of operation for Auxiliary Engine No.3 Generator")
        input_field("A/E No.4 Generator Hours of Operation (hrs)", "number", search_term, min_value=0.0, step=0.1, help="Enter the hours of operation for Auxiliary Engine No.4 Generator")
    input_field("Shaft Generator Power (kw)", "number", search_term, min_value=0.0, step=0.1, help="Enter the power output of the Shaft Generator in kilowatts")

def lube_oil_section(search_term):
    lube_oil_data = {
        "Lube Oil": ["ME Cylinder Oil", "ME Cylinder Oil 40 TBN", "ME Cylinder Oil 70 TBN", "ME Cylinder Oil 100 TBN", "ME/MT System Oil", "AE System Oil", "AE System Oil 15TBN", "TG System Oil", "Other Lub Oils"],
        "Prev.ROB": [0.0] * 9,
        "Cons": [0.0] * 9,
        "Received": [0.0] * 9,
        "ROB": [0.0] * 9
    }
    lube_oil_df = pd.DataFrame(lube_oil_data)
    st.data_editor(lube_oil_df, key="lube_oil_editor", hide_index=True)

def fresh_water_section(search_term):
    fresh_water_data = {
        "Fresh Water": ["Domestic Fresh Water", "Drinking Water", "Boiler Water", "Tank Cleaning Water"],
        "Previous ROB": [0.0] * 4,
        "Produced": [0.0] * 4,
        "ROB": [0.0] * 4,
        "Consumption": [0.0] * 4
    }
    fresh_water_df = pd.DataFrame(fresh_water_data)
    st.data_editor(fresh_water_df, key="fresh_water_editor", hide_index=True)

def fuel_consumption_section(search_term):
    col1, col2 = st.columns(2)
    with col1:
        input_field("FO Cons Rate (mt/day)", "number", search_term, min_value=0.0, step=0.1, help="Enter the Fuel Oil consumption rate in metric tons per day")
        input_field("DO Cons Rate (mt/day)", "number", search_term, min_value=0.0, step=0.1, help="Enter the Diesel Oil consumption rate in metric tons per day")
        input_field("Density @ 15°C", "number", search_term, min_value=0.0, step=0.001, help="Enter the fuel density at 15°C")
        input_field("Sulphur Content %", "number", search_term, min_value=0.0, max_value=100.0, step=0.01, help="Enter the fuel sulphur content as a percentage")
    with col2:
        input_field("FO Cons since COSP (mt/day)", "number", search_term, min_value=0.0, step=0.1, help="Enter the Fuel Oil consumption since Commencement of Sea Passage")
        input_field("DO Cons since COSP (mt/day)", "number", search_term, min_value=0.0, step=0.1, help="Enter the Diesel Oil consumption since Commencement of Sea Passage")
        input_field("Bilge Tank ROB (cu.m)", "number", search_term, min_value=0.0, step=0.1, help="Enter the Remaining on Board volume of the Bilge Tank in cubic meters")
        input_field("Total Sludge Retained onboard (cu.m)", "number", search_term, min_value=0.0, step=0.1, help="Enter the total volume of sludge retained onboard in cubic meters")

def detailed_fuel_consumption_section(search_term):
    consumptions_data = {
        "Oil Type": [
            "Heavy Fuel Oil RME-RMK - 80cSt", "Heavy Fuel Oil RMA-RMD - 80cSt",
            "VLSFO RME-RMK Visc >80cSt 0.5%S Max", "VLSFO RMA-RMD Visc >80cSt 0.5%S Max",
            "ULSFO RME-RMK <80cSt 0.1%S Max", "ULSFO RMA-RMD <80cSt 0.1%S Max",
            "VLSMGO 0.5%S Max", "ULSMGO 0.1%S Max",
            "Biofuel - 30", "Biofuel Distillate FO",
            "LPG - Propane", "LPG - Butane",
            "LNG Boil Off", "LNG (Bunkered)"
        ],
        "Previous ROB": [0.0] * 14,
        "AT SEA M/E": [0.0] * 14,
        "AT SEA A/E": [0.0] * 14,
        "AT SEA BLR": [0.0] * 14,
        "AT SEA IGG": [0.0] * 14,
        "AT SEA C/ENG": [0.0] * 14,
        "AT SEA OTH": [0.0] * 14,
        "IN PORT M/E": [0.0] * 14,
        "IN PORT A/E": [0.0] * 14,
        "IN PORT BLR": [0.0] * 14,
        "IN PORT IGG": [0.0] * 14,
        "IN PORT C/ENG": [0.0] * 14,
        "IN PORT OTH": [0.0] * 14,
        "Bunker Qty": [0.0] * 14,
        "Sulphur %": [0.0] * 14,
        "Total": [0.0] * 14,
        "ROB at Noon": [0.0] * 14
    }
    consumptions_df = pd.DataFrame(consumptions_data)
    st.data_editor(consumptions_df, key="detailed_fuel_consumption_editor", hide_index=True)

def input_field(label, field_type, search_term, **kwargs):
    if search_term.lower() in label.lower():
        st.markdown(f"**{label}**")
    if field_type == "text":
        return st.text_input(label, key=label, help=kwargs.get("help", ""), value=st.session_state.form_data.get(label, ""))
    elif field_type == "number":
        return st.number_input(label, key=label, help=kwargs.get("help", ""), value=st.session_state.form_data.get(label, 0.0), **kwargs)
    elif field_type == "date":
        return st.date_input(label, key=label, help=kwargs.get("help", ""), value=st.session_state.form_data.get(label, datetime.now().date()))
    elif field_type == "time":
        return st.time_input(label, key=label, help=kwargs.get("help", ""), value=st.session_state.form_data.get(label, datetime.now().time()))
    elif field_type == "selectbox":
        return st.selectbox(label, key=label, help=kwargs.get("help", ""), options=kwargs.get("options", []), index=kwargs.get("options", []).index(st.session_state.form_data.get(label, kwargs.get("options", [""])[0])))
    elif field_type == "radio":
        return st.radio(label, key=label, help=kwargs.get("help", ""), options=kwargs.get("options", []), index=kwargs.get("options", []).index(st.session_state.form_data.get(label, kwargs.get("options", [""])[0])))
    elif field_type == "checkbox":
        return st.checkbox(label, key=label, help=kwargs.get("help", ""), value=st.session_state.form_data.get(label, False))

def create_summary():
    summary = {}
    for key, value in st.session_state.items():
        if not key.startswith('_') and key != 'form_data':
            summary[key] = value
    return summary

def display_summary():
    st.title("Report Summary")
    summary = create_summary()
    for section, fields in summary.items():
        st.header(section)
        for field, value in fields.items():
            st.write(f"{field}: {value}")

def save_report():
    summary = create_summary()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"maritime_report_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(summary, f)
    st.success(f"Report saved as {filename}")

# Add keyboard shortcuts
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 's') {
        document.querySelector('button:contains("Save Current Report")').click();
        e.preventDefault();
    } else if (e.ctrlKey && e.key === 'r') {
        document.querySelector('button:contains("Review Summary")').click();
        e.preventDefault();
    }
});
</script>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
