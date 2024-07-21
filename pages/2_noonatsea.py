import streamlit as st
from datetime import datetime

st.set_page_config(layout="wide")
st.title("Noon at Sea Report")

# Tabs for different sections
tabs = st.tabs(["Deck", "Engine"])

# Deck Tab
with tabs[0]:
    st.header("General Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        ship_mean_time_utc = st.time_input("Ship Mean Time (UTC)", datetime.now().time(), key="ship_mean_time_utc")
        report_date_lt = st.date_input("Report Date (LT)", datetime.now().date(), key="report_date_lt")
        report_time_lt = st.time_input("Report Time (LT)", datetime.now().time(), key="report_time_lt")
    with col2:
        report_time_utc = st.time_input("UTC", datetime.now().time(), key="report_time_utc")
        voyage_no = st.text_input("Voyage No", key="voyage_no")
        cargo_no = st.text_input("Cargo No", key="cargo_no")
    with col3:
        vessel_status = st.selectbox("Vessel's Status", ["At Sea", "In Port"], key="vessel_status")
        current_port = st.text_input("Current Port", key="current_port")
        last_port = st.text_input("Last Port", key="last_port")
        berth_location = st.text_input("Berth / Location", key="berth_location")

    col1, col2 = st.columns(2)
    with col1:
        latitude = st.text_input("Latitude", key="latitude")
        longitude = st.text_input("Longitude", key="longitude")
    with col2:
        next_port = st.text_input("Next Port", key="next_port")
        eta_date = st.date_input("ETA Date", datetime.now().date(), key="eta_date")
        eta_time = st.time_input("ETA Time", datetime.now().time(), key="eta_time")

    col1, col2 = st.columns(2)
    with col1:
        etb_date = st.date_input("ETB Date", datetime.now().date(), key="etb_date")
        etb_time = st.time_input("ETB Time", datetime.now().time(), key="etb_time")
    with col2:
        etcd_date = st.date_input("ETC/D Date", datetime.now().date(), key="etcd_date")
        etcd_time = st.time_input("ETC/D Time", datetime.now().time(), key="etcd_time")

    col1, col2 = st.columns(2)
    with col1:
        best_eta_pbg_lt = st.date_input("Best ETA PBG (LT) Date", datetime.now().date(), key="best_eta_pbg_lt_date")
        best_eta_pbg_lt_time = st.time_input("Best ETA PBG (LT) Time", datetime.now().time(), key="best_eta_pbg_lt_time")
    with col2:
        best_eta_pbg_utc = st.date_input("Best ETA PBG (UTC) Date", datetime.now().date(), key="best_eta_pbg_utc_date")
        best_eta_pbg_utc_time = st.time_input("Best ETA PBG (UTC) Time", datetime.now().time(), key="best_eta_pbg_utc_time")

    st.header("Speed and Consumption")
    col1, col2 = st.columns(2)
    with col1:
        full_speed_hours = st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1, key="full_speed_hours")
        full_speed_nm = st.number_input("Full Speed (nm)", min_value=0.0, step=0.1, key="full_speed_nm")
        reduced_speed_hours = st.number_input("Reduced Speed/Slow Steaming (hrs)", min_value=0.0, step=0.1, key="reduced_speed_hours")
        reduced_speed_nm = st.number_input("Reduced Speed/Slow Steaming (nm)", min_value=0.0, step=0.1, key="reduced_speed_nm")
        stopped_hours = st.number_input("Stopped (hrs)", min_value=0.0, step=0.1, key="stopped_hours")
        distance_observed = st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1, key="distance_observed")
        obs_speed_sog = st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1, key="obs_speed_sog")
    with col2:
        em_log_speed_log = st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1, key="em_log_speed_log")
        voyage_average_speed = st.number_input("Voyage Average Speed (kts)", min_value=0.0, step=0.1, key="voyage_average_speed")
        distance_to_go = st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1, key="distance_to_go")
        distance_since_cosp = st.number_input("Distance since COSP (nm)", min_value=0.0, step=0.1, key="distance_since_cosp")
        voyage_order_speed = st.number_input("Voyage Order Speed (kts)", min_value=0.0, step=0.1, key="voyage_order_speed")
        voyage_order_me_fo_cons = st.number_input("Voyage Order ME FO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_fo_cons")
        voyage_order_me_do_cons = st.number_input("Voyage Order ME DO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_do_cons")

    col1, col2 = st.columns(2)
    with col1:
        course = st.number_input("Course (°T)", min_value=0.0, step=0.1, key="course")
        draft_f = st.number_input("Draft F (m)", min_value=0.0, step=0.1, key="draft_f")
    with col2:
        draft_a = st.number_input("Draft A (m)", min_value=0.0, step=0.1, key="draft_a")
        displacement = st.number_input("Displacement (mt)", min_value=0.0, step=0.1, key="displacement")

    st.header("Wind and Weather")
    col1, col2 = st.columns(2)
    with col1:
        wind_direction = st.selectbox("Wind Direction", ["North", "North East", "East", "South East", "South", "South West", "West", "North West"], key="wind_direction")
        wind_force = st.number_input("Wind Force", min_value=0.0, step=0.1, key="wind_force")
        visibility = st.number_input("Visibility (nm)", min_value=0.0, step=0.1, key="visibility")
        period_bad_weather = st.number_input("Period of bad Weather (hrs)", min_value=0.0, step=0.1, key="period_bad_weather")
    with col2:
        sea_height = st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key="sea_height")
        sea_direction = st.selectbox("Sea Direction", ["North", "North East", "East", "South East", "South", "South West", "West", "North West"], key="sea_direction")
        swell_height = st.number_input("Swell Height (m)", min_value=0.0, step=0.1, key="swell_height")
        current_set = st.number_input("Current Set (kts)", min_value=0.0, step=0.1, key="current_set")
        current_drift = st.selectbox("Current Drift", ["North", "North East", "East", "South East", "South", "South West", "West", "North West"], key="current_drift")
        air_temp = st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="air_temp")
        icing_on_deck = st.checkbox("Icing on Deck?", key="icing_on_deck")

    st.header("High Risk and Special Areas")
    hra_col1, hra_col2 = st.columns([1, 3])
    with hra_col1:
        in_hra = st.radio("Is vessel currently in Gulf of Aden / HRA or will be Transiting Gulf of Aden / HRA within next 14 days?", ["Yes", "No"], key="in_hra")
    with hra_col2:
        hra_entry_date = st.date_input("Entry into HRA", datetime.now().date(), key="hra_entry_date")
        hra_entry_time = st.time_input("Entry into HRA Time", datetime.now().time(), key="hra_entry_time")
        hra_exit_date = st.date_input("Exit From HRA", datetime.now().date(), key="hra_exit_date")
        hra_exit_time = st.time_input("Exit From HRA Time", datetime.now().time(), key="hra_exit_time")

    st.header("Environmental Control Area")
    eca_col1, eca_col2 = st.columns([1, 3])
    with eca_col1:
        in_eca = st.radio("Is vessel in an ECA area or will enter ECA area within next 3 days?", ["Yes", "No"], key="in_eca")
    with eca_col2:
        eca_entry_date = st.date_input("Entry into ECA", datetime.now().date(), key="eca_entry_date")
        eca_entry_time = st.time_input("Entry into ECA Time", datetime.now().time(), key="eca_entry_time")
        eca_exit_date = st.date_input("Exit From ECA", datetime.now().date(), key="eca_exit_date")
        eca_exit_time = st.time_input("Exit From ECA Time", datetime.now().time(), key="eca_exit_time")
        eca_latitude = st.text_input("ECA Latitude", key="eca_latitude")
        eca_longitude = st.text_input("ECA Longitude", key="eca_longitude")
        eca_fuel_used = st.selectbox("Fuel used in ECA", ["HFO", "MGO", "LNG"], key="eca_fuel_used")
        eca_fuel_changeover_time = st.date_input("Fuel C/O Time", datetime.now().date(), key="eca_fuel_changeover_time")

    st.header("Breaching International Navigating Limits")
    iwl_col1, iwl_col2 = st.columns([1, 3])
    with iwl_col1:
        in_iwl = st.radio("Is the vessel in IWL Breach area or will enter IWL Breach area within next 7 days?", ["Yes", "No"], key="in_iwl")
    with iwl_col2:
        iwl_entry_date = st.date_input("Entry into IWL Breach", datetime.now().date(), key="iwl_entry_date")
        iwl_entry_time = st.time_input("Entry into IWL Breach Time", datetime.now().time(), key="iwl_entry_time")
        iwl_exit_date = st.date_input("Exit From IWL Breach", datetime.now().date(), key="iwl_exit_date")
        iwl_exit_time = st.time_input("Exit From IWL Breach Time", datetime.now().time(), key="iwl_exit_time")

    st.header("Drifting")
    drifting_start_col1, drifting_start_col2 = st.columns(2)
    with drifting_start_col1:
        drifting_start_lat = st.text_input("Drifting Start Latitude", key="drifting_start_lat")
        drifting_start_long = st.text_input("Drifting Start Longitude", key="drifting_start_long")
        drifting_start_date = st.date_input("Drifting Start Date", datetime.now().date(), key="drifting_start_date")
        drifting_start_time = st.time_input("Drifting Start Time", datetime.now().time(), key="drifting_start_time")
    with drifting_start_col2:
        drifting_end_lat = st.text_input("Drifting End Latitude", key="drifting_end_lat")
        drifting_end_long = st.text_input("Drifting End Longitude", key="drifting_end_long")
        drifting_end_date = st.date_input("Drifting End Date", datetime.now().date(), key="drifting_end_date")
        drifting_end_time = st.time_input("Drifting End Time", datetime.now().time(), key="drifting_end_time")
    drifting_distance = st.number_input("Drifting Distance (nm)", min_value=0.0, step=0.1, key="drifting_distance")
    drifting_hours = st.number_input("Drifting Hours (hrs)", min_value=0.0, step=0.1, key="drifting_hours")

if st.button("Submit", key="submit"):
    st.write("Form submitted successfully!")
