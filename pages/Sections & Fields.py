import streamlit as st
import pandas as pd
from datetime import datetime, time
import uuid

st.set_page_config(layout="wide", page_title="Noon Reporting Portal")

def main():
    st.title("Noon Reporting Portal")

    sections = [
        "General Information",
        "Voyage Details",
        "Speed, Position and Navigation",
        "Weather and Sea Conditions",
        "Cargo Operations",
        "Fuel Consumption",
        "Fuel Allocation",
        "Machinery",
        "Environmental Compliance",
        "Fresh Water",
        "Lubricating Oil",
        "Vessel Performance",
        "Special Events and Remarks"
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

def display_general_information():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("IMO Number", key=f"imo_number_{uuid.uuid4()}")
        st.date_input("Date (Local)", value=datetime.now(), key=f"local_date_{uuid.uuid4()}")
        st.time_input("Time (Local)", value=datetime.now().time(), key=f"local_time_{uuid.uuid4()}")
    with col2:
        st.text_input("Vessel Name", key=f"vessel_name_{uuid.uuid4()}")
        st.date_input("Date (UTC)", value=datetime.now(), key=f"utc_date_{uuid.uuid4()}")
        st.time_input("Time (UTC)", value=datetime.now().time(), key=f"utc_time_{uuid.uuid4()}")
    with col3:
        st.text_input("Vessel Type", key=f"vessel_type_{uuid.uuid4()}")

def display_voyage_details():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Voyage From", key=f"voyage_from_{uuid.uuid4()}")
        st.text_input("Voyage To", key=f"voyage_to_{uuid.uuid4()}")
        st.text_input("Voyage ID", key=f"voyage_id_{uuid.uuid4()}")
        st.text_input("Segment ID", key=f"segment_id_{uuid.uuid4()}")
    with col2:
        st.selectbox("Voyage Type", ["", "One-way", "Round trip", "STS"], key=f"voyage_type_{uuid.uuid4()}")
        st.selectbox("Voyage Stage", ["", "East", "West", "Ballast", "Laden"], key=f"voyage_stage_{uuid.uuid4()}")
        st.date_input("ETA", value=datetime.now(), key=f"eta_{uuid.uuid4()}")
        st.text_input("Speed Order", key=f"speed_order_{uuid.uuid4()}")
    with col3:
        st.text_input("Charter Type", key=f"charter_type_{uuid.uuid4()}")
        st.number_input("Time Since Last Report (hours)", min_value=0.0, step=0.1, key=f"time_since_last_report_{uuid.uuid4()}")
        st.selectbox("Clocks Advanced/Retarded", ["", "Advanced", "Retarded"], key=f"clocks_change_{uuid.uuid4()}")
        st.number_input("Clocks Changed By (minutes)", min_value=0, step=1, key=f"clocks_change_minutes_{uuid.uuid4()}")
    with col4:
        offhire = st.checkbox("Off-hire", key=f"offhire_{uuid.uuid4()}")
        eca_transit = st.checkbox("ECA Transit", key=f"eca_transit_{uuid.uuid4()}")
        fuel_changeover = st.checkbox("Fuel Changeover", key=f"fuel_changeover_{uuid.uuid4()}")
        idl_crossing = st.checkbox("IDL Crossing", key=f"idl_crossing_{uuid.uuid4()}")
        ice_navigation = st.checkbox("Ice Navigation", key=f"ice_navigation_{uuid.uuid4()}")
    
    if offhire:
        display_offhire_details()
    if eca_transit:
        display_eca_transit_details()
    if fuel_changeover:
        display_fuel_changeover_details()
    if idl_crossing:
        st.selectbox("IDL Direction", ["East", "West"], key=f"idl_direction_{uuid.uuid4()}")
    if ice_navigation:
        st.number_input("Ice Navigation Hours", min_value=0.0, step=0.1, key=f"ice_navigation_hours_{uuid.uuid4()}")

def display_offhire_details():
    st.subheader("Off-hire Details")
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Off-hire Start Date", key=f"offhire_start_date_{uuid.uuid4()}")
        st.time_input("Off-hire Start Time", key=f"offhire_start_time_{uuid.uuid4()}")
    with col2:
        st.date_input("Off-hire End Date", key=f"offhire_end_date_{uuid.uuid4()}")
        st.time_input("Off-hire End Time", key=f"offhire_end_time_{uuid.uuid4()}")
    st.text_area("Off-hire Reason", key=f"offhire_reason_{uuid.uuid4()}")

def display_eca_transit_details():
    st.subheader("ECA Transit Details")
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("ECA Entry Date", key=f"eca_entry_date_{uuid.uuid4()}")
        st.time_input("ECA Entry Time", key=f"eca_entry_time_{uuid.uuid4()}")
        st.text_input("ECA Entry Latitude", key=f"eca_entry_lat_{uuid.uuid4()}")
        st.text_input("ECA Entry Longitude", key=f"eca_entry_lon_{uuid.uuid4()}")
    with col2:
        st.date_input("ECA Exit Date", key=f"eca_exit_date_{uuid.uuid4()}")
        st.time_input("ECA Exit Time", key=f"eca_exit_time_{uuid.uuid4()}")
        st.text_input("ECA Exit Latitude", key=f"eca_exit_lat_{uuid.uuid4()}")
        st.text_input("ECA Exit Longitude", key=f"eca_exit_lon_{uuid.uuid4()}")
    st.text_input("ECA Name", key=f"eca_name_{uuid.uuid4()}")

def display_fuel_changeover_details():
    st.subheader("Fuel Changeover Details")
    st.subheader("Start of Changeover")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.date_input("Changeover Start Date", key=f"changeover_start_date_{uuid.uuid4()}")
        st.time_input("Changeover Start Time", key=f"changeover_start_time_{uuid.uuid4()}")
    with col2:
        st.text_input("Changeover Start Latitude", key=f"changeover_start_lat_{uuid.uuid4()}")
        st.text_input("Changeover Start Longitude", key=f"changeover_start_lon_{uuid.uuid4()}")
    with col3:
        st.number_input("VLSFO ROB at Start (MT)", min_value=0.0, step=0.1, key=f"vlsfo_rob_start_{uuid.uuid4()}")
        st.number_input("LSMGO ROB at Start (MT)", min_value=0.0, step=0.1, key=f"lsmgo_rob_start_{uuid.uuid4()}")
    
    st.subheader("End of Changeover")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.date_input("Changeover End Date", key=f"changeover_end_date_{uuid.uuid4()}")
        st.time_input("Changeover End Time", key=f"changeover_end_time_{uuid.uuid4()}")
    with col2:
        st.text_input("Changeover End Latitude", key=f"changeover_end_lat_{uuid.uuid4()}")
        st.text_input("Changeover End Longitude", key=f"changeover_end_lon_{uuid.uuid4()}")
    with col3:
        st.number_input("VLSFO ROB at End (MT)", min_value=0.0, step=0.1, key=f"vlsfo_rob_end_{uuid.uuid4()}")
        st.number_input("LSMGO ROB at End (MT)", min_value=0.0, step=0.1, key=f"lsmgo_rob_end_{uuid.uuid4()}")

def display_speed_position_and_navigation():
    st.subheader("Speed, Position and Navigation")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1, key=f"full_speed_hrs_{uuid.uuid4()}")
        st.number_input("Reduced Speed/Slow Steaming (hrs)", min_value=0.0, step=0.1, key=f"reduced_speed_hrs_{uuid.uuid4()}")
        st.number_input("Stopped (hrs)", min_value=0.0, step=0.1, key=f"stopped_hrs_{uuid.uuid4()}")
        st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1, value=0.00, key=f"distance_observed_{uuid.uuid4()}")
    with col2:
        st.number_input("Distance Through Water (nm)", min_value=0.0, step=0.1, key=f"distance_through_water_{uuid.uuid4()}")
        st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1, key=f"obs_speed_sog_{uuid.uuid4()}")
        st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1, key=f"em_log_speed_{uuid.uuid4()}")
        st.number_input("Latitude Degree", min_value=-90, max_value=90, step=1, key=f"lat_degree_{uuid.uuid4()}")
    with col3:
        st.number_input("Latitude Minutes", min_value=0.0, max_value=59.99, step=0.01, format="%.2f", key=f"lat_minutes_{uuid.uuid4()}")
        st.selectbox("Latitude N/S", ["N", "S"], key=f"lat_ns_{uuid.uuid4()}")
        st.number_input("Longitude Degree", min_value=-180, max_value=180, step=1, key=f"lon_degree_{uuid.uuid4()}")
        st.number_input("Longitude Minutes", min_value=0.0, max_value=59.99, step=0.01, format="%.2f", key=f"lon_minutes_{uuid.uuid4()}")
    with col4:
        st.selectbox("Longitude E/W", ["E", "W"], key=f"lon_ew_{uuid.uuid4()}")
        st.number_input("Course (°)", min_value=0, max_value=359, step=1, key=f"course_{uuid.uuid4()}")
        st.number_input("Heading (°)", min_value=0, max_value=359, step=1, key=f"heading_{uuid.uuid4()}")
        st.number_input("True Heading (°)", min_value=0, max_value=359, step=1, key=f"true_heading_{uuid.uuid4()}")

