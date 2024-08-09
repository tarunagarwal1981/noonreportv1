import streamlit as st
import pandas as pd
from datetime import datetime, time
import numpy as np
import uuid

st.set_page_config(layout="wide", page_title="Noon Reporting Portal")

def main():
    st.title("Noon Reporting Portal")

    noon_report_type = st.selectbox("Select Noon Report Type",
                                    ["Noon at Sea", "Noon at Port", "Noon at Anchor", "Noon at Drifting", "Noon at STS", "Noon at Canal/River Passage"])

    if noon_report_type in ["Noon at Sea", "Noon at Drifting", "Noon at Canal/River Passage"]:
        display_base_report_form()
    else:
        display_custom_report_form(noon_report_type)

def display_base_report_form():
    sections = [
        "Vessel Information",
        "Voyage Information",
        "Special Events",
        "Speed, Position and Navigation",
        "Weather and Sea Conditions",
        "Cargo and Stability",
        "Fuel Consumption",
        "Machinery",
        "Environmental Compliance",
        "Miscellaneous Consumables",
    ]

    for section in sections:
        with st.expander(section, expanded=False):
            function_name = f"display_{section.lower().replace(' ', '_').replace(',', '')}"
            if function_name in globals():
                globals()[function_name]()
            else:
                st.write(f"Function {function_name} not found.")

    if st.button("Submit Report", type="primary", key=f"submit_report_{uuid.uuid4()}"):
        st.success("Report submitted successfully!")

def display_custom_report_form(noon_report_type):
    sections = [
        "Vessel Information",
        "Voyage Information",
        "Special Events",
        "Speed, Position and Navigation",
        "Weather and Sea Conditions",
        "Cargo and Stability",
        "Fuel Consumption",
        "Machinery",
        "Environmental Compliance",
        "Miscellaneous Consumables",
    ]

    for section in sections:
        with st.expander(section, expanded=False):
            function_name = f"display_custom_{section.lower().replace(' ', '_').replace(',', '')}"
            if function_name in globals():
                globals()[function_name](noon_report_type)
            else:
                st.write(f"Function {function_name} not found.")

    if st.button("Submit Report", type="primary", key=f"submit_report_{uuid.uuid4()}"):
        st.success("Report submitted successfully!")

def display_vessel_information():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("IMO Number", key=f"imo_number_{uuid.uuid4()}")   
        
    with col2:
        st.text_input("Vessel Name", key=f"vessel_name_{uuid.uuid4()}")
        
    with col3:
        st.text_input("Vessel Type", key=f"vessel_type_{uuid.uuid4()}")

def display_custom_vessel_information(noon_report_type):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("IMO Number", key=f"imo_number_{uuid.uuid4()}")
       
        
        
    with col1:
        st.text_input("Vessel Name", key=f"vessel_name_{uuid.uuid4()}")
       
    with col2:
        st.text_input("Vessel Type", key=f"vessel_type_{uuid.uuid4()}")


def display_voyage_information():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Departure Port", key="voyage_from")
        st.text_input("UNLOCODE", key="voyage_fromunlo")
        st.text_input("Arrival Port", key="voyage_to")
        st.text_input("UNLOCODE", key="voyage_tounlo")  
        st.text_input("Voyage ID", key=f"voyage_id_{uuid.uuid4()}")
    
    with col2:
        st.selectbox("Voyage Type", ["", "One-way", "Round trip", "STS"], key="voyage_type")
        st.selectbox("Vessel Condition", ["", "Laden", "Ballast"], key=f"vessel_condition_{uuid.uuid4()}")
        st.date_input("ETA", value=datetime.now(), key="eta")
        st.text_input("Charter Type", key="charter_type")
        st.text_input("Segment ID", key=f"segment_id_{uuid.uuid4()}")
    
    with col3:
       
        st.text_input("Speed Order", key="speed_order")
        idl_crossing = st.checkbox("IDL Crossing", key="idl_crossing")
        if idl_crossing:
            st.selectbox("IDL Direction", ["East", "West"], key="idl_direction")
    
    
