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

    st.subheader("Best ETA PBG")
    col1, col2, col3 = st.columns(3)
    with col1:
        best_eta_pbg_lt_date = st.date_input("Best ETA PBG (LT) Date", datetime.now().date(), key="best_eta_pbg_lt_date")
        best_eta_pbg_lt_time = st.time_input("Best ETA PBG (LT) Time", datetime.now().time(), key="best_eta_pbg_lt_time")
    with col2:
        best_eta_pbg_utc_date = st.date_input("Best ETA PBG (UTC) Date", datetime.now().date(), key="best_eta_pbg_utc_date")
        best_eta_pbg_utc_time = st.time_input("Best ETA PBG (UTC) Time", datetime.now().time(), key="best_eta_pbg_utc_time")

    ballast_laden = st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden")

if st.button("Submit", key="submit_noon_at_sea"):
    st.write("Noon at Sea report submitted successfully!")