def display_weather_and_sea_conditions():
    st.subheader("Weather and Sea Conditions")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("True Wind Speed (kts)", min_value=0.0, step=0.1, key=f"true_wind_speed_{uuid.uuid4()}")
        st.selectbox("BF Scale", range(13), key=f"bf_scale_{uuid.uuid4()}")
        st.number_input("True Wind Direction (°)", min_value=0, max_value=359, step=1, key=f"true_wind_direction_{uuid.uuid4()}")
    with col2:
        st.number_input("Significant Wave Height (m)", min_value=0.0, step=0.1, key=f"sig_wave_height_{uuid.uuid4()}")
        st.selectbox("Sea State (Douglas)", range(10), key=f"douglas_sea_state_{uuid.uuid4()}")
        st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key=f"sea_height_{uuid.uuid4()}")
    with col3:
        st.number_input("Sea Direction (°)", min_value=0, max_value=359, step=1, key=f"sea_direction_{uuid.uuid4()}")
        st.number_input("Swell Direction (°)", min_value=0, max_value=359, step=1, key=f"swell_direction_{uuid.uuid4()}")
        st.number_input("Swell Height (m) (DSS)", min_value=0.0, step=0.1, key=f"swell_height_{uuid.uuid4()}")
    with col4:
        st.number_input("Current Strength (kts)", min_value=0.0, step=0.1, key=f"current_strength_{uuid.uuid4()}")
        st.number_input("Current Direction (°)", min_value=0, max_value=359, step=1, key=f"current_direction_{uuid.uuid4()}")
        st.number_input("Sea Water Temp (°C)", min_value=-2.0, max_value=35.0, step=0.1, key=f"sea_water_temp_{uuid.uuid4()}")
        st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key=f"air_temp_{uuid.uuid4()}")

