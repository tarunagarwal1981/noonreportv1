import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime COSP Report")

def main():
    st.title("Maritime Commencement of Sea Passage (COSP) Report")

    cosp_scenario = st.selectbox("COSP Scenario", [
        "Departing from Port",
        "Departing from Anchorage",
        "Commencing from Drifting",
        "Exiting Canal/River",
        "Departing after STS Operation"
    ])

    tabs = st.tabs(["COSP Information", "Navigation", "Weather", "Engine", "Cargo", "Consumption", "Environmental"])

    with tabs[0]:
        cosp_info_tab(cosp_scenario)

    with tabs[1]:
        navigation_tab(cosp_scenario)

    with tabs[2]:
        weather_tab()

    with tabs[3]:
        engine_tab()

    with tabs[4]:
        cargo_tab()

    with tabs[5]:
        consumption_tab()

    with tabs[6]:
        environmental_tab()

    if st.button("Submit COSP Report", type="primary"):
        st.success("COSP report submitted successfully!")

def cosp_info_tab(cosp_scenario):
    st.header("COSP Information")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Vessel", key="vessel_cosp")
        st.text_input("Voyage No", key="voyage_no_cosp")
        st.text_input("Port/Location of Departure", key="port_location_cosp")
        st.text_input("Latitude", key="latitude_cosp")
        st.text_input("Longitude", key="longitude_cosp")
    with col2:
        st.time_input("Ship Mean Time (UTC)", datetime.now().time(), key="ship_mean_time_utc_cosp")
        st.time_input("Ship Mean Time (LT)", datetime.now().time(), key="ship_mean_time_lt_cosp")
        st.date_input("COSP Date", datetime.now().date(), key="cosp_date")
        st.time_input("COSP Time", datetime.now().time(), key="cosp_time")
    with col3:
        st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden_cosp")
        st.checkbox("Start New Voyage", key="start_new_voyage")
        st.number_input("Off Hire Delay (hrs)", min_value=0.0, step=0.01, key="off_hire_delay")

    st.number_input("Time since SBE (hrs)", min_value=0.0, step=0.1, key="time_since_sbe")
    
    if cosp_scenario == "Departing from Port":
        st.text_input("Name of Berth", key="berth_name")
        st.time_input("Last Line Time", datetime.now().time(), key="last_line_time")
        st.number_input("Total Port Stay (hrs)", min_value=0.0, step=0.1, key="total_port_stay")
    elif cosp_scenario == "Departing from Anchorage":
        st.time_input("Anchor Aweigh Time", datetime.now().time(), key="anchor_aweigh_time")
        st.number_input("Total Anchorage Time (hrs)", min_value=0.0, step=0.1, key="total_anchorage_time")
    elif cosp_scenario == "Commencing from Drifting":
        st.number_input("Total Drifting Time (hrs)", min_value=0.0, step=0.1, key="total_drifting_time")
    elif cosp_scenario == "Exiting Canal/River":
        st.text_input("Canal/River Name", key="canal_river_name")
        st.time_input("Exit Time", datetime.now().time(), key="canal_exit_time")
        st.number_input("Total Transit Time (hrs)", min_value=0.0, step=0.1, key="total_transit_time")
    elif cosp_scenario == "Departing after STS Operation":
        st.text_input("STS Partner Vessel", key="sts_partner_vessel")
        st.time_input("STS Completion Time", datetime.now().time(), key="sts_completion_time")
        st.number_input("Total STS Operation Time (hrs)", min_value=0.0, step=0.1, key="total_sts_time")

    st.text_input("Next Port", key="next_port")
    st.text_input("Next Port Operation", key="next_port_operation")

def navigation_tab(cosp_scenario):
    st.header("Navigation Details")

    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Draft F (m)", min_value=0.0, step=0.01, key="draft_f_cosp")
        st.number_input("Draft A (m)", min_value=0.0, step=0.01, key="draft_a_cosp")
        st.number_input("Distance to Go (nm)", min_value=0.0, step=0.01, key="distance_to_go")
    with col2:
        st.date_input("ETA Date", datetime.now().date(), key="eta_date")
        st.time_input("ETA Time", datetime.now().time(), key="eta_time")
        st.number_input("Estimated Speed (kts)", min_value=0.0, step=0.1, key="estimated_speed")

    st.subheader("Maneuvering Details")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Maneuvering Time (hrs)", min_value=0.0, step=0.1, key="maneuvering_time")
    with col2:
        st.number_input("Maneuvering Distance (nm)", min_value=0.0, step=0.1, key="maneuvering_distance")

    st.subheader("Pilot Information")
    col1, col2 = st.columns(2)
    with col1:
        st.time_input("Pilot on Board Time", datetime.now().time(), key="pilot_on_board_time")
        st.time_input("Pilot off Time", datetime.now().time(), key="pilot_off_time")
    with col2:
        st.text_input("Pilot Name", key="pilot_name")

    st.subheader("Voyage Planning")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.checkbox("Optimum Speed", key="optimum_speed")
        st.checkbox("Optimum Trim", key="optimum_trim")
    with col2:
        st.checkbox("Most Efficient Route", key="most_efficient_route")
        st.checkbox("Cargo Stowage", key="cargo_stowage")
    with col3:
        st.checkbox("Any Cargo tank / Cargo Hold Cleaning", key="any_cargo_tank_cargo_hold_cleaning")
        st.text_input("Charter Standard", key="charter_standard")
    st.text_area("Voyage Plan Remarks", height=100, key="voyage_plan_remarks")

