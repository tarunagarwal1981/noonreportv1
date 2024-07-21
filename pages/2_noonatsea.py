import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
st.title("Noon at Sea Report")

# Tabs for Deck and Engine
tabs = st.tabs(["Deck", "Engine"])

# Deck Tab
with tabs[0]:
    st.header("General Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        vessel_name = st.text_input("Vessel Name", key="vessel_name")
        voyage_no = st.text_input("Voyage No", key="voyage_no")
        cargo_no = st.text_input("Cargo No", key="cargo_no")
        vessel_status = st.selectbox("Vessel's Status", ["At Sea", "In Port"], key="vessel_status")
        current_port = st.text_input("Current Port", key="current_port")
        last_port = st.text_input("Last Port", key="last_port")
        berth_location = st.text_input("Berth / Location", key="berth_location")
        latitude = st.text_input("Latitude", key="latitude")
        longitude = st.text_input("Longitude", key="longitude")
    with col2:
        report_date_lt = st.date_input("Report Date (LT)", datetime.now().date(), key="report_date_lt")
        report_time_lt = st.time_input("Report Time (LT)", datetime.now().time(), key="report_time_lt")
        report_date_utc = st.date_input("Report Date (UTC)", datetime.now().date(), key="report_date_utc")
        report_time_utc = st.time_input("Report Time (UTC)", datetime.now().time(), key="report_time_utc")
        idl_crossing = st.text_input("IDL Crossing", key="idl_crossing")
        idl_direction = st.selectbox("IDL Direction", ["--Select--", "East", "West"], key="idl_direction")
        off_port_limits = st.checkbox("Off Port Limits", key="off_port_limits")
    with col3:
        next_port = st.text_input("Next Port", key="next_port")
        eta_date = st.date_input("ETA Date", datetime.now().date(), key="eta_date")
        eta_time = st.time_input("ETA Time", datetime.now().time(), key="eta_time")
        speed_required = st.number_input("Speed required to achieve Scheduled ETA (kts)", min_value=0.0, step=0.1, key="speed_required")
        etb = st.date_input("ETB", datetime.now().date(), key="etb")
        etc_d = st.date_input("ETC/D", datetime.now().date(), key="etc_d")
        best_eta_pbg_lt = st.date_input("Best ETA PBG (LT)", datetime.now().date(), key="best_eta_pbg_lt")
        best_eta_pbg_time_lt = st.time_input("Best ETA PBG Time (LT)", datetime.now().time(), key="best_eta_pbg_time_lt")
        best_eta_pbg_utc = st.date_input("Best ETA PBG (UTC)", datetime.now().date(), key="best_eta_pbg_utc")
        best_eta_pbg_time_utc = st.time_input("Best ETA PBG Time (UTC)", datetime.now().time(), key="best_eta_pbg_time_utc")
        ballast_laden = st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden")

    st.header("Speed and Consumption")
    col1, col2, col3 = st.columns(3)
    with col1:
        full_speed_hours = st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1, key="full_speed_hours")
        full_speed_distance = st.number_input("Full Speed (nm)", min_value=0.0, step=0.1, key="full_speed_distance")
        reduced_speed_hours = st.number_input("Reduced Speed/Slow Steaming (hrs)", min_value=0.0, step=0.1, key="reduced_speed_hours")
        reduced_speed_distance = st.number_input("Reduced Speed/Slow Steaming (nm)", min_value=0.0, step=0.1, key="reduced_speed_distance")
        stopped_hours = st.number_input("Stopped (hrs)", min_value=0.0, step=0.1, key="stopped_hours")
        stopped_distance = st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1, key="stopped_distance")
    with col2:
        obs_speed_sog = st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1, key="obs_speed_sog")
        em_log_speed_log = st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1, key="em_log_speed_log")
        voyage_avg_speed = st.number_input("Voyage Average Speed (kts)", min_value=0.0, step=0.1, key="voyage_avg_speed")
        distance_to_go = st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1, key="distance_to_go")
        distance_since_cosp = st.number_input("Distance since COSP (nm)", min_value=0.0, step=0.1, key="distance_since_cosp")
    with col3:
        voyage_order_speed = st.number_input("Voyage Order Speed (kts)", min_value=0.0, step=0.1, key="voyage_order_speed")
        voyage_order_me_fo_cons = st.number_input("Voyage Order ME FO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_fo_cons")
        voyage_order_me_do_cons = st.number_input("Voyage Order ME DO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_do_cons")
        course = st.number_input("Course (°)", min_value=0.0, step=1.0, key="course")
        draft_f = st.number_input("Draft F (m)", min_value=0.0, step=0.01, key="draft_f")
        draft_a = st.number_input("Draft A (m)", min_value=0.0, step=0.01, key="draft_a")
        displacement = st.number_input("Displacement (mt)", min_value=0.0, step=0.1, key="displacement")

    st.header("Wind and Weather")
    col1, col2, col3 = st.columns(3)
    with col1:
        wind_direction = st.selectbox("Wind Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="wind_direction")
        wind_force = st.number_input("Wind Force", min_value=0.0, step=0.1, key="wind_force")
        visibility = st.number_input("Visibility (nm)", min_value=0.0, step=0.1, key="visibility")
        bad_weather_hours = st.number_input("Period of bad Weather (beyond BF scale 5, in Hours)", min_value=0.0, step=0.1, key="bad_weather_hours")
    with col2:
        sea_height = st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key="sea_height")
        sea_direction = st.selectbox("Sea Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="sea_direction")
        swell_height = st.number_input("Swell Height (m)", min_value=0.0, step=0.1, key="swell_height")
        swell_direction = st.selectbox("Swell Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="swell_direction")
    with col3:
        current_set = st.number_input("Current Set (kts)", min_value=0.0, step=0.1, key="current_set")
        current_drift = st.selectbox("Current Drift", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="current_drift")
        air_temp = st.number_input("Air Temp (°C)", min_value=-50.0, step=0.1, key="air_temp")
        icing_on_deck = st.checkbox("Icing on Deck?", key="icing_on_deck")

    st.header("High Risk and Special Areas")
    hra = st.radio("Is vessel currently in Gulf of Aden / HRA or will be Transiting Gulf of Aden / HRA within next 14 days?", ["Yes", "No"], key="hra")
    col1, col2 = st.columns(2)
    with col1:
        entry_hra_date = st.date_input("Entry into HRA Date", datetime.now().date(), key="entry_hra_date")
        entry_hra_time = st.time_input("Entry into HRA Time", datetime.now().time(), key="entry_hra_time")
    with col2:
        exit_hra_date = st.date_input("Exit from HRA Date", datetime.now().date(), key="exit_hra_date")
        exit_hra_time = st.time_input("Exit from HRA Time", datetime.now().time(), key="exit_hra_time")

    st.header("Environmental Control Area")
    eca = st.radio("Is vessel in an ECA area or will enter ECA area within next 3 days?", ["Yes", "No"], key="eca")
    col1, col2 = st.columns(2)
    with col1:
        entry_eca_date = st.date_input("Entry into ECA Date", datetime.now().date(), key="entry_eca_date")
        entry_eca_time = st.time_input("Entry into ECA Time", datetime.now().time(), key="entry_eca_time")
    with col2:
        exit_eca_date = st.date_input("Exit from ECA Date", datetime.now().date(), key="exit_eca_date")
        exit_eca_time = st.time_input("Exit from ECA Time", datetime.now().time(), key="exit_eca_time")
        latitude_eca = st.text_input("Latitude (ECA)", key="latitude_eca")
        longitude_eca = st.text_input("Longitude (ECA)", key="longitude_eca")
        fuel_used_eca = st.text_input("Fuel used in ECA", key="fuel_used_eca")
        fuel_changeover_time = st.time_input("Fuel C/O Time", datetime.now().time(), key="fuel_changeover_time")

    st.header("Breaching International Navigating Limits")
    inl = st.radio("Is the vessel in IWL Breach area or will enter IWL Breach area within next 7 days?", ["Yes", "No"], key="inl")
    col1, col2 = st.columns(2)
    with col1:
        entry_iwl_date = st.date_input("Entry into IWL Breach Date", datetime.now().date(), key="entry_iwl_date")
        entry_iwl_time = st.time_input("Entry into IWL Breach Time", datetime.now().time(), key="entry_iwl_time")
    with col2:
        exit_iwl_date = st.date_input("Exit from IWL Breach Date", datetime.now().date(), key="exit_iwl_date")
        exit_iwl_time = st.time_input("Exit from IWL Breach Time", datetime.now().time(), key="exit_iwl_time")

    st.header("Drifting")
    col1, col2 = st.columns(2)
    with col1:
        drift_start_latitude = st.text_input("Drifting Start Latitude", key="drift_start_latitude")
        drift_start_longitude = st.text_input("Drifting Start Longitude", key="drift_start_longitude")
        drift_start_date = st.date_input("Drifting Start Date", datetime.now().date(), key="drift_start_date")
        drift_start_time = st.time_input("Drifting Start Time", datetime.now().time(), key="drift_start_time")
        drift_distance = st.number_input("Drifting Distance (nm)", min_value=0.0, step=0.1, key="drift_distance")
    with col2:
        drift_end_latitude = st.text_input("Drifting End Latitude", key="drift_end_latitude")
        drift_end_longitude = st.text_input("Drifting End Longitude", key="drift_end_longitude")
        drift_end_date = st.date_input("Drifting End Date", datetime.now().date(), key="drift_end_date")
        drift_end_time = st.time_input("Drifting End Time", datetime.now().time(), key="drift_end_time")
        drift_time = st.number_input("Drifting Time (hrs)", min_value=0.0, step=0.1, key="drift_time")

# Engine Tab
with tabs[1]:
    st.header("General Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        engine_distance = st.number_input("Engine Distance (nm)", min_value=0.0, step=0.1, key="engine_distance")
        slip = st.number_input("Slip (%)", min_value=0.0, step=0.1, key="slip")
    with col2:
        er_temp = st.number_input("ER Temp (°C)", min_value=0.0, step=0.1, key="er_temp")
        sw_temp = st.number_input("SW Temp (°C)", min_value=0.0, step=0.1, key="sw_temp")
    with col3:
        avg_slip_cosp = st.number_input("Avg Slip since COSP (%)", min_value=0.0, step=0.1, key="avg_slip_cosp")
        avg_sw_press_cosp = st.number_input("Avg SW Press since COSP (bar)", min_value=0.0, step=0.1, key="avg_sw_press_cosp")

    st.header("Main Engine")
    col1, col2, col3 = st.columns(3)
    with col1:
        me_rev_counter = st.number_input("ME Rev Counter", min_value=0.0, step=1.0, key="me_rev_counter")
        avg_rpm = st.number_input("Average RPM", min_value=0.0, step=0.1, key="avg_rpm")
        avg_rpm_cosp = st.number_input("Avg RPM since COSP", min_value=0.0, step=0.1, key="avg_rpm_cosp")
        power_output = st.radio("Power Output", ["BHP", "KW"], key="power_output")
        calculated_bhp = st.number_input("Calculated BHP", min_value=0.0, step=1.0, key="calculated_bhp")
        governor_setting = st.number_input("Governor Setting or Fuel rack Setting (%)", min_value=0.0, step=0.1, key="governor_setting")
        speed_setting = st.number_input("Speed Setting", min_value=0.0, step=0.1, key="speed_setting")
    with col2:
        scav_air_temp = st.number_input("Scav Air Temp (°C)", min_value=0.0, step=0.1, key="scav_air_temp")
        scav_air_press = st.number_input("Scav Air Press (bar)", min_value=0.0, step=0.1, key="scav_air_press")
        fo_inlet_temp = st.number_input("FO Inlet Temp (°C)", min_value=0.0, step=0.1, key="fo_inlet_temp")
        fo_cat_fines = st.number_input("FO Cat Fines (ppm)", min_value=0.0, step=0.1, key="fo_cat_fines")
        fo_press = st.number_input("FO Press (bar)", min_value=0.0, step=0.1, key="fo_press")
        scav_air_temp_min = st.number_input("Scav Air Temp Min (°C)", min_value=0.0, step=0.1, key="scav_air_temp_min")
    with col3:
        exhaust_temp_max = st.number_input("Exh Temp Max (°C)", min_value=0.0, step=0.1, key="exhaust_temp_max")
        exhaust_temp_min = st.number_input("Exh Temp Min (°C)", min_value=0.0, step=0.1, key="exhaust_temp_min")
        exhaust_press = st.number_input("Exh Press (bar)", min_value=0.0, step=0.1, key="exhaust_press")
        exhaust_temp = st.number_input("Exhaust Temp (°C)", min_value=0.0, step=0.1, key="exhaust_temp")
        fo_temp = st.number_input("FO Temp (°C)", min_value=0.0, step=0.1, key="fo_temp")
        scav_air_press_min = st.number_input("Scav Air Press Min (bar)", min_value=0.0, step=0.1, key="scav_air_press_min")

    st.header("Auxiliary Engines")
    col1, col2 = st.columns(2)
    with col1:
        ae_no1_load = st.number_input("A/E No.1 Generator Load (kw)", min_value=0.0, step=1.0, key="ae_no1_load")
        ae_no2_load = st.number_input("A/E No.2 Generator Load (kw)", min_value=0.0, step=1.0, key="ae_no2_load")
        ae_no3_load = st.number_input("A/E No.3 Generator Load (kw)", min_value=0.0, step=1.0, key="ae_no3_load")
        ae_no4_load = st.number_input("A/E No.4 Generator Load (kw)", min_value=0.0, step=1.0, key="ae_no4_load")
    with col2:
        ae_no1_hours = st.number_input("A/E No.1 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae_no1_hours")
        ae_no2_hours = st.number_input("A/E No.2 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae_no2_hours")
        ae_no3_hours = st.number_input("A/E No.3 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae_no3_hours")
        ae_no4_hours = st.number_input("A/E No.4 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae_no4_hours")
        shaft_generator_power = st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1, key="shaft_generator_power")

    st.header("Lube Oil Consumptions (Ltrs)")
    lube_oil_data = {
        "Lube Oil": ["ME Cylinder Oil", "ME Cylinder Oil 40 TBN", "ME Cylinder Oil 70 TBN", "ME Cylinder Oil 100 TBN", "ME/MT System Oil", "AE System Oil", "AE System Oil 15TBN", "TG System Oil", "Other Lub Oils"],
        "Prev.ROB": [0.0, 24526.0, 0.0, 17500.0, 32000.0, 16800.0, 0.0, 0.0, 0.0],
        "Cons": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Received": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "ROB": [0.0, 24526.0, 0.0, 17500.0, 32000.0, 16800.0, 0.0, 0.0, 0.0]
    }
    lube_oil_df = pd.DataFrame(lube_oil_data)
    st.dataframe(lube_oil_df)

    st.header("Fresh Water")
    fresh_water_data = {
        "Fresh Water": ["Domestic Fresh Water", "Drinking Water", "Boiler Water", "Tank Cleaning Water"],
        "Previous ROB": [241.0, 0.0, 0.0, 0.0],
        "Produced": [0.0, 0.0, 0.0, 0.0],
        "ROB": [240.0, 0.0, 0.0, 0.0],
        "Consumption": [1.0, 0.0, 0.0, 0.0]
    }
    fresh_water_df = pd.DataFrame(fresh_water_data)
    st.dataframe(fresh_water_df)

    st.header("Fuel, Bilge, and Sludge")
    col1, col2, col3 = st.columns(3)
    with col1:
        fo_cons_rate = st.number_input("FO Cons Rate (mt/day)", min_value=0.0, step=0.1, key="fo_cons_rate")
        do_cons_rate = st.number_input("DO Cons Rate (mt/day)", min_value=0.0, step=0.1, key="do_cons_rate")
        density_15c = st.number_input("Density @ 15°C", min_value=0.0, step=0.1, key="density_15c")
        sulphur_content = st.number_input("Sulphur Content %", min_value=0.0, step=0.1, key="sulphur_content")
    with col2:
        fo_cons_since_cosp = st.number_input("FO Cons since COSP (mt/day)", min_value=0.0, step=0.1, key="fo_cons_since_cosp")
        do_cons_since_cosp = st.number_input("DO Cons since COSP (mt/day)", min_value=0.0, step=0.1, key="do_cons_since_cosp")
    with col3:
        hfo_pfr1_hours = st.number_input("HFO PFR 1 Operation Hrs", min_value=0.0, step=0.1, key="hfo_pfr1_hours")
        hfo_pfr2_hours = st.number_input("HFO PFR 2 Operation Hrs", min_value=0.0, step=0.1, key="hfo_pfr2_hours")
        do_pfr_hours = st.number_input("DO PFR Operation Hrs", min_value=0.0, step=0.1, key="do_pfr_hours")
        me_lo_pfr_hours = st.number_input("ME LO PFR Operation Hrs", min_value=0.0, step=0.1, key="me_lo_pfr_hours")
        ae_lo_pfr_hours = st.number_input("AE LO PFR Operation Hrs", min_value=0.0, step=0.1, key="ae_lo_pfr_hours")
        bilge_tank_rob = st.number_input("Bilge Tank ROB (cu.m)", min_value=0.0, step=0.1, key="bilge_tank_rob")
        total_sludge = st.number_input("Total Sludge Retained onboard (cu.m)", min_value=0.0, step=0.1, key="total_sludge")
        last_landing_bilge_water = st.date_input("Last landing of Bilge Water", datetime.now().date(), key="last_landing_bilge_water")
        last_landing_sludge = st.date_input("Last landing of Sludge", datetime.now().date(), key="last_landing_sludge")

    st.header("Consumptions (mT)")
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
        "Previous ROB": [0.0, 0.0, 21.0, 0.0, 0.0, 0.0, 0.0, 472.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "AT SEA M/E": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 29.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "AT SEA A/E": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "AT SEA BLR": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "AT SEA IGG": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "AT SEA C/ENG": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "AT SEA OTH": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "IN PORT M/E": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "IN PORT A/E": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "IN PORT BLR": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "IN PORT IGG": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "IN PORT C/ENG": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "IN PORT OTH": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Bunker Qty": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Sulphur %": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Total": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 29.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "ROB at Noon": [0.0, 0.0, 21.0, 0.0, 0.0, 0.0, 443.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
    consumptions_df = pd.DataFrame(consumptions_data)
    st.dataframe(consumptions_df)

if st.button("Submit", key="submit"):
    st.write("Form submitted successfully!")