def display_special_events():
    st.subheader("Special Events")
    
    events = [
        "Off-hire",
        "ECA Transit",
        "Fuel Changeover",
        "Stoppage",
        "Deviation",
        "    Heavy weather",
        "    SAR operation",
        "    Navigational area Warning",
        "    Med-evac",
        "    Others",
        "Transiting Special Area",
        "    JWC area",
        "    IWL",
        "    ICE regions",
        "    HRA"
    ]
    
    # Create a DataFrame to hold the event data
    df = pd.DataFrame(index=events, columns=[
        "Start Date Time (LT)", "Start Lat", "Start Long",
        "End Date Time (LT)", "End Lat", "End Long",
        "Distance", "Consumption", "Tank Name"
    ])
    
    # Fill the DataFrame with input widgets
    for event in events:
        if not event.startswith("    "):  # Main events
            st.markdown(f"### {event}")
        else:
            st.markdown(f"#### {event.strip()}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            df.loc[event, "Start Date Time (LT)"] = st.text_input(f"{event} Start Date Time (LT)", key=f"{event}_start_dt")
            df.loc[event, "Start Lat"] = st.text_input(f"{event} Start Lat", key=f"{event}_start_lat")
            df.loc[event, "Start Long"] = st.text_input(f"{event} Start Long", key=f"{event}_start_long")
        with col2:
            df.loc[event, "End Date Time (LT)"] = st.text_input(f"{event} End Date Time (LT)", key=f"{event}_end_dt")
            df.loc[event, "End Lat"] = st.text_input(f"{event} End Lat", key=f"{event}_end_lat")
            df.loc[event, "End Long"] = st.text_input(f"{event} End Long", key=f"{event}_end_long")
        with col3:
            df.loc[event, "Distance"] = st.number_input(f"{event} Distance", key=f"{event}_distance", step=0.1, format="%.1f")
            df.loc[event, "Consumption"] = st.number_input(f"{event} Consumption", key=f"{event}_consumption", step=0.1, format="%.1f")
            df.loc[event, "Tank Name"] = st.selectbox(
                f"{event} Tank Name",
                options=[f"Tank {i}" for i in range(1, 9)],
                key=f"{event}_tank"
            )
        
        st.markdown("---")  # Add a separator line after each event
    
    # Display the DataFrame
    st.subheader("Special Events Summary")
    st.dataframe(df)

    # Add a download button for the DataFrame
    csv = df.to_csv(index=True)
    st.download_button(
        label="Download Special Events Data",
        data=csv,
        file_name="special_events.csv",
        mime="text/csv",
    )

def display_custom_voyage_details(noon_report_type):

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Port Name", key=f"port_name_{uuid.uuid4()}")
        st.text_input("Port UNLOCODE", key=f"port_unlo_{uuid.uuid4()}")
        st.text_input("Speed Order", key="speed_order")
    
    with col2:
        st.selectbox("Voyage Type", ["", "One-way", "Round trip", "STS"], key="voyage_type")
        
        st.date_input("ETA", value=datetime.now(), key="eta")
        st.text_input("Charter Type", key="charter_type")
    
    with col3:
        st.selectbox("Vessel Condition", ["", "Laden", "Ballast"], key=f"vessel_condition_{uuid.uuid4()}")
    
    with col4:
        offhire = st.checkbox("Off-hire", key="offhire")
        eca_transit = st.checkbox("ECA Transit", key="eca_transit")
        fuel_changeover = st.checkbox("Fuel Changeover", key="fuel_changeover")
        drydock = st.checkbox("Drydock", key="drydock")
                
    if offhire:
        st.subheader("Off-hire Details")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.date_input("Off-hire Start Date (LT)", key="offhire_start_date_lt")
            st.time_input("Off-hire Start Time (LT)", key="offhire_start_time_lt")
            st.date_input("Off-hire Start Date (UTC)", key="offhire_start_date_utc")
            st.time_input("Off-hire Start Time (UTC)", key="offhire_start_time_utc")
        with col2:
            st.text_input("Start Off-hire Position Latitude", key="start_offhire_lat")
            st.text_input("Start Off-hire Position Longitude", key="start_offhire_lon")
            st.date_input("Off-hire End Date (LT)", key="offhire_end_date_lt")
            st.time_input("Off-hire End Time (LT)", key="offhire_end_time_lt")
        with col3:
            st.date_input("Off-hire End Date (UTC)", key="offhire_end_date_utc")
            st.time_input("Off-hire End Time (UTC)", key="offhire_end_time_utc")
            st.text_input("End Off-hire Position Latitude", key="end_offhire_lat")
            st.text_input("End Off-hire Position Longitude", key="end_offhire_lon")
        with col4:
            st.text_area("Off-hire Reason", key="offhire_reason")
    
    if eca_transit:
        st.subheader("ECA Transit Details")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.date_input("ECA Entry Date", key="eca_entry_date")
            st.time_input("ECA Entry Time", key="eca_entry_time")
        with col2:
            st.text_input("ECA Entry Latitude", key="eca_entry_lat")
            st.text_input("ECA Entry Longitude", key="eca_entry_lon")
        with col3:
            st.date_input("ECA Exit Date", key="eca_exit_date")
            st.time_input("ECA Exit Time", key="eca_exit_time")
        with col4:
            st.text_input("ECA Exit Latitude", key="eca_exit_lat")
            st.text_input("ECA Exit Longitude", key="eca_exit_lon")
        st.text_input("ECA Name", key="eca_name")
    
    if fuel_changeover:
        st.subheader("Fuel Changeover Details")
        st.subheader("Start of Changeover")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.date_input("Changeover Start Date", key="changeover_start_date")
            st.time_input("Changeover Start Time", key="changeover_start_time")
        with col2:
            st.text_input("Changeover Start Latitude", key="changeover_start_lat")
            st.text_input("Changeover Start Longitude", key="changeover_start_lon")
        with col3:
            st.number_input("VLSFO ROB at Start (MT)", min_value=0.0, step=0.1, key="vlsfo_rob_start")
            st.number_input("LSMGO ROB at Start (MT)", min_value=0.0, step=0.1, key="lsmgo_rob_start")
        
        st.subheader("End of Changeover")
        with col1:
            st.date_input("Changeover End Date", key="changeover_end_date")
            st.time_input("Changeover End Time", key="changeover_end_time")
        with col2:
            st.text_input("Changeover End Latitude", key="changeover_end_lat")
            st.text_input("Changeover End Longitude", key="changeover_end_lon")
        with col3:
            st.number_input("VLSFO ROB at End (MT)", min_value=0.0, step=0.1, key="vlsfo_rob_end")
            st.number_input("LSMGO ROB at End (MT)", min_value=0.0, step=0.1, key="lsmgo_rob_end")
    
    
                                                                                
def display_speed_position_and_navigation():
    st.subheader("Speed, Position and Navigation")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Time Since Last Report (hours)", min_value=0.0, step=0.1, key="time_since_last_report")
        st.selectbox("Clocks Advanced/Retarded", ["", "Advanced", "Retarded"], key="clocks_change")
        st.number_input("Clocks Changed By (minutes)", min_value=0, step=1, key="clocks_change_minutes")
        st.time_input("Date Time (Local)", value=datetime.now().time(), key=f"local_time_{uuid.uuid4()}")
        st.time_input("Vessel Timezone", value=datetime.now().time(), key=f"local_timezone_{uuid.uuid4()}")
        st.date_input("Date Time (UTC)", value=datetime.now(), key=f"utc_date_{uuid.uuid4()}")
               
    with col2:
        st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1, value=0.00, key=f"distance_observed_{uuid.uuid4()}")
        st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1, value=0.00, key=f"distance_togo_{uuid.uuid4()}")    
        st.number_input("Distance Through Water (nm)", min_value=0.0, step=0.1, key=f"distance_through_water_{uuid.uuid4()}")
        st.number_input("Distance Adjusted (nm)", min_value=0.0, step=0.1, value=0.00, key=f"distance_adj_{uuid.uuid4()}")
        st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1, key=f"obs_speed_sog_{uuid.uuid4()}")
        st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1, key=f"em_log_speed_{uuid.uuid4()}")
        
        
    with col3:
        st.number_input("Latitude", min_value=-90, max_value=90, step=1, key=f"lat_degree_{uuid.uuid4()}")
        st.selectbox("Latitude N/S", ["N", "S"], key=f"lat_ns_{uuid.uuid4()}")
        st.number_input("Longitude", min_value=-180, max_value=180, step=1, key=f"lon_degree_{uuid.uuid4()}")
        st.selectbox("Longitude E/W", ["E", "W"], key=f"lon_ew_{uuid.uuid4()}")
        st.number_input("Course (°)", min_value=0, max_value=359, step=1, key=f"course_{uuid.uuid4()}")
        st.number_input("Heading (°)", min_value=0, max_value=359, step=1, key=f"heading_{uuid.uuid4()}")
        
        
    with col4:
        st.text_input("Ordered Speed", key=f"speed_order_{uuid.uuid4()}")
        
        

def display_custom_speed_position_and_navigation(noon_report_type):
    st.subheader("Speed, Position and Navigation")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        
        st.number_input("Latitude", min_value=-90, max_value=90, step=1, key=f"lat_degree_{uuid.uuid4()}")
        st.date_input("Date (Local)", value=datetime.now(), key=f"local_date_{uuid.uuid4()}")
        
        
    with col2:
        
        st.selectbox("Latitude N/S", ["N", "S"], key=f"lat_ns_{uuid.uuid4()}")
        st.number_input("Longitude", min_value=-180, max_value=180, step=1, key=f"lon_degree_{uuid.uuid4()}")
        
    with col3:
       
        st.selectbox("Longitude E/W", ["E", "W"], key=f"lon_ew_{uuid.uuid4()}")
        st.time_input("Time (UTC)", value=datetime.now().time(), key=f"utc_time_{uuid.uuid4()}")
        
    with col4:
        st.time_input("Time (Local)", value=datetime.now().time(), key=f"local_time_{uuid.uuid4()}")
        st.date_input("Date (UTC)", value=datetime.now(), key=f"utc_date_{uuid.uuid4()}")
        

