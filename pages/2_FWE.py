import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime FWE Report")

def main():
    st.title("Maritime Finished With Engine (FWE) Report")

    fwe_scenario = st.selectbox("FWE Scenario", [
        "Departure Port", 
        "Departure Anchoring",
        "End Drifting",
        "Departure STS"
    ])

    tabs = st.tabs(["FWE Information", "Navigation", "Engine", "Consumption"])

    with tabs[0]:
        fwe_info_tab(fwe_scenario)

    with tabs[1]:
        navigation_tab(fwe_scenario)

    with tabs[2]:
        engine_tab()

    with tabs[3]:
        consumption_tab()

    if st.button("Submit FWE Report", type="primary"):
        st.success("FWE report submitted successfully!")

def fwe_info_tab(fwe_scenario):
    st.header("FWE Information")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Vessel", key="vessel_fwe")
        st.text_input("Voyage No", key="voyage_fwe")
        st.text_input("Port/Location", key="port_location_fwe")
        st.text_input("Latitude", key="latitude_fwe")
        st.text_input("Longitude", key="longitude_fwe")
    with col2:
        st.time_input("Ship Mean Time (UTC)", datetime.now().time(), key="ship_mean_time_utc_fwe")
        st.time_input("Ship Mean Time (LT)", datetime.now().time(), key="ship_mean_time_lt_fwe")
        st.date_input("FWE Date", datetime.now().date(), key="fwe_date")
        st.time_input("FWE Time", datetime.now().time(), key="fwe_time")
    with col3:
        st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden_fwe")
        st.checkbox("Start New Voyage", key="start_new_voyage")

    if "Alongside" in fwe_scenario:
        st.text_input("Name of Berth", key="berth_name")
        st.time_input("All Fast Time", datetime.now().time(), key="all_fast_time")
        st.time_input("Gangway Down Time", datetime.now().time(), key="gangway_down_time")
    
    if "Anchoring" in fwe_scenario:
        st.text_input("Anchorage Name", key="anchorage_name")
        st.number_input("Water Depth (m)", min_value=0.0, step=0.1, key="water_depth")
        st.number_input("Chain Length (shackles)", min_value=0, step=1, key="chain_length")
    
    if "Drifting" in fwe_scenario:
        st.text_input("Drifting Area", key="drifting_area")
        st.number_input("Expected Drifting Time (hrs)", min_value=0.0, step=0.1, key="expected_drifting_time")
    
    if "STS" in fwe_scenario:
        st.text_input("STS Area", key="sts_area")
        st.text_input("Name of Other Vessel", key="other_vessel_name")
        st.text_input("Type of STS Operation", key="sts_operation_type")
    
    if "Canal/River" in fwe_scenario:
        st.text_input("Canal/River Name", key="canal_river_name")
        st.text_input("Waiting Position", key="waiting_position")

    if "After EOSP" in fwe_scenario:
        st.time_input("EOSP Time", datetime.now().time(), key="eosp_time")
    
    st.date_input("Free Pratique Granted (FPG) Date", datetime.now(), key="fpg_date")
    st.time_input("Free Pratique Granted (FPG) Time", datetime.now().time(), key="fpg_time")

