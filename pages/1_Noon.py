import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime Noon Report")

def main():
    st.title("Maritime Noon Report")

    report_type = st.selectbox(
        "Select Noon Report Type",
        ["Noon at Sea", "Noon at Port", "Noon at Anchor", "Noon at Drifting", "Noon at STS", "Noon at Canal/River Passage"],
        index=0
    )

    if report_type in ["Noon at Sea", "Noon at Drifting", "Noon at Canal/River Passage"]:
        noon_at_sea_report(report_type)
    else:
        noon_other_report(report_type)

def noon_at_sea_report(report_type):
    st.header(f"{report_type} Report")
    
    general_information(report_type)
    voyage_details(report_type)
    speed_position_navigation(report_type)
    weather_conditions(report_type)
    cargo_stability(report_type)
    fuel_consumption(report_type)
    fuel_allocation(report_type)
    machinery(report_type)
    environmental_compliance(report_type)
    miscellaneous_consumables(report_type)

    if st.button(f"Submit {report_type} Report", type="primary"):
        st.success(f"{report_type} Report submitted successfully!")

def noon_other_report(report_type):
    st.header(f"{report_type} Report")
    
    general_information(report_type)
    voyage_details_other(report_type)
    position_navigation_other(report_type)
    weather_conditions(report_type)
    cargo_stability(report_type)
    fuel_consumption_other(report_type)
    fuel_allocation(report_type)
    machinery_other(report_type)
    environmental_compliance_other(report_type)
    miscellaneous_consumables(report_type)

    if st.button(f"Submit {report_type} Report", type="primary"):
        st.success(f"{report_type} Report submitted successfully!")

def general_information(report_type):
    with st.expander("General Information", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Vessel Name", key=f"vessel_name_{report_type}")
            st.text_input("Voyage No", key=f"voyage_no_{report_type}")
            st.text_input("Last Port", key=f"last_port_{report_type}")
        with col2:
            st.date_input("Report Date (LT)", datetime.now(), key=f"report_date_lt_{report_type}")
            st.time_input("Report Time (LT)", datetime.now().time(), key=f"report_time_lt_{report_type}")
            st.date_input("Report Date (UTC)", datetime.now(), key=f"report_date_utc_{report_type}")
            st.time_input("Report Time (UTC)", datetime.now().time(), key=f"report_time_utc_{report_type}")
        with col3:
            st.text_input("Ship Mean Time", value="UTC", key=f"ship_mean_time_{report_type}")
            st.number_input("Offset", min_value=-12, max_value=12, step=1, key=f"offset_{report_type}")
            st.checkbox("IDL Crossing", key=f"idl_crossing_{report_type}")
            st.selectbox("IDL Direction", ["--Select--", "East", "West"], key=f"idl_direction_{report_type}")

def voyage_details(report_type):
    with st.expander("Voyage Details", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Voyage From", key=f"voyage_from_{report_type}")
            st.text_input("Voyage To", key=f"voyage_to_{report_type}")
            st.selectbox("Voyage Stage", ["", "East", "West", "Ballast", "Laden"], key=f"voyage_stage_{report_type}")
        with col2:
            st.text_input("Speed Order", key=f"speed_order_{report_type}")
            st.text_input("ETA", key=f"eta_{report_type}")
            st.radio("Ballast/Laden", ["Ballast", "Laden"], key=f"ballast_laden_{report_type}")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.checkbox("Off-hire", key=f"off_hire_{report_type}")
        with col2:
            st.checkbox("ECA Transit", key=f"eca_transit_{report_type}")
        with col3:
            st.checkbox("Fuel Changeover", key=f"fuel_changeover_{report_type}")
        with col4:
            st.checkbox("Deviation", key=f"deviation_{report_type}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Ice Navigation", key=f"ice_navigation_{report_type}")
        with col2:
            st.checkbox("IDL Crossing", key=f"idl_crossing_voyage_{report_type}")
        
        st.checkbox("Transiting Special Area", key=f"transiting_special_area_{report_type}")

def voyage_details_other(report_type):
    with st.expander("Voyage Details", expanded=False):
        st.text_input("Port Name", key=f"port_name_{report_type}")
        st.radio("Ballast/Laden", ["Ballast", "Laden"], key=f"ballast_laden_{report_type}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.checkbox("Off-hire", key=f"off_hire_{report_type}")
        with col2:
            st.checkbox("ECA Transit", key=f"eca_transit_{report_type}")
        with col3:
            st.checkbox("Fuel Changeover", key=f"fuel_changeover_{report_type}")

def speed_position_navigation(report_type):
    with st.expander("Speed, Position and Navigation", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1, key=f"full_speed_{report_type}")
            st.number_input("Reduced Speed (hrs)", min_value=0.0, step=0.1, key=f"reduced_speed_{report_type}")
            st.number_input("Stopped (hrs)", min_value=0.0, step=0.1, key=f"stopped_{report_type}")
            st.text_input("Latitude", key=f"latitude_{report_type}")
            st.text_input("Longitude", key=f"longitude_{report_type}")
        with col2:
            st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1, key=f"distance_observed_{report_type}")
            st.number_input("Distance Through Water (nm)", min_value=0.0, step=0.1, key=f"distance_through_water_{report_type}")
            st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1, key=f"obs_speed_{report_type}")
            st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1, key=f"em_log_speed_{report_type}")
        with col3:
            st.number_input("Course (°)", min_value=0.0, max_value=360.0, step=1.0, key=f"course_{report_type}")
            st.number_input("Heading (°)", min_value=0.0, max_value=360.0, step=1.0, key=f"heading_{report_type}")

