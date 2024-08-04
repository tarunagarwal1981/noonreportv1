import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Noon Reporting Portal")

def main():
    st.title("Noon Reporting Portal")

    sections = [
        "General Information",
        "Voyage Details",
        "Speed, Position and Navigation",
        "Weather and Sea Conditions",
        "Time Elapsed",
        "Cargo Operations",
        "Fuel Consumption",
        "Engine Performance",
        "Auxiliary Systems",
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

    if st.button("Submit Report", type="primary"):
        st.success("Report submitted successfully!")

def display_general_information():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("IMO Number", key="imo_number")
        st.date_input("Date (Local)", value=datetime.now(), key="local_date")
        st.time_input("Time (Local)", value=datetime.now().time(), key="local_time")
        
    with col2:
        st.text_input("Vessel Name", key="vessel_name")
        st.date_input("Date (UTC)", value=datetime.now(), key="utc_date")
        st.time_input("Time (UTC)", value=datetime.now().time(), key="utc_time")
       
    with col3:
        st.text_input("Vessel Type", key="vessel_type")

def display_voyage_details():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Voyage From", key="voyage_from")
        st.text_input("Voyage To", key="voyage_to")
        st.text_input("Voyage ID", key="voyage_id")
        st.text_input("Segment ID", key="segment_id")
    
    with col2:
        st.selectbox("Voyage Type", ["", "One-way", "Round trip", "STS"], key="voyage_type")
        st.selectbox("Voyage Stage", ["", "East", "West", "Ballast", "Laden"], key="voyage_stage")
        st.date_input("ETA", value=datetime.now(), key="eta")
        st.text_input("Speed Order", key="speed_order")
    
    with col3:
        st.text_input("Charter Type", key="charter_type")
        st.number_input("Time Since Last Report (hours)", min_value=0.0, step=0.1, key="time_since_last_report")
        st.selectbox("Clocks Advanced/Retarded", ["", "Advanced", "Retarded"], key="clocks_change")
        st.number_input("Clocks Changed By (minutes)", min_value=0, step=1, key="clocks_change_minutes")
    
    with col4:
        offhire = st.checkbox("Off-hire", key="offhire")
        eca_transit = st.checkbox("ECA Transit", key="eca_transit")
        fuel_changeover = st.checkbox("Fuel Changeover", key="fuel_changeover")
        idl_crossing = st.checkbox("IDL Crossing", key="idl_crossing")
        
    if offhire:
        st.subheader("Off-hire Details")
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Off-hire Start Date", key="offhire_start_date")
            st.time_input("Off-hire Start Time", key="offhire_start_time")
        with col2:
            st.date_input("Off-hire End Date", key="offhire_end_date")
            st.time_input("Off-hire End Time", key="offhire_end_time")
        st.text_area("Off-hire Reason", key="offhire_reason")
    
    if eca_transit:
        st.subheader("ECA Transit Details")
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
        st.subheader("Fuel Changeover Details")
        st.subheader("Start of Changeover")
        col1, col2, col3 = st.columns(3)
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
        col1, col2, col3 = st.columns(3)
        with col1:
            st.date_input("Changeover End Date", key="changeover_end_date")
            st.time_input("Changeover End Time", key="changeover_end_time")
        with col2:
            st.text_input("Changeover End Latitude", key="changeover_end_lat")
            st.text_input("Changeover End Longitude", key="changeover_end_lon")
        with col3:
            st.number_input("VLSFO ROB at End (MT)", min_value=0.0, step=0.1, key="vlsfo_rob_end")
            st.number_input("LSMGO ROB at End (MT)", min_value=0.0, step=0.1, key="lsmgo_rob_end")
    
    if idl_crossing:
        st.selectbox("IDL Direction", ["East", "West"], key="idl_direction")

def display_speed_position_and_navigation():
    st.subheader("Speed, Position and Navigation")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1, key="full_speed_hrs")
        st.number_input("Reduced Speed/Slow Steaming (hrs)", min_value=0.0, step=0.1, key="reduced_speed_hrs")
        st.number_input("Stopped (hrs)", min_value=0.0, step=0.1, key="stopped_hrs")
        st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1, value=0.00, key="distance_observed")
        st.number_input("Distance Through Water (nm)", min_value=0.0, step=0.1, key="distance_through_water")
        st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1, key="obs_speed_sog")
        st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1, key="em_log_speed")
        st.number_input("Latitude Degree", min_value=-90, max_value=90, step=1, key="lat_degree")
        st.number_input("Latitude Minutes", min_value=0.0, max_value=59.99, step=0.01, format="%.2f", key="lat_minutes")
        st.selectbox("Latitude N/S", ["N", "S"], key="lat_ns")
    
    with col2:
        st.number_input("Full Speed (nm)", min_value=0.0, step=0.1, key="full_speed_nm")
        st.number_input("Reduced Speed/Slow Steaming (nm)", min_value=0.0, step=0.1, key="reduced_speed_nm")
        st.number_input("Voyage Average Speed (kts)", min_value=0.0, step=0.1, key="voyage_avg_speed")
        st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1, key="distance_to_go")
        st.number_input("Distance since COSP (nm)", min_value=0.0, step=0.1, key="distance_since_cosp")
        st.number_input("Average Speed GPS (knots)", min_value=0.0, step=0.1, key="avg_speed_gps")
        st.number_input("Average Speed Through Water (knots)", min_value=0.0, step=0.1, key="avg_speed_water")
        st.number_input("Longitude Degree", min_value=-180, max_value=180, step=1, key="lon_degree")
        st.number_input("Longitude Minutes", min_value=0.0, max_value=59.99, step=0.01, format="%.2f", key="lon_minutes")
        st.selectbox("Longitude E/W", ["E", "W"], key="lon_ew")
    
    with col3:
        st.number_input("Voyage Order Speed (kts)", min_value=0.0, step=0.1, key="voyage_order_speed")
        st.number_input("Voyage Order ME FO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_fo_cons")
        st.number_input("Voyage Order ME DO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_do_cons")
        st.number_input("Course (°)", min_value=0, max_value=359, step=1, key="course")
        st.number_input("Heading (°)", min_value=0, max_value=359, step=1, key="heading")
        st.number_input("True Heading (°)", min_value=0, max_value=359, step=1, key="true_heading")
        st.number_input("Water Depth (m)", min_value=0.0, step=0.1, key="water_depth")
    
    with col4:
        st.number_input("Draft F (m)", min_value=0.0, step=0.01, value=10.36, key="draft_f")
        st.number_input("Draft A (m)", min_value=0.0, step=0.01, value=11.50, key="draft_a")
        st.number_input("Displacement (mt)", min_value=0.0, step=0.1, value=70498.00, key="displacement")