def display_weather_and_sea_conditions():
    st.subheader("Weather and Sea Conditions")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("True Wind Speed (kts)", min_value=0.0, step=0.1, key=f"true_wind_speed_{uuid.uuid4()}")
        st.selectbox("BF Scale", range(13), key=f"bf_scale_{uuid.uuid4()}")
        st.number_input("True Wind Direction (°)", min_value=0, max_value=359, step=1, key=f"true_wind_direction_{uuid.uuid4()}")
        st.number_input("Sea Water Temp (°C)", min_value=-2.0, max_value=35.0, step=0.1, key=f"sea_water_temp_{uuid.uuid4()}")
        
    with col2:
        st.number_input("Significant Wave Height (m)", min_value=0.0, step=0.1, key=f"sig_wave_height_{uuid.uuid4()}")
        st.selectbox("Sea State (Douglas)", range(10), key=f"douglas_sea_state_{uuid.uuid4()}")
        st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key=f"sea_height_{uuid.uuid4()}")
        st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key=f"air_temp_{uuid.uuid4()}")
        
    with col3:
        st.number_input("Sea Direction (°)", min_value=0, max_value=359, step=1, key=f"sea_direction_{uuid.uuid4()}")
        st.number_input("Swell Direction (°)", min_value=0, max_value=359, step=1, key=f"swell_direction_{uuid.uuid4()}")
        st.number_input("Swell Height (m) (DSS)", min_value=0.0, step=0.1, key=f"swell_height_{uuid.uuid4()}")
    with col4:
        st.number_input("Current Strength (kts)", min_value=0.0, step=0.1, key=f"current_strength_{uuid.uuid4()}")
        st.number_input("Current Direction (°)", min_value=0, max_value=359, step=1, key=f"current_direction_{uuid.uuid4()}")
        st.number_input("Atm Pr (bar)", min_value=0, max_value=359, step=1, key=f"atms_pr_{uuid.uuid4()}")

def display_custom_weather_and_sea_conditions(noon_report_type):
    st.subheader("Weather and Sea Conditions")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("True Wind Speed (kts)", min_value=0.0, step=0.1, key=f"true_wind_speed_{uuid.uuid4()}")
        st.selectbox("BF Scale", range(13), key=f"bf_scale_{uuid.uuid4()}")
        st.number_input("True Wind Direction (°)", min_value=0, max_value=359, step=1, key=f"true_wind_direction_{uuid.uuid4()}")
        st.number_input("Sea Water Temp (°C)", min_value=-2.0, max_value=35.0, step=0.1, key=f"sea_water_temp_{uuid.uuid4()}")
        
    with col2:
        st.number_input("Significant Wave Height (m)", min_value=0.0, step=0.1, key=f"sig_wave_height_{uuid.uuid4()}")
        st.selectbox("Sea State (Douglas)", range(10), key=f"douglas_sea_state_{uuid.uuid4()}")
        st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key=f"sea_height_{uuid.uuid4()}")
        st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key=f"air_temp_{uuid.uuid4()}")
    with col3:
        st.number_input("Sea Direction (°)", min_value=0, max_value=359, step=1, key=f"sea_direction_{uuid.uuid4()}")
        st.number_input("Swell Direction (°)", min_value=0, max_value=359, step=1, key=f"swell_direction_{uuid.uuid4()}")
        st.number_input("Swell Height (m) (DSS)", min_value=0.0, step=0.1, key=f"swell_height_{uuid.uuid4()}")
    with col4:
        st.number_input("Current Strength (kts)", min_value=0.0, step=0.1, key=f"current_strength_{uuid.uuid4()}")
        st.number_input("Current Direction (°)", min_value=0, max_value=359, step=1, key=f"current_direction_{uuid.uuid4()}")
        st.number_input("Atm Pr (bar)", min_value=0, max_value=359, step=1, key=f"atms_pr_{uuid.uuid4()}")

def display_cargo_and_stability():
    st.subheader("Cargo and Stability")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        
        st.number_input("FWD Draft (m)", min_value=0.0, step=0.01, key=f"fwd_draft_{uuid.uuid4()}")
        st.number_input("GM (m)", min_value=0.0, step=0.01, key=f"gm_{uuid.uuid4()}")
        st.number_input("LCG (m)", min_value=0.0, step=0.01, key=f"lcg_{uuid.uuid4()}")
    with col2:
        st.number_input("Displacement (MT)", min_value=0.0, step=0.1, key=f"displacement_{uuid.uuid4()}")
        st.number_input("Mid Draft (m)", min_value=0.0, step=0.01, key=f"mid_draft_{uuid.uuid4()}")
        st.number_input("Ballast Quantity (m³)", min_value=0.0, step=0.1, key=f"ballast_qty_{uuid.uuid4()}")
        st.number_input("VCG (m)", min_value=0.0, step=0.01, key=f"vcg_{uuid.uuid4()}")
    with col3:
        st.number_input("Water Plane Co-efficient", min_value=0.0, step=0.01, key=f"water_plane_coefficient_{uuid.uuid4()}")
        st.number_input("AFT Draft (m)", min_value=0.0, step=0.01, key=f"aft_draft_{uuid.uuid4()}")
        st.number_input("Freeboard (m)", min_value=0.0, step=0.01, key=f"freeboard_{uuid.uuid4()}")
        st.number_input("Cb (Block Co-efficient)", min_value=0.0, step=0.01, key=f"cb_{uuid.uuid4()}")

    st.markdown("<h3 style='font-size: 18px;'>Cargo Operations</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Cargo Weight (MT)", min_value=0.0, step=0.1, key=f"cargo_weight_{uuid.uuid4()}")
        st.number_input("Cargo Volume (m³)", min_value=0.0, step=0.1, key=f"cargo_volume_{uuid.uuid4()}")
        
        st.number_input("Total TEU", min_value=0, step=1, key=f"total_teu_{uuid.uuid4()}")
    with col2:
        st.number_input("Reefer TEU", min_value=0, step=1, key=f"reefer_teu_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Chilled", min_value=0, step=1, key=f"reefer_20ft_chilled_{uuid.uuid4()}")
        st.number_input("Reefer 40ft Chilled", min_value=0, step=1, key=f"reefer_40ft_chilled_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Frozen", min_value=0, step=1, key=f"reefer_20ft_frozen_{uuid.uuid4()}")
        st.number_input("Reefer 40ft Frozen", min_value=0, step=1, key=f"reefer_40ft_frozen_{uuid.uuid4()}")

