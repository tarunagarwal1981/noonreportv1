import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
st.title("Vessel Departure Report")

# Tabs for different sections
tabs = st.tabs(["General Information", "Operations", "Emissions in Port"])

# General Information Tab
with tabs[0]:
    st.header("Voyage Information - A")
    col1, col2, col3 = st.columns(3)
    with col1:
        vessel = st.text_input("Vessel", key="vessel")
        imo_number = st.text_input("IMO Number", key="imo_number")
        port_of_departure = st.text_input("Port of Departure", key="port_of_departure")
        port_of_departure_unloc = st.text_input("UNLOC", key="port_of_departure_unloc")
        port_of_arrival = st.text_input("Port of Arrival", key="port_of_arrival")
        port_of_arrival_unloc = st.text_input("UNLOC", key="port_of_arrival_unloc")
        drafts_forward = st.number_input("Drafts Forward", min_value=0.0, step=0.01, key="drafts_forward")
        gm = st.number_input("GM", min_value=0.0, step=0.01, key="gm")
        cargo_type = st.text_input("Cargo Type", key="cargo_type")
        cargo_weight = st.number_input("Cargo Weight", min_value=0.0, step=0.01, key="cargo_weight")
    with col2:
        voyage_id = st.text_input("Voyage ID", key="voyage_id")
        date = st.date_input("Date", datetime.now().date(), key="date")
        voyage_leg = st.text_input("Voyage Leg", key="voyage_leg")
        time_zone_departure = st.text_input("Time Zone", key="time_zone_departure")
        time_zone_arrival = st.text_input("Time Zone", key="time_zone_arrival")
        operation_departure = st.text_input("Operation", key="operation_departure")
        operation_arrival = st.text_input("Operation", key="operation_arrival")
        drafts_aft = st.number_input("Drafts Aft", min_value=0.0, step=0.01, key="drafts_aft")
        ballast_weight = st.number_input("Ballast Weight", min_value=0.0, step=0.01, key="ballast_weight")
        bill_of_lading_date = st.date_input("Bill of Lading Date", datetime.now().date(), key="bill_of_lading_date")
        volume = st.number_input("Volume", min_value=0.0, step=0.01, key="volume")
    with col3:
        drafts_mean = st.number_input("Drafts Mean", min_value=0.0, step=0.01, key="drafts_mean")
        displacement = st.number_input("Displacement", min_value=0.0, step=0.01, key="displacement")
        passengers = st.number_input("Passengers", min_value=0.0, step=1, key="passengers")
        cargo_parameters = st.text_area("Cargo Parameters to be Modified as per Ship Type", key="cargo_parameters")

    st.header("Voyage Information - B")
    col1, col2, col3 = st.columns(3)
    with col1:
        sbe_date = st.date_input("SBE Date", datetime.now().date(), key="sbe_date")
        sbe_time_lt = st.time_input("SBE Time (LT)", datetime.now().time(), key="sbe_time_lt")
        sbe_position_terminal = st.text_input("SBE Position / Terminal (Optional)", key="sbe_position_terminal")
        cosp_date = st.date_input("COSP Date", datetime.now().date(), key="cosp_date")
        cosp_time_lt = st.time_input("COSP Time (LT)", datetime.now().time(), key="cosp_time_lt")
        position_latitude = st.text_input("Position Latitude", key="position_latitude")
        position_longitude = st.text_input("Position Longitude", key="position_longitude")
    with col2:
        sbe_time_utc = st.time_input("SBE Time (UTC)", datetime.now().time(), key="sbe_time_utc")
        cosp_time_utc = st.time_input("COSP Time (UTC)", datetime.now().time(), key="cosp_time_utc")
        steaming_time = st.text_input("Steaming Time", key="steaming_time")
        manoeuvring_distance = st.number_input("Manoeuvring Distance", min_value=0.0, step=0.01, key="manoeuvring_distance")
        engine_distance = st.number_input("Engine Distance", min_value=0.0, step=0.01, key="engine_distance")
        sog = st.number_input("SOG", min_value=0.0, step=0.01, key="sog")
        tugs_used = st.selectbox("Tugs Used", ["One", "Two"], key="tugs_used")
    with col3:
        distance_to_next_port = st.number_input("Distance to Next Port (nm)", min_value=0.0, step=0.01, key="distance_to_next_port")
        speed_instruction = st.text_input("Speed Instruction", key="speed_instruction")
        eta_rta_next_port_date = st.date_input("ETA/RTA Next Port Date", datetime.now().date(), key="eta_rta_next_port_date")
        eta_rta_next_port_time_lt = st.time_input("ETA/RTA Next Port Time (LT)", datetime.now().time(), key="eta_rta_next_port_time_lt")
        eta_rta_next_port_time_utc = st.time_input("ETA/RTA Next Port Time (UTC)", datetime.now().time(), key="eta_rta_next_port_time_utc")
        eta_terminal_berth_date = st.date_input("ETA Terminal/Berth Date", datetime.now().date(), key="eta_terminal_berth_date")
        eta_terminal_berth_time_lt = st.time_input("ETA Terminal/Berth Time (LT)", datetime.now().time(), key="eta_terminal_berth_time_lt")
        eta_terminal_berth_time_utc = st.time_input("ETA Terminal/Berth Time (UTC)", datetime.now().time(), key="eta_terminal_berth_time_utc")

    st.header("Weather Observation @COSP")
    col1, col2, col3 = st.columns(3)
    with col1:
        wind_force = st.number_input("Wind Force", min_value=0.0, step=0.01, key="wind_force")
        wind_speed = st.number_input("Wind Speed", min_value=0.0, step=0.01, key="wind_speed")
        wind_direction_true = st.text_input("Wind Direction (True)", key="wind_direction_true")
        wind_direction_relative = st.text_input("Wind Direction (Relative)", key="wind_direction_relative")
    with col2:
        sea_state_code = st.text_input("Sea State Code", key="sea_state_code")
        sea_height = st.number_input("Sea Height", min_value=0.0, step=0.01, key="sea_height")
        sea_direction_true = st.text_input("Sea Direction (True)", key="sea_direction_true")
        sea_direction_relative = st.text_input("Sea Direction (Relative)", key="sea_direction_relative")
    with col3:
        swell_height = st.number_input("Swell Height", min_value=0.0, step=0.01, key="swell_height")
        swell_direction_true = st.text_input("Swell Direction (True)", key="swell_direction_true")
        swell_direction_relative = st.text_input("Swell Direction (Relative)", key="swell_direction_relative")

    st.header("Remarks")
    remarks_general = st.text_area("Remarks", height=100, key="remarks_general")

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