def display_weather_and_sea_conditions():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Wind Direction (°)", min_value=0, max_value=359, key="wind_direction")
        st.number_input("Wind Force (knots)", min_value=0.0, step=0.1, key="wind_force")
        st.number_input("Sea State Direction (°)", min_value=0, max_value=359, key="sea_state_direction")
        st.selectbox("Sea State (Douglas Scale)", [""] + [str(i) for i in range(10)], key="sea_state")
        st.number_input("Swell Height (m)", min_value=0.0, step=0.1, key="swell_height")
    with col2:
        st.number_input("Current Direction (°)", min_value=0, max_value=359, key="current_direction")
        st.number_input("Current Speed (knots)", min_value=0.0, step=0.1, key="current_speed")
        st.number_input("Air Temperature (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="air_temp")
        st.number_input("Sea Temperature (°C)", min_value=-2.0, max_value=35.0, step=0.1, key="sea_temp")

def display_time_elapsed():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Time Since Previous Report (hours)", min_value=0.0, step=0.1, key="time_since_prev_report")
        st.number_input("Time Elapsed Sailing (hours)", min_value=0.0, step=0.1, key="time_elapsed_sailing")
        st.number_input("Time Elapsed Anchoring (hours)", min_value=0.0, step=0.1, key="time_elapsed_anchoring")
        st.number_input("Time Elapsed DP (hours)", min_value=0.0, step=0.1, key="time_elapsed_dp")
    with col2:
        st.number_input("Time Elapsed Ice (hours)", min_value=0.0, step=0.1, key="time_elapsed_ice")
        st.number_input("Time Elapsed Maneuvering (hours)", min_value=0.0, step=0.1, key="time_elapsed_maneuvering")
        st.number_input("Time Elapsed Waiting (hours)", min_value=0.0, step=0.1, key="time_elapsed_waiting")
        st.number_input("Time Elapsed Loading/Unloading (hours)", min_value=0.0, step=0.1, key="time_elapsed_loading_unloading")

def display_cargo_operations():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Cargo Weight (MT)", min_value=0.0, step=0.1, key="cargo_weight")
        st.number_input("Cargo Volume (m³)", min_value=0.0, step=0.1, key="cargo_volume")
        st.number_input("Number of Passengers", min_value=0, step=1, key="passengers")
        st.number_input("Total TEU", min_value=0, step=1, key="total_teu")
    with col2:
        st.number_input("Reefer TEU", min_value=0, step=1, key="reefer_teu")
        st.number_input("Reefer 20ft Chilled", min_value=0, step=1, key="reefer_20ft_chilled")
        st.number_input("Reefer 40ft Chilled", min_value=0, step=1, key="reefer_40ft_chilled")
        st.number_input("Reefer 20ft Frozen", min_value=0, step=1, key="reefer_20ft_frozen")
        st.number_input("Reefer 40ft Frozen", min_value=0, step=1, key="reefer_40ft_frozen")

def display_fuel_consumption():
    fuel_types = ["HFO", "LFO", "MGO", "MDO", "LPGP", "LPGB", "LNG", "Methanol", "Ethanol", "Other"]
    consumers = ["ME", "AE", "Boiler", "Inert Gas"]
    
    for consumer in consumers:
        st.subheader(f"{consumer} Consumption")
        cols = st.columns(5)
        for i, fuel in enumerate(fuel_types):
            cols[i % 5].number_input(f"{consumer} {fuel} (MT)", min_value=0.0, step=0.1, key=f"{consumer}_{fuel.lower()}")

def display_engine_performance():
    st.subheader("Main Engine")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("ME Load (kW)", min_value=0, step=1, key="me_load")
        st.number_input("ME Load Percentage (%)", min_value=0.0, max_value=100.0, step=0.1, key="me_load_percentage")
        st.number_input("ME Speed (RPM)", min_value=0, step=1, key="me_speed")
    with col2:
        st.number_input("ME SFOC (g/kWh)", min_value=0.0, step=0.1, key="me_sfoc")
        st.number_input("ME SFOC ISO Corrected (g/kWh)", min_value=0.0, step=0.1, key="me_sfoc_iso")
        st.number_input("ME Running Hours", min_value=0.0, step=0.1, key="me_running_hours")
    with col3:
        st.number_input("ME Work (kWh)", min_value=0, step=1, key="me_work")
        st.number_input("ME Average Load (kW)", min_value=0, step=1, key="me_avg_load")
        st.number_input("ME Average Load Percentage (%)", min_value=0.0, max_value=100.0, step=0.1, key="me_avg_load_percentage")

    st.subheader("Auxiliary Engine")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("AE Load (kW)", min_value=0, step=1, key="ae_load")
        st.number_input("AE SFOC (g/kWh)", min_value=0.0, step=0.1, key="ae_sfoc")
        st.number_input("AE SFOC ISO Corrected (g/kWh)", min_value=0.0, step=0.1, key="ae_sfoc_iso")
    with col2:
        st.number_input("AE Running Hours", min_value=0.0, step=0.1, key="ae_running_hours")
        st.number_input("AE Average Load (kW)", min_value=0, step=1, key="ae_avg_load")
        st.number_input("AE Work (kWh)", min_value=0, step=1, key="ae_work")

def display_auxiliary_systems():
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Boiler 1 Operation Mode", key="boiler1_operation_mode")
        st.number_input("Boiler 1 Feed Water Flow (m³/min)", min_value=0.0, step=0.1, key="boiler1_feed_water_flow")
        st.number_input("Boiler 1 Steam Pressure (bar)", min_value=0.0, step=0.1, key="boiler1_steam_pressure")
        st.number_input("Boiler 1 Running Hours", min_value=0.0, step=0.1, key="boiler1_running_hours")
    with col2:
        st.number_input("Air Compressor 1 Running Time (hours)", min_value=0.0, step=0.1, key="air_comp1_running_time")
        st.number_input("Air Compressor 2 Running Time (hours)", min_value=0.0, step=0.1, key="air_comp2_running_time")
        st.number_input("Thruster 1 Running Time (hours)", min_value=0.0, step=0.1, key="thruster1_running_time")
        st.number_input("Thruster 2 Running Time (hours)", min_value=0.0, step=0.1, key="thruster2_running_time")

def display_environmental_compliance():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Total Fuel ROB (MT)", min_value=0.0, step=0.1, key="total_fuel_rob")
        st.number_input("HFO ROB (MT)", min_value=0.0, step=0.1, key="hfo_rob")
        st.number_input("LFO ROB (MT)", min_value=0.0, step=0.1, key="lfo_rob")
        st.number_input("MGO ROB (MT)", min_value=0.0, step=0.1, key="mgo_rob")
    with col2:
        st.number_input("MDO ROB (MT)", min_value=0.0, step=0.1, key="mdo_rob")
        st.number_input("LNG ROB (MT)", min_value=0.0, step=0.1, key="lng_rob")
        st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1, key="sludge_rob")
        st.number_input("Shore Side Electricity Reception (kWh)", min_value=0, step=1, key="shore_side_electricity")

