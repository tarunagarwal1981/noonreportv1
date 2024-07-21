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

if st.button("Submit", key="submit_noon_at_sea"):
    st.write("Noon at Sea report submitted successfully!")