def display_cargo_operations():
    st.subheader("Cargo Operations")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Cargo Weight (MT)", min_value=0.0, step=0.1, key=f"cargo_weight_{uuid.uuid4()}")
        st.number_input("Cargo Volume (m³)", min_value=0.0, step=0.1, key=f"cargo_volume_{uuid.uuid4()}")
        st.number_input("Number of Passengers", min_value=0, step=1, key=f"passengers_{uuid.uuid4()}")
        st.number_input("Total TEU", min_value=0, step=1, key=f"total_teu_{uuid.uuid4()}")
    with col2:
        st.number_input("Reefer TEU", min_value=0, step=1, key=f"reefer_teu_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Chilled", min_value=0, step=1, key=f"reefer_20ft_chilled_{uuid.uuid4()}")
        st.number_input("Reefer 40ft Chilled", min_value=0, step=1, key=f"reefer_40ft_chilled_{uuid.uuid4()}")
        st.number_input("Reefer 20ft Frozen", min_value=0, step=1, key=f"reefer_20ft_frozen_{uuid.uuid4()}")
        st.number_input("Reefer 40ft Frozen", min_value=0, step=1, key=f"reefer_40ft_frozen_{uuid.uuid4()}")

def display_fuel_consumption():
    st.markdown("""
    <style>
    .fuel-table {
        font-size: 12px;
    }
    .fuel-table input, .fuel-table select {
        font-size: 12px;
        padding: 2px 5px;
        height: 25px;
        min-height: 25px;
    }
    .fuel-table th {
        font-weight: bold;
        text-align: center;
        padding: 2px;
    }
    .fuel-table td {
        padding: 2px;
    }
    .stButton > button {
        font-size: 10px;
        padding: 2px 5px;
        height: auto;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 18px;'>Fuel Consumption (mt)</h3>", unsafe_allow_html=True)
    
    # Bunkering checkbox
    bunkering_happened = st.checkbox("Bunkering Happened")

    if bunkering_happened:
        st.markdown("<h4 style='font-size: 16px;'>Bunkering Details</h4>", unsafe_allow_html=True)
        
        # Initialize bunkering entries in session state if not present
        if 'bunkering_entries' not in st.session_state:
            st.session_state.bunkering_entries = [{}]

        # Display each bunkering entry without using expander
        for i, entry in enumerate(st.session_state.bunkering_entries):
            st.markdown(f"**Bunkering Entry {i+1}**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                entry['grade'] = st.selectbox("Grade of Fuel Bunkered", 
                                              ["VLSFO", "HFO", "MGO", "LSMGO", "LNG"], 
                                              key=f"grade_{i}")
                entry['grade_bdn'] = st.text_input("Grade as per BDN", key=f"grade_bdn_{i}")
            with col2:
                entry['qty_bdn'] = st.number_input("Quantity as per BDN (mt)", 
                                                   min_value=0.0, step=0.1, key=f"qty_bdn_{i}")
                entry['density'] = st.number_input("Density (kg/m³)", 
                                                   min_value=0.0, step=0.1, key=f"density_{i}")
            with col3:
                entry['viscosity'] = st.number_input("Viscosity (cSt)", 
                                                     min_value=0.0, step=0.1, key=f"viscosity_{i}")
                entry['lcv'] = st.number_input("LCV (MJ/kg)", 
                                               min_value=0.0, step=0.1, key=f"lcv_{i}")
            with col4:
                entry['bdn_file'] = st.file_uploader("Upload BDN", 
                                                     type=['pdf', 'jpg', 'png'], 
                                                     key=f"bdn_file_{i}")

        # Button to add new bunkering entry
        if st.button("➕ Add Bunkering Entry"):
            st.session_state.bunkering_entries.append({})
            st.experimental_rerun()

    # Rest of the fuel consumption table code
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
               "Bunker Qty", "Sulphur %", "Total", "ROB at Noon", "Action"]

    # Create the header row
    header_html = "<tr>"
    for col in columns:
        header_html += f"<th>{col}</th>"
    header_html += "</tr>"

    rows_html = ""
    for fuel in fuel_types:
        rows_html += "<tr>"
        rows_html += f"<td>{fuel}</td>"
        for i in range(1, len(columns) - 1):  # Skip the last column (Action)
            if columns[i] == "Sulphur %":
                rows_html += f"<td><input type='number' step='0.01' min='0' max='100' style='width: 100%;'></td>"
            else:
                rows_html += f"<td><input type='number' step='0.1' min='0' style='width: 100%;'></td>"
        rows_html += "<td><button>Edit</button> <button>Delete</button></td>"
        rows_html += "</tr>"

    table_html = f"""
    <div class="fuel-table">
        <table style="width: 100%;">
            {header_html}
            {rows_html}
        </table>
    </div>
    """

    st.markdown(table_html, unsafe_allow_html=True)

    if st.button("Add New Fuel Type"):
        st.text_input("New Fuel Type Name")

def display_fuel_allocation():
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
    edited_df = st.data_editor(df, num_rows="dynamic", key=f"fuel_allocation_table_{uuid.uuid4()}")

    st.subheader("Additional Allocation Details")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("Reefer container")
        st.number_input("Work", key=f"reefer_work_{uuid.uuid4()}", step=0.1)
        st.number_input("SFOC", key=f"reefer_sfoc_{uuid.uuid4()}", step=0.1)
        st.text_input("Fuel type", key=f"reefer_fuel_type_{uuid.uuid4()}")
        st.text_input("Fuel BDN", key=f"reefer_fuel_bdn_{uuid.uuid4()}")

    with col2:
        st.subheader("Cargo cooling")
        st.number_input("Work", key=f"cargo_cooling_work_{uuid.uuid4()}", step=0.1)
        st.number_input("SFOC", key=f"cargo_cooling_sfoc_{uuid.uuid4()}", step=0.1)
        st.text_input("Fuel type", key=f"cargo_cooling_fuel_type_{uuid.uuid4()}")
        st.text_input("Fuel BDN", key=f"cargo_cooling_fuel_bdn_{uuid.uuid4()}")

    with col3:
        st.subheader("Heating/Discharge pump")
        st.number_input("Work", key=f"heating_discharge_work_{uuid.uuid4()}", step=0.1)
        st.number_input("SFOC", key=f"heating_discharge_sfoc_{uuid.uuid4()}", step=0.1)
        st.text_input("Fuel type", key=f"heating_discharge_fuel_type_{uuid.uuid4()}")
        st.text_input("Fuel BDN", key=f"heating_discharge_fuel_bdn_{uuid.uuid4()}")

    with col4:
        st.subheader("Shore-Side Electricity")
        st.number_input("Work", key=f"shore_side_work_{uuid.uuid4()}", step=0.1)

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

def display_fresh_water():
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


def display_lubricating_oil():
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


def display_vessel_performance():
    st.subheader("Vessel Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Draft Actual Fore (m)", min_value=0.0, step=0.01, key=f"draft_actual_fore_{uuid.uuid4()}")
        st.number_input("Draft Actual Aft (m)", min_value=0.0, step=0.01, key=f"draft_actual_aft_{uuid.uuid4()}")
        st.number_input("Draft Recommended Fore (m)", min_value=0.0, step=0.01, key=f"draft_recommended_fore_{uuid.uuid4()}")
        st.number_input("Draft Recommended Aft (m)", min_value=0.0, step=0.01, key=f"draft_recommended_aft_{uuid.uuid4()}")
    with col2:
        st.number_input("Propeller Pitch (m)", min_value=0.0, step=0.01, key=f"propeller_pitch_{uuid.uuid4()}")
        st.number_input("Propeller Pitch Ratio", min_value=0.0, step=0.01, key=f"propeller_pitch_ratio_{uuid.uuid4()}")
        st.number_input("Average Propeller Speed (RPM)", min_value=0, step=1, key=f"avg_propeller_speed_{uuid.uuid4()}")
        st.number_input("Slip (%)", min_value=0.0, max_value=100.0, step=0.1, key=f"slip_percentage_{uuid.uuid4()}")
        st.number_input("ME Projected Consumption (MT/day)", min_value=0.0, step=0.1, key=f"me_projected_consumption_{uuid.uuid4()}")
        st.number_input("AE Projected Consumption (MT/day)", min_value=0.0, step=0.1, key=f"ae_projected_consumption_{uuid.uuid4()}")

def display_special_events_and_remarks():
    st.subheader("Special Events and Remarks")
    st.selectbox("Operation Mode", ["", "At Sea", "In Port", "Maneuvering", "Anchoring", "Drifting"], key=f"operation_mode_{uuid.uuid4()}")
    st.selectbox("Cleaning Event", ["", "Propeller Cleaning", "Hull Cleaning", "Tank Cleaning"], key=f"cleaning_event_{uuid.uuid4()}")
    st.number_input("Number of Tugs", min_value=0, step=1, key=f"number_of_tugs_{uuid.uuid4()}")
    st.text_input("Reason for Schedule Deviation", key=f"schedule_deviation_reason_{uuid.uuid4()}")
    st.text_area("Remarks", key=f"remarks_{uuid.uuid4()}")
    st.text_input("Entry Made By (Deck)", key=f"entry_by_deck_{uuid.uuid4()}")
    st.text_input("Entry Made By (Engine)", key=f"entry_by_engine_{uuid.uuid4()}")
    st.text_input("Contact Email", key=f"contact_email_{uuid.uuid4()}")
    st.date_input("Reporting Date", value=datetime.now(), key=f"reporting_date_{uuid.uuid4()}")

if __name__ == "__main__":
    main()