def display_fresh_water():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Fresh Water Bunkered (m³)", min_value=0.0, step=0.1, key="fw_bunkered")
        st.number_input("Fresh Water Consumption - Drinking (m³)", min_value=0.0, step=0.1, key="fw_consumption_drinking")
        st.number_input("Fresh Water Consumption - Technical (m³)", min_value=0.0, step=0.1, key="fw_consumption_technical")
    with col2:
        st.number_input("Fresh Water Consumption - Washing (m³)", min_value=0.0, step=0.1, key="fw_consumption_washing")
        st.number_input("Fresh Water Produced (m³)", min_value=0.0, step=0.1, key="fw_produced")
        st.number_input("Fresh Water ROB (m³)", min_value=0.0, step=0.1, key="fw_rob")

def display_lubricating_oil():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("ME Cylinder Oil ROB (liters)", min_value=0, step=1, key="me_cyl_oil_rob")
        st.number_input("ME Cylinder Oil High BN ROB (liters)", min_value=0, step=1, key="me_cyl_oil_high_bn_rob")
        st.number_input("ME Cylinder Oil Low BN ROB (liters)", min_value=0, step=1, key="me_cyl_oil_low_bn_rob")
        st.number_input("ME System Oil ROB (liters)", min_value=0, step=1, key="me_system_oil_rob")
    with col2:
        st.number_input("AE System Oil ROB (liters)", min_value=0, step=1, key="ae_system_oil_rob")
        st.number_input("ME Cylinder Oil Consumption (liters)", min_value=0, step=1, key="me_cyl_oil_consumption")
        st.number_input("ME Cylinder Oil Feed Rate (g/kWh)", min_value=0.0, step=0.1, key="me_cyl_oil_feed_rate")
        st.number_input("ME System Oil Consumption (liters)", min_value=0, step=1, key="me_system_oil_consumption")

