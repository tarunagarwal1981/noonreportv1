import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime Arrival Report")

def main():
    st.title("Maritime Arrival Report")

    tabs = st.tabs(["Arrival Information", "Consumption"])

    with tabs[0]:
        arrival_info_tab()

    with tabs[1]:
        consumption_tab()

    if st.button("Submit Report", type="primary"):
        st.success("Arrival report submitted successfully!")

def arrival_info_tab():
    st.header("Arrival Information")

    with st.expander("General Information", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Vessel", key="vessel_arrival")
            st.text_input("Voyage", key="voyage_arrival")
            st.text_input("Port", key="port_arrival")
            st.text_input("Name of Berth / Anchorage", key="berth_location_arrival")
            st.text_input("Latitude", key="latitude_arrival")
            st.text_input("Longitude", key="longitude_arrival")
        with col2:
            st.time_input("Ship Mean Time (UTC)", datetime.now().time(), key="ship_mean_time_utc_arrival")
            st.time_input("Ship Mean Time (LT)", datetime.now().time(), key="ship_mean_time_lt_arrival")
            st.text_input("EOSP", key="eosp_arrival")
            st.text_input("FWE", key="fwe_arrival")
        with col3:
            st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden")
            st.checkbox("Start New Voyage", key="start_new_voyage")
            st.number_input("Maneuvering (hrs)", min_value=0.0, step=0.01, key="maneuvering_hrs")
            st.number_input("Maneuvering Distance (nm)", min_value=0.0, step=0.01, key="maneuvering_distance")
            st.text_input("ME Rev Counter @ FWE", key="me_rev_counter_fwe")

    with st.expander("Event Times", expanded=True):
        events = [
            "Arrival Date", "End of Sea Passage (EOSP)", "APS", "Arrival customary Anchorage",
            "Arrival drifting position", "Anchor aweigh", "Commenced proceeding to berth from drifting position",
            "Pilot on Board (POB)", "First Line Ashore (FLA)", "First Shackle in water (FSW)",
            "Let Go Anchor (LGA)", "All Fast", "Gangway Down", "Finished with Engine (FWE)", "Pilot Away (POB)"
        ]
        for event in events:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(event)
            with col2:
                st.date_input(f"{event} LT Date", datetime.now().date(), key=f"{event}_lt_date_arrival")
            with col3:
                st.time_input(f"{event} LT Time", datetime.now().time(), key=f"{event}_lt_time_arrival")
            with col4:
                st.time_input(f"{event} UTC Time", datetime.now().time(), key=f"{event}_utc_time_arrival")

    with st.expander("Additional Times", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Free Pratique Granted (FPG) Date", datetime.now().date(), key="fpg_date")
            st.time_input("Free Pratique Granted (FPG) Time", datetime.now().time(), key="fpg_time")
            st.date_input("ETB Date", datetime.now().date(), key="etb_date")
            st.time_input("ETB Time", datetime.now().time(), key="etb_time")
        with col2:
            st.date_input("ETD Date", datetime.now().date(), key="etd_date")
            st.time_input("ETD Time", datetime.now().time(), key="etd_time")

    with st.expander("From Noon to EOSP", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Full Speed (hrs)", min_value=0.0, step=0.01, key="full_speed")
            st.number_input("Reduced Speed (hrs)", min_value=0.0, step=0.01, key="reduced_speed")
            st.number_input("Stopped (hrs)", min_value=0.0, step=0.01, key="stopped")
            st.number_input("Distance Observed (nm)", min_value=0.0, step=0.01, key="distance_observed")
            st.number_input("Obs Speed (kts)", min_value=0.0, step=0.01, key="obs_speed")
        with col2:
            st.number_input("EM Log Speed (kts)", min_value=0.0, step=0.01, key="em_log_speed")
            st.number_input("Voyage Order Speed (kts)", min_value=0.0, step=0.01, key="voyage_order_speed")
            st.number_input("Voyage Order Cons (kts)", min_value=0.0, step=0.01, key="voyage_order_cons")
            st.number_input("Course", min_value=0, step=1, key="course")
            st.number_input("Draft F (m)", min_value=0.0, step=0.01, key="draft_f_arrival")
        with col3:
            st.number_input("Draft A (m)", min_value=0.0, step=0.01, key="draft_a_arrival")
            st.text_input("Wind Direction", key="wind_direction")
            st.number_input("Wind Force", min_value=0, step=1, key="wind_force")
            st.number_input("Sea Height (m)", min_value=0.0, step=0.01, key="sea_height")
            st.text_input("Sea Direction", key="sea_direction")

    with st.expander("Weather and Conditions", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Swell (m)", min_value=0.0, step=0.01, key="swell")
            st.text_input("Set and Drift of Current", key="set_and_drift_of_current")
            st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="air_temp")
        with col2:
            st.checkbox("Icing on Deck?", key="icing_on_deck")
            st.number_input("DWT/Displacement (mt)", min_value=0.0, step=1.0, key="dwt_displacement")

    with st.expander("Drifting / STS", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.radio("Is Drifting / STS", ["Drifting", "STS"], key="drifting_sts")
            st.number_input("ME RPM Counter", min_value=0, step=1, key="me_rpm_counter")
            st.text_input("Latitude", key="latitude_drifting")
            st.text_input("Longitude", key="longitude_drifting")
            st.date_input("Drifting Date Start", datetime.now().date(), key="drifting_date_start")
        with col2:
            st.time_input("Drifting Time Start", datetime.now().time(), key="drifting_time_start")
            st.date_input("Drifting Date End", datetime.now().date(), key="drifting_date_end")
            st.time_input("Drifting Time End", datetime.now().time(), key="drifting_time_end")
            st.number_input("Drifting Distance (nm)", min_value=0.0, step=0.01, key="drifting_distance")

    with st.expander("Environmental Control Area", expanded=True):
        st.text_input("Fuel Used in ECA", key="fuel_used_in_eca")
        st.number_input("Fuel CO Time (hrs)", min_value=0.0, step=0.01, key="fuel_co_time")

def consumption_tab():
    st.header("Consumption (MT)")

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
        "Previous ROB": [0.0] * 13,
        "At Sea M/E": [0.0] * 13,
        "At Sea A/E": [0.0] * 13,
        "At Sea BLR": [0.0] * 13,
        "At Sea IGG": [0.0] * 13,
        "At Sea GE/EG": [0.0] * 13,
        "At Sea OTH": [0.0] * 13,
        "ROB @ COSP": [0.0] * 13,
        "At Harbour M/E": [0.0] * 13,
        "At Harbour A/E": [0.0] * 13,
        "At Harbour BLR": [0.0] * 13,
        "At Harbour IGG": [0.0] * 13,
        "At Harbour GE/EG": [0.0] * 13,
        "At Harbour OTH": [0.0] * 13,
        "Bunker Qty": [0.0] * 13,
        "Sulphur %": [0.0] * 13,
        "Total ROB @ FWE": [0.0] * 13,
    }
    consumption_df = pd.DataFrame(consumption_data)
    st.data_editor(consumption_df, key="consumption_editor", hide_index=True)

if __name__ == "__main__":
    main()