def display_custom_cargo_and_stability(noon_report_type):
    st.subheader("Cargo and Stability")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        
        st.number_input("FWD Draft (m)", min_value=0.0, step=0.01, key=f"fwd_draft_{uuid.uuid4()}")
        st.number_input("GM (m)", min_value=0.0, step=0.01, key=f"gm_{uuid.uuid4()}")
        st.number_input("LCG (m)", min_value=0.0, step=0.01, key=f"lcg_{uuid.uuid4()}")
        st.number_input("Water Depth (m)", min_value=0.0, step=0.01, key=f"water_depth{uuid.uuid4()}")
    with col2:
        st.number_input("Displacement (MT)", min_value=0.0, step=0.1, key=f"displacement_{uuid.uuid4()}")
        st.number_input("Mid Draft (m)", min_value=0.0, step=0.01, key=f"mid_draft_{uuid.uuid4()}")
        st.number_input("Ballast Quantity (m³)", min_value=0.0, step=0.1, key=f"ballast_qty_{uuid.uuid4()}")
        st.number_input("VCG (m)", min_value=0.0, step=0.01, key=f"vcg_{uuid.uuid4()}")
    with col3:
        st.number_input("Water Plane Co-efficient", min_value=0.0, step=0.01, key=f"water_plane_coefficient_{uuid.uuid4()}")
        st.number_input("AFT Draft (m)", min_value=0.0, step=0.01, key=f"aft_draft_{uuid.uuid4()}")
        st.number_input("Freeboard (m)", min_value=0.0, step=0.01, key=f"freeboard_{uuid.uuid4()}")
        st.number_input("Cb (Block Co-efficient)", min_value=0.0, step=0.01, key=f"cb_{uuid.uuid4()}")

    st.markdown("<h3 style='font-size: 18px;'>Cargo Operations</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Cargo Weight (MT)", min_value=0.0, step=0.1, key=f"cargo_weight_{uuid.uuid4()}")
        st.number_input("Cargo Volume (m³)", min_value=0.0, step=0.1, key=f"cargo_volume_{uuid.uuid4()}")
        st.number_input("Total TEU", min_value=0, step=1, key=f"total_teu_{uuid.uuid4()}")
        st.number_input("Cargo Loaded (MT)", min_value=0.0, step=0.1, key=f"cargo_weight_{uuid.uuid4()}")
        st.number_input("Cargo Loaded (m³)", min_value=0.0, step=0.1, key=f"cargo_volume_{uuid.uuid4()}")
        st.number_input("Total TEU Loaded", min_value=0, step=1, key=f"total_teu_{uuid.uuid4()}")
    with col2:
        st.number_input("Reefer TEU Loaded", min_value=0, step=1, key=f"reefer_teu_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Chilled Loaded", min_value=0, step=1, key=f"reefer_20ft_chilled_{uuid.uuid4()}")
        st.number_input("Reefer 40ft Chilled Loaded", min_value=0, step=1, key=f"reefer_40ft_chilled_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Frozen Loaded", min_value=0, step=1, key=f"reefer_20ft_frozen_{uuid.uuid4()}")
        st.number_input("Reefer 40ft Frozen Loaded", min_value=0, step=1, key=f"reefer_40ft_frozen_{uuid.uuid4()}")
    with col3:
        st.number_input("Cargo Discharged (MT)", min_value=0.0, step=0.1, key=f"cargo_weight_{uuid.uuid4()}")
        st.number_input("Cargo Discharged (m³)", min_value=0.0, step=0.1, key=f"cargo_volume_{uuid.uuid4()}")
        st.number_input("Total TEU Discharged", min_value=0, step=1, key=f"total_teu_{uuid.uuid4()}")
    with col4:
        st.number_input("Reefer TEU Discharged", min_value=0, step=1, key=f"reefer_teu_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Chilled Discharged", min_value=0, step=1, key=f"reefer_20ft_chilled_{uuid.uuid4()}")
        st.number_input("Reefer 40ft Chilled Discharged", min_value=0, step=1, key=f"reefer_40ft_chilled_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Frozen Discharged", min_value=0, step=1, key=f"reefer_20ft_frozen_{uuid.uuid4()}")
        st.number_input("Reefer 40ft Frozen Discharged", min_value=0, step=1, key=f"reefer_40ft_frozen_{uuid.uuid4()}")



