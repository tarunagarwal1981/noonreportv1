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
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        vessel = st.text_input("Vessel", key="vessel")
        voyage_no = st.text_input("Voyage No", key="voyage_no")
        port = st.text_input("Port", key="port")
        berth_location = st.text_input("Name of Berth/Location", key="berth_location")
        latitude = st.text_input("Latitude", key="latitude")
        longitude = st.text_input("Longitude", key="longitude")
        ship_mean_time_utc = st.time_input("Ship Mean Time (UTC)", datetime.now().time(), key="ship_mean_time_utc")
        ship_mean_time_lt = st.time_input("Ship Mean Time (LT)", datetime.now().time(), key="ship_mean_time_lt")
    with col2:
        cosp = st.text_input("COSP", key="cosp")
        departure_date = st.date_input("Departure Date", datetime.now().date(), key="departure_date")
        pilot_on_board_pob_lt = st.time_input("Pilot on Board (POB) LT", datetime.now().time(), key="pilot_on_board_pob_lt")
        pilot_on_board_pob_utc = st.time_input("Pilot on Board (POB) UTC", datetime.now().time(), key="pilot_on_board_pob_utc")
        standby_engines_sbe_lt = st.time_input("Standby Engines (SBE) LT", datetime.now().time(), key="standby_engines_sbe_lt")
        standby_engines_sbe_utc = st.time_input("Standby Engines (SBE) UTC", datetime.now().time(), key="standby_engines_sbe_utc")
        all_gone_and_clear_llc_lt = st.time_input("All Gone and Clear (LLC) LT", datetime.now().time(), key="all_gone_and_clear_llc_lt")
        all_gone_and_clear_llc_utc = st.time_input("All Gone and Clear (LLC) UTC", datetime.now().time(), key="all_gone_and_clear_llc_utc")
        anchor_aweigh_aaw_lt = st.time_input("Anchor Aweigh (AAW) LT", datetime.now().time(), key="anchor_aweigh_aaw_lt")
        anchor_aweigh_aaw_utc = st.time_input("Anchor Aweigh (AAW) UTC", datetime.now().time(), key="anchor_aweigh_aaw_utc")
    with col3:
        dropping_of_last_outward_sea_pilot_dlosp_lt = st.time_input("Dropping of Last Outward Sea Pilot (DLOSP) LT", datetime.now().time(), key="dropping_of_last_outward_sea_pilot_dlosp_lt")
        dropping_of_last_outward_sea_pilot_dlosp_utc = st.time_input("Dropping of Last Outward Sea Pilot (DLOSP) UTC", datetime.now().time(), key="dropping_of_last_outward_sea_pilot_dlosp_utc")
        ring_full_away_rfa_lt = st.time_input("Ring Full Away (RFA) LT", datetime.now().time(), key="ring_full_away_rfa_lt")
        ring_full_away_rfa_utc = st.time_input("Ring Full Away (RFA) UTC", datetime.now().time(), key="ring_full_away_rfa_utc")
        commencement_of_sea_passage_cosp_lt = st.time_input("Commencement of Sea Passage (COSP) LT", datetime.now().time(), key="commencement_of_sea_passage_cosp_lt")
        commencement_of_sea_passage_cosp_utc = st.time_input("Commencement of Sea Passage (COSP) UTC", datetime.now().time(), key="commencement_of_sea_passage_cosp_utc")
        ballast_laden = st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden")
        draft_f = st.number_input("Draft F (m)", min_value=0.0, step=0.01, key="draft_f")
        draft_a = st.number_input("Draft A (m)", min_value=0.0, step=0.01, key="draft_a")

    st.header("Voyage Planning")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        optimum_speed = st.checkbox("Optimum Speed", key="optimum_speed")
        optimum_trim = st.checkbox("Optimum Trim", key="optimum_trim")
    with col2:
        most_efficient_route = st.checkbox("Most Efficient Route", key="most_efficient_route")
        cargo_stowage = st.checkbox("Cargo Stowage", key="cargo_stowage")
    with col3:
        any_cargo_tank_cargo_hold_cleaning = st.checkbox("Any Cargo tank / Cargo Hold Cleaning", key="any_cargo_tank_cargo_hold_cleaning")
        charter_standard = st.text_input("Charter Standard", key="charter_standard")
    voyage_plan_remarks = st.text_area("Voyage Plan Remarks", height=100, key="voyage_plan_remarks")
    
    st.header("Remarks")
    remarks_general = st.text_area("General Remarks", height=100, key="remarks_general")
    
    st.header("Services in Port")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        service_type = st.text_input("Service Type", key="service_type")
        qty = st.number_input("Qty", min_value=0.0, step=0.01, key="qty")
    with col2:
        unit = st.text_input("Unit", key="unit")
        est_cost = st.number_input("Est Cost", min_value=0.0, step=0.01, key="est_cost")
    with col3:
        currency = st.text_input("Currency", key="currency")
        service_on = st.text_input("Service On", key="service_on")
    remarks_service = st.text_area("Service Remarks", height=100, key="remarks_service")
    
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
        "Sulphur %": [0.0, 0.0, 0.48, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
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
        no_cargo_operations = st.checkbox("No Cargo Operations in this port", key="no_cargo_operations")
        cargo_operation_cargo = st.text_input("Cargo Operations - Cargo", key="cargo_operation_cargo")
        cargo_operation_is_critical = st.checkbox("Cargo Operations - Is Critical", key="cargo_operation_is_critical")
    with col2:
        cargo_operation_qty = st.number_input("Cargo Operations - Qty (MT)", min_value=0.0, step=0.01, key="cargo_operation_qty")
        cargo_operation_vapour_qty = st.number_input("Cargo Operations - Vapour Qty (MT)", min_value=0.0, step=0.01, key="cargo_operation_vapour_qty")
        cargo_operation_oil_major_cargo = st.text_input("Cargo Operations - Oil Major Cargo", key="cargo_operation_oil_major_cargo")
        cargo_operation_oil_major = st.text_input("Cargo Operations - Oil Major", key="cargo_operation_oil_major")
        cargo_operation_basis_final_qty = st.text_input("Cargo Operations - Basis of Final Qty", key="cargo_operation_basis_final_qty")
        cargo_operation_btb_transfer = st.text_input("Cargo Operations - BTB Transfer Y/N", key="cargo_operation_btb_transfer")
    col1, col2 = st.columns(2)
    with col1:
        cargo_operation_commenced_date = st.date_input("Cargo Operations - Commenced Date", datetime.now().date(), key="cargo_operation_commenced_date")
        cargo_operation_commenced_time = st.time_input("Cargo Operations - Commenced Time", datetime.now().time(), key="cargo_operation_commenced_time")
    with col2:
        cargo_operation_completed_date = st.date_input("Cargo Operations - Completed Date", datetime.now().date(), key="cargo_operation_completed_date")
        cargo_operation_completed_time = st.time_input("Cargo Operations - Completed Time", datetime.now().time(), key="cargo_operation_completed_time")
    cargo_operation_action = st.text_input("Cargo Operations - Action", key="cargo_operation_action")
    
    st.subheader("Ballasting / Deballasting")
    col1, col2 = st.columns(2)
    with col1:
        ballasting_commenced_date = st.date_input("Ballasting - Commenced Date", datetime.now().date(), key="ballasting_commenced_date")
        ballasting_commenced_time = st.time_input("Ballasting - Commenced Time", datetime.now().time(), key="ballasting_commenced_time")
    with col2:
        ballasting_completed_date = st.date_input("Ballasting - Completed Date", datetime.now().date(), key="ballasting_completed_date")
        ballasting_completed_time = st.time_input("Ballasting - Completed Time", datetime.now().time(), key="ballasting_completed_time")
        ballasting_quantity = st.number_input("Ballasting - Quantity (MT)", min_value=0.0, step=0.01, key="ballasting_quantity")
    col1, col2 = st.columns(2)
    with col1:
        deballasting_commenced_date = st.date_input("Deballasting - Commenced Date", datetime.now().date(), key="deballasting_commenced_date")
        deballasting_commenced_time = st.time_input("Deballasting - Commenced Time", datetime.now().time(), key="deballasting_commenced_time")
    with col2:
        deballasting_completed_date = st.date_input("Deballasting - Completed Date", datetime.now().date(), key="deballasting_completed_date")
        deballasting_completed_time = st.time_input("Deballasting - Completed Time", datetime.now().time(), key="deballasting_completed_time")
        deballasting_quantity = st.number_input("Deballasting - Quantity (MT)", min_value=0.0, step=0.01, key="deballasting_quantity")
    
    st.subheader("Tank Cleaning")
    col1, col2 = st.columns(2)
    with col1:
        hold_tank_cleaning = st.checkbox("Tank Cleaning - Hold / Tank Cleaning", key="hold_tank_cleaning")
        hold_tank_cleaning_commenced_date = st.date_input("Tank Cleaning - Commenced Date", datetime.now().date(), key="hold_tank_cleaning_commenced_date")
        hold_tank_cleaning_commenced_time = st.time_input("Tank Cleaning - Commenced Time", datetime.now().time(), key="hold_tank_cleaning_commenced_time")
    with col2:
        hold_tank_cleaning_completed_date = st.date_input("Tank Cleaning - Completed Date", datetime.now().date(), key="hold_tank_cleaning_completed_date")
        hold_tank_cleaning_completed_time = st.time_input("Tank Cleaning - Completed Time", datetime.now().time(), key="hold_tank_cleaning_completed_time")
        stripping_draining = st.checkbox("Tank Cleaning - Stripping / Draining", key="stripping_draining")
    stripping_draining_remarks = st.text_area("Tank Cleaning - Stripping / Draining Remarks", height=100, key="stripping_draining_remarks")
    
    st.subheader("Other Operations")
    col1, col2 = st.columns(2)
    with col1:
        other_operations_description = st.text_area("Other Operations - Description", height=100, key="other_operations_description")
    with col2:
        other_operations_commenced_date = st.date_input("Other Operations - Commenced Date", datetime.now().date(), key="other_operations_commenced_date")
        other_operations_commenced_time = st.time_input("Other Operations - Commenced Time", datetime.now().time(), key="other_operations_commenced_time")
        other_operations_completed_date = st.date_input("Other Operations - Completed Date", datetime.now().date(), key="other_operations_completed_date")
        other_operations_completed_time = st.time_input("Other Operations - Completed Time", datetime.now().time(), key="other_operations_completed_time")
        other_operations_action = st.text_input("Other Operations - Action", key="other_operations_action")

# Emissions in Port Tab
with tabs[2]:
    st.header("Emissions in Port")
    
    st.subheader("General Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        vessel_name = st.text_input("Vessel Name", key="vessel_name_emission")
        voyage_no_emission = st.text_input("Voyage No", key="voyage_no_emission")
        port_emission = st.text_input("Port", key="port_emission")
    with col2:
        ballast_laden_emission = st.checkbox("Ballast", key="ballast_laden_emission")
        eu_port = st.checkbox("EU Port", key="eu_port")
    with col3:
        arrival_date = st.date_input("Arrival Date", datetime.now().date(), key="arrival_date_emission")
        arrival_time = st.time_input("Arrival Time", datetime.now().time(), key="arrival_time_emission")
        departure_date = st.date_input("Departure Date", datetime.now().date(), key="departure_date_emission")
        departure_time = st.time_input("Departure Time", datetime.now().time(), key="departure_time_emission")
        total_time_in_port = st.number_input("Total Time in Port (hrs)", min_value=0.0, step=0.01, key="total_time_in_port_emission")
        total_aggregated_co2_emitted = st.number_input("Total Aggregated CO2 Emitted (T CO2)", min_value=0.0, step=0.01, key="total_aggregated_co2_emitted")
    
    st.subheader("Consumption (MT)")
    consumption_emissions_data = {
        "Fuel Type": [
            "LNG", "Propane LPG", "Butane LPG",
            "HFO", "Other Fuel", "LFO", "MDO/MGO"
        ],
        "Emission Factor": [2.750, 3.000, 3.300, 3.114, 3.115, 3.151, 3.206],
        "ROB @ FWE": [0.0, 0.0, 0.0, 508.12, 0.0, 0.0, 100.61],
        "Bunkered": [0.0, 0.0, 0.0, 385.80, 0.0, 0.0, 571.00],
        "ROB @ BBE": [0.0, 0.0, 0.0, 892.42, 0.0, 0.0, 671.51],
        "Total FO Cons": [0.0, 0.0, 0.0, 892.42, 0.0, 0.0, 671.51],
        "Cargo Heating Cons": [0.0, 0.0, 0.0, 1.60, 0.0, 0.0, 0.0],
        "Aggregated CO2 Emitted (MT CO2)": [0.0, 0.0, 0.0, 4.67, 0.0, 0.0, 0.0]
    }
    consumption_emissions_df = pd.DataFrame(consumption_emissions_data)
    st.dataframe(consumption_emissions_df)

if st.button("Submit", key="submit"):
    st.write("Form submitted successfully!")
