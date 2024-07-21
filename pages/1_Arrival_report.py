import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
st.title("Vessel Arrival Report")

# Arrival Information Tab
st.header("Arrival Information")

col1, col2 = st.columns([2, 1])
with col1:
    vessel = st.text_input("Vessel", key="vessel_arrival")
    voyage = st.text_input("Voyage", key="voyage_arrival")
    port = st.text_input("Port", key="port_arrival")
    berth_location = st.text_input("Name of Berth / Anchorage", key="berth_location_arrival")
    latitude = st.text_input("Latitude", key="latitude_arrival")
    longitude = st.text_input("Longitude", key="longitude_arrival")
    ship_mean_time_utc = st.time_input("Ship Mean Time (UTC)", datetime.now().time(), key="ship_mean_time_utc_arrival")
    ship_mean_time_lt = st.time_input("Ship Mean Time (LT)", datetime.now().time(), key="ship_mean_time_lt_arrival")

with col2:
    eosp = st.text_input("EOSP", key="eosp_arrival")
    fwe = st.text_input("FWE", key="fwe_arrival")

st.header("Event Times")
for event in ["Arrival Date", "End of Sea Passage (EOSP)", "APS", "Arrival customary Anchorage", "Arrival drifting position", "Anchor aweigh", "Commenced proceeding to berth from drifting position", "Pilot on Board (POB)", "First Line Ashore (FLA)", "First Shackle in water (FSW)", "Let Go Anchor (LGA)", "All Fast", "Gangway Down", "Finished with Engine (FWE)", "Pilot Away (POB)"]:
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        st.write(event)
    with col2:
        st.date_input(f"{event} LT Date", datetime.now().date(), key=f"{event}_lt_date_arrival")
        st.time_input(f"{event} LT Time", datetime.now().time(), key=f"{event}_lt_time_arrival")
    with col3:
        st.date_input(f"{event} UTC Date", datetime.now().date(), key=f"{event}_utc_date_arrival")
        st.time_input(f"{event} UTC Time", datetime.now().time(), key=f"{event}_utc_time_arrival")

col1, col2 = st.columns(2)
with col1:
    fpg_date = st.date_input("Free Pratique Granted (FPG) Date", datetime.now().date(), key="fpg_date")
    fpg_time = st.time_input("Free Pratique Granted (FPG) Time", datetime.now().time(), key="fpg_time")
    etb_date = st.date_input("ETB Date", datetime.now().date(), key="etb_date")
    etb_time = st.time_input("ETB Time", datetime.now().time(), key="etb_time")
    etd_date = st.date_input("ETD Date", datetime.now().date(), key="etd_date")
    etd_time = st.time_input("ETD Time", datetime.now().time(), key="etd_time")
    ballast_laden = st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden")
with col2:
    start_new_voyage = st.checkbox("Start New Voyage", key="start_new_voyage")
    maneuvering_hrs = st.number_input("Maneuvering (hrs)", min_value=0.0, step=0.01, key="maneuvering_hrs")
    maneuvering_distance = st.number_input("Maneuvering Distance (nm)", min_value=0.0, step=0.01, key="maneuvering_distance")
    me_rev_counter_fwe = st.text_input("ME Rev Counter @ FWE", key="me_rev_counter_fwe")

st.header("From Noon to EOSP")

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    full_speed = st.number_input("Full Speed (hrs)", min_value=0.0, step=0.01, key="full_speed")
    reduced_speed = st.number_input("Reduced Speed (hrs)", min_value=0.0, step=0.01, key="reduced_speed")
    stopped = st.number_input("Stopped (hrs)", min_value=0.0, step=0.01, key="stopped")
    distance_observed = st.number_input("Distance Observed (nm)", min_value=0.0, step=0.01, key="distance_observed")
    obs_speed = st.number_input("Obs Speed (kts)", min_value=0.0, step=0.01, key="obs_speed")
    em_log_speed = st.number_input("EM Log Speed (kts)", min_value=0.0, step=0.01, key="em_log_speed")
    voyage_order_speed = st.number_input("Voyage Order Speed (kts)", min_value=0.0, step=0.01, key="voyage_order_speed")
    voyage_order_cons = st.number_input("Voyage Order Cons (kts)", min_value=0.0, step=0.01, key="voyage_order_cons")
    course = st.number_input("Course", min_value=0, step=1, key="course")
    
