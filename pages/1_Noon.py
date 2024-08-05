import streamlit as st
import pandas as pd
from datetime import datetime, time
import uuid

st.set_page_config(layout="wide", page_title="Noon Reporting Portal")

def main():
    st.title("Noon Reporting Portal")

    report_type = st.selectbox("Select Noon Report Type", 
                               ["Noon at Sea", "Noon at Port", "Noon at Anchor", 
                                "Noon at Drifting", "Noon at STS", "Noon at Canal/River Passage"])

    if report_type in ["Noon at Sea", "Noon at Drifting", "Noon at Canal/River Passage"]:
        display_base_report(report_type)
    else:
        display_custom_report(report_type)

    if st.button("Submit Report", type="primary", key=f"submit_report_{uuid.uuid4()}"):
        st.success("Report submitted successfully!")

def display_base_report(report_type):
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

    for section in sections:
        with st.expander(section, expanded=False):
            function_name = f"display_{section.lower().replace(' ', '_').replace(',', '')}"
            if function_name in globals():
                globals()[function_name](report_type)
            else:
                st.write(f"Function {function_name} not found.")

def display_custom_report(report_type):
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

    for section in sections:
        with st.expander(section, expanded=False):
            function_name = f"display_custom_{section.lower().replace(' ', '_').replace(',', '')}_{report_type.lower().replace(' ', '_')}"
            if function_name in globals():
                globals()[function_name]()
            else:
                fallback_function = f"display_{section.lower().replace(' ', '_').replace(',', '')}"
                if fallback_function in globals():
                    globals()[fallback_function](report_type)
                else:
                    st.write(f"Function {function_name} not found.")

def display_general_information(report_type):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("IMO Number", key=f"imo_number_{report_type}")
        st.text_input("Voyage ID", key=f"voyage_id_{report_type}")
        
    with col2:
        st.text_input("Vessel Name", key=f"vessel_name_{report_type}")
        st.text_input("Segment ID", key=f"segment_id_{report_type}")
    with col3:
        st.text_input("Vessel Type", key=f"vessel_type_{report_type}")

