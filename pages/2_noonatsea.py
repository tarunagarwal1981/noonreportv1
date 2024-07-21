import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
st.title("Noon at Sea Report")

# Tabs for Deck and Engine
tabs = st.tabs(["Deck", "Engine"])

# General Information Section for Deck Tab
with tabs[0]:
    st.header("General Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ship_mean_time = st.text_input("Ship Mean Time", key="ship_mean_time")
        utc_offset = st.number_input("UTC Offset", min_value=-12, max_value=12, step=1, key="utc_offset")
        report_date_lt = st.date_input("Report Date (LT)", datetime.now().date(), key="report_date_lt")
        report_time_lt = st.time_input("Report Time (LT)", datetime.now().time(), key="report_time_lt")
        report_date_utc = st.date_input("Report Date (UTC)", datetime.now().date(), key="report_date_utc")
        report_time_utc = st.time_input("Report Time (UTC)", datetime.now().time(), key="report_time_utc")
        idl_crossing = st.checkbox("IDL Crossing", key="idl_crossing")
        idl_direction = st.selectbox("IDL Direction", ["East", "West"], key="idl_direction")

    with col2:
        voyage_no = st.text_input("Voyage No", key="voyage_no")
        cargo_no = st.text_input("Cargo No", key="cargo_no")
        vessel_status = st.selectbox("Vessel's Status", ["At Sea", "In Port"], key="vessel_status")
        current_port = st.text_input("Current Port", key="current_port")
        last_port = st.text_input("Last Port", key="last_port")
        off_port_limits = st.checkbox("Off Port Limits", key="off_port_limits")
        berth_location = st.text_input("Berth / Location", key="berth_location")

    with col3:
        latitude = st.text_input("Latitude", key="latitude")
        longitude = st.text_input("Longitude", key="longitude")
        next_port = st.text_input("Next Port", key="next_port")
        eta_date = st.date_input("ETA Date", datetime.now().date(), key="eta_date")
        eta_time = st.time_input("ETA Time", datetime.now().time(), key="eta_time")
        speed_required = st.number_input("Speed required to achieve Scheduled ETA (kts)", min_value=0.0, step=0.1, key="speed_required")

    col1, col2 = st.columns(2)
    with col1:
        best_eta_pbg_lt_date = st.date_input("Best ETA PBG (LT) Date", datetime.now().date(), key="best_eta_pbg_lt_date")
        best_eta_pbg_lt_time = st.time_input("Best ETA PBG (LT) Time", datetime.now().time(), key="best_eta_pbg_lt_time")
    with col2:
        best_eta_pbg_utc_date = st.date_input("Best ETA PBG (UTC) Date", datetime.now().date(), key="best_eta_pbg_utc_date")
        best_eta_pbg_utc_time = st.time_input("Best ETA PBG (UTC) Time", datetime.now().time(), key="best_eta_pbg_utc_time")

    ballast_laden = st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden")

    # Speed and Consumption Section
    st.header("Speed and Consumption")
    col1, col2, col3 = st.columns(3)

    with col1:
        full_speed_hrs = st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1, key="full_speed_hrs")
        full_speed_nm = st.number_input("Full Speed (nm)", min_value=0.0, step=0.1, key="full_speed_nm")
        reduced_speed_hrs = st.number_input("Reduced Speed/Slow Steaming (hrs)", min_value=0.0, step=0.1, key="reduced_speed_hrs")
        reduced_speed_nm = st.number_input("Reduced Speed/Slow Steaming (nm)", min_value=0.0, step=0.1, key="reduced_speed_nm")
        stopped_hrs = st.number_input("Stopped (hrs)", min_value=0.0, step=0.1, key="stopped_hrs")

    with col2:
        distance_observed = st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1, key="distance_observed")
        obs_speed_sog = st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1, key="obs_speed_sog")
        em_log_speed = st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1, key="em_log_speed")
        voyage_average_speed = st.number_input("Voyage Average Speed (kts)", min_value=0.0, step=0.1, key="voyage_average_speed")
        distance_to_go = st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1, key="distance_to_go")

    with col3:
        distance_since_cosp = st.number_input("Distance since COSP (nm)", min_value=0.0, step=0.1, key="distance_since_cosp")
        voyage_order_speed = st.number_input("Voyage Order Speed (kts)", min_value=0.0, step=0.1, key="voyage_order_speed")
        voyage_order_me_fo_cons = st.number_input("Voyage Order ME FO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_fo_cons")
        voyage_order_me_do_cons = st.number_input("Voyage Order ME DO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_do_cons")
        course = st.number_input("Course (°T)", min_value=0.0, step=0.1, key="course")
        draft_f = st.number_input("Draft F (m)", min_value=0.0, step=0.1, key="draft_f")
        draft_a = st.number_input("Draft A (m)", min_value=0.0, step=0.1, key="draft_a")
        displacement = st.number_input("Displacement (mt)", min_value=0.0, step=0.1, key="displacement")

    # Wind and Weather Section
    st.header("Wind and Weather")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        wind_direction = st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key="wind_direction")
        wind_force = st.number_input("Wind Force", min_value=0, step=1, key="wind_force")
        visibility = st.number_input("Visibility (nm)", min_value=0.0, step=0.1, key="visibility")
        bad_weather_period = st.number_input("Period of bad Weather (hrs)", min_value=0.0, step=0.1, key="bad_weather_period")
        
    with col2:
        sea_height = st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key="sea_height")
        sea_direction = st.selectbox("Sea Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key="sea_direction")
        swell_height = st.number_input("Swell Height (m)", min_value=0.0, step=0.1, key="swell_height")
        swell_direction = st.selectbox("Swell Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key="swell_direction")
        
    with col3:
        current_set = st.number_input("Current Set (kts)", min_value=0.0, step=0.1, key="current_set")
        current_drift = st.selectbox("Current Drift", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key="current_drift")
        air_temp = st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="air_temp")
        icing_on_deck = st.checkbox("Icing on Deck?", key="icing_on_deck")

    # High Risk and Special Areas Section
    st.header("High Risk and Special Areas")
    hra_col1, hra_col2 = st.columns([1, 3])
    
    with hra_col1:
        in_hra = st.radio("Is vessel currently in Gulf of Aden / HRA or will be Transiting Gulf of Aden / HRA in next 14 days?", ["Yes", "No"], key="in_hra")
    with hra_col2:
        hra_entry_date = st.date_input("Entry into HRA", datetime.now().date(), key="hra_entry_date")
        hra_entry_time = st.time_input("Entry into HRA Time", datetime.now().time(), key="hra_entry_time")
        hra_exit_date = st.date_input("Exit From HRA", datetime.now().date(), key="hra_exit_date")
        hra_exit_time = st.time_input("Exit From HRA Time", datetime.now().time(), key="hra_exit_time")

    # Environmental Control Area Section
    st.header("Environmental Control Area")
    eca_col1, eca_col2 = st.columns([1, 3])
    
    with eca_col1:
        in_eca = st.radio("Is vessel in an ECA area or will enter ECA area within next 3 days?", ["Yes", "No"], key="in_eca")
    with eca_col2:
        eca_entry_date = st.date_input("Entry into ECA", datetime.now().date(), key="eca_entry_date")
        eca_entry_time = st.time_input("Entry into ECA Time", datetime.now().time(), key="eca_entry_time")
        eca_exit_date = st.date_input("Exit From ECA", datetime.now().date(), key="eca_exit_date")
        eca_exit_time = st.time_input("Exit From ECA Time", datetime.now().time(), key="eca_exit_time")
        eca_latitude = st.text_input("Latitude", key="eca_latitude")
        eca_longitude = st.text_input("Longitude", key="eca_longitude")
        fuel_used_in_eca = st.selectbox("Fuel used in ECA", ["IFO", "MDO", "MGO"], key="fuel_used_in_eca")
        fuel_c_o_time = st.date_input("Fuel C/O Time", datetime.now().date(), key="fuel_c_o_time")

    # Breaching International Navigating Limits Section
    st.header("Breaching International Navigating Limits")
    in_iwl = st.radio("Is the vessel in IWL Breach area or will enter IWL Breach area within next 7 days?", ["Yes", "No"], key="in_iwl")
    
    iwl_entry_date = st.date_input("Entry into IWL Breach", datetime.now().date(), key="iwl_entry_date")
    iwl_entry_time = st.time_input("Entry into IWL Breach Time", datetime.now().time(), key="iwl_entry_time")
    iwl_exit_date = st.date_input("Exit From IWL Breach", datetime.now().date(), key="iwl_exit_date")
    iwl_exit_time = st.time_input("Exit From IWL Breach Time", datetime.now().time(), key="iwl_exit_time")