with col2:
    draft_f = st.number_input("Draft F (m)", min_value=0.0, step=0.01, key="draft_f_arrival")
    draft_a = st.number_input("Draft A (m)", min_value=0.0, step=0.01, key="draft_a_arrival")
    wind_direction = st.text_input("Wind Direction", key="wind_direction")
    wind_force = st.number_input("Wind Force", min_value=0, step=1, key="wind_force")
    sea_height = st.number_input("Sea Height (m)", min_value=0.0, step=0.01, key="sea_height")
    sea_direction = st.text_input("Sea Direction", key="sea_direction")
    swell = st.number_input("Swell (m)", min_value=0.0, step=0.01, key="swell")
    set_and_drift_of_current = st.text_input("Set and Drift of Current", key="set_and_drift_of_current")
    
with col3:
    air_temp = st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="air_temp")
    icing_on_deck = st.checkbox("Icing on Deck?", key="icing_on_deck")
    dwt_displacement = st.number_input("DWT/Displacement (mt)", min_value=0.0, step=1.0, key="dwt_displacement")

st.header("Drifting / STS")

col1, col2 = st.columns(2)
with col1:
    drifting_sts = st.radio("Is Drifting / STS", ["Drifting", "STS"], key="drifting_sts")
    me_rpm_counter = st.number_input("ME RPM Counter", min_value=0, step=1, key="me_rpm_counter")
    latitude_drifting = st.text_input("Latitude", key="latitude_drifting")
    longitude_drifting = st.text_input("Longitude", key="longitude_drifting")
    drifting_date_start = st.date_input("Drifting Date Start", datetime.now().date(), key="drifting_date_start")
    drifting_time_start = st.time_input("Drifting Time Start", datetime.now().time(), key="drifting_time_start")
    
with col2:
    drifting_date_end = st.date_input("Drifting Date End", datetime.now().date(), key="drifting_date_end")
    drifting_time_end = st.time_input("Drifting Time End", datetime.now().time(), key="drifting_time_end")
    drifting_distance = st.number_input("Drifting Distance (nm)", min_value=0.0, step=0.01, key="drifting_distance")
    
st.header("Environmental Control Area")
col1, col2 = st.columns(2)
with col1:
    fuel_used_in_eca = st.text_input("Fuel Used in ECA", key="fuel_used_in_eca")
    fuel_co_time = st.number_input("Fuel CO Time (hrs)", min_value=0.0, step=0.01, key="fuel_co_time")
    
st.header("Consumption (MT)")
st.subheader("Consumption (MT)")
consumption_data = {
    "Fuel Type": [
        "Heavy Fuel Oil RME-RMK - 380cSt", "Heavy Fuel Oil RMA-RMD - 80cSt",
        "VLSFO RME-RMK Visc >380cSt 0.5%S Max", "VLSFO RMA-RMD Visc >80cSt 0.5%S Max",
        "ULSFO RME-RMK <380cSt 0.1%S Max", "ULSFO RMA-RMD <80cSt 0.1%S Max",
        "VLSMGO 0.5%S Max", "ULSMGO 0.1%S Max",
        "Biofuel - 30", "Biofuel Distillate FO",
        "LPG - Propane", "LPG - Butane",
        "LNG (Bunkered)"
    ],
    "Previous ROB": [0.0, 0.0, 410.70, 0.0, 0.0, 0.0, 0.0, 571.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "At Sea M/E": [0.0, 0.0, 18.20, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "At Sea A/E": [0.0, 0.0, 0.10, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "At Sea BLR": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "At Sea IGG": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "At Sea GE/EG": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "At Sea OTH": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "ROB @ COSP": [0.0, 0.0, 392.40, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "At Harbour M/E": [0.0, 0.0, 4.40, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "At Harbour A/E": [0.0, 0.0, 2.10, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "At Harbour BLR": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "At Harbour IGG": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "At Harbour GE/EG": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "At Harbour OTH": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Bunker Qty": [0.0, 0.0, 385.80, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Sulphur %": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Total ROB @ FWE": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Action": ["", "", "", "", "", "", "", "", "", "", "", "", ""]
}
consumption_emissions_df = pd.DataFrame(consumption_data)
st.dataframe(consumption_emissions_df)

if st.button("Submit", key="submit_arrival"):
    st.write("Arrival report submitted successfully!")