def display_voyage_details(report_type):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Voyage From", key=f"voyage_from_{report_type}")
        st.text_input("Voyage To", key=f"voyage_to_{report_type}")
        st.text_input("Speed Order", key=f"speed_order_{report_type}")
    
    with col2:
        st.selectbox("Voyage Type", ["", "One-way", "Round trip", "STS"], key=f"voyage_type_{report_type}")
        st.selectbox("Voyage Stage", ["", "East", "West", "Ballast", "Laden"], key=f"voyage_stage_{report_type}")
        st.date_input("ETA", value=datetime.now(), key=f"eta_{report_type}")
        st.text_input("Charter Type", key=f"charter_type_{report_type}")
    
    with col3:
        st.number_input("Time Since Last Report (hours)", min_value=0.0, step=0.1, key=f"time_since_last_report_{report_type}")
        st.selectbox("Clocks Advanced/Retarded", ["", "Advanced", "Retarded"], key=f"clocks_change_{report_type}")
        st.number_input("Clocks Changed By (minutes)", min_value=0, step=1, key=f"clocks_change_minutes_{report_type}")
    
    with col4:
        offhire = st.checkbox("Off-hire", key=f"offhire_{report_type}")
        eca_transit = st.checkbox("ECA Transit", key=f"eca_transit_{report_type}")
        fuel_changeover = st.checkbox("Fuel Changeover", key=f"fuel_changeover_{report_type}")
        idl_crossing = st.checkbox("IDL Crossing", key=f"idl_crossing_{report_type}")
        ice_navigation = st.checkbox("Ice Navigation", key=f"ice_navigation_{report_type}")
        deviation = st.checkbox("Deviation", key=f"deviation_{report_type}")
        special_area = st.checkbox("Transiting Special Area", key=f"special_area_{report_type}")
        
    if offhire:
        st.subheader("Off-hire Details")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.date_input("Off-hire Start Date (LT)", key=f"offhire_start_date_lt_{report_type}")
            st.time_input("Off-hire Start Time (LT)", key=f"offhire_start_time_lt_{report_type}")
            st.date_input("Off-hire Start Date (UTC)", key=f"offhire_start_date_utc_{report_type}")
            st.time_input("Off-hire Start Time (UTC)", key=f"offhire_start_time_utc_{report_type}")
        with col2:
            st.text_input("Start Off-hire Position Latitude", key=f"start_offhire_lat_{report_type}")
            st.text_input("Start Off-hire Position Longitude", key=f"start_offhire_lon_{report_type}")
            st.date_input("Off-hire End Date (LT)", key=f"offhire_end_date_lt_{report_type}")
            st.time_input("Off-hire End Time (LT)", key=f"offhire_end_time_lt_{report_type}")
        with col3:
            st.date_input("Off-hire End Date (UTC)", key=f"offhire_end_date_utc_{report_type}")
            st.time_input("Off-hire End Time (UTC)", key=f"offhire_end_time_utc_{report_type}")
            st.text_input("End Off-hire Position Latitude", key=f"end_offhire_lat_{report_type}")
            st.text_input("End Off-hire Position Longitude", key=f"end_offhire_lon_{report_type}")
        with col4:
            st.text_area("Off-hire Reason", key=f"offhire_reason_{report_type}")
    
    if eca_transit:
        st.subheader("ECA Transit Details")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.date_input("ECA Entry Date", key=f"eca_entry_date_{report_type}")
            st.time_input("ECA Entry Time", key=f"eca_entry_time_{report_type}")
        with col2:
            st.text_input("ECA Entry Latitude", key=f"eca_entry_lat_{report_type}")
            st.text_input("ECA Entry Longitude", key=f"eca_entry_lon_{report_type}")
        with col3:
            st.date_input("ECA Exit Date", key=f"eca_exit_date_{report_type}")
            st.time_input("ECA Exit Time", key=f"eca_exit_time_{report_type}")
        with col4:
            st.text_input("ECA Exit Latitude", key=f"eca_exit_lat_{report_type}")
            st.text_input("ECA Exit Longitude", key=f"eca_exit_lon_{report_type}")
        st.text_input("ECA Name", key=f"eca_name_{report_type}")
    
    if fuel_changeover:
        st.subheader("Fuel Changeover Details")
        st.subheader("Start of Changeover")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.date_input("Changeover Start Date", key=f"changeover_start_date_{report_type}")
            st.time_input("Changeover Start Time", key=f"changeover_start_time_{report_type}")
        with col2:
            st.text_input("Changeover Start Latitude", key=f"changeover_start_lat_{report_type}")
            st.text_input("Changeover Start Longitude", key=f"changeover_start_lon_{report_type}")
        with col3:
            st.number_input("VLSFO ROB at Start (MT)", min_value=0.0, step=0.1, key=f"vlsfo_rob_start_{report_type}")
            st.number_input("LSMGO ROB at Start (MT)", min_value=0.0, step=0.1, key=f"lsmgo_rob_start_{report_type}")
        
        st.subheader("End of Changeover")
        with col1:
            st.date_input("Changeover End Date", key=f"changeover_end_date_{report_type}")
            st.time_input("Changeover End Time", key=f"changeover_end_time_{report_type}")
        with col2:
            st.text_input("Changeover End Latitude", key=f"changeover_end_lat_{report_type}")
            st.text_input("Changeover End Longitude", key=f"changeover_end_lon_{report_type}")
        with col3:
            st.number_input("VLSFO ROB at End (MT)", min_value=0.0, step=0.1, key=f"vlsfo_rob_end_{report_type}")
            st.number_input("LSMGO ROB at End (MT)", min_value=0.0, step=0.1, key=f"lsmgo_rob_end_{report_type}")
    
    if idl_crossing:
        st.selectbox("IDL Direction", ["East", "West"], key=f"idl_direction_{report_type}")
    
    if ice_navigation:
        st.number_input("Ice Navigation Hours", min_value=0.0, step=0.1, key=f"ice_navigation_hours_{report_type}")
    
    if deviation:
        st.subheader("Deviation Details")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            reason = st.selectbox("Reason for Deviation", ["Heavy weather", "SAR operation", "Navigational area Warning", "Med-evac", "Others"], key=f"deviation_reason_{report_type}")
        with col2:
            if reason == "Others":
                st.text_input("Specify Other Reason", key=f"deviation_other_reason_{report_type}")
        with col3:
            st.date_input("Start Deviation Date (LT)", key=f"start_deviation_date_lt_{report_type}")
            st.time_input("Start Deviation Time (LT)", key=f"start_deviation_time_lt_{report_type}")
            st.date_input("Start Deviation Date (UTC)", key=f"start_deviation_date_utc_{report_type}")
            st.time_input("Start Deviation Time (UTC)", key=f"start_deviation_time_utc_{report_type}")
        with col4:
            st.text_input("Start Deviation Position Latitude", key=f"start_deviation_lat_{report_type}")
            st.text_input("Start Deviation Position Longitude", key=f"start_deviation_lon_{report_type}")

        st.subheader("End of Deviation")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.date_input("End Deviation Date (LT)", key=f"end_deviation_date_lt_{report_type}")
            st.time_input("End Deviation Time (LT)", key=f"end_deviation_time_lt_{report_type}")
            st.date_input("End Deviation Date (UTC)", key=f"end_deviation_date_utc_{report_type}")
            st.time_input("End Deviation Time (UTC)", key=f"end_deviation_time_utc_{report_type}")
        with col2:
            st.text_input("End Deviation Position Latitude", key=f"end_deviation_lat_{report_type}")
            st.text_input("End Deviation Position Longitude", key=f"end_deviation_lon_{report_type}")
        with col3:
            st.text_area("Deviation Comments", key=f"deviation_comments_{report_type}")

    if special_area:
        st.subheader("Transiting Special Area Details")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            special_area_type = st.selectbox("Special Area Type", ["JWC area", "IWL", "ICE regions", "HRA"], key=f"special_area_type_{report_type}")
        with col2:
            st.date_input("Entry Special Area Date (LT)", key=f"entry_special_area_date_lt_{report_type}")
            st.time_input("Entry Special Area Time (LT)", key=f"entry_special_area_time_lt_{report_type}")
            st.date_input("Entry Special Area Date (UTC)", key=f"entry_special_area_date_utc_{report_type}")
            st.time_input("Entry Special Area Time (UTC)", key=f"entry_special_area_time_utc_{report_type}")
        with col3:
            st.text_input("Entry Special Area Position Latitude", key=f"entry_special_area_lat_{report_type}")
            st.text_input("Entry Special Area Position Longitude", key=f"entry_special_area_lon_{report_type}")
            st.date_input("Exit Special Area Date (LT)", key=f"exit_special_area_date_lt_{report_type}")
            st.time_input("Exit Special Area Time (LT)", key=f"exit_special_area_time_lt_{report_type}")
        with col4:
            st.date_input("Exit Special Area Date (UTC)", key=f"exit_special_area_date_utc_{report_type}")
            st.time_input("Exit Special Area Time (UTC)", key=f"exit_special_area_time_utc_{report_type}")
            st.text_input("Exit Special Area Position Latitude", key=f"exit_special_area_lat_{report_type}")
            st.text_input("Exit Special Area Position Longitude", key=f"exit_special_area_lon_{report_type}")
            st.text_area("Special Area Comments", key=f"special_area_comments_{report_type}")

