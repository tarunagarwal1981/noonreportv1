import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime SBE Report")

def main():
    st.title("Maritime Departure (SBE) Report")

    sbe_scenario = st.selectbox("Departure Scenario", [
        "Departure Anchorage",
        "Departure Port",
        "Departure STS",
        "Departure for River/Canal Transit",
        "Departure from Drifting position",
        "Preparing for Berth Shifting"
    ])

    tabs = st.tabs(["SBE Information", "Navigation", "Engine", "Cargo Operations", "Bunkers"])

    with tabs[0]:
        sbe_info_tab(sbe_scenario)

    with tabs[1]:
        navigation_tab(sbe_scenario)

    with tabs[2]:
        engine_tab()

    with tabs[3]:
        cargo_operations_tab(sbe_scenario)

    with tabs[4]:
        bunkers_tab()

    if st.button("Submit SBE Report", type="primary"):
        st.success("SBE report submitted successfully!")

def sbe_info_tab(sbe_scenario):
    st.header("SBE Information")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Vessel", key="vessel_sbe")
        st.text_input("Voyage No", key="voyage_no_sbe")
        st.text_input("Port/Location", key="port_location_sbe")
        st.text_input("Name of Berth/Anchorage", key="berth_location_sbe")
        st.text_input("Latitude", key="latitude_sbe")
        st.text_input("Longitude", key="longitude_sbe")
    with col2:
        st.time_input("Ship Mean Time (UTC)", datetime.now().time(), key="ship_mean_time_utc_sbe")
        st.time_input("Ship Mean Time (LT)", datetime.now().time(), key="ship_mean_time_lt_sbe")
        st.date_input("SBE Date", datetime.now().date(), key="sbe_date")
        st.time_input("SBE Time", datetime.now().time(), key="sbe_time")
        st.number_input("Hours since last Noon Report", min_value=0.0, step=0.1, key="hours_since_noon")
    with col3:
        st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden_sbe")
        st.number_input("Off Hire Delay (hrs)", min_value=0.0, step=0.01, key="off_hire_delay")
        st.number_input("SBE Report Number", min_value=1, step=1, key="sbe_report_number", 
                        help="Use this for multiple SBE reports before sailing")

    if sbe_scenario == "Preparing to Sail from Port":
        st.text_input("Last Line Station", key="last_line_station")
    elif sbe_scenario == "Preparing to Sail from Anchorage":
        st.number_input("Anchor Chain Length (shackles)", min_value=0, step=1, key="anchor_chain_length")
    elif sbe_scenario == "Preparing for Canal/River Transit":
        st.text_input("Canal/River Name", key="canal_river_name")
        st.text_input("Pilot Station", key="pilot_station")
    elif sbe_scenario == "Preparing to Commence STS Operation":
        st.text_input("STS Area", key="sts_area")
        st.text_input("Name of Other Vessel", key="other_vessel_name")
    elif sbe_scenario == "Preparing to Shift Berth":
        st.text_input("Current Berth", key="current_berth")
        st.text_input("Destination Berth", key="destination_berth")

    st.text_input("Next Port", key="next_port")
    st.text_input("Next Port operation", key="next_port_operation")

    st.subheader("Pilot Information")
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Expected Pilot Boarding Date", datetime.now().date(), key="pilot_boarding_date")
        st.time_input("Expected Pilot Boarding Time", datetime.now().time(), key="pilot_boarding_time")
    with col2:
        st.text_input("Pilot Boarding Position", key="pilot_boarding_position")

    st.subheader("Next Expected Action")
    st.selectbox("Next Action after SBE", ["COSP (Commencement of Sea Passage)", "Canal Entry", "STS Operation Start", "Berthing"], key="next_action")
    st.date_input("Expected Date of Next Action", datetime.now().date(), key="next_action_date")
    st.time_input("Expected Time of Next Action", datetime.now().time(), key="next_action_time")

def navigation_tab(sbe_scenario):
    st.header("Navigation Details")

    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Draft F (m)", min_value=0.0, step=0.01, key="draft_f_sbe")
        st.number_input("Draft A (m)", min_value=0.0, step=0.01, key="draft_a_sbe")
        st.number_input("Distance to Go (nm)", min_value=0.0, step=0.01, key="distance_to_go")
    with col2:
        st.date_input("ETA Date", datetime.now().date(), key="eta_date")
        st.time_input("ETA Time", datetime.now().time(), key="eta_time")

    if sbe_scenario in ["Preparing to Sail from Port", "Preparing to Sail from Anchorage", "Preparing to Move from Drifting"]:
        st.subheader("Departure Planning")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Estimated Sailing Draft F (m)", min_value=0.0, step=0.01, key="est_sailing_draft_f")
            st.number_input("Estimated Sailing Draft A (m)", min_value=0.0, step=0.01, key="est_sailing_draft_a")
        with col2:
            st.number_input("Estimated UKC at Departure (m)", min_value=0.0, step=0.01, key="est_ukc_departure")
            st.number_input("Tidal Window Opens (hrs)", min_value=0.0, step=0.1, key="tidal_window_opens")
            st.number_input("Tidal Window Closes (hrs)", min_value=0.0, step=0.1, key="tidal_window_closes")

    if sbe_scenario == "Preparing for Canal/River Transit":
        st.subheader("Canal/River Transit Planning")
        st.number_input("Estimated Transit Time (hrs)", min_value=0.0, step=0.1, key="est_transit_time")
        st.number_input("Maximum Allowed Draft (m)", min_value=0.0, step=0.01, key="max_allowed_draft")

    st.subheader("Weather Forecast")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Wind Direction Forecast", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key="wind_direction_forecast")
        st.number_input("Wind Force Forecast (Beaufort)", min_value=0, max_value=12, step=1, key="wind_force_forecast")
    with col2:
        st.number_input("Sea State Forecast (Douglas Scale)", min_value=0, max_value=9, step=1, key="sea_state_forecast")
        st.number_input("Visibility Forecast (nm)", min_value=0.0, step=0.1, key="visibility_forecast")

