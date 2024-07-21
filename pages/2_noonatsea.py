import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
st.title("Noon at Sea Report")

# Tabs for different sections
tabs = st.tabs(["Deck", "Engine"])

# Deck Tab
with tabs[0]:
    st.header("General Information")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ship_mean_time_utc = st.time_input("Ship Mean Time (UTC)", datetime.now().time(), key="ship_mean_time_utc")
        report_date_lt = st.date_input("Report Date (LT)", datetime.now().date(), key="report_date_lt")
        report_time_lt = st.time_input("Report Time (LT)", datetime.now().time(), key="report_time_lt")
    with col2:
        report_time_utc = st.time_input("UTC", datetime.now().time(), key="report_time_utc")
        idl_crossing = st.text_input("IDL Crossing", key="idl_crossing")
        idl_direction = st.text_input("IDL Direction", key="idl_direction")
    with col3:
        voyage_no = st.text_input("Voyage No", key="voyage_no")
        cargo_no = st.text_input("Cargo No", key="cargo_no")
        vessel_status = st.selectbox("Vessel's Status", ["At Sea", "In Port"], key="vessel_status")
    with col4:
        current_port = st.text_input("Current Port", key="current_port")
        last_port = st.text_input("Last Port", key="last_port")
        off_port_limits = st.text_input("Off Port Limits", key="off_port_limits")
        berth_location = st.text_input("Berth / Location", key="berth_location")
        latitude = st.text_input("Latitude", key="latitude")
        longitude = st.text_input("Longitude", key="longitude")

    col1, col2 = st.columns(2)
    with col1:
        next_port = st.text_input("Next Port", key="next_port")
        eta_date = st.date_input("ETA Date", datetime.now().date(), key="eta_date")
        eta_time = st.time_input("ETA Time", datetime.now().time(), key="eta_time")
    with col2:
        speed_required = st.number_input("Speed required to achieve Scheduled ETA (kts)", min_value=0.0, step=0.1, key="speed_required")
        best_eta_pbg_lt_date = st.date_input("Best ETA PBG (LT) Date", datetime.now().date(), key="best_eta_pbg_lt_date")
        best_eta_pbg_lt_time = st.time_input("Best ETA PBG (LT) Time", datetime.now().time(), key="best_eta_pbg_lt_time")
        best_eta_pbg_utc_date = st.date_input("Best ETA PBG (UTC) Date", datetime.now().date(), key="best_eta_pbg_utc_date")
        best_eta_pbg_utc_time = st.time_input("Best ETA PBG (UTC) Time", datetime.now().time(), key="best_eta_pbg_utc_time")
        etb_date = st.date_input("ETB Date", datetime.now().date(), key="etb_date")
        etb_time = st.time_input("ETB Time", datetime.now().time(), key="etb_time")
        etcd_date = st.date_input("ETC/D Date", datetime.now().date(), key="etcd_date")
        etcd_time = st.time_input("ETC/D Time", datetime.now().time(), key="etcd_time")
        ballast_laden = st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden")

    st.header("Speed and Consumption")
    col1, col2 = st.columns(2)
    with col1:
        full_speed_hours = st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1, key="full_speed_hours")
        full_speed_nm = st.number_input("Full Speed (nm)", min_value=0.0, step=0.1, key="full_speed_nm")
        reduced_speed_hours = st.number_input("Reduced Speed/Slow Steaming (hrs)", min_value=0.0, step=0.1, key="reduced_speed_hours")
        reduced_speed_nm = st.number_input("Reduced Speed/Slow Steaming (nm)", min_value=0.0, step=0.1, key="reduced_speed_nm")
        stopped_hours = st.number_input("Stopped (hrs)", min_value=0.0, step=0.1, key="stopped_hours")
        stopped_nm = st.number_input("Stopped (nm)", min_value=0.0, step=0.1, key="stopped_nm")
        distance_observed_nm = st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1, key="distance_observed_nm")
    with col2:
        obs_speed_sog = st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1, key="obs_speed_sog")
        em_log_speed_log = st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1, key="em_log_speed_log")
        voyage_average_speed = st.number_input("Voyage Average Speed (kts)", min_value=0.0, step=0.1, key="voyage_average_speed")
        distance_to_go = st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1, key="distance_to_go")
        distance_since_cosp = st.number_input("Distance since COSP (nm)", min_value=0.0, step=0.1, key="distance_since_cosp")
        voyage_order_speed = st.number_input("Voyage Order Speed (kts)", min_value=0.0, step=0.1, key="voyage_order_speed")
        voyage_order_me_fo_cons = st.number_input("Voyage Order ME FO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_fo_cons")
        voyage_order_me_do_cons = st.number_input("Voyage Order ME DO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_do_cons")
        course = st.number_input("Course (°T)", min_value=0.0, step=0.1, key="course")
        draft_f = st.number_input("Draft F (m)", min_value=0.0, step=0.01, key="draft_f")
        draft_a = st.number_input("Draft A (m)", min_value=0.0, step=0.01, key="draft_a")
        displacement = st.number_input("Displacement (mt)", min_value=0.0, step=0.1, key="displacement")

    st.header("Wind and Weather")
    col1, col2 = st.columns(2)
    with col1:
        wind_direction = st.selectbox("Wind Direction", ["North", "North East", "East", "South East", "South", "South West", "West", "North West"], key="wind_direction")
        wind_force = st.number_input("Wind Force", min_value=0.0, step=0.1, key="wind_force")
        visibility = st.number_input("Visibility (nm)", min_value=0.0, step=0.1, key="visibility")
        period_bad_weather = st.number_input("Period of bad Weather (beyond BF scale 5, in Hours)", min_value=0.0, step=0.1, key="period_bad_weather")
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
        in_hra = st.radio("Is vessel currently in Gulf of Aden / HRA or will be Transiting Gulf of Aden / HRA in next 14 days?", ["Yes", "No"], key="in_hra")
    with hra_col2:
        hra_entry_date = st.date_input("Entry into HRA", datetime.now().date(), key="hra_entry_date")
        hra_entry_time = st.time_input("Entry into HRA Time", datetime.now().time(), key="hra_entry_time")
        hra_exit_date = st.date_input("Exit from HRA", datetime.now().date(), key="hra_exit_date")
        hra_exit_time = st.time_input("Exit from HRA Time", datetime.now().time(), key="hra_exit_time")

    st.header("Environmental Control Area")
    eca_col1, eca_col2 = st.columns([1, 3])
    with eca_col1:
        in_eca = st.radio("Is vessel in an ECA area or will enter ECA area within next 3 days?", ["Yes", "No"], key="in_eca")
    with eca_col2:
        eca_entry_date = st.date_input("Entry into ECA", datetime.now().date(), key="eca_entry_date")
        eca_entry_time = st.time_input("Entry into ECA Time", datetime.now().time(), key="eca_entry_time")
        eca_exit_date = st.date_input("Exit from ECA", datetime.now().date(), key="eca_exit_date")
        eca_exit_time = st.time_input("Exit from ECA Time", datetime.now().time(), key="eca_exit_time")
        eca_latitude = st.text_input("Latitude", key="eca_latitude")
        eca_longitude = st.text_input("Longitude", key="eca_longitude")
        fuel_used_in_eca = st.selectbox("Fuel used in ECA", ["HFO", "MDO", "LNG", "Other"], key="fuel_used_in_eca")
        fuel_co_time = st.number_input("Fuel C/O Time (hrs)", min_value=0.0, step=0.1, key="fuel_co_time")

    st.header("Breaching International Navigating Limits")
    iwl_col1, iwl_col2 = st.columns([1, 3])
    with iwl_col1:
        in_iwl = st.radio("Is the vessel in IWL Breach area or will enter IWL Breach area within next 7 days?", ["Yes", "No"], key="in_iwl")
    with iwl_col2:
        iwl_entry_date = st.date_input("Entry into IWL Breach", datetime.now().date(), key="iwl_entry_date")
        iwl_entry_time = st.time_input("Entry into IWL Breach Time", datetime.now().time(), key="iwl_entry_time")
        iwl_exit_date = st.date_input("Exit from IWL Breach", datetime.now().date(), key="iwl_exit_date")
        iwl_exit_time = st.time_input("Exit from IWL Breach Time", datetime.now().time(), key="iwl_exit_time")

    st.header("Drifting")
    drifting_col1, drifting_col2 = st.columns(2)
    with drifting_col1:
        drifting_start_lat = st.text_input("Drifting Start Latitude", key="drifting_start_lat")
        drifting_start_long = st.text_input("Drifting Start Longitude", key="drifting_start_long")
        drifting_start_date = st.date_input("Drifting Start Date", datetime.now().date(), key="drifting_start_date")
        drifting_start_time = st.time_input("Drifting Start Time", datetime.now().time(), key="drifting_start_time")
        drifting_start_distance = st.number_input("Drifting Start Distance (nm)", min_value=0.0, step=0.1, key="drifting_start_distance")
    with drifting_col2:
        drifting_end_lat = st.text_input("Drifting End Latitude", key="drifting_end_lat")
        drifting_end_long = st.text_input("Drifting End Longitude", key="drifting_end_long")
        drifting_end_date = st.date_input("Drifting End Date", datetime.now().date(), key="drifting_end_date")
        drifting_end_time = st.time_input("Drifting End Time", datetime.now().time(), key="drifting_end_time")
        drifting_end_distance = st.number_input("Drifting End Distance (hrs)", min_value=0.0, step=0.1, key="drifting_end_distance")

