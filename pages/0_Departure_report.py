import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
st.title("Vessel Departure Report")

# Tabs for different sections
tabs = st.tabs(["General Information", "Operations", "Emissions in Port"])

# General Information Tab
with tabs[0]:
    st.header("General Information")
    # General Information Fields
    col1, col2, col3 = st.columns(3)
    with col1:
        vessel = st.text_input("Vessel")
        voyage_no = st.text_input("Voyage No")
        port = st.text_input("Port")
        next_port = st.text_input("Next Port")
        eta = st.date_input("ETA Date", datetime.now().date())
        eta_time = st.time_input("ETA Time", datetime.now().time())
    with col2:
        berth_location = st.text_input("Name of Berth/Location")
        cosp = st.text_input("COSP")
        ship_mean_time_utc = st.time_input("Ship Mean Time (UTC)", datetime.now().time())
        ship_mean_time_lt = st.time_input("Ship Mean Time (LT)", datetime.now().time())
        me_time_counter_at_cosp = st.text_input("ME Time Counter at COSP")
        shaft_generator_power = st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.01)
    with col3:
        departure_date = st.date_input("Departure Date", datetime.now().date())
        last_port = st.text_input("Last Port")
        next_port_operation = st.text_input("Next Port operation")
        distance_to_go = st.number_input("Distance to Go (nm)", min_value=0.0, step=0.01)
        draft_f = st.number_input("Draft F (m)", min_value=0.0, step=0.01)
        draft_a = st.number_input("Draft A (m)", min_value=0.0, step=0.01)
        start_new_voyage = st.checkbox("Start New Voyage")
        off_hire_delay = st.number_input("Off Hire Delay (hrs)", min_value=0.0, step=0.01)
        maneuvering = st.number_input("Maneuvering (hrs)", min_value=0.0, step=0.01)
        maneuvering_distance = st.number_input("Maneuvering distance (nm)", min_value=0.0, step=0.01)

    st.header("Voyage Planning")
    col1, col2, col3 = st.columns(3)
    with col1:
        optimum_speed = st.checkbox("Optimum Speed")
        optimum_trim = st.checkbox("Optimum Trim")
    with col2:
        most_efficient_route = st.checkbox("Most Efficient Route")
        cargo_stowage = st.checkbox("Cargo Stowage")
    with col3:
        any_cargo_tank_cargo_hold_cleaning = st.checkbox("Any Cargo tank / Cargo Hold Cleaning")
        charter_standard = st.text_input("Charter Standard")
    voyage_plan_remarks = st.text_area("Voyage Plan Remarks", height=100)
    
    st.header("Remarks")
    remarks_general = st.text_area("General Remarks", height=100)
    
    st.header("Services in Port")
    col1, col2, col3 = st.columns(3)
    with col1:
        service_type = st.text_input("Service Type")
        qty = st.number_input("Qty", min_value=0.0, step=0.01)
    with col2:
        unit = st.text_input("Unit")
        est_cost = st.number_input("Est Cost", min_value=0.0, step=0.01)
    with col3:
        currency = st.text_input("Currency")
        service_on = st.text_input("Service On")
    remarks_service = st.text_area("Service Remarks", height=100)
    
    st.header("Lube Oil (Ltrs)")
    st.subheader("Lube Oil")
    lube_oil_data = {
        "Lube Oil": ["ME Cylinder Oil", "ME Cylinder Oil 40 TBN", "ME Cylinder Oil 70 TBN", "ME Cylinder Oil 100 TBN", "ME/MT System Oil", "AE System Oil", "AE System Oil 15TBN", "T/O System Oil"],
        "Prev. ROB": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Cons": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Received": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "ROB": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
    lube_oil_df = pd.DataFrame(lube_oil_data)
    st.dataframe(lube_oil_df)

    st.header("Fresh Water")
    st.subheader("Fresh Water")
    fresh_water_data = {
        "Fresh Water": ["Domestic Fresh Water", "Drinking Water", "Boiler Water", "Tank Cleaning Water"],
        "Previous ROB": [240.0, 0.0, 0.0, 0.0],
        "Received": [0.0, 0.0, 0.0, 0.0],
        "ROB on Dep": [232.0, 0.0, 0.0, 0.0],
        "Cons": [0.0, 0.0, 0.0, 0.0]
    }
    fresh_water_df = pd.DataFrame(fresh_water_data)
    st.dataframe(fresh_water_df)
    
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
        "Previous ROB": [0.0, 0.0, 385.6, 0.0, 0.0, 0.0, 0.0, 571.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "In Port M/E": [0.0, 0.0, 1.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "In Port A/E": [0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "In Port BLR": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "In Port IGG": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "In Port GE/EG": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "In Port OTH": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Bunker Qty": [0.0, 0.0, 568.12, 0.0, 0.0, 0.0, 100.51, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Sulphur %": [0.0, 0.0, 0.48, 0.0, 0.0, 0.0, 0.00, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "ROB @ BDN": [0.0, 0.0, 892.42, 0.0, 0.0, 0.0, 671.51, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "At Harbour M/E": [0.0, 0.0, 15.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "At Harbour A/E": [0.0, 0.0, 5.12, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "At Harbour BLR": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "At Harbour IGG": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "At Harbour GE/EG": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "At Harbour OTH": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "ROB @ COSP": [0.0, 0.0, 871.8, 0.0, 0.0, 0.0, 671.51, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Action": ["", "", "", "", "", "", "", "", "", "", "", "", ""]
    }
    consumption_df = pd.DataFrame(consumption_data)
    st.dataframe(consumption_df)

# Operations Tab
with tabs[1]:
    st.header("Operations")
    
    st.subheader("Cargo Operations")
    col1, col2 = st.columns(2)
    with col1:
        no_cargo_operations = st.checkbox("No Cargo Operations in this port")
        cargo_operation_cargo = st.text_input("Cargo Operations - Cargo")
        cargo_operation_is_critical = st.checkbox("Cargo Operations - Is Critical")
    with col2:
        cargo_operation_qty = st.number_input("Cargo Operations - Qty (MT)", min_value=0.0, step=0.01)
        cargo_operation_vapour_qty = st.number_input("Cargo Operations - Vapour Qty (MT)", min_value=0.0, step=0.01)
        cargo_operation_oil_major_cargo = st.text_input("Cargo Operations - Oil Major Cargo")
        cargo_operation_oil_major = st.text_input("Cargo Operations - Oil Major")
        cargo_operation_basis_final_qty = st.text_input("Cargo Operations - Basis of Final Qty")
        cargo_operation_btb_transfer = st.text_input("Cargo Operations - BTB Transfer Y/N")
    col1, col2 = st.columns(2)
    with col1:
        cargo_operation_commenced_date = st.date_input("Cargo Operations - Commenced Date", datetime.now().date())
        cargo_operation_commenced_time = st.time_input("Cargo Operations - Commenced Time", datetime.now().time())
    with col2:
        cargo_operation_completed_date = st.date_input("Cargo Operations - Completed Date", datetime.now().date())
        cargo_operation_completed_time = st.time_input("Cargo Operations - Completed Time", datetime.now().time())
    cargo_operation_action = st.text_input("Cargo Operations - Action")
    
    st.subheader("Ballasting / Deballasting")
    col1, col2 = st.columns(2)
    with col1:
        ballasting_commenced_date = st.date_input("Ballasting - Commenced Date", datetime.now().date())
        ballasting_commenced_time = st.time_input("Ballasting - Commenced Time", datetime.now().time())
    with col2:
        ballasting_completed_date = st.date_input("Ballasting - Completed Date", datetime.now().date())
        ballasting_completed_time = st.time_input("Ballasting - Completed Time", datetime.now().time())
        ballasting_quantity = st.number_input("Ballasting - Quantity (MT)", min_value=0.0, step=0.01)
    col1, col2 = st.columns(2)
    with col1:
        deballasting_commenced_date = st.date_input("Deballasting - Commenced Date", datetime.now().date())
        deballasting_commenced_time = st.time_input("Deballasting - Commenced Time", datetime.now().time())
    with col2:
        deballasting_completed_date = st.date_input("Deballasting - Completed Date", datetime.now().date())
        deballasting_completed_time = st.time_input("Deballasting - Completed Time", datetime.now().time())
        deballasting_quantity = st.number_input("Deballasting - Quantity (MT)", min_value=0.0, step=0.01)
    
    st.subheader("Tank Cleaning")
    col1, col2 = st.columns(2)
    with col1:
        hold_tank_cleaning = st.checkbox("Tank Cleaning - Hold / Tank Cleaning")
        hold_tank_cleaning_commenced_date = st.date_input("Tank Cleaning - Commenced Date", datetime.now().date())
        hold_tank_cleaning_commenced_time = st.time_input("Tank Cleaning - Commenced Time", datetime.now().time())
    with col2:
        hold_tank_cleaning_completed_date = st.date_input("Tank Cleaning - Completed Date", datetime.now().date())
        hold_tank_cleaning_completed_time = st.time_input("Tank Cleaning - Completed Time", datetime.now().time())
        stripping_draining = st.checkbox("Tank Cleaning - Stripping / Draining")
    stripping_draining_remarks = st.text_area("Tank Cleaning - Stripping / Draining Remarks", height=100)
    
    st.subheader("Other Operations")
    col1, col2 = st.columns(2)
    with col1:
        other_operations_description = st.text_area("Other Operations - Description", height=100)
    with col2:
        other_operations_commenced_date = st.date_input("Other Operations - Commenced Date", datetime.now().date())
        other_operations_commenced_time = st.time_input("Other Operations - Commenced Time", datetime.now().time())
        other_operations_completed_date = st.date_input("Other Operations - Completed Date", datetime.now().date())
        other_operations_completed_time = st.time_input("Other Operations - Completed Time", datetime.now().time())
        other_operations_action = st.text_input("Other Operations - Action")

# Emissions in Port Tab
with tabs[2]:
    st.header("Emissions in Port")
    col1, col2 = st.columns(2)
    with col1:
        vessel_name = st.text_input("Emissions - Vessel Name")
        voyage_no_emission = st.text_input("Emissions - Voyage No")
        port_emission = st.text_input("Emissions - Port")
        ballast_laden_emission = st.checkbox("Emissions - Ballast/Laden")
        eu_port = st.checkbox("Emissions - EU Port")
    with col2:
        arrival_date = st.date_input("Emissions - Arrival Date", datetime.now().date())
        arrival_time = st.time_input("Emissions - Arrival Time", datetime.now().time())
        departure_date = st.date_input("Emissions - Departure Date", datetime.now().date())
        departure_time = st.time_input("Emissions - Departure Time", datetime.now().time())
    
    col1, col2 = st.columns(2)
    with col1:
        total_time_in_port = st.number_input("Emissions - Total Time in Port (hrs)", min_value=0.0, step=0.01)
        total_aggregated_co2_emitted = st.number_input("Emissions - Total Aggregated CO2 Emitted (T CO2)", min_value=0.0, step=0.01)
    with col2:
        fuel_type = st.text_input("Emissions - Fuel Type")
        emission_factor = st.number_input("Emissions - Emission Factor", min_value=0.0, step=0.01)
        rob_at_fwe = st.number_input("Emissions - ROB @ FWE", min_value=0.0, step=0.01)
        bunkered = st.number_input("Emissions - Bunkered", min_value=0.0, step=0.01)
        rob_at_swe = st.number_input("Emissions - ROB @ SWE", min_value=0.0, step=0.01)
        total_fo_cons = st.number_input("Emissions - Total FO Cons", min_value=0.0, step=0.01)
        cargo_heating_cons = st.number_input("Emissions - Cargo Heating Cons", min_value=0.0, step=0.01)
        aggregated_co2_emitted = st.number_input("Emissions - Aggregated CO2 Emitted (MT CO2)", min_value=0.0, step=0.01)

if st.button("Submit"):
    st.write("Form submitted successfully!")