def display_fuel_consumption():
    

    # Initialize session state variables
    if 'consumers' not in st.session_state:
        st.session_state.consumers = [
            'Main Engine', 'Aux Engine1', 'Aux Engine2', 'Aux Engine3',
            'Boiler 1',
            '    Boiler 1 - Cargo Heating',
            '    Boiler 1 - Discharge',
            'Boiler 2',
            '    Boiler 2 - Cargo Heating',
            '    Boiler 2 - Discharge',
            'IGG', 'Incinerator',
            'DPP1', 'DPP2', 'DPP3'
        ]
    if 'tanks' not in st.session_state:
        st.session_state.tanks = [f'Tank {i}' for i in range(1, 9)]
    if 'consumption_data' not in st.session_state:
        st.session_state.consumption_data = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.tanks)
    if 'viscosity' not in st.session_state:
        st.session_state.viscosity = {tank: np.random.uniform(20, 100) for tank in st.session_state.tanks}
    if 'sulfur' not in st.session_state:
        st.session_state.sulfur = {tank: np.random.uniform(0.05, 0.49) for tank in st.session_state.tanks}
    if 'previous_rob' not in st.session_state:
        st.session_state.previous_rob = pd.Series({tank: np.random.uniform(100, 1000) for tank in st.session_state.tanks})

    st.title('Fuel Consumption Tracker')

    # Function to create a formatted column header
    def format_column_header(tank):
        return f"{tank}\nVisc: {st.session_state.viscosity[tank]:.1f}\nSulfur: {st.session_state.sulfur[tank]:.2f}%"

    # Function to create an editable dataframe
    def create_editable_dataframe():
        index = ['Previous ROB'] + st.session_state.consumers + ['Current ROB']
        
        df = pd.DataFrame(index=index, columns=st.session_state.tanks)
        df.loc['Previous ROB'] = st.session_state.previous_rob
        df.loc[st.session_state.consumers] = st.session_state.consumption_data
        
        # Calculate Current ROB
        total_consumption = df.loc[st.session_state.consumers].sum()
        df.loc['Current ROB'] = df.loc['Previous ROB'] - total_consumption
        
        # Format column headers
        df.columns = [format_column_header(tank) for tank in st.session_state.tanks]
        return df

    # Create the editable dataframe
    df = create_editable_dataframe()

    # Display the editable table
    st.write("Fuel Consumption Data:")
    
    # Custom CSS to style the dataframe
    custom_css = """
    <style>
        .dataframe td:first-child {
            font-weight: bold;
        }
        .dataframe td.italic-row {
            font-style: italic;
        }
        .dataframe td.boiler-subsection {
            padding-left: 30px !important;
            font-style: italic;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Convert dataframe to HTML and apply custom styling
    df_html = df.to_html(classes='dataframe', escape=False)
    df_html = df_html.replace('<th>', '<th style="text-align: center;">')
    
    italic_rows = ['Boiler 1', 'Boiler 2', 'DPP1', 'DPP2', 'DPP3']
    for consumer in st.session_state.consumers:
        if consumer.startswith('    '):
            df_html = df_html.replace(f'<td>{consumer}</td>', f'<td class="boiler-subsection">{consumer.strip()}</td>')
        elif consumer in italic_rows:
            df_html = df_html.replace(f'<td>{consumer}</td>', f'<td class="italic-row">{consumer}</td>')

    # Display the styled dataframe
    st.markdown(df_html, unsafe_allow_html=True)

    # Function to create and display the additional table
    def display_additional_table():
        st.write("Additional Consumption Data:")
        
        # Create the dataframe for the additional table
        additional_data = pd.DataFrame({
            'Work': [0, 0, 0, 0],
            'SFOC': [0, 0, 0, ''],
            'Tank Name': ['', '', '', '']
        }, index=['Reefer container', 'Cargo cooling', 'Heating/Discharge pump', 'Shore-Side Electricity'])
        
        # Custom CSS for the additional table
        custom_css = """
        <style>
            .additional-table th {
                text-align: center !important;
            }
            .additional-table td {
                text-align: center !important;
            }
            .grey-out {
                background-color: #f0f0f0 !important;
                color: #888 !important;
            }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
        
        # Convert dataframe to HTML and apply custom styling
        table_html = additional_data.to_html(classes='additional-table', escape=False)
        table_html = table_html.replace('<td></td>', '<td>-</td>')  # Replace empty cells with '-'
        table_html = table_html.replace('<td>Shore-Side Electricity</td><td>0</td><td></td><td></td>', 
                                        '<td>Shore-Side Electricity</td><td>0</td><td class="grey-out">-</td><td class="grey-out">-</td>')
        
        # Display the styled table
        st.markdown(table_html, unsafe_allow_html=True)

    # Display the additional table
    display_additional_table()

    # Function to edit tank properties
    def edit_tank_properties():
        st.write("Edit tank properties:")
        
        # Create a dataframe for tank properties
        tank_props = pd.DataFrame({
            'Viscosity': st.session_state.viscosity,
            'Sulfur (%)': st.session_state.sulfur
        })
        
        # Display editable dataframe for tank properties
        edited_props = st.data_editor(
            tank_props,
            use_container_width=True,
            column_config={
                'Viscosity': st.column_config.NumberColumn(
                    'Viscosity',
                    min_value=20.0,
                    max_value=100.0,
                    step=0.1,
                    format="%.1f"
                ),
                'Sulfur (%)': st.column_config.NumberColumn(
                    'Sulfur (%)',
                    min_value=0.05,
                    max_value=0.49,
                    step=0.01,
                    format="%.2f"
                )
            }
        )
        
        # Update session state with edited values
        st.session_state.viscosity = edited_props['Viscosity'].to_dict()
        st.session_state.sulfur = edited_props['Sulfur (%)'].to_dict()

    # Add a section to edit tank properties
    if st.checkbox("Edit Tank Properties"):
        edit_tank_properties()


    