# Engine Tab
with tabs[1]:
    st.header("Engine Information")

    st.subheader("General")
    col1, col2 = st.columns(2)
    with col1:
        engine_distance = st.number_input("Engine Distance (nm)", min_value=0.0, step=0.1, key="engine_distance")
        er_temp = st.number_input("ER Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="er_temp")
        slip = st.number_input("Slip (%)", min_value=0.0, step=0.1, key="slip")
    with col2:
        avg_slip_cosp = st.number_input("Avg Slip since COSP", min_value=0.0, step=0.1, key="avg_slip_cosp")
        sw_temp = st.number_input("SW Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="sw_temp")

    st.subheader("Auxiliary Engines")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ae1_load = st.number_input("A/E No. 1 Generator Load (kw)", min_value=0.0, step=0.1, key="ae1_load")
        ae1_hours = st.number_input("A/E No. 1 Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae1_hours")
    with col2:
        ae2_load = st.number_input("A/E No. 2 Generator Load (kw)", min_value=0.0, step=0.1, key="ae2_load")
        ae2_hours = st.number_input("A/E No. 2 Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae2_hours")
    with col3:
        ae3_load = st.number_input("A/E No. 3 Generator Load (kw)", min_value=0.0, step=0.1, key="ae3_load")
        ae3_hours = st.number_input("A/E No. 3 Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae3_hours")
    with col4:
        ae4_load = st.number_input("A/E No. 4 Generator Load (kw)", min_value=0.0, step=0.1, key="ae4_load")
        ae4_hours = st.number_input("A/E No. 4 Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae4_hours")

    col1, col2 = st.columns(2)
    with col1:
        shaft_gen_power = st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1, key="shaft_gen_power")
        earth_fault_monitor_440 = st.number_input("Earth Fault Monitor 440 Volts (MΩ)", min_value=0.0, step=0.1, key="earth_fault_monitor_440")
    with col2:
        earth_fault_monitor_230 = st.number_input("Earth Fault Monitor 230/110 Volts (MΩ)", min_value=0.0, step=0.1, key="earth_fault_monitor_230")

    st.subheader("Fresh Water")
    fresh_water_data = {
        "Fresh Water": ["Domestic Fresh Water", "Drinking Water", "Boiler Water", "Tank Cleaning Water"],
        "Previous ROB": [241.0, 0.0, 0.0, 0.0],
        "Produced": [0.0, 0.0, 0.0, 0.0],
        "ROB": [240.0, 0.0, 0.0, 0.0],
        "Consumption": [1.0, 0.0, 0.0, 0.0]
    }
    fresh_water_df = pd.DataFrame(fresh_water_data)
    st.dataframe(fresh_water_df)

    boiler_water_chlorides = st.number_input("Boiler Water Chlorides (ppm)", min_value=0.0, step=0.1, key="boiler_water_chlorides")

    st.subheader("Main Engine")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        me_rev_counter = st.number_input("M/E Rev Counter", min_value=0.0, step=0.1, key="me_rev_counter")
        me_avg_rpm = st.number_input("Average RPM", min_value=0.0, step=0.1, key="me_avg_rpm")
        me_avg_rpm_cosp = st.number_input("Avg RPM since COSP", min_value=0.0, step=0.1, key="me_avg_rpm_cosp")
        me_power_output = st.radio("Power Output", ["BHP", "KW"], key="me_power_output")
        me_power_output_value = st.number_input("Power Output Value", min_value=0.0, step=0.1, key="me_power_output_value")
    with col2:
        me_calculated_bhp = st.number_input("Calculated BHP", min_value=0.0, step=0.1, key="me_calculated_bhp")
        me_avg_power_output = st.number_input("Avg power output", min_value=0.0, step=0.1, key="me_avg_power_output")
        governor_setting = st.number_input("Governor Setting or Fuel rack", min_value=0.0, step=0.1, key="governor_setting")
        speed_setting = st.number_input("Speed Setting", min_value=0.0, step=0.1, key="speed_setting")
    with col3:
        fine_filter_me_fo = st.number_input("ME FO AUTO BACK WASH", min_value=0.0, step=0.1, key="fine_filter_me_fo")
        fine_filter_me_lo = st.number_input("ME LO AUTO BACK WASH", min_value=0.0, step=0.1, key="fine_filter_me_lo")
        no_of_operations_me_fo = st.number_input("No of Operations ME FO", min_value=0.0, step=0.1, key="no_of_operations_me_fo")
        no_of_operations_me_lo = st.number_input("No of Operations ME LO", min_value=0.0, step=0.1, key="no_of_operations_me_lo")
    with col4:
        tco_exh_gas_temp_in = st.number_input("T/C Exh Gas Temp In", min_value=0.0, step=0.1, key="tco_exh_gas_temp_in")
        tco_exh_gas_temp_out = st.number_input("T/C Exh Gas Temp Out", min_value=0.0, step=0.1, key="tco_exh_gas_temp_out")
        bearing_oil_temp_in = st.number_input("Bearing Oil Temp In", min_value=0.0, step=0.1, key="bearing_oil_temp_in")
        bearing_oil_temp_out = st.number_input("Bearing Oil Temp Out", min_value=0.0, step=0.1, key="bearing_oil_temp_out")
        bearing_oil_pressure = st.number_input("Bearing Oil Pressure", min_value=0.0, step=0.1, key="bearing_oil_pressure")
        tc_suction_pressure_drop = st.number_input("TC Suction Pressure drop", min_value=0.0, step=0.1, key="tc_suction_pressure_drop")

    st.subheader("Lube Oil Consumptions (Ltr)")
    lube_oil_data = {
        "Lube Oil": ["ME Cylinder Oil", "ME Cylinder Oil 15 TBN", "ME Cylinder Oil 40 TBN", "ME Cylinder Oil 70 TBN", "ME Cylinder Oil 100 TBN", "ME/MT System Oil", "AE System Oil", "AE System Oil 15TBN", "TG System Oil", "Other Lub Oils"],
        "Prev.ROB": [0.0, 0.0, 24526.0, 0.0, 17500.0, 32000.0, 16800.0, 0.0, 0.0, 0.0],
        "Cons": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Received": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "ROB": [0.0, 0.0, 24526.0, 0.0, 17500.0, 32000.0, 16800.0, 0.0, 0.0, 0.0]
    }
    lube_oil_df = pd.DataFrame(lube_oil_data)
    st.dataframe(lube_oil_df)

    st.subheader("Fuel, Bilge and Sludge")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        fo_cons_rate = st.number_input("FO Cons Rate (mt/day)", min_value=0.0, step=0.1, key="fo_cons_rate")
        do_cons_rate = st.number_input("DO Cons Rate (mt/day)", min_value=0.0, step=0.1, key="do_cons_rate")
        density_15c = st.number_input("Density @ 15°C", min_value=0.0, step=0.1, key="density_15c")
        sulphur_content = st.number_input("Sulphur Content %", min_value=0.0, step=0.01, key="sulphur_content")
    with col2:
        fo_cons_since_cosp = st.number_input("FO Cons since COSP (mt/day)", min_value=0.0, step=0.1, key="fo_cons_since_cosp")
        do_cons_since_cosp = st.number_input("DO Cons since COSP (mt/day)", min_value=0.0, step=0.1, key="do_cons_since_cosp")
        purifier_hfo_pfr1 = st.number_input("HFO PFR 1 Operation Hrs", min_value=0.0, step=0.1, key="purifier_hfo_pfr1")
        purifier_hfo_pfr2 = st.number_input("HFO PFR 2 Operation Hrs", min_value=0.0, step=0.1, key="purifier_hfo_pfr2")
    with col3:
        purifier_do_pfr = st.number_input("DO PFR Operation Hrs", min_value=0.0, step=0.1, key="purifier_do_pfr")
        purifier_me_lo_pfr = st.number_input("ME LO PFR Operation Hrs", min_value=0.0, step=0.1, key="purifier_me_lo_pfr")
        purifier_ae_lo_pfr = st.number_input("AE LO PFR Operation Hrs", min_value=0.0, step=0.1, key="purifier_ae_lo_pfr")
        bilge_tank_rob = st.number_input("Bilge Tank ROB (cu.m)", min_value=0.0, step=0.1, key="bilge_tank_rob")
    with col4:
        sludge_tank_rob = st.number_input("Sludge Tank ROB (cu.m)", min_value=0.0, step=0.1, key="sludge_tank_rob")
        total_sludge_retained = st.number_input("Total Sludge Retained onboard (cu.m)", min_value=0.0, step=0.1, key="total_sludge_retained")
        last_landing_bilge = st.date_input("Last landing of Bilge Water", datetime.now().date(), key="last_landing_bilge")
        days_since_last_bilge = st.number_input("Days since last landing of Bilge Water", min_value=0.0, step=0.1, key="days_since_last_bilge")
        last_landing_sludge = st.date_input("Last landing of Sludge", datetime.now().date(), key="last_landing_sludge")
        days_since_last_sludge = st.number_input("Days since last landing of Sludge", min_value=0.0, step=0.1, key="days_since_last_sludge")

    st.subheader("Chief Engineer Remarks")
    ce_remarks = st.text_area("C.E Remarks", height=100, key="ce_remarks")

if st.button("Submit", key="submit"):
    st.write("Form submitted successfully!")