def engine_tab():
    st.header("Engine Information")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("ME Time Counter at SBE", key="me_time_counter_at_sbe")
        st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.01, key="shaft_generator_power")
    with col2:
        st.number_input("ME Test RPM", min_value=0, step=1, key="me_test_rpm")
        st.text_input("ME Test Duration", key="me_test_duration")

    st.subheader("Auxiliary Engines")
    col1, col2 = st.columns(2)
    for i in range(1, 5):
        with col1:
            st.number_input(f"A/E No.{i} Load (%)", min_value=0.0, max_value=100.0, step=0.1, key=f"ae_no{i}_load")
        with col2:
            st.number_input(f"A/E No.{i} Running Hours", min_value=0.0, step=0.1, key=f"ae_no{i}_running_hours")

def cargo_operations_tab(sbe_scenario):
    st.header("Cargo Operations")

    st.checkbox("No Cargo Operations in this port", key="no_cargo_operations")

    if not st.session_state.no_cargo_operations:
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Cargo", key="cargo_operation_cargo")
            st.checkbox("Is Critical", key="cargo_operation_is_critical")
            st.number_input("Qty (MT)", min_value=0.0, step=0.01, key="cargo_operation_qty")
            st.number_input("Vapour Qty (MT)", min_value=0.0, step=0.01, key="cargo_operation_vapour_qty")
            st.text_input("Oil Major Cargo", key="cargo_operation_oil_major_cargo")
        with col2:
            st.text_input("Oil Major", key="cargo_operation_oil_major")
            st.text_input("Basis of Final Qty", key="cargo_operation_basis_final_qty")
            st.text_input("BTB Transfer Y/N", key="cargo_operation_btb_transfer")
            st.date_input("Commenced Date", datetime.now().date(), key="cargo_operation_commenced_date")
            st.time_input("Commenced Time", datetime.now().time(), key="cargo_operation_commenced_time")
            st.date_input("Completed Date", datetime.now().date(), key="cargo_operation_completed_date")
            st.time_input("Completed Time", datetime.now().time(), key="cargo_operation_completed_time")
        st.text_input("Action", key="cargo_operation_action")

    st.subheader("Ballasting / Deballasting")
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Ballasting - Commenced Date", datetime.now().date(), key="ballasting_commenced_date")
        st.time_input("Ballasting - Commenced Time", datetime.now().time(), key="ballasting_commenced_time")
        st.date_input("Ballasting - Completed Date", datetime.now().date(), key="ballasting_completed_date")
        st.time_input("Ballasting - Completed Time", datetime.now().time(), key="ballasting_completed_time")
        st.number_input("Ballasting - Quantity (MT)", min_value=0.0, step=0.01, key="ballasting_quantity")
    with col2:
        st.date_input("Deballasting - Commenced Date", datetime.now().date(), key="deballasting_commenced_date")
        st.time_input("Deballasting - Commenced Time", datetime.now().time(), key="deballasting_commenced_time")
        st.date_input("Deballasting - Completed Date", datetime.now().date(), key="deballasting_completed_date")
        st.time_input("Deballasting - Completed Time", datetime.now().time(), key="deballasting_completed_time")
        st.number_input("Deballasting - Quantity (MT)", min_value=0.0, step=0.01, key="deballasting_quantity")

def bunkers_tab():
    st.header("Bunkers")

    bunkers_data = {
        "Fuel Type": [
            "Heavy Fuel Oil RME-RMK - 380cSt", "Heavy Fuel Oil RMA-RMD - 80cSt",
            "VLSFO RME-RMK Visc >380cSt 0.5%S Max", "VLSFO RMA-RMD Visc >80cSt 0.5%S Max",
            "ULSFO RME-RMK <380cSt 0.1%S Max", "ULSFO RMA-RMD <80cSt 0.1%S Max",
            "VLSMGO 0.5%S Max", "ULSMGO 0.1%S Max",
            "Biofuel - 30", "Biofuel Distillate FO",
            "LPG - Propane", "LPG - Butane",
            "LNG (Bunkered)"
        ],
        "ROB": [0.0] * 13,
        "Sulphur %": [0.0] * 13
    }
    bunkers_df = pd.DataFrame(bunkers_data)
    st.data_editor(bunkers_df, key="bunkers_editor", hide_index=True)

if __name__ == "__main__":
    main()