def display_custom_fuel_consumption(noon_report_type):



    # Initialize session state variables
    if 'consumers' not in st.session_state:
        st.session_state.consumers = [
            'Main Engine', 'Aux Engine1', 'Aux Engine2', 'Aux Engine3',
            'Boiler 1',
            '    Boiler 1 - Cargo Heating',
            '    Boiler 1 - Discharge',
            'Boiler 2',
            '    Boiler 2 - Cargo Heating',
            '    Boiler 2 - Discharge',
            'IGG', 'Incinerator',
            'DPP1', 'DPP2', 'DPP3'
        ]
    if 'tanks' not in st.session_state:
        st.session_state.tanks = [f'Tank {i}' for i in range(1, 9)]
    if 'consumption_data' not in st.session_state:
        st.session_state.consumption_data = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.tanks)
    if 'viscosity' not in st.session_state:
        st.session_state.viscosity = {tank: np.random.uniform(20, 100) for tank in st.session_state.tanks}
    if 'sulfur' not in st.session_state:
        st.session_state.sulfur = {tank: np.random.uniform(0.05, 0.49) for tank in st.session_state.tanks}
    if 'previous_rob' not in st.session_state:
        st.session_state.previous_rob = pd.Series({tank: np.random.uniform(100, 1000) for tank in st.session_state.tanks})
    if 'bunkered_qty' not in st.session_state:
        st.session_state.bunkered_qty = pd.Series({tank: 0 for tank in st.session_state.tanks})
    if 'debunkered_qty' not in st.session_state:
        st.session_state.debunkered_qty = pd.Series({tank: 0 for tank in st.session_state.tanks})
    if 'bunkering_entries' not in st.session_state:
        st.session_state.bunkering_entries = []
    if 'debunkering_entries' not in st.session_state:
        st.session_state.debunkering_entries = []

    st.title('Fuel Consumption Tracker')

    # Bunkering and Debunkering checkboxes
    col1, col2 = st.columns(2)
    with col1:
        bunkering_happened = st.checkbox("Bunkering Happened")
    with col2:
        debunkering_happened = st.checkbox("Debunkering Happened")

    # Bunkering details section
    if bunkering_happened:
        st.markdown("<h4 style='font-size: 18px;'>Bunkering Details</h4>", unsafe_allow_html=True)
        
        # Display each bunkering entry
        for i, entry in enumerate(st.session_state.bunkering_entries):
            st.markdown(f"<h5 style='font-size: 16px;'>Bunkering Entry {i+1}</h5>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                entry['date'] = st.date_input("Date of Bunkering", key=f"bunker_date_{i}")
                entry['grade'] = st.selectbox("Grade of Fuel Bunkered", 
                                              ["VLSFO", "HFO", "MGO", "LSMGO", "LNG"], 
                                              key=f"grade_{i}")
                entry['grade_bdn'] = st.text_input("Grade as per BDN", key=f"grade_bdn_{i}")
            with col2:
                entry['total_qty'] = st.number_input("Total Quantity Bunkered (mt)", 
                                                     min_value=0.0, step=0.1, key=f"total_qty_{i}")
                entry['density'] = st.number_input("Density (kg/m³)", 
                                                   min_value=0.0, step=0.1, key=f"density_{i}")
                entry['viscosity'] = st.number_input("Viscosity (cSt)", 
                                                     min_value=0.0, step=0.1, key=f"viscosity_{i}")
            with col3:
                entry['lcv'] = st.number_input("LCV (MJ/kg)", 
                                               min_value=0.0, step=0.1, key=f"lcv_{i}")
                entry['bdn_number'] = st.text_input("BDN Number", key=f"bdn_number_{i}")
                entry['bdn_file'] = st.file_uploader("Upload BDN", 
                                                     type=['pdf', 'jpg', 'png'], 
                                                     key=f"bdn_file_{i}")

        # Button to add new bunkering entry
        if st.button("➕ Add Bunkering Entry"):
            st.session_state.bunkering_entries.append({})
            st.experimental_rerun()

    # Debunkering details section
    if debunkering_happened:
        st.markdown("<h4 style='font-size: 18px;'>Debunkering Details</h4>", unsafe_allow_html=True)
        
        # Display each debunkering entry
        for i, entry in enumerate(st.session_state.debunkering_entries):
            st.markdown(f"<h5 style='font-size: 16px;'>Debunkering Entry {i+1}</h5>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                entry['date'] = st.date_input("Date of Debunkering", key=f"debunker_date_{i}")
                entry['quantity'] = st.number_input("Quantity Debunkered (mt)", 
                                                    min_value=0.0, step=0.1, key=f"debunker_qty_{i}")
            with col2:
                entry['bdn_number'] = st.text_input("BDN Number of Debunkered Oil", key=f"debunker_bdn_{i}")
                entry['receipt_file'] = st.file_uploader("Upload Receipt", 
                                                     type=['pdf', 'jpg', 'png'], 
                                                     key=f"receipt_file_{i}")

        # Button to add new debunkering entry
        if st.button("➕ Add Debunkering Entry"):
            st.session_state.debunkering_entries.append({})
            st.experimental_rerun()

    # Function to create a formatted column header
    def format_column_header(tank):
        return f"{tank}\nVisc: {st.session_state.viscosity[tank]:.1f}\nSulfur: {st.session_state.sulfur[tank]:.2f}%"

    # Function to create an editable dataframe
    def create_editable_dataframe():
        index = ['Previous ROB'] + st.session_state.consumers
        if bunkering_happened:
            index += ['Bunkered Qty']
        if debunkering_happened:
            index += ['Debunkered Qty']
        index += ['Current ROB']
        
        df = pd.DataFrame(index=index, columns=st.session_state.tanks)
        df.loc['Previous ROB'] = st.session_state.previous_rob
        df.loc[st.session_state.consumers] = st.session_state.consumption_data
        if bunkering_happened:
            total_bunkered = sum(entry.get('total_qty', 0) for entry in st.session_state.bunkering_entries)
            df.loc['Bunkered Qty'] = [total_bunkered] + [0] * (len(st.session_state.tanks) - 1)
        if debunkering_happened:
            total_debunkered = sum(entry.get('quantity', 0) for entry in st.session_state.debunkering_entries)
            df.loc['Debunkered Qty'] = [total_debunkered] + [0] * (len(st.session_state.tanks) - 1)
        
        # Calculate Current ROB
        total_consumption = df.loc[st.session_state.consumers].sum()
        df.loc['Current ROB'] = df.loc['Previous ROB'] - total_consumption
        if bunkering_happened:
            df.loc['Current ROB'] += df.loc['Bunkered Qty']
        if debunkering_happened:
            df.loc['Current ROB'] -= df.loc['Debunkered Qty']
        
        # Format column headers
        df.columns = [format_column_header(tank) for tank in st.session_state.tanks]
        return df

    # Create the editable dataframe
    df = create_editable_dataframe()

    # Display the editable table
    st.write("Fuel Consumption Data:")
    
    # Custom CSS to style the dataframe
    custom_css = """
    <style>
        .dataframe td:first-child {
            font-weight: bold;
        }
        .dataframe td.italic-row {
            font-style: italic;
        }
        .dataframe td.boiler-subsection {
            padding-left: 30px !important;
            font-style: italic;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Convert dataframe to HTML and apply custom styling
    df_html = df.to_html(classes='dataframe', escape=False)
    df_html = df_html.replace('<th>', '<th style="text-align: center;">')
    
    italic_rows = ['Boiler 1', 'Boiler 2', 'DPP1', 'DPP2', 'DPP3']
    for consumer in st.session_state.consumers:
        if consumer.startswith('    '):
            df_html = df_html.replace(f'<td>{consumer}</td>', f'<td class="boiler-subsection">{consumer.strip()}</td>')
        elif consumer in italic_rows:
            df_html = df_html.replace(f'<td>{consumer}</td>', f'<td class="italic-row">{consumer}</td>')

    # Display the styled dataframe
    st.markdown(df_html, unsafe_allow_html=True)

    # Function to create and display the additional table
    def display_additional_table():
        st.write("Additional Consumption Data:")
        
        # Create the dataframe for the additional table
        additional_data = pd.DataFrame({
            'Work': [0, 0, 0, 0],
            'SFOC': [0, 0, 0, ''],
            'Tank Name': ['', '', '', '']
        }, index=['Reefer container', 'Cargo cooling', 'Heating/Discharge pump', 'Shore-Side Electricity'])
        
        # Custom CSS for the additional table
        custom_css = """
        <style>
            .additional-table th {
                text-align: center !important;
            }
            .additional-table td {
                text-align: center !important;
            }
            .grey-out {
                background-color: #f0f0f0 !important;
                color: #888 !important;
            }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
        
        # Convert dataframe to HTML and apply custom styling
        table_html = additional_data.to_html(classes='additional-table', escape=False)
        table_html = table_html.replace('<td></td>', '<td>-</td>')  # Replace empty cells with '-'
        table_html = table_html.replace('<td>Shore-Side Electricity</td><td>0</td><td></td><td></td>', 
                                        '<td>Shore-Side Electricity</td><td>0</td><td class="grey-out">-</td><td class="grey-out">-</td>')
        
        # Display the styled table
        st.markdown(table_html, unsafe_allow_html=True)

    # Display the additional table
    display_additional_table()

    # Function to edit tank properties
    def edit_tank_properties():
        st.write("Edit tank properties:")
        
        # Create a dataframe for tank properties
        tank_props = pd.DataFrame({
            'Viscosity': st.session_state.viscosity,
            'Sulfur (%)': st.session_state.sulfur
        })
        
        # Display editable dataframe for tank properties
        edited_props = st.data_editor(
            tank_props,
            use_container_width=True,
            column_config={
                'Viscosity': st.column_config.NumberColumn(
                    'Viscosity',
                    min_value=20.0,
                    max_value=100.0,
                    step=0.1,
                    format="%.1f"
                ),
                'Sulfur (%)': st.column_config.NumberColumn(
                    'Sulfur (%)',
                    min_value=0.05,
                    max_value=0.49,
                    step=0.01,
                    format="%.2f"
                )
            }
        )
        
        # Update session state with edited values
        st.session_state.viscosity = edited_props['Viscosity'].to_dict()
        st.session_state.sulfur = edited_props['Sulfur (%)'].to_dict()

    # Add a section to edit tank properties
    if st.checkbox("Edit Tank Properties"):
        edit_tank_properties()
   


def display_machinery():
    st.subheader("Machinery")

    # Main Engine
    st.subheader("Main Engine")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("ME RPM", min_value=0.0, step=0.1, key=f"me_rpm_{uuid.uuid4()}")
        st.number_input("ME TC1 RPM", min_value=0.0, step=0.1, key=f"me_tc1_rpm_{uuid.uuid4()}")
        st.number_input("ME TC2 RPM", min_value=0.0, step=0.1, key=f"me_tc2_rpm_{uuid.uuid4()}")
    with col2:
        st.number_input("Exhaust Max. Temp.(C)", min_value=0.0, step=0.1, key=f"exhaust_max_temp_{uuid.uuid4()}")
        st.number_input("Exhaust Min. Temp.(C)", min_value=0.0, step=0.1, key=f"exhaust_min_temp_{uuid.uuid4()}")
        st.number_input("M/E rev counter", min_value=0, step=1, key=f"me_rev_counter_{uuid.uuid4()}")
    with col3:
        st.number_input("Scavenge pressure(BAR)", min_value=0.0, step=0.01, key=f"scavenge_pressure_{uuid.uuid4()}")
        st.number_input("MCR", min_value=0.0, max_value=100.0, step=0.1, key=f"mcr_{uuid.uuid4()}")
        st.number_input("Avg KW", min_value=0.0, step=0.1, key=f"avg_kw_{uuid.uuid4()}")
    with col4:
        st.number_input("Slip", min_value=0.0, max_value=100.0, step=0.1, key=f"slip_{uuid.uuid4()}")
        st.number_input("SFOC", min_value=0.0, step=0.1, key=f"sfoc_{uuid.uuid4()}")
        st.number_input("Propeller pitch", min_value=0.0, step=0.1, key=f"propeller_pitch_{uuid.uuid4()}")

    # Auxiliary Engines
    st.subheader("Auxiliary Engines")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Avg A/E power 1", min_value=0.0, step=0.1, key=f"avg_ae_power_1_{uuid.uuid4()}")
    with col2:
        st.number_input("Avg A/E power 2", min_value=0.0, step=0.1, key=f"avg_ae_power_2_{uuid.uuid4()}")
    with col3:
        st.number_input("Avg A/E power 3", min_value=0.0, step=0.1, key=f"avg_ae_power_3_{uuid.uuid4()}")
    with col4:
        st.number_input("Avg A/E power 4", min_value=0.0, step=0.1, key=f"avg_ae_power_4_{uuid.uuid4()}")

    # Running Hours
    st.subheader("Running Hours")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Main engine", min_value=0.0, step=0.1, key=f"main_engine_hours_{uuid.uuid4()}")
        st.number_input("AE-1", min_value=0.0, step=0.1, key=f"ae_1_hours_{uuid.uuid4()}")
    with col2:
        st.number_input("A/E 2", min_value=0.0, step=0.1, key=f"ae_2_hours_{uuid.uuid4()}")
        st.number_input("A/E 3", min_value=0.0, step=0.1, key=f"ae_3_hours_{uuid.uuid4()}")
    with col3:
        st.number_input("A/E 4", min_value=0.0, step=0.1, key=f"ae_4_hours_{uuid.uuid4()}")
        st.number_input("Boilers", min_value=0.0, step=0.1, key=f"boilers_hours_{uuid.uuid4()}")
    with col4:
        st.number_input("Scrubbers", min_value=0.0, step=0.1, key=f"scrubbers_hours_{uuid.uuid4()}")
        st.number_input("Shaft gen", min_value=0.0, step=0.1, key=f"shaft_gen_hours_{uuid.uuid4()}")

    # Boilers
    st.subheader("Boilers")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Boiler 1 running hrs", min_value=0.0, step=0.1, key=f"boiler_1_hours_{uuid.uuid4()}")
    with col2:
        st.number_input("Boiler 2 running hrs", min_value=0.0, step=0.1, key=f"boiler_2_hours_{uuid.uuid4()}")

def display_custom_machinery(noon_report_type):
    st.subheader("Machinery")

    # Main Engine
    st.subheader("Main Engine")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("M/E rev counter", min_value=0, step=1, key=f"me_rev_counter_{uuid.uuid4()}")
    
    # Auxiliary Engines
    st.subheader("Auxiliary Engines")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Avg A/E power 1", min_value=0.0, step=0.1, key=f"avg_ae_power_1_{uuid.uuid4()}")
    with col2:
        st.number_input("Avg A/E power 2", min_value=0.0, step=0.1, key=f"avg_ae_power_2_{uuid.uuid4()}")
    with col3:
        st.number_input("Avg A/E power 3", min_value=0.0, step=0.1, key=f"avg_ae_power_3_{uuid.uuid4()}")
    with col4:
        st.number_input("Avg A/E power 4", min_value=0.0, step=0.1, key=f"avg_ae_power_4_{uuid.uuid4()}")

    # Running Hours
    st.subheader("Running Hours")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Main engine", min_value=0.0, step=0.1, key=f"main_engine_hours_{uuid.uuid4()}")
        st.number_input("AE-1", min_value=0.0, step=0.1, key=f"ae_1_hours_{uuid.uuid4()}")
    with col2:
        st.number_input("A/E 2", min_value=0.0, step=0.1, key=f"ae_2_hours_{uuid.uuid4()}")
        st.number_input("A/E 3", min_value=0.0, step=0.1, key=f"ae_3_hours_{uuid.uuid4()}")
    with col3:
        st.number_input("A/E 4", min_value=0.0, step=0.1, key=f"ae_4_hours_{uuid.uuid4()}")
        st.number_input("Boilers", min_value=0.0, step=0.1, key=f"boilers_hours_{uuid.uuid4()}")
    with col4:
        st.number_input("Scrubbers", min_value=0.0, step=0.1, key=f"scrubbers_hours_{uuid.uuid4()}")
        st.number_input("Shaft gen", min_value=0.0, step=0.1, key=f"shaft_gen_hours_{uuid.uuid4()}")

    # Boilers
    st.subheader("Boilers")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Boiler 1 running hrs", min_value=0.0, step=0.1, key=f"boiler_1_hours_{uuid.uuid4()}")
    with col2:
        st.number_input("Boiler 2 running hrs", min_value=0.0, step=0.1, key=f"boiler_2_hours_{uuid.uuid4()}")

def display_environmental_compliance():
    st.subheader("Environmental Compliance")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1, key=f"sludge_rob_{uuid.uuid4()}")
        st.number_input("Sludge Burnt in Incinerator (MT)", min_value=0.0, step=0.1, key=f"sludge_burnt_{uuid.uuid4()}")
    
    with col2:
        st.number_input("Sludge Landed Ashore (MT)", min_value=0.0, step=0.1, key=f"sludge_landed_{uuid.uuid4()}")
        st.number_input("Bilge Water Quantity (m³)", min_value=0.0, step=0.1, key=f"bilge_water_qty_{uuid.uuid4()}")
    
    with col3:
        st.number_input("Bilge Water Pumped Out through 15ppm Equipment (m³)", min_value=0.0, step=0.1, key=f"bilge_pumped_out_{uuid.uuid4()}")
        st.number_input("Bilge Water Landed Ashore (m³)", min_value=0.0, step=0.1, key=f"bilge_landed_{uuid.uuid4()}")

def display_custom_environmental_compliance(noon_report_type):
    st.subheader("Environmental Compliance")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1, key=f"sludge_rob_{uuid.uuid4()}")
    
    with col2:
        st.number_input("Sludge Landed Ashore (MT)", min_value=0.0, step=0.1, key=f"sludge_landed_{uuid.uuid4()}")
        st.number_input("Bilge Water Quantity (m³)", min_value=0.0, step=0.1, key=f"bilge_water_qty_{uuid.uuid4()}")
    
    with col3:
        st.number_input("Bilge Water Landed Ashore (m³)", min_value=0.0, step=0.1, key=f"bilge_landed_{uuid.uuid4()}")