def display_vessel_performance():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Draft Actual Fore (m)", min_value=0.0, step=0.01, key="draft_actual_fore")
        st.number_input("Draft Actual Aft (m)", min_value=0.0, step=0.01, key="draft_actual_aft")
        st.number_input("Draft Recommended Fore (m)", min_value=0.0, step=0.01, key="draft_recommended_fore")
        st.number_input("Draft Recommended Aft (m)", min_value=0.0, step=0.01, key="draft_recommended_aft")
    with col2:
        st.number_input("Propeller Pitch (m)", min_value=0.0, step=0.01, key="propeller_pitch")
        st.number_input("Propeller Pitch Ratio", min_value=0.0, step=0.01, key="propeller_pitch_ratio")
        st.number_input("Average Propeller Speed (RPM)", min_value=0, step=1, key="avg_propeller_speed")
        st.number_input("Slip (%)", min_value=0.0, max_value=100.0, step=0.1, key="slip_percentage")
        st.number_input("ME Projected Consumption (MT/day)", min_value=0.0, step=0.1, key="me_projected_consumption")
        st.number_input("AE Projected Consumption (MT/day)", min_value=0.0, step=0.1, key="ae_projected_consumption")

def display_special_events_and_remarks():
    st.selectbox("Operation Mode", ["", "At Sea", "In Port", "Maneuvering", "Anchoring", "Drifting"], key="operation_mode")
    st.selectbox("Cleaning Event", ["", "Propeller Cleaning", "Hull Cleaning", "Tank Cleaning"], key="cleaning_event")
    st.number_input("Number of Tugs", min_value=0, step=1, key="number_of_tugs")
    st.text_input("Reason for Schedule Deviation", key="schedule_deviation_reason")
    st.text_area("Remarks", key="remarks")
    st.text_input("Entry Made By (Deck)", key="entry_by_deck")
    st.text_input("Entry Made By (Engine)", key="entry_by_engine")
    st.text_input("Contact Email", key="contact_email")
    st.date_input("Reporting Date", value=datetime.now(), key="reporting_date")

if __name__ == "__main__":
    main()