def navigation_tab(fwe_scenario):
    st.header("Navigation Details")

    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Draft F (m)", min_value=0.0, step=0.01, key="draft_f_fwe")
        st.number_input("Draft A (m)", min_value=0.0, step=0.01, key="draft_a_fwe")
        st.number_input("List (degrees)", min_value=-10.0, max_value=10.0, step=0.1, key="list")
        st.number_input("Trim (m)", min_value=-5.0, max_value=5.0, step=0.1, key="trim")
    with col2:
        st.number_input("DWT/Displacement (mt)", min_value=0.0, step=1.0, key="dwt_displacement")
        if "Alongside" not in fwe_scenario:
            st.number_input("Distance to Shore (nm)", min_value=0.0, step=0.1, key="distance_to_shore")
        st.date_input("ETD Date", datetime.now(), key="etd_date")
        st.time_input("ETD Time", datetime.now().time(), key="etd_time")

    st.subheader("From Last Report to FWE")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("Full Speed (hrs)", min_value=0.0, step=0.01, key="full_speed_hrs")
        st.number_input("Reduced Speed (hrs)", min_value=0.0, step=0.01, key="reduced_speed_hrs")
        st.number_input("Maneuvering (hrs)", min_value=0.0, step=0.01, key="maneuvering_hrs")
    with col2:
        st.number_input("Stopped (hrs)", min_value=0.0, step=0.01, key="stopped_hrs")
        st.number_input("Distance Observed (nm)", min_value=0.0, step=0.01, key="distance_observed")
        st.number_input("Maneuvering Distance (nm)", min_value=0.0, step=0.01, key="maneuvering_distance")
    with col3:
        st.number_input("Average Speed (kts)", min_value=0.0, step=0.1, key="average_speed_fwe")
        st.number_input("EM Log Speed (kts)", min_value=0.0, step=0.01, key="em_log_speed")

    if "After EOSP" in fwe_scenario:
        st.subheader("EOSP to FWE Details")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Time from EOSP to FWE (hrs)", min_value=0.0, step=0.1, key="time_eosp_to_fwe")
            st.number_input("Distance from EOSP to FWE (nm)", min_value=0.0, step=0.1, key="distance_eosp_to_fwe")
        with col2:
            st.number_input("Average Speed EOSP to FWE (kts)", min_value=0.0, step=0.1, key="avg_speed_eosp_to_fwe")

def engine_tab():
    st.header("Engine Information")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("ME Rev Counter @ FWE", key="me_rev_counter_fwe")
        st.number_input("ME RPM Counter", min_value=0, step=1, key="me_rpm_counter")
    with col2:
        st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1, key="shaft_generator_power_fwe")
        st.text_input("Shaft Generator Hours", key="shaft_generator_hours")

    st.subheader("Auxiliary Engines")
    col1, col2 = st.columns(2)
    with col1:
        for i in range(1, 5):
            st.number_input(f"A/E No.{i} Generator Load (kw)", min_value=0, step=1, key=f"ae_no{i}_generator_load")
    with col2:
        for i in range(1, 5):
            st.number_input(f"A/E No.{i} Generator Hours of Operation (hrs)", min_value=0.0, step=0.1, key=f"ae_no{i}_generator_hours")

    st.number_input("Earth Fault Monitor 440 Volts (MΩ)", min_value=0.0, step=0.1, key="earth_fault_monitor_440v")
    st.number_input("Earth Fault Monitor 230/110 Volts (MΩ)", min_value=0.0, step=0.1, key="earth_fault_monitor_230v")

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
        "Maneuvering M/E": [0.0] * 13,
        "Maneuvering A/E": [0.0] * 13,
        "Maneuvering BLR": [0.0] * 13,
        "Maneuvering IGG": [0.0] * 13,
        "Maneuvering GE/EG": [0.0] * 13,
        "Maneuvering OTH": [0.0] * 13,
        "Total Consumption": [0.0] * 13,
        "ROB @ FWE": [0.0] * 13,
    }
    consumption_df = pd.DataFrame(consumption_data)
    st.data_editor(consumption_df, key="consumption_editor", hide_index=True)

    st.subheader("Fuel and Bilge")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("FO Cons Rate (mt/day)", min_value=0.0, step=0.1, key="fo_cons_rate")
        st.number_input("DO Cons Rate (mt/day)", min_value=0.0, step=0.1, key="do_cons_rate")
        st.number_input("Density @ 15°C", min_value=0.0, step=0.001, key="density")
    with col2:
        st.number_input("Sulphur Content %", min_value=0.0, max_value=100.0, step=0.01, key="sulphur_content")
        st.number_input("Bilge Tank ROB (cu.m)", min_value=0.0, step=0.1, key="bilge_tank_rob")
        st.number_input("Total Sludge Retained onboard (cu.m)", min_value=0.0, step=0.1, key="total_sludge_retained")

    st.subheader("Environmental Control Area")
    st.text_input("Fuel Used in ECA", key="fuel_used_in_eca")
    st.number_input("Fuel CO Time (hrs)", min_value=0.0, step=0.01, key="fuel_co_time")

if __name__ == "__main__":
    main()