def position_navigation_other(report_type):
    with st.expander("Position and Navigation", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Latitude", key=f"latitude_{report_type}")
            st.text_input("Longitude", key=f"longitude_{report_type}")
        with col2:
            st.number_input("True Heading (°)", min_value=0.0, max_value=360.0, step=1.0, key=f"true_heading_{report_type}")

def weather_conditions(report_type):
    with st.expander("Weather and Conditions", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=f"wind_direction_{report_type}")
            st.number_input("Wind Force (Beaufort)", min_value=0, max_value=12, key=f"wind_force_{report_type}")
            st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key=f"sea_height_{report_type}")
            st.selectbox("Sea Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=f"sea_direction_{report_type}")
        with col2:
            st.number_input("Swell Height (m)", min_value=0.0, step=0.1, key=f"swell_height_{report_type}")
            st.selectbox("Swell Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=f"swell_direction_{report_type}")
            st.number_input("Current Speed (kts)", min_value=0.0, step=0.1, key=f"current_speed_{report_type}")
            st.selectbox("Current Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=f"current_direction_{report_type}")
            st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key=f"air_temp_{report_type}")
            st.number_input("Sea Temp (°C)", min_value=-2.0, max_value=35.0, step=0.1, key=f"sea_temp_{report_type}")

        st.number_input("Visibility (nm)", min_value=0.0, step=0.1, key=f"visibility_{report_type}")
        st.checkbox("Icing on Deck?", key=f"icing_on_deck_{report_type}")

def cargo_stability(report_type):
    with st.expander("Cargo and Stability", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Draft F (m)", min_value=0.0, step=0.01, key=f"draft_f_{report_type}")
            st.number_input("Draft A (m)", min_value=0.0, step=0.01, key=f"draft_a_{report_type}")
            st.number_input("Draft M (m)", min_value=0.0, step=0.01, key=f"draft_m_{report_type}")
        with col2:
            st.number_input("Displacement (MT)", min_value=0.0, step=0.1, key=f"displacement_{report_type}")
            st.number_input("Deadweight (MT)", min_value=0.0, step=0.1, key=f"deadweight_{report_type}")
        with col3:
            st.number_input("GM (m)", min_value=0.0, step=0.01, key=f"gm_{report_type}")
            st.number_input("Trim (m)", min_value=-10.0, max_value=10.0, step=0.01, key=f"trim_{report_type}")

def fuel_consumption(report_type):
    with st.expander("Fuel Consumption", expanded=False):
        consumption_data = {
            "Fuel Type": ["HFO", "LSFO", "MGO", "LNG"],
            "Previous ROB": [0.0] * 4,
            "Consumption (At Sea)": [0.0] * 4,
            "ROB": [0.0] * 4
        }
        consumption_df = pd.DataFrame(consumption_data)
        st.data_editor(consumption_df, key=f"consumption_editor_{report_type}", hide_index=True)

def fuel_consumption_other(report_type):
    with st.expander("Fuel Consumption", expanded=False):
        consumption_data = {
            "Fuel Type": ["HFO", "LSFO", "MGO", "LNG"],
            "Previous ROB": [0.0] * 4,
            "Consumption (In Port)": [0.0] * 4,
            "ROB": [0.0] * 4
        }
        consumption_df = pd.DataFrame(consumption_data)
        st.data_editor(consumption_df, key=f"consumption_editor_{report_type}", hide_index=True)

def fuel_allocation(report_type):
    with st.expander("Fuel Allocation", expanded=False):
        allocation_data = {
            "Fuel Type": ["HFO", "LSFO", "MGO", "LNG"],
            "Main Engine": [0.0] * 4,
            "Auxiliary Engine": [0.0] * 4,
            "Boilers": [0.0] * 4,
            "Others": [0.0] * 4
        }
        allocation_df = pd.DataFrame(allocation_data)
        st.data_editor(allocation_df, key=f"allocation_editor_{report_type}", hide_index=True)

def machinery(report_type):
    with st.expander("Machinery", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("ME Rev Counter", min_value=0, step=1, key=f"me_rev_counter_{report_type}")
            st.number_input("Average RPM", min_value=0.0, step=0.1, key=f"average_rpm_{report_type}")
            st.radio("Power Output", ["BHP", "KW"], key=f"power_output_{report_type}")
            st.number_input("Calculated Power", min_value=0, step=1, key=f"calculated_power_{report_type}")
        with col2:
            st.number_input("Governor Setting (%)", min_value=0.0, max_value=100.0, step=0.1, key=f"governor_setting_{report_type}")
            st.number_input("Scav Air Temp (°C)", min_value=0.0, step=0.1, key=f"scav_air_temp_{report_type}")
            st.number_input("Scav Air Press (bar)", min_value=0.0, step=0.1, key=f"scav_air_press_{report_type}")
        with col3:
            st.number_input("FO Inlet Temp (°C)", min_value=0.0, step=0.1, key=f"fo_inlet_temp_{report_type}")
            st.number_input("FO Press (bar)", min_value=0.0, step=0.1, key=f"fo_press_{report_type}")
            st.number_input("Exh Temp Avg (°C)", min_value=0.0, step=0.1, key=f"exh_temp_avg_{report_type}")

        st.subheader("Auxiliary Engines")
        col1, col2 = st.columns(2)
        for i in range(1, 5):
            with col1:
                st.number_input(f"A/E No.{i} Generator Load (kw)", min_value=0, step=1, key=f"ae_no{i}_load_{report_type}")
            with col2:
                st.number_input(f"A/E No.{i} Running Hours", min_value=0.0, step=0.1, key=f"ae_no{i}_hours_{report_type}")
        st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1, key=f"shaft_gen_power_{report_type}")

def machinery_other(report_type):
    with st.expander("Machinery", expanded=False):
        st.number_input("ME Rev Counter", min_value=0, step=1, key=f"me_rev_counter_{report_type}")

        st.subheader("Auxiliary Engines")
        col1, col2 = st.columns(2)
        for i in range(1, 5):
            with col1:
                st.number_input(f"A/E No.{i} Generator Load (kw)", min_value=0, step=1, key=f"ae_no{i}_load_{report_type}")
            with col2:
                st.number_input(f"A/E No.{i} Running Hours", min_value=0.0, step=0.1, key=f"ae_no{i}_hours_{report_type}")
        st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1, key=f"shaft_gen_power_{report_type}")

def environmental_compliance(report_type):
    with st.expander("Environmental Compliance", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1, key=f"sludge_rob_{report_type}")
            st.number_input("Sludge Burnt in Incinerator (MT)", min_value=0.0, step=0.1, key=f"sludge_burnt_{report_type}")
            st.number_input("Sludge Landed Ashore (MT)", min_value=0.0, step=0.1, key=f"sludge_landed_{report_type}")
        with col2:
            st.number_input("Bilge Water Quantity (m³)", min_value=0.0, step=0.1, key=f"bilge_water_qty_{report_type}")
            st.number_input("Bilge Water Pumped Out through 15ppm Equipment (m³)", min_value=0.0, step=0.1, key=f"bilge_pumped_out_{report_type}")
            st.number_input("Bilge Water Landed Ashore (m³)", min_value=0.0, step=0.1, key=f"bilge_landed_{report_type}")

def environmental_compliance_other(report_type):
    with st.expander("Environmental Compliance", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1, key=f"sludge_rob_{report_type}")
            st.number_input("Sludge Landed Ashore (MT)", min_value=0.0, step=0.1, key=f"sludge_landed_{report_type}")
        with col2:
            st.number_input("Bilge Water Quantity (m³)", min_value=0.0, step=0.1, key=f"bilge_water_qty_{report_type}")
            st.number_input("Bilge Water Landed Ashore (m³)", min_value=0.0, step=0.1, key=f"bilge_landed_{report_type}")

def miscellaneous_consumables(report_type):
    with st.expander("Miscellaneous Consumables", expanded=False):
        st.subheader("Fresh Water")
        fresh_water_data = {
            "Fresh Water": ["Domestic Fresh Water", "Drinking Water", "Boiler Water", "Tank Cleaning Water"],
            "Previous ROB": [0.0] * 4,
            "Produced": [0.0] * 4,
            "ROB": [0.0] * 4,
            "Consumption": [0.0] * 4
        }
        fresh_water_df = pd.DataFrame(fresh_water_data)
        st.data_editor(fresh_water_df, key=f"fresh_water_editor_{report_type}", hide_index=True)

        st.subheader("Lubricating Oil")
        lube_oil_data = {
            "Lube Oil": ["ME Cylinder Oil", "ME System Oil", "AE System Oil"],
            "Previous ROB": [0.0] * 3,
            "Consumption": [0.0] * 3,
            "ROB": [0.0] * 3
        }
        lube_oil_df = pd.DataFrame(lube_oil_data)
        st.data_editor(lube_oil_df, key=f"lube_oil_editor_{report_type}", hide_index=True)

if __name__ == "__main__":
    main()