def display_speed_position_and_navigation(report_type):
    st.subheader("Speed, Position and Navigation")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1, key=f"full_speed_hrs_{report_type}")
        st.number_input("Reduced Speed/Slow Steaming (hrs)", min_value=0.0, step=0.1, key=f"reduced_speed_hrs_{report_type}")
        st.number_input("Stopped (hrs)", min_value=0.0, step=0.1, key=f"stopped_hrs_{report_type}")
        st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1, value=0.00, key=f"distance_observed_{report_type}")
        st.date_input("Date (Local)", value=datetime.now(), key=f"local_date_{report_type}")
        
    with col2:
        st.number_input("Distance Through Water (nm)", min_value=0.0, step=0.1, key=f"distance_through_water_{report_type}")
        st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1, key=f"obs_speed_sog_{report_type}")
        st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1, key=f"em_log_speed_{report_type}")
        st.number_input("Latitude Degree", min_value=-90, max_value=90, step=1, key=f"lat_degree_{report_type}")
        st.time_input("Time (Local)", value=datetime.now().time(), key=f"local_time_{report_type}")
    with col3:
        st.number_input("Latitude Minutes", min_value=0.0, max_value=59.99, step=0.01, format="%.2f", key=f"lat_minutes_{report_type}")
        st.selectbox("Latitude N/S", ["N", "S"], key=f"lat_ns_{report_type}")
        st.number_input("Longitude Degree", min_value=-180, max_value=180, step=1, key=f"lon_degree_{report_type}")
        st.number_input("Longitude Minutes", min_value=0.0, max_value=59.99, step=0.01, format="%.2f", key=f"lon_minutes_{report_type}")
        st.date_input("Date (UTC)", value=datetime.now(), key=f"utc_date_{report_type}")
        
    with col4:
        st.selectbox("Longitude E/W", ["E", "W"], key=f"lon_ew_{report_type}")
        st.number_input("Course (°)", min_value=0, max_value=359, step=1, key=f"course_{report_type}")
        st.number_input("Heading (°)", min_value=0, max_value=359, step=1, key=f"heading_{report_type}")
        st.number_input("True Heading (°)", min_value=0, max_value=359, step=1, key=f"true_heading_{report_type}")
        st.time_input("Time (UTC)", value=datetime.now().time(), key=f"utc_time_{report_type}")

