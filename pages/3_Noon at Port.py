import streamlit as st
import pandas as pd
from datetime import datetime

# Set up the page layout
st.set_page_config(layout="wide", page_title="Noon in Port Report")

def main():
    st.title("Noon in Port Report")

    tabs = st.tabs(["Deck", "Engine"])

    with tabs[0]:
        deck_tab()
        
    with tabs[1]:
        engine_tab()

def deck_tab():
    st.header("Deck Information")

    # General Information Section
    st.subheader("General Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Ship Mean Time", value="UTC")
        st.number_input("Offset", min_value=-12, max_value=12, step=1, key="offset")
    with col2:
        st.date_input("Report Date (LT)", datetime.now(), key="report_date_lt")
        st.time_input("Report Time (LT)", datetime.now().time(), key="report_time_lt")
    with col3:
        st.date_input("Report Date (UTC)", datetime.now(), key="report_date_utc")
        st.time_input("Report Time (UTC)", datetime.now().time(), key="report_time_utc")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.checkbox("IDL Crossing", key="idl_crossing")
        st.selectbox("IDL Direction", ["--Select--", "East", "West"], key="idl_direction")
        st.text_input("Voyage No", key="voyage_no")
    with col2:
        st.text_input("Cargo No", key="cargo_no")
        st.selectbox("Vessel's Status", ["At Sea", "In Port"], key="vessel_status")
        st.text_input("Current Port", key="current_port")
    with col3:
        st.text_input("Last Port", key="last_port")
        st.checkbox("Off Port Limits", key="off_port_limits")
        st.text_input("Berth / Location", key="berth_location")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Latitude", key="latitude")
    with col2:
        st.text_input("Longitude", key="longitude")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Next Port", key="next_port")
        st.date_input("ETA Date", datetime.now(), key="eta_date")
        st.time_input("ETA Time", datetime.now().time(), key="eta_time")
    with col2:
        st.text_input("Speed required to achieve Scheduled ETA (kts)", key="speed_required_eta")
        st.date_input("ETB", datetime.now(), key="etb")
        st.date_input("ETC/D", datetime.now(), key="etc_d")
        st.time_input("ETC/D Time", datetime.now().time(), key="etc_d_time")

    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Best ETA PBG (LT)", datetime.now(), key="best_eta_pbg_lt_date")
        st.time_input("Best ETA PBG Time (LT)", datetime.now().time(), key="best_eta_pbg_lt_time")
    with col2:
        st.date_input("Best ETA PBG (UTC)", datetime.now(), key="best_eta_pbg_utc_date")
        st.time_input("Best ETA PBG Time (UTC)", datetime.now().time(), key="best_eta_pbg_utc_time")

    st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden")

    # Speed and Consumption Section
    st.subheader("Speed and Consumption")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1, key="full_speed_hrs")
        st.number_input("Full Speed (nm)", min_value=0.0, step=0.1, key="full_speed_nm")
        st.number_input("Reduced Speed/Slow Steaming (hrs)", min_value=0.0, step=0.1, key="reduced_speed_hrs")
        st.number_input("Reduced Speed/Slow Steaming (nm)", min_value=0.0, step=0.1, key="reduced_speed_nm")
        st.number_input("Stopped (hrs)", min_value=0.0, step=0.1, key="stopped_hrs")
        st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1, key="distance_observed")
    with col2:
        st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1, key="obs_speed")
        st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1, key="em_log_speed")
        st.number_input("Voyage Average Speed (kts)", min_value=0.0, step=0.1, key="voyage_avg_speed")
        st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1, key="distance_to_go")
        st.number_input("Distance since COSP (nm)", min_value=0.0, step=0.1, key="distance_since_cosp")
    with col3:
        st.number_input("Voyage Order Speed (kts)", min_value=0.0, step=0.1, key="voyage_order_speed")
        st.number_input("Voyage Order ME FO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_fo_cons")
        st.number_input("Voyage Order ME DO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_do_cons")
        st.number_input("Course (°)", min_value=0.0, max_value=360.0, step=1.0, key="course")
        st.number_input("Draft F (m)", min_value=0.0, step=0.01, key="draft_f")
        st.number_input("Draft A (m)", min_value=0.0, step=0.01, key="draft_a")
        st.number_input("Displacement (mt)", min_value=0.0, step=0.1, key="displacement")

    # Wind and Weather Section
    st.subheader("Wind and Weather")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Wind Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="wind_direction")
        st.number_input("Wind Force", min_value=0, max_value=12, key="wind_force")
        st.number_input("Visibility (nm)", min_value=0.0, step=0.1, key="visibility")
        st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key="sea_height")
        st.selectbox("Sea Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="sea_direction")
    with col2:
        st.number_input("Swell Height (m)", min_value=0.0, step=0.1, key="swell_height")
        st.selectbox("Swell Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="swell_direction")
        st.number_input("Current Set (kts)", min_value=0.0, step=0.1, key="current_set")
        st.selectbox("Current Drift", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="current_drift")
        st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="air_temp")
        st.checkbox("Icing on Deck?", key="icing_on_deck")
    st.number_input("Period of bad Weather (beyond BF scale 5, in Hours)", min_value=0.0, step=0.1, key="period_bad_weather")

    # Forecast next 24 Hrs Section
    st.subheader("Forecast next 24 Hrs")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Wind Direction Forecast", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="wind_direction_forecast")
        st.number_input("Wind Force Forecast", min_value=0, max_value=12, key="wind_force_forecast")
        st.number_input("Sea Height Forecast (m)", min_value=0.0, step=0.1, key="sea_height_forecast")
    with col2:
        st.selectbox("Sea Direction Forecast", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="sea_direction_forecast")
        st.number_input("Swell Height Forecast (m)", min_value=0.0, step=0.1, key="swell_height_forecast")

    # Drifting Section
    st.subheader("Drifting")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Drifting Start Latitude", key="drifting_start_latitude")
        st.text_input("Drifting Start Longitude", key="drifting_start_longitude")
        st.date_input("Drifting Start Date", datetime.now(), key="drifting_start_date")
        st.time_input("Drifting Start Time", datetime.now().time(), key="drifting_start_time")
        st.number_input("Drifting Distance (nm)", min_value=0.0, step=0.1, key="drifting_distance")
    with col2:
        st.text_input("Drifting End Latitude", key="drifting_end_latitude")
        st.text_input("Drifting End Longitude", key="drifting_end_longitude")
        st.date_input("Drifting End Date", datetime.now(), key="drifting_end_date")
        st.time_input("Drifting End Time", datetime.now().time(), key="drifting_end_time")
        st.number_input("Drifting Time (hrs)", min_value=0.0, step=0.1, key="drifting_time")

def engine_tab():
    st.header("Engine Information")

    # Main Engine Section
    st.subheader("Main Engine")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("M/E Rev Counter", min_value=0, step=1, key="me_rev_counter")
        st.number_input("Average RPM", min_value=0.0, step=0.1, key="avg_rpm")
        st.number_input("Avg RPM since COSP", min_value=0.0, step=0.1, key="avg_rpm_since_cosp")
        st.radio("Power Output", ["BHP", "KW"], key="power_output")
        st.number_input("Calculated BHP", min_value=0, step=1, key="calculated_bhp")
    with col2:
        st.number_input("Governor Setting or Fuel rack Setting (%)", min_value=0.0, max_value=100.0, step=0.1, key="governor_setting")
        st.number_input("Speed Setting", min_value=0.0, step=0.1, key="speed_setting")
        st.number_input("Scav Air Temp (°C)", min_value=0.0, step=0.1, key="scav_air_temp")
        st.number_input("Scav Air Press (bar)", min_value=0.0, step=0.1, key="scav_air_press")
        st.number_input("FO Inlet Temp (°C)", min_value=0.0, step=0.1, key="fo_inlet_temp")
    with col3:
        st.number_input("FO Cat Fines (ppm)", min_value=0.0, step=0.1, key="fo_cat_fines")
        st.number_input("FO Press (bar)", min_value=0.0, step=0.1, key="fo_press")
        st.number_input("Exh Temp Max (°C)", min_value=0.0, step=0.1, key="exh_temp_max")
        st.number_input("Exh Temp Min (°C)", min_value=0.0, step=0.1, key="exh_temp_min")
        st.number_input("Exh Press (bar)", min_value=0.0, step=0.1, key="exh_press")

    # Auxiliary Engines Section
    st.subheader("Auxiliary Engines")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("A/E No.1 Generator Load (kw)", min_value=0, step=1, key="ae1_generator_load")
        st.number_input("A/E No.2 Generator Load (kw)", min_value=0, step=1, key="ae2_generator_load")
        st.number_input("A/E No.3 Generator Load (kw)", min_value=0, step=1, key="ae3_generator_load")
        st.number_input("A/E No.4 Generator Load (kw)", min_value=0, step=1, key="ae4_generator_load")
    with col2:
        st.number_input("A/E No.1 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae1_generator_hours")
        st.number_input("A/E No.2 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae2_generator_hours")
        st.number_input("A/E No.3 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae3_generator_hours")
        st.number_input("A/E No.4 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae4_generator_hours")
    st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1, key="shaft_generator_power")

    # Fresh Water Section
    st.subheader("Fresh Water")
    fresh_water_data = {
        "Fresh Water": ["Domestic Fresh Water", "Drinking Water", "Boiler Water", "Tank Cleaning Water"],
        "Previous ROB": [0.0] * 4,
        "Produced": [0.0] * 4,
        "ROB": [0.0] * 4,
        "Consumption": [0.0] * 4
    }
    fresh_water_df = pd.DataFrame(fresh_water_data)
    st.data_editor(fresh_water_df, key="fresh_water_editor", hide_index=True)

    # Fuel, Bilge, and Sludge Section
    st.subheader("Fuel, Bilge and Sludge")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("FO Cons Rate (mt/day)", min_value=0.0, step=0.1, key="fo_cons_rate")
        st.number_input("DO Cons Rate (mt/day)", min_value=0.0, step=0.1, key="do_cons_rate")
        st.number_input("Density @ 15°C", min_value=0.0, step=0.001, key="density_15c")
        st.number_input("Sulphur Content %", min_value=0.0, max_value=100.0, step=0.01, key="sulphur_content")
    with col2:
        st.number_input("FO Cons since COSP (mt/day)", min_value=0.0, step=0.1, key="fo_cons_since_cosp")
        st.number_input("DO Cons since COSP (mt/day)", min_value=0.0, step=0.1, key="do_cons_since_cosp")
        st.number_input("Bilge Tank ROB (cu.m)", min_value=0.0, step=0.1, key="bilge_tank_rob")
        st.number_input("Total Sludge Retained onboard (cu.m)", min_value=0.0, step=0.1, key="total_sludge_retained_onboard")
        st.date_input("Last landing of Bilge Water", datetime.now(), key="last_landing_bilge_water")
        st.number_input("Days since last landing", min_value=0, step=1, key="days_since_last_landing")

    # Lube Oil Consumptions Section
    st.subheader("Lube Oil Consumptions (Ltr)")
    lube_oil_data = {
        "Lube Oil": ["ME Cylinder Oil", "ME Cylinder Oil 40 TBN", "ME Cylinder Oil 70 TBN", "ME Cylinder Oil 100 TBN", "ME/MT System Oil", "AE System Oil", "AE System Oil 15TBN", "TG System Oil", "Other Lub Oils"],
        "Prev.ROB": [0.0] * 9,
        "Cons": [0.0] * 9,
        "Received": [0.0] * 9,
        "ROB": [0.0] * 9
    }
    lube_oil_df = pd.DataFrame(lube_oil_data)
    st.data_editor(lube_oil_df, key="lube_oil_editor", hide_index=True)

    # Detailed Fuel Consumption Section
    st.subheader("Consumptions (mT)")
    consumptions_data = {
        "Oil Type": [
            "Heavy Fuel Oil RME-RMK - 80cSt", "Heavy Fuel Oil RMA-RMD - 80cSt",
            "VLSFO RME-RMK Visc >80cSt 0.5%S Max", "VLSFO RMA-RMD Visc >80cSt 0.5%S Max",
            "ULSFO RME-RMK <80cSt 0.1%S Max", "ULSFO RMA-RMD <80cSt 0.1%S Max",
            "VLSMGO 0.5%S Max", "ULSMGO 0.1%S Max",
            "Biofuel - 30", "Biofuel Distillate FO",
            "LPG - Propane", "LPG - Butane",
            "LNG Boil Off", "LNG (Bunkered)"
        ],
        "Previous ROB": [0.0] * 14,
        "AT SEA M/E": [0.0] * 14,
        "AT SEA A/E": [0.0] * 14,
        "AT SEA BLR": [0.0] * 14,
        "AT SEA IGG": [0.0] * 14,
        "AT SEA C/ENG": [0.0] * 14,
        "AT SEA OTH": [0.0] * 14,
        "IN PORT M/E": [0.0] * 14,
        "IN PORT A/E": [0.0] * 14,
        "IN PORT BLR": [0.0] * 14,
        "IN PORT IGG": [0.0] * 14,
        "IN PORT C/ENG": [0.0] * 14,
        "IN PORT OTH": [0.0] * 14,
        "Bunker Qty": [0.0] * 14,
        "Sulphur %": [0.0] * 14,
        "Total": [0.0] * 14,
        "ROB at Noon": [0.0] * 14
    }
    consumptions_df = pd.DataFrame(consumptions_data)
    st.data_editor(consumptions_df, key="consumptions_editor", hide_index=True)

if __name__ == "__main__":
    main()