def weather_tab():
    st.header("Weather and Sea Conditions")

    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key="wind_direction")
        st.number_input("Wind Force (Beaufort)", min_value=0, max_value=12, step=1, key="wind_force")
        st.number_input("Sea State (Douglas Scale)", min_value=0, max_value=9, step=1, key="sea_state")
        st.number_input("Swell Height (m)", min_value=0.0, step=0.1, key="swell_height")
    with col2:
        st.selectbox("Swell Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key="swell_direction")
        st.number_input("Air Temperature (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="air_temperature")
        st.number_input("Sea Temperature (°C)", min_value=-2.0, max_value=35.0, step=0.1, key="sea_temperature")
        st.number_input("Visibility (nm)", min_value=0.0, step=0.1, key="visibility")

def engine_tab():
    st.header("Engine Information")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("ME Time Counter at COSP", key="me_time_counter_at_cosp")
        st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1, key="shaft_generator_power")
    with col2:
        st.number_input("ME RPM", min_value=0, step=1, key="me_rpm")
        st.number_input("ME Load (%)", min_value=0.0, max_value=100.0, step=0.1, key="me_load")

    st.subheader("Auxiliary Engines")
    col1, col2 = st.columns(2)
    for i in range(1, 5):
        with col1:
            st.number_input(f"A/E No.{i} Load (%)", min_value=0.0, max_value=100.0, step=0.1, key=f"ae_no{i}_load")
        with col2:
            st.number_input(f"A/E No.{i} Running Hours", min_value=0.0, step=0.1, key=f"ae_no{i}_running_hours")

def cargo_tab():
    st.header("Cargo Information")

    st.number_input("Total Cargo Weight (mt)", min_value=0.0, step=0.1, key="total_cargo_weight")
    st.number_input("Deadweight (mt)", min_value=0.0, step=0.1, key="deadweight")

    cargo_types = st.multiselect("Cargo Types", ["Containers", "Bulk", "Liquid", "Break Bulk", "Ro-Ro"])
    
    for cargo in cargo_types:
        st.number_input(f"{cargo} Cargo Quantity", min_value=0.0, step=0.1, key=f"{cargo.lower()}_quantity")

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
        "Consumption": [0.0] * 13,
        "ROB @ COSP": [0.0] * 13,
        "Sulphur %": [0.0] * 13
    }
    consumption_df = pd.DataFrame(consumption_data)
    st.data_editor(consumption_df, key="consumption_editor", hide_index=True)

    st.subheader("Lube Oil (Ltrs)")
    lube_oil_data = {
        "Lube Oil": ["ME Cylinder Oil", "ME Cylinder Oil 40 TBN", "ME Cylinder Oil 70 TBN", "ME Cylinder Oil 100 TBN", "ME/MT System Oil", "AE System Oil", "AE System Oil 15TBN", "T/O System Oil"],
        "Prev. ROB": [0.0] * 8,
        "Cons": [0.0] * 8,
        "Received": [0.0] * 8,
        "ROB": [0.0] * 8
    }
    lube_oil_df = pd.DataFrame(lube_oil_data)
    st.data_editor(lube_oil_df, key="lube_oil_editor", hide_index=True)

    st.subheader("Fresh Water")
    fresh_water_data = {
        "Fresh Water": ["Domestic Fresh Water", "Drinking Water", "Boiler Water", "Tank Cleaning Water"],
        "Previous ROB": [0.0] * 4,
        "Received": [0.0] * 4,
        "ROB on Dep": [0.0] * 4,
        "Cons": [0.0] * 4
    }
    fresh_water_df = pd.DataFrame(fresh_water_data)
    st.data_editor(fresh_water_df, key="fresh_water_editor", hide_index=True)

def environmental_tab():
    st.header("Environmental Control Area (ECA) Information")

    st.checkbox("Entering ECA", key="entering_eca")
    st.checkbox("Exiting ECA", key="exiting_eca")

    col1, col2 = st.columns(2)
    with col1:
        st.date_input("ECA Entry/Exit Date", datetime.now().date(), key="eca_date")
        st.time_input("ECA Entry/Exit Time", datetime.now().time(), key="eca_time")
    with col2:
        st.text_input("ECA Region", key="eca_region")
        st.text_input("Fuel Used in ECA", key="fuel_used_in_eca")

    st.number_input("Fuel Changeover Time (hrs)", min_value=0.0, step=0.1, key="fuel_changeover_time")
    st.text_area("ECA Compliance Remarks", height=100, key="eca_compliance_remarks")

    st.subheader("Emissions Control")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("CO2 Emissions (tons)", min_value=0.0, step=0.1, key="co2_emissions")
        st.number_input("SOx Emissions (kg)", min_value=0.0, step=0.1, key="sox_emissions")
    with col2:
        st.number_input("NOx Emissions (kg)", min_value=0.0, step=0.1, key="nox_emissions")
        st.number_input("Particulate Matter Emissions (kg)", min_value=0.0, step=0.1, key="pm_emissions")

if __name__ == "__main__":
    main()