def display_miscellaneous_consumables():
    st.subheader("Miscellaneous Consumables")

    st.markdown("Fresh Water")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.number_input("Fresh Water Bunkered (m³)", min_value=0.0, step=0.1, key=f"fw_bunkered_{uuid.uuid4()}")
        st.number_input("Fresh Water Consumption - Drinking (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_drinking_{uuid.uuid4()}")
    
    with col2:
        st.number_input("Fresh Water Consumption - Technical (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_technical_{uuid.uuid4()}")
        st.number_input("Fresh Water Consumption - Washing (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_washing_{uuid.uuid4()}")
    
    with col3:
        st.number_input("Fresh Water Produced (m³)", min_value=0.0, step=0.1, key=f"fw_produced_{uuid.uuid4()}")
        st.number_input("Fresh Water ROB (m³)", min_value=0.0, step=0.1, key=f"fw_rob_{uuid.uuid4()}")
    
    with col4:
        st.number_input("Fresh Water Usage - Galley (m³)", min_value=0.0, step=0.1, key=f"fw_usage_galley_{uuid.uuid4()}")
        st.number_input("Fresh Water Usage - Laundry (m³)", min_value=0.0, step=0.1, key=f"fw_usage_laundry_{uuid.uuid4()}")

    st.markdown("Lubricating Oil")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.number_input("ME Cylinder Oil High BN ROB (liters)", min_value=0, step=1, key=f"me_cyl_oil_high_bn_rob_{uuid.uuid4()}")
        st.number_input("ME Cylinder Oil Low BN ROB (liters)", min_value=0, step=1, key=f"me_cyl_oil_low_bn_rob_{uuid.uuid4()}")
    
    with col2:
        st.number_input("ME System Oil ROB (liters)", min_value=0, step=1, key=f"me_system_oil_rob_{uuid.uuid4()}")
        st.number_input("AE System Oil ROB (liters)", min_value=0, step=1, key=f"ae_system_oil_rob_{uuid.uuid4()}")
    
    with col3:
        st.number_input("ME Cylinder Oil Consumption (liters)", min_value=0, step=1, key=f"me_cyl_oil_consumption_{uuid.uuid4()}")
        st.number_input("ME Cylinder Oil Feed Rate (g/kWh)", min_value=0.0, step=0.1, key=f"me_cyl_oil_feed_rate_{uuid.uuid4()}")
    
    with col4:
        st.number_input("ME System Oil Consumption (liters)", min_value=0, step=1, key=f"me_system_oil_consumption_{uuid.uuid4()}")
        st.number_input("AE System Oil Consumption (liters)", min_value=0, step=1, key=f"ae_system_oil_consumption_{uuid.uuid4()}")