def display_weather_and_sea_conditions(report_type):
    st.subheader("Weather and Sea Conditions")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=f"wind_direction_{report_type}")
        st.number_input("Wind Force (Beaufort)", min_value=0, max_value=12, key=f"wind_force_{report_type}")
        st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key=f"sea_height_{report_type}")
        st.selectbox("Sea Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=f"sea_direction_{report_type}")
    with col2:
        st.number_input("Swell Height (m)", min_value=0.0, step=0.1, key=f"swell_height_{report_type}")
        st.selectbox("Swell Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=f"swell_direction_{report_type}")
        st.number_input("Current Speed (kts)", min_value=0.0, step=0.1, key=f"current_speed_{report_type}")
        st.selectbox("Current Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=f"current_direction_{report_type}")
        st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key=f"air_temp_{report_type}")
        st.number_input("Sea Temp (°C)", min_value=-2.0, max_value=35.0, step=0.1, key=f"sea_temp_{report_type}")

    st.number_input("Visibility (nm)", min_value=0.0, step=0.1, key=f"visibility_{report_type}")
    st.checkbox("Icing on Deck?", key=f"icing_on_deck_{report_type}")

def display_cargo_and_stability(report_type):
    st.subheader("Cargo and Stability")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("Draft F (m)", min_value=0.0, step=0.01, key=f"draft_f_{report_type}")
        st.number_input("Draft A (m)", min_value=0.0, step=0.01, key=f"draft_a_{report_type}")
        st.number_input("Draft M (m)", min_value=0.0, step=0.01, key=f"draft_m_{report_type}")
    with col2:
        st.number_input("Displacement (MT)", min_value=0.0, step=0.1, key=f"displacement_{report_type}")
        st.number_input("Deadweight (MT)", min_value=0.0, step=0.1, key=f"deadweight_{report_type}")
    with col3:
        st.number_input("GM (m)", min_value=0.0, step=0.01, key=f"gm_{report_type}")
        st.number_input("Trim (m)", min_value=-10.0, max_value=10.0, step=0.01, key=f"trim_{report_type}")

def display_fuel_consumption(report_type):
    st.subheader("Fuel Consumption (mt)")
    
    # Bunkering checkbox
    bunkering_happened = st.checkbox("Bunkering Happened", key=f"bunkering_happened_{report_type}")

    if bunkering_happened:
        st.subheader("Bunkering Details")
        
        # Initialize bunkering entries in session state if not present
        if 'bunkering_entries' not in st.session_state:
            st.session_state.bunkering_entries = [{}]

        # Display each bunkering entry
        for i, entry in enumerate(st.session_state.bunkering_entries):
            st.markdown(f"**Bunkering Entry {i+1}**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                entry['grade'] = st.selectbox("Grade of Fuel Bunkered", 
                                              ["VLSFO", "HFO", "MGO", "LSMGO", "LNG"], 
                                              key=f"grade_{i}_{report_type}")
                entry['grade_bdn'] = st.text_input("Grade as per BDN", key=f"grade_bdn_{i}_{report_type}")
            with col2:
                entry['qty_bdn'] = st.number_input("Quantity as per BDN (mt)", 
                                                   min_value=0.0, step=0.1, key=f"qty_bdn_{i}_{report_type}")
                entry['density'] = st.number_input("Density (kg/m³)", 
                                                   min_value=0.0, step=0.1, key=f"density_{i}_{report_type}")
            with col3:
                entry['viscosity'] = st.number_input("Viscosity (cSt)", 
                                                     min_value=0.0, step=0.1, key=f"viscosity_{i}_{report_type}")
                entry['lcv'] = st.number_input("LCV (MJ/kg)", 
                                               min_value=0.0, step=0.1, key=f"lcv_{i}_{report_type}")
            with col4:
                entry['bdn_file'] = st.file_uploader("Upload BDN", 
                                                     type=['pdf', 'jpg', 'png'], 
                                                     key=f"bdn_file_{i}_{report_type}")

        # Button to add new bunkering entry
        if st.button("➕ Add Bunkering Entry", key=f"add_bunkering_entry_{report_type}"):
            st.session_state.bunkering_entries.append({})
            st.experimental_rerun()

    # Fuel consumption table
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
               "IN PORT M/E", "IN PORT A/E", "IN PORT BLR", "IN PORT IGG", "IN PORT GE/NG", "IN PORT OTH",
               "Bunker Qty", "Sulphur %", "Total", "ROB at Noon"]

    fuel_data = {col: [0.0 for _ in fuel_types] for col in columns[1:]}
    fuel_data["Oil Type"] = fuel_types

    df = pd.DataFrame(fuel_data)
    edited_df = st.data_editor(df, key=f"fuel_consumption_{report_type}")

    if st.button("Add New Fuel Type", key=f"add_fuel_type_{report_type}"):
        new_fuel_type = st.text_input("New Fuel Type Name", key=f"new_fuel_type_{report_type}")
        if new_fuel_type:
            fuel_types.append(new_fuel_type)
            st.experimental_rerun()

    st.subheader("Tank Distribution")

    tank_names = ["Tank1", "Tank2", "Tank3", "Tank4", "Tank5", "Tank6", 
                  "FO Serv Tank 1", "FO Serv Tank 2", "DO Serv Tank", 
                  "FO Overflow Tank", "FO Drain Tank"]
    
    tank_data = {
        "Tank Name": tank_names,
        "Grade of Fuel": ["" for _ in tank_names],
        "ROB (m³)": [0.0 for _ in tank_names]
    }

    tank_df = pd.DataFrame(tank_data)
    edited_tank_df = st.data_editor(tank_df, key=f"tank_distribution_{report_type}")

def display_fuel_allocation(report_type):
    st.subheader("Fuel Allocation")
    
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
    edited_df = st.data_editor(df, num_rows="dynamic", key=f"fuel_allocation_table_{report_type}")

    st.subheader("Additional Allocation Details")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("Reefer container")
        st.number_input("Work", key=f"reefer_work_{report_type}", step=0.1)
        st.number_input("SFOC", key=f"reefer_sfoc_{report_type}", step=0.1)
        st.text_input("Fuel type", key=f"reefer_fuel_type_{report_type}")
        st.text_input("Fuel BDN", key=f"reefer_fuel_bdn_{report_type}")

    with col2:
        st.subheader("Cargo cooling")
        st.number_input("Work", key=f"cargo_cooling_work_{report_type}", step=0.1)
        st.number_input("SFOC", key=f"cargo_cooling_sfoc_{report_type}", step=0.1)
        st.text_input("Fuel type", key=f"cargo_cooling_fuel_type_{report_type}")
        st.text_input("Fuel BDN", key=f"cargo_cooling_fuel_bdn_{report_type}")

    with col3:
        st.subheader("Heating/Discharge pump")
        st.number_input("Work", key=f"heating_discharge_work_{report_type}", step=0.1)
        st.number_input("SFOC", key=f"heating_discharge_sfoc_{report_type}", step=0.1)
        st.text_input("Fuel type", key=f"heating_discharge_fuel_type_{report_type}")
        st.text_input("Fuel BDN", key=f"heating_discharge_fuel_bdn_{report_type}")

    with col4:
        st.subheader("Shore-Side Electricity")
        st.number_input("Work", key=f"shore_side_work_{report_type}", step=0.1)

def display_machinery(report_type):
    st.subheader("Machinery")

    # Main Engine
    st.subheader("Main Engine")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("ME RPM", min_value=0.0, step=0.1, key=f"me_rpm_{report_type}")
        st.number_input("ME TC1 RPM", min_value=0.0, step=0.1, key=f"me_tc1_rpm_{report_type}")
        st.number_input("ME TC2 RPM", min_value=0.0, step=0.1, key=f"me_tc2_rpm_{report_type}")
    with col2:
        st.number_input("Exhaust Max. Temp.(C)", min_value=0.0, step=0.1, key=f"exhaust_max_temp_{report_type}")
        st.number_input("Exhaust Min. Temp.(C)", min_value=0.0, step=0.1, key=f"exhaust_min_temp_{report_type}")
        st.number_input("M/E rev counter", min_value=0, step=1, key=f"me_rev_counter_{report_type}")
    with col3:
        st.number_input("Scavenge pressure(BAR)", min_value=0.0, step=0.01, key=f"scavenge_pressure_{report_type}")
        st.number_input("MCR", min_value=0.0, max_value=100.0, step=0.1, key=f"mcr_{report_type}")
        st.number_input("Avg KW", min_value=0.0, step=0.1, key=f"avg_kw_{report_type}")
    with col4:
        st.number_input("Slip", min_value=0.0, max_value=100.0, step=0.1, key=f"slip_{report_type}")
        st.number_input("SFOC", min_value=0.0, step=0.1, key=f"sfoc_{report_type}")
        st.number_input("Propeller pitch", min_value=0.0, step=0.1, key=f"propeller_pitch_{report_type}")

    # Auxiliary Engines
    st.subheader("Auxiliary Engines")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Avg A/E power 1", min_value=0.0, step=0.1, key=f"avg_ae_power_1_{report_type}")
    with col2:
        st.number_input("Avg A/E power 2", min_value=0.0, step=0.1, key=f"avg_ae_power_2_{report_type}")
    with col3:
        st.number_input("Avg A/E power 3", min_value=0.0, step=0.1, key=f"avg_ae_power_3_{report_type}")
    with col4:
        st.number_input("Avg A/E power 4", min_value=0.0, step=0.1, key=f"avg_ae_power_4_{report_type}")

    # Running Hours
    st.subheader("Running Hours")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Main engine", min_value=0.0, step=0.1, key=f"main_engine_hours_{report_type}")
        st.number_input("AE-1", min_value=0.0, step=0.1, key=f"ae_1_hours_{report_type}")
    with col2:
        st.number_input("A/E 2", min_value=0.0, step=0.1, key=f"ae_2_hours_{report_type}")
        st.number_input("A/E 3", min_value=0.0, step=0.1, key=f"ae_3_hours_{report_type}")
    with col3:
        st.number_input("A/E 4", min_value=0.0, step=0.1, key=f"ae_4_hours_{report_type}")
        st.number_input("Boilers", min_value=0.0, step=0.1, key=f"boilers_hours_{report_type}")
    with col4:
        st.number_input("Scrubbers", min_value=0.0, step=0.1, key=f"scrubbers_hours_{report_type}")
        st.number_input("Shaft gen", min_value=0.0, step=0.1, key=f"shaft_gen_hours_{report_type}")

    # Boilers
    st.subheader("Boilers")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Boiler 1 running hrs", min_value=0.0, step=0.1, key=f"boiler_1_hours_{report_type}")
    with col2:
        st.number_input("Boiler 2 running hrs", min_value=0.0, step=0.1, key=f"boiler_2_hours_{report_type}")

def display_environmental_compliance(report_type):
    st.subheader("Environmental Compliance")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1, key=f"sludge_rob_{report_type}")
        st.number_input("Sludge Burnt in Incinerator (MT)", min_value=0.0, step=0.1, key=f"sludge_burnt_{report_type}")
    
    with col2:
        st.number_input("Sludge Landed Ashore (MT)", min_value=0.0, step=0.1, key=f"sludge_landed_{report_type}")
        st.number_input("Bilge Water Quantity (m³)", min_value=0.0, step=0.1, key=f"bilge_water_qty_{report_type}")
    
    with col3:
        st.number_input("Bilge Water Pumped Out through 15ppm Equipment (m³)", min_value=0.0, step=0.1, key=f"bilge_pumped_out_{report_type}")
        st.number_input("Bilge Water Landed Ashore (m³)", min_value=0.0, step=0.1, key=f"bilge_landed_{report_type}")

