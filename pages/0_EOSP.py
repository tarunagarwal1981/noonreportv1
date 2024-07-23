import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime EOSP Report")

def main():
    st.title("Maritime EOSP (End of Sea Passage) Report")

    tabs = st.tabs(["EOSP Information", "Navigation", "Weather", "Engine", "Consumption"])

    with tabs[0]:
        eosp_info_tab()

    with tabs[1]:
        navigation_tab()

    with tabs[2]:
        weather_tab()

    with tabs[3]:
        engine_tab()

    with tabs[4]:
        consumption_tab()

    if st.button("Submit EOSP Report", type="primary"):
        st.success("EOSP report submitted successfully!")

def eosp_info_tab():
    st.header("EOSP Information")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Vessel", key="vessel_eosp")
        st.text_input("Voyage", key="voyage_eosp")
        st.text_input("Port", key="port_eosp")
        st.text_input("Name of Berth / Anchorage", key="berth_location_eosp")
        st.text_input("Latitude", key="latitude_eosp")
        st.text_input("Longitude", key="longitude_eosp")
    with col2:
        st.time_input("Ship Mean Time (UTC)", datetime.now().time(), key="ship_mean_time_utc_eosp")
        st.time_input("Ship Mean Time (LT)", datetime.now().time(), key="ship_mean_time_lt_eosp")
        st.date_input("EOSP Date", datetime.now().date(), key="eosp_date")
        st.time_input("EOSP Time", datetime.now().time(), key="eosp_time")
    with col3:
        st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden_eosp")
        st.number_input("Maneuvering (hrs)", min_value=0.0, step=0.01, key="maneuvering_hrs_eosp")
        st.number_input("Maneuvering Distance (nm)", min_value=0.0, step=0.01, key="maneuvering_distance_eosp")

def navigation_tab():
    st.header("Navigation Details")

    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Total Distance Traveled (nm)", min_value=0.0, step=0.1, key="total_distance_traveled")
        st.number_input("Average Speed (kts)", min_value=0.0, step=0.1, key="average_speed_eosp")
        st.number_input("Draft F (m)", min_value=0.0, step=0.01, key="draft_f_eosp")
        st.number_input("Draft A (m)", min_value=0.0, step=0.01, key="draft_a_eosp")
    with col2:
        st.date_input("ETB Date", datetime.now(), key="etb_date")
        st.time_input("ETB Time", datetime.now().time(), key="etb_time")
        st.date_input("ETD Date", datetime.now(), key="etd_date")
        st.time_input("ETD Time", datetime.now().time(), key="etd_time")

    st.subheader("From Noon to EOSP")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("Full Speed (hrs)", min_value=0.0, step=0.01, key="full_speed_hrs")
        st.number_input("Reduced Speed (hrs)", min_value=0.0, step=0.01, key="reduced_speed_hrs")
        st.number_input("Stopped (hrs)", min_value=0.0, step=0.01, key="stopped_hrs")
    with col2:
        st.number_input("Distance Observed (nm)", min_value=0.0, step=0.01, key="distance_observed")
        st.number_input("Obs Speed (kts)", min_value=0.0, step=0.01, key="obs_speed")
        st.number_input("EM Log Speed (kts)", min_value=0.0, step=0.01, key="em_log_speed")
    with col3:
        st.number_input("Voyage Order Speed (kts)", min_value=0.0, step=0.01, key="voyage_order_speed")
        st.number_input("Voyage Order Cons (kts)", min_value=0.0, step=0.01, key="voyage_order_cons")
        st.number_input("Course", min_value=0, step=1, key="course")

def weather_tab():
    st.header("Weather and Conditions")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Wind Direction", key="wind_direction")
        st.number_input("Wind Force", min_value=0, step=1, key="wind_force")
        st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key="sea_height")
        st.text_input("Sea Direction", key="sea_direction")
    with col2:
        st.number_input("Swell (m)", min_value=0.0, step=0.1, key="swell")
        st.text_input("Set and Drift of Current", key="set_and_drift_of_current")
        st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="air_temp")
        st.checkbox("Icing on Deck?", key="icing_on_deck")

    st.number_input("DWT/Displacement (mt)", min_value=0.0, step=1.0, key="dwt_displacement")

def engine_tab():
    st.header("Engine Information")

    st.text_input("ME Rev Counter @ EOSP", key="me_rev_counter_eosp")
    st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1, key="shaft_generator_power_eosp")

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
        "Total Consumption": [0.0] * 13,
        "ROB @ EOSP": [0.0] * 13,
    }
    consumption_df = pd.DataFrame(consumption_data)
    st.data_editor(consumption_df, key="consumption_editor", hide_index=True)

    st.subheader("Environmental Control Area")
    st.text_input("Fuel Used in ECA", key="fuel_used_in_eca")
    st.number_input("Fuel CO Time (hrs)", min_value=0.0, step=0.01, key="fuel_co_time")

if __name__ == "__main__":
    main()