import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as tm
import json

# Initialize session state
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Main app
def main():
    st.set_page_config(layout="wide", page_title="Maritime Report")

    st.title("Maritime Report")

    search_term = st.sidebar.text_input("Search fields")

    tabs = st.tabs(["Deck", "Engine"])

    with tabs[0]:
        deck_tab(search_term)

    with tabs[1]:
        engine_tab(search_term)

    if st.button("Submit Report", type="primary"):
        save_report()
        st.success("Report submitted and saved successfully!")

def deck_tab(search_term):
    st.header("Deck Information")

    sections = [
        ("General Information", general_info_section),
        ("Speed and Consumption", speed_consumption_section),
        ("Wind and Weather", wind_weather_section),
        ("Drifting", drifting_section)
    ]

    for section_name, section_function in sections:
        with st.expander(section_name, expanded=True):
            section_function(search_term)

def engine_tab(search_term):
    st.header("Engine Information")

    sections = [
        ("General", engine_general_section),
        ("Auxiliary Engines", auxiliary_engines_section),
        ("Fresh Water", fresh_water_section)
    ]

    for section_name, section_function in sections:
        with st.expander(section_name, expanded=True):
            section_function(search_term)

# Section functions
def general_info_section(search_term):
    col1, col2, col3 = st.columns(3)
    with col1:
        input_field("Ship Mean Time", "number", search_term, min_value=-12, max_value=14, help="Enter the ship mean time")
        input_field("Report Date (LT)", "date", search_term, help="Enter the local date of the report")
        input_field("Report Time (LT)", "time", search_term, help="Enter the local time of the report")
        input_field("Report Date (UTC)", "date", search_term, help="Enter the UTC date of the report")
        input_field("Report Time (UTC)", "time", search_term, help="Enter the UTC time of the report")
        input_field("IDL Crossing", "text", search_term, help="Enter International Date Line crossing information if applicable")
        input_field("IDL Direction", "selectbox", search_term, options=["--Select--", "East", "West"], help="Select the direction of IDL crossing")
        input_field("Voyage No", "text", search_term, help="Enter the voyage number")
        input_field("Cargo No", "text", search_term, help="Enter the cargo number")
        input_field("Vessel's Status", "selectbox", search_term, options=["At Sea", "In Port"], help="Select the current status of the vessel")
    with col2:
        input_field("Current Port", "text", search_term, help="Enter the current port if in port")
        input_field("Last Port", "text", search_term, help="Enter the last port visited")
        input_field("Berth / Location", "text", search_term, help="Enter the specific berth or location")
        input_field("Latitude", "text", search_term, help="Enter the current latitude")
        input_field("Longitude", "text", search_term, help="Enter the current longitude")
        input_field("Next Port", "text", search_term, help="Enter the next port of call")
        input_field("ETA Date", "date", search_term, help="Enter the estimated date of arrival at the next port")
        input_field("ETA Time", "time", search_term, help="Enter the estimated time of arrival at the next port")
    with col3:
        input_field("Speed required to achieve Scheduled ETA (kts)", "number", search_term, min_value=0.0, step=0.1, help="Enter the required speed to meet the scheduled ETA")
        input_field("ETB", "date", search_term, help="Enter the Estimated Time of Berthing")
        input_field("ETC/D", "date", search_term, help="Enter the Estimated Time of Completion/Departure")
        input_field("Best ETA PBG (LT)", "date", search_term, help="Enter the best estimated time of arrival at Pilot Boarding Ground (Local Time)")
        input_field("Best ETA PBG Time (LT)", "time", search_term, help="Enter the best estimated time of arrival at Pilot Boarding Ground (Local Time)")
        input_field("Best ETA PBG (UTC)", "date", search_term, help="Enter the best estimated time of arrival at Pilot Boarding Ground (UTC)")
        input_field("Best ETA PBG Time (UTC)", "time", search_term, help="Enter the best estimated time of arrival at Pilot Boarding Ground (UTC)")
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

def wind_weather_section(search_term):
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

def engine_general_section(search_term):
    col1, col2, col3 = st.columns(3)
    with col1:
        input_field("Engine Distance", "number", search_term, min_value=0.0, step=0.1, help="Enter the engine distance")
        input_field("Slip", "number", search_term, min_value=0.0, max_value=100.0, step=0.1, help="Enter the slip percentage")
        input_field("Avg Slip since COSP", "number", search_term, min_value=0.0, step=0.1, help="Enter the average slip since Commencement of Sea Passage")
        input_field("ER Temp (°C)", "number", search_term, min_value=0.0, step=0.1, help="Enter the engine room temperature in Celsius")
    with col2:
        input_field("SW Temp (°C)", "number", search_term, min_value=0.0, step=0.1, help="Enter the sea water temperature in Celsius")
        input_field("SW Press (bar)", "number", search_term, min_value=0.0, step=0.1, help="Enter the sea water pressure in bar")

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
    input_field("Boiler water Chlorides (ppm)", "number", search_term, min_value=0.0, step=0.1, help="Enter the boiler water chlorides in ppm")

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

def save_report():
    summary = create_summary()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"maritime_report_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(summary, f)
    st.success(f"Report saved as {filename}")

def create_summary():
    summary = {}
    for key, value in st.session_state.items():
        if not key.startswith('_') and key != 'form_data':
            summary[key] = value
    return summary

if __name__ == "__main__":
    main()