def display_miscellaneous_consumables(report_type):
    st.subheader("Miscellaneous Consumables")

    st.markdown("Fresh Water")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.number_input("Fresh Water Bunkered (m³)", min_value=0.0, step=0.1, key=f"fw_bunkered_{report_type}")
        st.number_input("Fresh Water Consumption - Drinking (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_drinking_{report_type}")
    
    with col2:
        st.number_input("Fresh Water Consumption - Technical (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_technical_{report_type}")
        st.number_input("Fresh Water Consumption - Washing (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_washing_{report_type}")
    
    with col3:
        st.number_input("Fresh Water Produced (m³)", min_value=0.0, step=0.1, key=f"fw_produced_{report_type}")
        st.number_input("Fresh Water ROB (m³)", min_value=0.0, step=0.1, key=f"fw_rob_{report_type}")
    
    with col4:
        st.number_input("Fresh Water Usage - Galley (m³)", min_value=0.0, step=0.1, key=f"fw_usage_galley_{report_type}")
        st.number_input("Fresh Water Usage - Laundry (m³)", min_value=0.0, step=0.1, key=f"fw_usage_laundry_{report_type}")

    st.markdown("Lubricating Oil")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.number_input("ME Cylinder Oil High BN ROB (liters)", min_value=0, step=1, key=f"me_cyl_oil_high_bn_rob_{report_type}")
        st.number_input("ME Cylinder Oil Low BN ROB (liters)", min_value=0, step=1, key=f"me_cyl_oil_low_bn_rob_{report_type}")
    
    with col2:
        st.number_input("ME System Oil ROB (liters)", min_value=0, step=1, key=f"me_system_oil_rob_{report_type}")
        st.number_input("AE System Oil ROB (liters)", min_value=0, step=1, key=f"ae_system_oil_rob_{report_type}")
    
    with col3:
        st.number_input("ME Cylinder Oil Consumption (liters)", min_value=0, step=1, key=f"me_cyl_oil_consumption_{report_type}")
        st.number_input("ME Cylinder Oil Feed Rate (g/kWh)", min_value=0.0, step=0.1, key=f"me_cyl_oil_feed_rate_{report_type}")
    
    with col4:
        st.number_input("ME System Oil Consumption (liters)", min_value=0, step=1, key=f"me_system_oil_consumption_{report_type}")
        st.number_input("AE System Oil Consumption (liters)", min_value=0, step=1, key=f"ae_system_oil_consumption_{report_type}")

