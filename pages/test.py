import streamlit as st
import pandas as pd
from datetime import datetime, time
import uuid

st.set_page_config(layout="wide", page_title="Maritime Reporting Portal", page_icon="🚢")

# Custom CSS for improved aesthetics
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        font-family: 'Helvetica', sans-serif;
    }
    .main-header {
        background-color: #1E3A8A;
        padding: 1rem;
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .section-header {
        background-color: #3B82F6;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    .stButton > button {
        width: 100%;
    }
    .stTextInput > div > div > input {
        background-color: #F3F4F6;
    }
    .stSelectbox > div > div > select {
        background-color: #F3F4F6;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-header"><h1>Maritime Reporting Portal</h1></div>', unsafe_allow_html=True)

    # Sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        noon_report_type = st.selectbox("Select Noon Report Type",
                                        ["Noon at Sea", "Noon at Port", "Noon at Anchor", "Noon at Drifting", "Noon at STS", "Noon at Canal/River Passage"])
        
        if st.button("Generate Report", key="generate_report"):
            st.success("Report generation initiated!")

    # Main content
    if noon_report_type in ["Noon at Sea", "Noon at Drifting", "Noon at Canal/River Passage"]:
        display_base_report_form()
    else:
        display_custom_report_form(noon_report_type)

def display_base_report_form():
    sections = [
        "General Information",
        "Voyage Details",
        "Speed, Position and Navigation",
        "Weather and Sea Conditions",
        "Cargo and Stability",
        "Fuel Consumption",
        "Fuel Allocation",
        "Machinery",
        "Environmental Compliance",
        "Miscellaneous Consumables",
    ]

    selected_section = st.radio("Select Section", sections)

    for section in sections:
        if selected_section == section:
            st.markdown(f'<div class="section-header"><h2>{section}</h2></div>', unsafe_allow_html=True)
            function_name = f"display_{section.lower().replace(' ', '_').replace(',', '')}"
            if function_name in globals():
                globals()[function_name]()
            else:
                st.warning(f"Function {function_name} not found.")

    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("Submit Report", type="primary", key=f"submit_report_{uuid.uuid4()}"):
            st.success("Report submitted successfully!")

def display_custom_report_form(noon_report_type):
    sections = [
        "General Information",
        "Voyage Details",
        "Speed, Position and Navigation",
        "Weather and Sea Conditions",
        "Cargo and Stability",
        "Fuel Consumption",
        "Fuel Allocation",
        "Machinery",
        "Environmental Compliance",
        "Miscellaneous Consumables",
    ]

    selected_section = st.radio("Select Section", sections)

    for section in sections:
        if selected_section == section:
            st.markdown(f'<div class="section-header"><h2>{section}</h2></div>', unsafe_allow_html=True)
            function_name = f"display_custom_{section.lower().replace(' ', '_').replace(',', '')}"
            if function_name in globals():
                globals()[function_name](noon_report_type)
            else:
                st.warning(f"Function {function_name} not found.")

    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("Submit Report", type="primary", key=f"submit_report_{uuid.uuid4()}"):
            st.success("Report submitted successfully!")

def display_custom_report_form(noon_report_type):
    sections = [
        "General Information",
        "Voyage Details",
        "Speed, Position and Navigation",
        "Weather and Sea Conditions",
        "Cargo and Stability",
        "Fuel Consumption",
        "Fuel Allocation",
        "Machinery",
        "Environmental Compliance",
        "Miscellaneous Consumables",
    ]

    tabs = stx.tab_bar(data=[
        stx.TabBarItemData(id=section.lower().replace(" ", "_"), title=section, description="")
        for section in sections
    ])

    for section in sections:
        if tabs == section.lower().replace(" ", "_"):
            st.markdown(f'<div class="section-header"><h2>{section}</h2></div>', unsafe_allow_html=True)
            function_name = f"display_custom_{section.lower().replace(' ', '_').replace(',', '')}"
            if function_name in globals():
                globals()[function_name](noon_report_type)
            else:
                st.warning(f"Function {function_name} not found.")

    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("Submit Report", type="primary", key=f"submit_report_{uuid.uuid4()}"):
            st.success("Report submitted successfully!")

def display_general_information():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("IMO Number", key=f"imo_number_{uuid.uuid4()}")
        st.text_input("Voyage ID", key=f"voyage_id_{uuid.uuid4()}")
    with col2:
        st.text_input("Vessel Name", key=f"vessel_name_{uuid.uuid4()}")
        st.text_input("Segment ID", key=f"segment_id_{uuid.uuid4()}")
    with col3:
        st.text_input("Vessel Type", key=f"vessel_type_{uuid.uuid4()}")

def display_custom_general_information(noon_report_type):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Port Name", key=f"port_name_{uuid.uuid4()}")
        st.text_input("Port UNLOCODE", key=f"port_unlo_{uuid.uuid4()}")
    with col2:
        st.text_input("Vessel Name", key=f"vessel_name_{uuid.uuid4()}")
        st.text_input("Segment ID", key=f"segment_id_{uuid.uuid4()}")
    with col3:
        st.text_input("Vessel Type", key=f"vessel_type_{uuid.uuid4()}")

def display_voyage_details():
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Voyage From", key="voyage_from")
        st.text_input("Voyage To", key="voyage_to")
        st.text_input("Speed Order", key="speed_order")
        st.selectbox("Voyage Type", ["", "One-way", "Round trip", "STS"], key="voyage_type")
        st.selectbox("Voyage Stage", ["", "East", "West", "Ballast", "Laden"], key="voyage_stage")
        st.date_input("ETA", value=datetime.now(), key="eta")
        st.text_input("Charter Type", key="charter_type")
    
    with col2:
        st.number_input("Time Since Last Report (hours)", min_value=0.0, step=0.1, key="time_since_last_report")
        st.selectbox("Clocks Advanced/Retarded", ["", "Advanced", "Retarded"], key="clocks_change")
        st.number_input("Clocks Changed By (minutes)", min_value=0, step=1, key="clocks_change_minutes")
        
        st.markdown("### Special Conditions")
        col_a, col_b = st.columns(2)
        with col_a:
            offhire = st.checkbox("Off-hire", key="offhire")
            eca_transit = st.checkbox("ECA Transit", key="eca_transit")
            fuel_changeover = st.checkbox("Fuel Changeover", key="fuel_changeover")
            idl_crossing = st.checkbox("IDL Crossing", key="idl_crossing")
        with col_b:
            stoppage = st.checkbox("Stoppage", key="stoppage")
            deviation = st.checkbox("Deviation", key="deviation")
            special_area = st.checkbox("Transiting Special Area", key="special_area")

    if offhire:
        with st.expander("Off-hire Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.date_input("Off-hire Start Date (LT)", key="offhire_start_date_lt")
                st.time_input("Off-hire Start Time (LT)", key="offhire_start_time_lt")
                st.date_input("Off-hire Start Date (UTC)", key="offhire_start_date_utc")
                st.time_input("Off-hire Start Time (UTC)", key="offhire_start_time_utc")
                st.text_input("Start Off-hire Position Latitude", key="start_offhire_lat")
                st.text_input("Start Off-hire Position Longitude", key="start_offhire_lon")
            with col2:
                st.date_input("Off-hire End Date (LT)", key="offhire_end_date_lt")
                st.time_input("Off-hire End Time (LT)", key="offhire_end_time_lt")
                st.date_input("Off-hire End Date (UTC)", key="offhire_end_date_utc")
                st.time_input("Off-hire End Time (UTC)", key="offhire_end_time_utc")
                st.text_input("End Off-hire Position Latitude", key="end_offhire_lat")
                st.text_input("End Off-hire Position Longitude", key="end_offhire_lon")
            st.text_area("Off-hire Reason", key="offhire_reason")
    
    if eca_transit:
        with st.expander("ECA Transit Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.date_input("ECA Entry Date", key="eca_entry_date")
                st.time_input("ECA Entry Time", key="eca_entry_time")
                st.text_input("ECA Entry Latitude", key="eca_entry_lat")
                st.text_input("ECA Entry Longitude", key="eca_entry_lon")
            with col2:
                st.date_input("ECA Exit Date", key="eca_exit_date")
                st.time_input("ECA Exit Time", key="eca_exit_time")
                st.text_input("ECA Exit Latitude", key="eca_exit_lat")
                st.text_input("ECA Exit Longitude", key="eca_exit_lon")
            st.text_input("ECA Name", key="eca_name")
    
    if fuel_changeover:
        with st.expander("Fuel Changeover Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Start of Changeover")
                st.date_input("Changeover Start Date", key="changeover_start_date")
                st.time_input("Changeover Start Time", key="changeover_start_time")
                st.text_input("Changeover Start Latitude", key="changeover_start_lat")
                st.text_input("Changeover Start Longitude", key="changeover_start_lon")
                st.number_input("VLSFO ROB at Start (MT)", min_value=0.0, step=0.1, key="vlsfo_rob_start")
                st.number_input("LSMGO ROB at Start (MT)", min_value=0.0, step=0.1, key="lsmgo_rob_start")
            with col2:
                st.subheader("End of Changeover")
                st.date_input("Changeover End Date", key="changeover_end_date")
                st.time_input("Changeover End Time", key="changeover_end_time")
                st.text_input("Changeover End Latitude", key="changeover_end_lat")
                st.text_input("Changeover End Longitude", key="changeover_end_lon")
                st.number_input("VLSFO ROB at End (MT)", min_value=0.0, step=0.1, key="vlsfo_rob_end")
                st.number_input("LSMGO ROB at End (MT)", min_value=0.0, step=0.1, key="lsmgo_rob_end")
    
    if idl_crossing:
        with st.expander("IDL Crossing Details", expanded=True):
            st.selectbox("IDL Direction", ["East", "West"], key="idl_direction")
    
    if stoppage:
        with st.expander("Stoppage Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.date_input("Stoppage Start Date (LT)", key="stoppage_start_date_lt")
                st.time_input("Stoppage Start Time (LT)", key="stoppage_start_time_lt")
                st.date_input("Stoppage Start Date (UTC)", key="stoppage_start_date_utc")
                st.time_input("Stoppage Start Time (UTC)", key="stoppage_start_time_utc")
                st.text_input("Start Stoppage Position Latitude", key="start_stoppage_lat")
                st.text_input("Start Stoppage Position Longitude", key="start_stoppage_lon")
            with col2:
                st.date_input("Stoppage End Date (LT)", key="stoppage_end_date_lt")
                st.time_input("Stoppage End Time (LT)", key="stoppage_end_time_lt")
                st.date_input("Stoppage End Date (UTC)", key="stoppage_end_date_utc")
                st.time_input("Stoppage End Time (UTC)", key="stoppage_end_time_utc")
                st.text_input("End Stoppage Position Latitude", key="end_stoppage_lat")
                st.text_input("End Stoppage Position Longitude", key="end_stoppage_lon")
            st.text_area("Stoppage Reason", key="stoppage_reason")
        
    if deviation:
        with st.expander("Deviation Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                reason = st.selectbox("Reason for Deviation", ["Heavy weather", "SAR operation", "Navigational area Warning", "Med-evac", "Others"], key="deviation_reason")
                if reason == "Others":
                    st.text_input("Specify Other Reason", key="deviation_other_reason")
                st.date_input("Start Deviation Date (LT)", key="start_deviation_date_lt")
                st.time_input("Start Deviation Time (LT)", key="start_deviation_time_lt")
                st.date_input("Start Deviation Date (UTC)", key="start_deviation_date_utc")
                st.time_input("Start Deviation Time (UTC)", key="start_deviation_time_utc")
                st.text_input("Start Deviation Position Latitude", key="start_deviation_lat")
                st.text_input("Start Deviation Position Longitude", key="start_deviation_lon")
            with col2:
                st.subheader("End of Deviation")
                st.date_input("End Deviation Date (LT)", key="end_deviation_date_lt")
                st.time_input("End Deviation Time (LT)", key="end_deviation_time_lt")
                st.date_input("End Deviation Date (UTC)", key="end_deviation_date_utc")
                st.time_input("End Deviation Time (UTC)", key="end_deviation_time_utc")
                st.text_input("End Deviation Position Latitude", key="end_deviation_lat")
                st.text_input("End Deviation Position Longitude", key="end_deviation_lon")
            st.text_area("Deviation Comments", key="deviation_comments")

    if special_area:
        with st.expander("Transiting Special Area Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                special_area_type = st.selectbox("Special Area Type", ["JWC area", "IWL", "ICE regions", "HRA"], key="special_area_type")
                st.date_input("Entry Special Area Date (LT)", key="entry_special_area_date_lt")
                st.time_input("Entry Special Area Time (LT)", key="entry_special_area_time_lt")
                st.date_input("Entry Special Area Date (UTC)", key="entry_special_area_date_utc")
                st.time_input("Entry Special Area Time (UTC)", key="entry_special_area_time_utc")
                st.text_input("Entry Special Area Position Latitude", key="entry_special_area_lat")
                st.text_input("Entry Special Area Position Longitude", key="entry_special_area_lon")
            with col2:
                st.date_input("Exit Special Area Date (LT)", key="exit_special_area_date_lt")
                st.time_input("Exit Special Area Time (LT)", key="exit_special_area_time_lt")
                st.date_input("Exit Special Area Date (UTC)", key="exit_special_area_date_utc")
                st.time_input("Exit Special Area Time (UTC)", key="exit_special_area_time_utc")
                st.text_input("Exit Special Area Position Latitude", key="exit_special_area_lat")
                st.text_input("Exit Special Area Position Longitude", key="exit_special_area_lon")
            st.text_area("Special Area Comments", key="special_area_comments")

def display_custom_voyage_details(noon_report_type):
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Voyage From", key="voyage_from")
        st.text_input("Voyage To", key="voyage_to")
        st.text_input("Speed Order", key="speed_order")
        st.selectbox("Voyage Type", ["", "One-way", "Round trip", "STS"], key="voyage_type")
        st.selectbox("Voyage Stage", ["", "East", "West", "Ballast", "Laden"], key="voyage_stage")
        st.date_input("ETA", value=datetime.now(), key="eta")
        st.text_input("Charter Type", key="charter_type")
    
    with col2:
        st.number_input("Time Since Last Report (hours)", min_value=0.0, step=0.1, key="time_since_last_report")
        st.selectbox("Clocks Advanced/Retarded", ["", "Advanced", "Retarded"], key="clocks_change")
        st.number_input("Clocks Changed By (minutes)", min_value=0, step=1, key="clocks_change_minutes")
        
        st.markdown("### Special Conditions")
        col_a, col_b = st.columns(2)
        with col_a:
            offhire = st.checkbox("Off-hire", key="offhire")
            eca_transit = st.checkbox("ECA Transit", key="eca_transit")
            fuel_changeover = st.checkbox("Fuel Changeover", key="fuel_changeover")
        with col_b:
            drydock = st.checkbox("Drydock", key="drydock")

    if offhire:
        with st.expander("Off-hire Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.date_input("Off-hire Start Date (LT)", key="offhire_start_date_lt")
                st.time_input("Off-hire Start Time (LT)", key="offhire_start_time_lt")
                st.date_input("Off-hire Start Date (UTC)", key="offhire_start_date_utc")
                st.time_input("Off-hire Start Time (UTC)", key="offhire_start_time_utc")
                st.text_input("Start Off-hire Position Latitude", key="start_offhire_lat")
                st.text_input("Start Off-hire Position Longitude", key="start_offhire_lon")
            with col2:
                st.date_input("Off-hire End Date (LT)", key="offhire_end_date_lt")
                st.time_input("Off-hire End Time (LT)", key="offhire_end_time_lt")
                st.date_input("Off-hire End Date (UTC)", key="offhire_end_date_utc")
                st.time_input("Off-hire End Time (UTC)", key="offhire_end_time_utc")
                st.text_input("End Off-hire Position Latitude", key="end_offhire_lat")
                st.text_input("End Off-hire Position Longitude", key="end_offhire_lon")
            st.text_area("Off-hire Reason", key="offhire_reason")
    
    if eca_transit:
        with st.expander("ECA Transit Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.date_input("ECA Entry Date", key="eca_entry_date")
                st.time_input("ECA Entry Time", key="eca_entry_time")
                st.text_input("ECA Entry Latitude", key="eca_entry_lat")
                st.text_input("ECA Entry Longitude", key="eca_entry_lon")
            with col2:
                st.date_input("ECA Exit Date", key="eca_exit_date")
                st.time_input("ECA Exit Time", key="eca_exit_time")
                st.text_input("ECA Exit Latitude", key="eca_exit_lat")
                st.text_input("ECA Exit Longitude", key="eca_exit_lon")
            st.text_input("ECA Name", key="eca_name")
    
    if fuel_changeover:
        with st.expander("Fuel Changeover Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Start of Changeover")
                st.date_input("Changeover Start Date", key="changeover_start_date")
                st.time_input("Changeover Start Time", key="changeover_start_time")
                st.text_input("Changeover Start Latitude", key="changeover_start_lat")
                st.text_input("Changeover Start Longitude", key="changeover_start_lon")
                st.number_input("VLSFO ROB at Start (MT)", min_value=0.0, step=0.1, key="vlsfo_rob_start")
                st.number_input("LSMGO ROB at Start (MT)", min_value=0.0, step=0.1, key="lsmgo_rob_start")
            with col2:
                st.subheader("End of Changeover")
                st.date_input("Changeover End Date", key="changeover_end_date")
                st.time_input("Changeover End Time", key="changeover_end_time")
                st.text_input("Changeover End Latitude", key="changeover_end_lat")
                st.text_input("Changeover End Longitude", key="changeover_end_lon")
                st.number_input("VLSFO ROB at End (MT)", min_value=0.0, step=0.1, key="vlsfo_rob_end")
                st.number_input("LSMGO ROB at End (MT)", min_value=0.0, step=0.1, key="lsmgo_rob_end")

    if drydock:
        with st.expander("Drydock Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.date_input("Drydock Start Date", key="drydock_start_date")
                st.time_input("Drydock Start Time", key="drydock_start_time")
            with col2:
                st.date_input("Expected Drydock End Date", key="expected_drydock_end_date")
                st.time_input("Expected Drydock End Time", key="expected_drydock_end_time")
            st.text_input("Drydock Location", key="drydock_location")
            st.text_area("Drydock Purpose", key="drydock_purpose")

def display_speed_position_and_navigation():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1, value=0.00, key=f"distance_observed_{uuid.uuid4()}")
        st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1, value=0.00, key=f"distance_togo_{uuid.uuid4()}")
        st.date_input("Date (Local)", value=datetime.now(), key=f"local_date_{uuid.uuid4()}")
        st.text_input("Ordered Speed", key=f"speed_order_{uuid.uuid4()}")
        
    with col2:
        st.number_input("Distance Through Water (nm)", min_value=0.0, step=0.1, key=f"distance_through_water_{uuid.uuid4()}")
        st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1, key=f"obs_speed_sog_{uuid.uuid4()}")
        st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1, key=f"em_log_speed_{uuid.uuid4()}")
        st.time_input("Time (Local)", value=datetime.now().time(), key=f"local_time_{uuid.uuid4()}")
    
    with col3:
        col3_1, col3_2 = st.columns(2)
        with col3_1:
            st.number_input("Latitude", min_value=-90, max_value=90, step=1, key=f"lat_degree_{uuid.uuid4()}")
            st.number_input("Longitude", min_value=-180, max_value=180, step=1, key=f"lon_degree_{uuid.uuid4()}")
        with col3_2:
            st.selectbox("Latitude N/S", ["N", "S"], key=f"lat_ns_{uuid.uuid4()}")
            st.selectbox("Longitude E/W", ["E", "W"], key=f"lon_ew_{uuid.uuid4()}")
        
        st.number_input("Course (°)", min_value=0, max_value=359, step=1, key=f"course_{uuid.uuid4()}")
        st.number_input("Heading (°)", min_value=0, max_value=359, step=1, key=f"heading_{uuid.uuid4()}")
        
    col4, col5 = st.columns(2)
    with col4:
        st.date_input("Date (UTC)", value=datetime.now(), key=f"utc_date_{uuid.uuid4()}")
    with col5:
        st.time_input("Time (UTC)", value=datetime.now().time(), key=f"utc_time_{uuid.uuid4()}")

def display_custom_speed_position_and_navigation(noon_report_type):
    col1, col2, col3 = st.columns(3)
    with col1:
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            st.number_input("Latitude", min_value=-90, max_value=90, step=1, key=f"lat_degree_{uuid.uuid4()}")
        with col1_2:
            st.selectbox("Latitude N/S", ["N", "S"], key=f"lat_ns_{uuid.uuid4()}")
        st.date_input("Date (Local)", value=datetime.now(), key=f"local_date_{uuid.uuid4()}")
        
    with col2:
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            st.number_input("Longitude", min_value=-180, max_value=180, step=1, key=f"lon_degree_{uuid.uuid4()}")
        with col2_2:
            st.selectbox("Longitude E/W", ["E", "W"], key=f"lon_ew_{uuid.uuid4()}")
        st.time_input("Time (UTC)", value=datetime.now().time(), key=f"utc_time_{uuid.uuid4()}")
        
    with col3:
        st.time_input("Time (Local)", value=datetime.now().time(), key=f"local_time_{uuid.uuid4()}")
        st.date_input("Date (UTC)", value=datetime.now(), key=f"utc_date_{uuid.uuid4()}")

def display_weather_and_sea_conditions():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("True Wind Speed (kts)", min_value=0.0, step=0.1, key=f"true_wind_speed_{uuid.uuid4()}")
        st.selectbox("BF Scale", range(13), key=f"bf_scale_{uuid.uuid4()}")
        st.number_input("True Wind Direction (°)", min_value=0, max_value=359, step=1, key=f"true_wind_direction_{uuid.uuid4()}")
        st.number_input("Sea Water Temp (°C)", min_value=-2.0, max_value=35.0, step=0.1, key=f"sea_water_temp_{uuid.uuid4()}")
        st.number_input("Significant Wave Height (m)", min_value=0.0, step=0.1, key=f"sig_wave_height_{uuid.uuid4()}")
        st.selectbox("Sea State (Douglas)", range(10), key=f"douglas_sea_state_{uuid.uuid4()}")
        
    with col2:
        st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key=f"sea_height_{uuid.uuid4()}")
        st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key=f"air_temp_{uuid.uuid4()}")
        st.number_input("Sea Direction (°)", min_value=0, max_value=359, step=1, key=f"sea_direction_{uuid.uuid4()}")
        st.number_input("Swell Direction (°)", min_value=0, max_value=359, step=1, key=f"swell_direction_{uuid.uuid4()}")
        st.number_input("Swell Height (m) (DSS)", min_value=0.0, step=0.1, key=f"swell_height_{uuid.uuid4()}")
        st.number_input("Current Strength (kts)", min_value=0.0, step=0.1, key=f"current_strength_{uuid.uuid4()}")
        st.number_input("Current Direction (°)", min_value=0, max_value=359, step=1, key=f"current_direction_{uuid.uuid4()}")
        st.number_input("Atm Pr (bar)", min_value=900, max_value=1100, step=1, key=f"atms_pr_{uuid.uuid4()}")

def display_custom_weather_and_sea_conditions(noon_report_type):
    display_weather_and_sea_conditions()  # Same as non-custom version for this section

def display_cargo_and_stability():
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Vessel Condition", ["", "Laden", "Ballast"], key=f"vessel_condition_{uuid.uuid4()}")
        st.number_input("FWD Draft (m)", min_value=0.0, step=0.01, key=f"fwd_draft_{uuid.uuid4()}")
        st.number_input("GM (m)", min_value=0.0, step=0.01, key=f"gm_{uuid.uuid4()}")
        st.number_input("LCG (m)", min_value=0.0, step=0.01, key=f"lcg_{uuid.uuid4()}")
        st.number_input("Displacement (MT)", min_value=0.0, step=0.1, key=f"displacement_{uuid.uuid4()}")
        st.number_input("Mid Draft (m)", min_value=0.0, step=0.01, key=f"mid_draft_{uuid.uuid4()}")
    with col2:
        st.number_input("Ballast Quantity (m³)", min_value=0.0, step=0.1, key=f"ballast_qty_{uuid.uuid4()}")
        st.number_input("VCG (m)", min_value=0.0, step=0.01, key=f"vcg_{uuid.uuid4()}")
        st.number_input("Water Plane Co-efficient", min_value=0.0, step=0.01, key=f"water_plane_coefficient_{uuid.uuid4()}")
        st.number_input("AFT Draft (m)", min_value=0.0, step=0.01, key=f"aft_draft_{uuid.uuid4()}")
        st.number_input("Freeboard (m)", min_value=0.0, step=0.01, key=f"freeboard_{uuid.uuid4()}")
        st.number_input("Cb (Block Co-efficient)", min_value=0.0, step=0.01, key=f"cb_{uuid.uuid4()}")

    st.markdown("### Cargo Operations")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("Cargo Weight (MT)", min_value=0.0, step=0.1, key=f"cargo_weight_{uuid.uuid4()}")
        st.number_input("Cargo Volume (m³)", min_value=0.0, step=0.1, key=f"cargo_volume_{uuid.uuid4()}")
        st.number_input("Number of Passengers", min_value=0, step=1, key=f"passengers_{uuid.uuid4()}")
    with col2:
        st.number_input("Total TEU", min_value=0, step=1, key=f"total_teu_{uuid.uuid4()}")
        st.number_input("Reefer TEU", min_value=0, step=1, key=f"reefer_teu_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Chilled", min_value=0, step=1, key=f"reefer_20ft_chilled_{uuid.uuid4()}")
    with col3:
        st.number_input("Reefer 40ft Chilled", min_value=0, step=1, key=f"reefer_40ft_chilled_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Frozen", min_value=0, step=1, key=f"reefer_20ft_frozen_{uuid.uuid4()}")
        st.number_input("Reefer 40ft Frozen", min_value=0, step=1, key=f"reefer_40ft_frozen_{uuid.uuid4()}")

def display_custom_cargo_and_stability(noon_report_type):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Vessel Activity", ["Loading", "Discharging", "Both"], key=f"vessel_condition_{uuid.uuid4()}")
        st.number_input("FWD Draft (m)", min_value=0.0, step=0.01, key=f"fwd_draft_{uuid.uuid4()}")
        st.number_input("GM (m)", min_value=0.0, step=0.01, key=f"gm_{uuid.uuid4()}")
        st.number_input("LCG (m)", min_value=0.0, step=0.01, key=f"lcg_{uuid.uuid4()}")
        st.number_input("Displacement (MT)", min_value=0.0, step=0.1, key=f"displacement_{uuid.uuid4()}")
        st.number_input("Mid Draft (m)", min_value=0.0, step=0.01, key=f"mid_draft_{uuid.uuid4()}")
    with col2:
        st.number_input("Ballast Quantity (m³)", min_value=0.0, step=0.1, key=f"ballast_qty_{uuid.uuid4()}")
        st.number_input("VCG (m)", min_value=0.0, step=0.01, key=f"vcg_{uuid.uuid4()}")
        st.number_input("Water Plane Co-efficient", min_value=0.0, step=0.01, key=f"water_plane_coefficient_{uuid.uuid4()}")
        st.number_input("AFT Draft (m)", min_value=0.0, step=0.01, key=f"aft_draft_{uuid.uuid4()}")
        st.number_input("Freeboard (m)", min_value=0.0, step=0.01, key=f"freeboard_{uuid.uuid4()}")
        st.number_input("Cb (Block Co-efficient)", min_value=0.0, step=0.01, key=f"cb_{uuid.uuid4()}")

    st.markdown("### Cargo Operations")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cargo Loaded")
        st.number_input("Cargo Loaded (MT)", min_value=0.0, step=0.1, key=f"cargo_loaded_weight_{uuid.uuid4()}")
        st.number_input("Cargo Loaded (m³)", min_value=0.0, step=0.1, key=f"cargo_loaded_volume_{uuid.uuid4()}")
        st.number_input("Total TEU Loaded", min_value=0, step=1, key=f"total_teu_loaded_{uuid.uuid4()}")
        st.number_input("Reefer TEU Loaded", min_value=0, step=1, key=f"reefer_teu_loaded_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Chilled Loaded", min_value=0, step=1, key=f"reefer_20ft_chilled_loaded_{uuid.uuid4()}")
        st.number_input("Reefer 40ft Chilled Loaded", min_value=0, step=1, key=f"reefer_40ft_chilled_loaded_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Frozen Loaded", min_value=0, step=1, key=f"reefer_20ft_frozen_loaded_{uuid.uuid4()}")
        st.number_input("Reefer 40ft Frozen Loaded", min_value=0, step=1, key=f"reefer_40ft_frozen_loaded_{uuid.uuid4()}")
    with col2:
        st.subheader("Cargo Discharged")
        st.number_input("Cargo Discharged (MT)", min_value=0.0, step=0.1, key=f"cargo_discharged_weight_{uuid.uuid4()}")
        st.number_input("Cargo Discharged (m³)", min_value=0.0, step=0.1, key=f"cargo_discharged_volume_{uuid.uuid4()}")
        st.number_input("Total TEU Discharged", min_value=0, step=1, key=f"total_teu_discharged_{uuid.uuid4()}")
        st.number_input("Reefer TEU Discharged", min_value=0, step=1, key=f"reefer_teu_discharged_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Chilled Discharged", min_value=0, step=1, key=f"reefer_20ft_chilled_discharged_{uuid.uuid4()}")
        st.number_input("Reefer 40ft Chilled Discharged", min_value=0, step=1, key=f"reefer_40ft_chilled_discharged_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Frozen Discharged", min_value=0, step=1, key=f"reefer_20ft_frozen_discharged_{uuid.uuid4()}")
        st.number_input("Reefer 40ft Frozen Discharged", min_value=0, step=1, key=f"reefer_40ft_frozen_discharged_{uuid.uuid4()}")

def display_fuel_consumption():
    st.markdown("### Fuel Consumption (MT)")
    
    fuel_types = [
        "Heavy Fuel Oil RME-RMK >80cSt",
        "Heavy Fuel Oil RMA-RMD <80cSt",
        "VLSFO RME-RMK Visc >80cSt 0.5%S Max",
        "VLSFO RMA-RMD Visc <80cSt 0.5%S Max",
        "ULSFO RME-RMK <80cSt 0.1%S Max",
        "ULSFO RMA-RMD <80cSt 0.1%S Max",
        "VLSMGO 0.5%S Max",
        "ULSMGO 0.1%S Max",
        "Biofuel - 30",
        "Biofuel Distillate FO",
        "LPG - Propane",
        "LPG - Butane",
        "LNG Boil Off",
        "LNG (Bunkered)"
    ]

    columns = ["Oil Type", "Previous ROB", "AT SEA M/E", "AT SEA A/E", "AT SEA BLR", "AT SEA IGG", "AT SEA GE/NG", "AT SEA OTH",
               "Incinerator", "GCU", "Total", "ROB at Noon", "Action"]

    df = pd.DataFrame(columns=columns)
    df['Oil Type'] = fuel_types
    edited_df = st.data_editor(df, num_rows="dynamic", key=f"fuel_consumption_table_{uuid.uuid4()}")

    if st.button("Add New Fuel Type"):
        st.text_input("New Fuel Type Name")

    st.markdown("### Tank Distribution")
    tank_names = ["Tank1", "Tank2", "Tank3", "Tank4", "Tank5", "Tank6", 
                  "FO Serv Tank 1", "FO Serv Tank 2", "DO Serv Tank", 
                  "FO Overflow Tank", "FO Drain Tank"]
    
    tank_df = pd.DataFrame(columns=["Tank Name", "Grade of Fuel", "ROB (m³)"])
    tank_df['Tank Name'] = tank_names
    edited_tank_df = st.data_editor(tank_df, num_rows="dynamic", key=f"tank_distribution_table_{uuid.uuid4()}")

def display_custom_fuel_consumption(noon_report_type):
    st.markdown("### Fuel Consumption (mt)")
    
    bunkering_happened = st.checkbox("Bunkering Happened")

    if bunkering_happened:
        st.markdown("#### Bunkering Details")
        
        if 'bunkering_entries' not in st.session_state:
            st.session_state.bunkering_entries = [{}]

        for i, entry in enumerate(st.session_state.bunkering_entries):
            with st.expander(f"Bunkering Entry {i+1}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    entry['grade'] = st.selectbox("Grade of Fuel Bunkered", 
                                                  ["VLSFO", "HFO", "MGO", "LSMGO", "LNG"], 
                                                  key=f"grade_{i}")
                    entry['grade_bdn'] = st.text_input("Grade as per BDN", key=f"grade_bdn_{i}")
                    entry['qty_bdn'] = st.number_input("Quantity as per BDN (mt)", 
                                                       min_value=0.0, step=0.1, key=f"qty_bdn_{i}")
                with col2:
                    entry['density'] = st.number_input("Density (kg/m³)", 
                                                       min_value=0.0, step=0.1, key=f"density_{i}")
                    entry['viscosity'] = st.number_input("Viscosity (cSt)", 
                                                         min_value=0.0, step=0.1, key=f"viscosity_{i}")
                    entry['lcv'] = st.number_input("LCV (MJ/kg)", 
                                                   min_value=0.0, step=0.1, key=f"lcv_{i}")
                entry['bdn_file'] = st.file_uploader("Upload BDN", 
                                                     type=['pdf', 'jpg', 'png'], 
                                                     key=f"bdn_file_{i}")

        if st.button("➕ Add Bunkering Entry"):
            st.session_state.bunkering_entries.append({})
            st.experimental_rerun()

    fuel_types = [
        "Heavy Fuel Oil RME-RMK >80cSt",
        "Heavy Fuel Oil RMA-RMD <80cSt",
        "VLSFO RME-RMK Visc >80cSt 0.5%S Max",
        "VLSFO RMA-RMD Visc <80cSt 0.5%S Max",
        "ULSFO RME-RMK <80cSt 0.1%S Max",
        "ULSFO RMA-RMD <80cSt 0.1%S Max",
        "VLSMGO 0.5%S Max",
        "ULSMGO 0.1%S Max",
        "Biofuel - 30",
        "Biofuel Distillate FO",
        "LPG - Propane",
        "LPG - Butane",
        "LNG Boil Off",
        "LNG (Bunkered)"
    ]

    columns = ["Oil Type", "Previous ROB", "IN PORT M/E", "IN PORT A/E", "IN PORT BLR", "IN PORT IGG", "IN PORT GE/NG", "IN PORT OTH", "GCU", "Incinerator",
               "Bunker Qty", "Sulphur %", "Total", "ROB at Noon", "Action"]

    df = pd.DataFrame(columns=columns)
    df['Oil Type'] = fuel_types
    edited_df = st.data_editor(df, num_rows="dynamic", key=f"fuel_consumption_table_{uuid.uuid4()}")

    if st.button("Add New Fuel Type"):
        st.text_input("New Fuel Type Name")

    st.markdown("### Tank Distribution")
    tank_names = ["Tank1", "Tank2", "Tank3", "Tank4", "Tank5", "Tank6", 
                  "FO Serv Tank 1", "FO Serv Tank 2", "DO Serv Tank", 
                  "FO Overflow Tank", "FO Drain Tank"]
    
    tank_df = pd.DataFrame(columns=["Tank Name", "Grade of Fuel", "ROB (m³)"])
    tank_df['Tank Name'] = tank_names
    edited_tank_df = st.data_editor(tank_df, num_rows="dynamic", key=f"tank_distribution_table_{uuid.uuid4()}")

def display_fuel_allocation():
    st.markdown("### Fuel Allocation")
    
    fuel_types = [
        "Heavy Fuel Oil RME-RMK >80cSt",
        "Heavy Fuel Oil RMA-RMD <80cSt",
        "VLSFO RME-RMK Visc >80cSt 0.5%S Max",
        "VLSFO RMA-RMD Visc <80cSt 0.5%S Max",
        "ULSFO RME-RMK <80cSt 0.1%S Max",
        "ULSFO RMA-RMD <80cSt 0.1%S Max",
        "VLSMGO 0.5%S Max",
        "ULSMGO 0.1%S Max",
        "Biofuel - 30",
        "Biofuel Distillate FO",
        "LPG - Propane",
        "LPG - Butane",
        "LNG Boil Off",
        "LNG (Bunkered)"
    ]

    columns = ["Oil Type", "Cargo cooling", "Cargo heating", "Cargo discharging", "DPP Cargo pump consumption"]

    df = pd.DataFrame(columns=columns)
    df['Oil Type'] = fuel_types
    edited_df = st.data_editor(df, num_rows="dynamic", key=f"fuel_allocation_table_{uuid.uuid4()}")

    st.markdown("### Additional Allocation Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Reefer container")
        st.number_input("Work", key=f"reefer_work_{uuid.uuid4()}", step=0.1)
        st.number_input("SFOC", key=f"reefer_sfoc_{uuid.uuid4()}", step=0.1)
        st.text_input("Fuel type", key=f"reefer_fuel_type_{uuid.uuid4()}")
        st.text_input("Fuel BDN", key=f"reefer_fuel_bdn_{uuid.uuid4()}")

        st.subheader("Cargo cooling")
        st.number_input("Work", key=f"cargo_cooling_work_{uuid.uuid4()}", step=0.1)
        st.number_input("SFOC", key=f"cargo_cooling_sfoc_{uuid.uuid4()}", step=0.1)
        st.text_input("Fuel type", key=f"cargo_cooling_fuel_type_{uuid.uuid4()}")
        st.text_input("Fuel BDN", key=f"cargo_cooling_fuel_bdn_{uuid.uuid4()}")

    with col2:
        st.subheader("Heating/Discharge pump")
        st.number_input("Work", key=f"heating_discharge_work_{uuid.uuid4()}", step=0.1)
        st.number_input("SFOC", key=f"heating_discharge_sfoc_{uuid.uuid4()}", step=0.1)
        st.text_input("Fuel type", key=f"heating_discharge_fuel_type_{uuid.uuid4()}")
        st.text_input("Fuel BDN", key=f"heating_discharge_fuel_bdn_{uuid.uuid4()}")

        st.subheader("Shore-Side Electricity")
        st.number_input("Work", key=f"shore_side_work_{uuid.uuid4()}", step=0.1)

def display_custom_fuel_allocation(noon_report_type):
    display_fuel_allocation()  # Same as non-custom version for this section

def display_machinery():
    st.markdown("### Machinery")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Main Engine")
        st.number_input("ME RPM", min_value=0.0, step=0.1, key=f"me_rpm_{uuid.uuid4()}")
        st.number_input("ME TC1 RPM", min_value=0.0, step=0.1, key=f"me_tc1_rpm_{uuid.uuid4()}")
        st.number_input("ME TC2 RPM", min_value=0.0, step=0.1, key=f"me_tc2_rpm_{uuid.uuid4()}")
        st.number_input("Exhaust Max. Temp.(C)", min_value=0.0, step=0.1, key=f"exhaust_max_temp_{uuid.uuid4()}")
        st.number_input("Exhaust Min. Temp.(C)", min_value=0.0, step=0.1, key=f"exhaust_min_temp_{uuid.uuid4()}")
        st.number_input("M/E rev counter", min_value=0, step=1, key=f"me_rev_counter_{uuid.uuid4()}")
        st.number_input("Scavenge pressure(BAR)", min_value=0.0, step=0.01, key=f"scavenge_pressure_{uuid.uuid4()}")
        st.number_input("MCR", min_value=0.0, max_value=100.0, step=0.1, key=f"mcr_{uuid.uuid4()}")
        st.number_input("Avg KW", min_value=0.0, step=0.1, key=f"avg_kw_{uuid.uuid4()}")
        st.number_input("Slip", min_value=0.0, max_value=100.0, step=0.1, key=f"slip_{uuid.uuid4()}")
        st.number_input("SFOC", min_value=0.0, step=0.1, key=f"sfoc_{uuid.uuid4()}")
        st.number_input("Propeller pitch", min_value=0.0, step=0.1, key=f"propeller_pitch_{uuid.uuid4()}")

    with col2:
        st.subheader("Auxiliary Engines")
        for i in range(1, 5):
            st.number_input(f"Avg A/E power {i}", min_value=0.0, step=0.1, key=f"avg_ae_power_{i}_{uuid.uuid4()}")

        st.subheader("Running Hours")
        st.number_input("Main engine", min_value=0.0, step=0.1, key=f"main_engine_hours_{uuid.uuid4()}")
        for i in range(1, 5):
            st.number_input(f"A/E {i}", min_value=0.0, step=0.1, key=f"ae_{i}_hours_{uuid.uuid4()}")
        st.number_input("Boilers", min_value=0.0, step=0.1, key=f"boilers_hours_{uuid.uuid4()}")
        st.number_input("Scrubbers", min_value=0.0, step=0.1, key=f"scrubbers_hours_{uuid.uuid4()}")
        st.number_input("Shaft gen", min_value=0.0, step=0.1, key=f"shaft_gen_hours_{uuid.uuid4()}")

        st.subheader("Boilers")
        st.number_input("Boiler 1 running hrs", min_value=0.0, step=0.1, key=f"boiler_1_hours_{uuid.uuid4()}")
        st.number_input("Boiler 2 running hrs", min_value=0.0, step=0.1, key=f"boiler_2_hours_{uuid.uuid4()}")

def display_custom_machinery(noon_report_type):
    st.markdown("### Machinery")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Main Engine")
        st.number_input("M/E rev counter", min_value=0, step=1, key=f"me_rev_counter_{uuid.uuid4()}")
    
    with col2:
        st.subheader("Auxiliary Engines")
        for i in range(1, 5):
            st.number_input(f"Avg A/E power {i}", min_value=0.0, step=0.1, key=f"avg_ae_power_{i}_{uuid.uuid4()}")

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

    st.subheader("Boilers")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Boiler 1 running hrs", min_value=0.0, step=0.1, key=f"boiler_1_hours_{uuid.uuid4()}")
    with col2:
        st.number_input("Boiler 2 running hrs", min_value=0.0, step=0.1, key=f"boiler_2_hours_{uuid.uuid4()}")

def display_environmental_compliance():
    st.markdown("### Environmental Compliance")
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1, key=f"sludge_rob_{uuid.uuid4()}")
        st.number_input("Sludge Burnt in Incinerator (MT)", min_value=0.0, step=0.1, key=f"sludge_burnt_{uuid.uuid4()}")
        st.number_input("Sludge Landed Ashore (MT)", min_value=0.0, step=0.1, key=f"sludge_landed_{uuid.uuid4()}")
    
    with col2:
        st.number_input("Bilge Water Quantity (m³)", min_value=0.0, step=0.1, key=f"bilge_water_qty_{uuid.uuid4()}")
        st.number_input("Bilge Water Pumped Out through 15ppm Equipment (m³)", min_value=0.0, step=0.1, key=f"bilge_pumped_out_{uuid.uuid4()}")
        st.number_input("Bilge Water Landed Ashore (m³)", min_value=0.0, step=0.1, key=f"bilge_landed_{uuid.uuid4()}")

def display_custom_environmental_compliance(noon_report_type):
    st.markdown("### Environmental Compliance")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1, key=f"sludge_rob_{uuid.uuid4()}")
    
    with col2:
        st.number_input("Sludge Landed Ashore (MT)", min_value=0.0, step=0.1, key=f"sludge_landed_{uuid.uuid4()}")
        st.number_input("Bilge Water Quantity (m³)", min_value=0.0, step=0.1, key=f"bilge_water_qty_{uuid.uuid4()}")
    
    with col3:
        st.number_input("Bilge Water Landed Ashore (m³)", min_value=0.0, step=0.1, key=f"bilge_landed_{uuid.uuid4()}")

def display_miscellaneous_consumables():
    st.markdown("### Miscellaneous Consumables")

    st.subheader("Fresh Water")
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

    st.subheader("Lubricating Oil")
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
    display_miscellaneous_consumables()  # Same as non-custom version for this section

# Main function
if __name__ == "__main__":
    main()