def display_custom_miscellaneous_consumables(noon_report_type):
    st.subheader("Miscellaneous Consumables")

    st.markdown("Fresh Water")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.number_input("Fresh Water Bunkered (m³)", min_value=0.0, step=0.1, key=f"fw_bunkered_{uuid.uuid4()}")
        st.number_input("Fresh Water Consumption - Drinking (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_drinking_{uuid.uuid4()}")
    
    with col2:
        st.number_input("Fresh Water Consumption - Technical (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_technical_{uuid.uuid4()}")
        st.number_input("Fresh Water Consumption - Washing (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_washing_{uuid.uuid4()}")
    
    with col3:
        st.number_input("Fresh Water Produced (m³)", min_value=0.0, step=0.1, key=f"fw_produced_{uuid.uuid4()}")
        st.number_input("Fresh Water ROB (m³)", min_value=0.0, step=0.1, key=f"fw_rob_{uuid.uuid4()}")
    
    with col4:
        st.number_input("Fresh Water Usage - Galley (m³)", min_value=0.0, step=0.1, key=f"fw_usage_galley_{uuid.uuid4()}")
        st.number_input("Fresh Water Usage - Laundry (m³)", min_value=0.0, step=0.1, key=f"fw_usage_laundry_{uuid.uuid4()}")

    st.markdown("Lubricating Oil")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.number_input("ME Cylinder Oil High BN ROB (liters)", min_value=0, step=1, key=f"me_cyl_oil_high_bn_rob_{uuid.uuid4()}")
        st.number_input("ME Cylinder Oil Low BN ROB (liters)", min_value=0, step=1, key=f"me_cyl_oil_low_bn_rob_{uuid.uuid4()}")
    
    with col2:
        st.number_input("ME System Oil ROB (liters)", min_value=0, step=1, key=f"me_system_oil_rob_{uuid.uuid4()}")
        st.number_input("AE System Oil ROB (liters)", min_value=0, step=1, key=f"ae_system_oil_rob_{uuid.uuid4()}")
    
    with col3:
        st.number_input("ME Cylinder Oil Consumption (liters)", min_value=0, step=1, key=f"me_cyl_oil_consumption_{uuid.uuid4()}")
        st.number_input("ME Cylinder Oil Feed Rate (g/kWh)", min_value=0.0, step=0.1, key=f"me_cyl_oil_feed_rate_{uuid.uuid4()}")
    
    with col4:
        st.number_input("ME System Oil Consumption (liters)", min_value=0, step=1, key=f"me_system_oil_consumption_{uuid.uuid4()}")
        st.number_input("AE System Oil Consumption (liters)", min_value=0, step=1, key=f"ae_system_oil_consumption_{uuid.uuid4()}")

if __name__ == "__main__":
    main()