def display_custom_voyage_details_noon_at_port():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Port Name", key="port_name")
    
    with col2:
        st.text_input("Charter Type", key="charter_type")
    
    with col3:
        st.number_input("Time Since Last Report (hours)", min_value=0.0, step=0.1, key="time_since_last_report")
        st.selectbox("Clocks Advanced/Retarded", ["", "Advanced", "Retarded"], key="clocks_change")
        st.number_input("Clocks Changed By (minutes)", min_value=0, step=1, key="clocks_change_minutes")
    
    with col4:
        offhire = st.checkbox("Off-hire", key="offhire")
        eca_transit = st.checkbox("ECA Transit", key="eca_transit")
        fuel_changeover = st.checkbox("Fuel Changeover", key="fuel_changeover")
        
    # ... (rest of the custom voyage details code remains the same)

def display_custom_speed_position_and_navigation_noon_at_port():
    st.subheader("Speed, Position and Navigation")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Stopped (hrs)", min_value=0.0, step=0.1, key="stopped_hrs")
        st.date_input("Date (Local)", value=datetime.now(), key="local_date")
        
    with col2:
        st.number_input("Latitude Degree", min_value=-90, max_value=90, step=1, key="lat_degree")
        st.time_input("Time (Local)", value=datetime.now().time(), key="local_time")
    with col3:
        st.number_input("Latitude Minutes", min_value=0.0, max_value=59.99, step=0.01, format="%.2f", key="lat_minutes")
        st.selectbox("Latitude N/S", ["N", "S"], key="lat_ns")
        st.number_input("Longitude Degree", min_value=-180, max_value=180, step=1, key="lon_degree")
        st.number_input("Longitude Minutes", min_value=0.0, max_value=59.99, step=0.01, format="%.2f", key="lon_minutes")
        st.date_input("Date (UTC)", value=datetime.now(), key="utc_date")
        
    with col4:
        st.selectbox("Longitude E/W", ["E", "W"], key="lon_ew")
        st.number_input("Heading (°)", min_value=0, max_value=359, step=1, key="heading")
        st.number_input("True Heading (°)", min_value=0, max_value=359, step=1, key="true_heading")
        st.time_input("Time (UTC)", value=datetime.now().time(), key="utc_time")

def display_custom_voyage_details_noon_at_sts():
    display_custom_voyage_details_noon_at_port()

def display_custom_voyage_details_noon_at_anchor():
    display_custom_voyage_details_noon_at_port()

def display_custom_speed_position_and_navigation_noon_at_sts():
    display_custom_speed_position_and_navigation_noon_at_port()

def display_custom_speed_position_and_navigation_noon_at_anchor():
    display_custom_speed_position_and_navigation_noon_at_port()

def display_custom_machinery_noon_at_port():
    st.subheader("Machinery")

    # Auxiliary Engines
    st.subheader("Auxiliary Engines")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Avg A/E power 1", min_value=0.0, step=0.1, key="avg_ae_power_1")
    with col2:
        st.number_input("Avg A/E power 2", min_value=0.0, step=0.1, key="avg_ae_power_2")
    with col3:
        st.number_input("Avg A/E power 3", min_value=0.0, step=0.1, key="avg_ae_power_3")
    with col4:
        st.number_input("Avg A/E power 4", min_value=0.0, step=0.1, key="avg_ae_power_4")

    # Running Hours
    st.subheader("Running Hours")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Main engine", min_value=0.0, step=0.1, key="main_engine_hours")
        st.number_input("AE-1", min_value=0.0, step=0.1, key="ae_1_hours")
    with col2:
        st.number_input("A/E 2", min_value=0.0, step=0.1, key="ae_2_hours")
        st.number_input("A/E 3", min_value=0.0, step=0.1, key="ae_3_hours")
    with col3:
        st.number_input("A/E 4", min_value=0.0, step=0.1, key="ae_4_hours")
        st.number_input("Boilers", min_value=0.0, step=0.1, key="boilers_hours")
    with col4:
        st.number_input("Scrubbers", min_value=0.0, step=0.1, key="scrubbers_hours")
        st.number_input("Shaft gen", min_value=0.0, step=0.1, key="shaft_gen_hours")

    # Boilers
    st.subheader("Boilers")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Boiler 1 running hrs", min_value=0.0, step=0.1, key="boiler_1_hours")
    with col2:
        st.number_input("Boiler 2 running hrs", min_value=0.0, step=0.1, key="boiler_2_hours")

def display_custom_machinery_noon_at_sts():
    display_custom_machinery_noon_at_port()

def display_custom_machinery_noon_at_anchor():
    display_custom_machinery_noon_at_port()

def display_custom_environmental_compliance_noon_at_port():
    st.subheader("Environmental Compliance")
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1, key="sludge_rob")
    
    with col2:
        st.number_input("Sludge Landed Ashore (MT)", min_value=0.0, step=0.1, key="sludge_landed")

def display_custom_environmental_compliance_noon_at_sts():
    display_custom_environmental_compliance_noon_at_port()

def display_custom_environmental_compliance_noon_at_anchor():
    display_custom_environmental_compliance_noon_at_port()

if __name__ == "__main__":
    main()
