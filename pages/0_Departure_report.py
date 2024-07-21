import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime Departure Report")

def main():
    st.title("Maritime Departure Report")

    tabs = st.tabs(["General Information", "Operations", "Emissions in Port"])

    with tabs[0]:
        general_info_tab()

    with tabs[1]:
        operations_tab()

    with tabs[2]:
        emissions_tab()

    if st.button("Submit Report", type="primary"):
        st.success("Departure report submitted successfully!")

def general_info_tab():
    st.header("General Information")

    with st.expander("Basic Details", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Vessel", key="vessel")
            st.text_input("Voyage No", key="voyage_no")
            st.text_input("Port", key="port")
            st.text_input("Name of Berth/Location", key="berth_location")
            st.text_input("Latitude", key="latitude")
            st.text_input("Longitude", key="longitude")
        with col2:
            st.time_input("Ship Mean Time (UTC)", datetime.now().time(), key="ship_mean_time_utc")
            st.time_input("Ship Mean Time (LT)", datetime.now().time(), key="ship_mean_time_lt")
            st.text_input("COSP", key="cosp")
            st.date_input("Departure Date", datetime.now().date(), key="departure_date")
        with col3:
            st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden")
            st.checkbox("Start New Voyage", key="start_new_voyage")
            st.number_input("Off Hire Delay (hrs)", min_value=0.0, step=0.01, key="off_hire_delay")
            st.number_input("Maneuvering (hrs)", min_value=0.0, step=0.01, key="maneuvering")
            st.number_input("Maneuvering distance (nm)", min_value=0.0, step=0.01, key="maneuvering_distance")

    with st.expander("Event Times", expanded=True):
        events = [
            "Pilot on Board (POB)", "Standby Engines (SBE)", "All Gone and Clear (LLC)", 
            "Anchor Aweigh (AAW)", "Dropping of Last Outward Sea Pilot (DLOSP)", 
            "Ring Full Away (RFA)", "Commencement of Sea Passage (COSP)"
        ]
        for event in events:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(event)
            with col2:
                st.date_input(f"{event} LT Date", datetime.now().date(), key=f"{event}_lt_date")
            with col3:
                st.time_input(f"{event} LT Time", datetime.now().time(), key=f"{event}_lt_time")
            with col4:
                st.time_input(f"{event} UTC Time", datetime.now().time(), key=f"{event}_utc_time")

    with st.expander("Navigation Details", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Draft F (m)", min_value=0.0, step=0.01, key="draft_f")
            st.number_input("Draft A (m)", min_value=0.0, step=0.01, key="draft_a")
            st.text_input("Next Port", key="next_port")
            st.text_input("Next Port operation", key="next_port_operation")
            st.number_input("Distance to Go (nm)", min_value=0.0, step=0.01, key="distance_to_go")
        with col2:
            st.date_input("ETA Date", datetime.now().date(), key="eta_date")
            st.time_input("ETA Time", datetime.now().time(), key="eta_time")
            st.text_input("ME Time Counter at COSP", key="me_time_counter_at_cosp")
            st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.01, key="shaft_generator_power")

    with st.expander("Voyage Planning", expanded=True):
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

    with st.expander("Remarks", expanded=True):
        st.text_area("General Remarks", height=100, key="remarks_general")

    with st.expander("Services in Port", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Service Type", key="service_type")
            st.number_input("Qty", min_value=0.0, step=0.01, key="qty")
        with col2:
            st.text_input("Unit", key="unit")
            st.number_input("Est Cost", min_value=0.0, step=0.01, key="est_cost")
        with col3:
            st.text_input("Currency", key="currency")
            st.text_input("Service On", key="service_on")
        st.text_area("Service Remarks", height=100, key="remarks_service")

    with st.expander("Lube Oil (Ltrs)", expanded=True):
        lube_oil_data = {
            "Lube Oil": ["ME Cylinder Oil", "ME Cylinder Oil 40 TBN", "ME Cylinder Oil 70 TBN", "ME Cylinder Oil 100 TBN", "ME/MT System Oil", "AE System Oil", "AE System Oil 15TBN", "T/O System Oil"],
            "Prev. ROB": [0.0] * 8,
            "Cons": [0.0] * 8,
            "Received": [0.0] * 8,
            "ROB": [0.0] * 8
        }
        lube_oil_df = pd.DataFrame(lube_oil_data)
        st.data_editor(lube_oil_df, key="lube_oil_editor", hide_index=True)

    with st.expander("Fresh Water", expanded=True):
        fresh_water_data = {
            "Fresh Water": ["Domestic Fresh Water", "Drinking Water", "Boiler Water", "Tank Cleaning Water"],
            "Previous ROB": [240.0, 0.0, 0.0, 0.0],
            "Received": [0.0] * 4,
            "ROB on Dep": [232.0, 0.0, 0.0, 0.0],
            "Cons": [0.0] * 4
        }
        fresh_water_df = pd.DataFrame(fresh_water_data)
        st.data_editor(fresh_water_df, key="fresh_water_editor", hide_index=True)

    with st.expander("Consumption (MT)", expanded=True):
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
            "In Port M/E": [0.0] * 13,
            "In Port A/E": [0.0] * 13,
            "In Port BLR": [0.0] * 13,
            "In Port IGG": [0.0] * 13,
            "In Port GE/EG": [0.0] * 13,
            "In Port OTH": [0.0] * 13,
            "Bunker Qty": [0.0, 0.0, 568.12, 0.0, 0.0, 0.0, 100.51, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "Sulphur %": [0.0, 0.0, 0.48, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "ROB @ BDN": [0.0, 0.0, 892.42, 0.0, 0.0, 0.0, 671.51, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "At Harbour M/E": [0.0] * 13,
            "At Harbour A/E": [0.0] * 13,
            "At Harbour BLR": [0.0] * 13,
            "At Harbour IGG": [0.0] * 13,
            "At Harbour GE/EG": [0.0] * 13,
            "At Harbour OTH": [0.0] * 13,
            "ROB @ COSP": [0.0, 0.0, 871.8, 0.0, 0.0, 0.0, 671.51, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        }
        consumption_df = pd.DataFrame(consumption_data)
        st.data_editor(consumption_df, key="consumption_editor", hide_index=True)

def operations_tab():
    st.header("Operations")

    with st.expander("Cargo Operations", expanded=True):
        st.checkbox("No Cargo Operations in this port", key="no_cargo_operations")
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

    with st.expander("Ballasting / Deballasting", expanded=True):
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

    with st.expander("Tank Cleaning", expanded=True):
        st.checkbox("Hold / Tank Cleaning", key="hold_tank_cleaning")
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Commenced Date", datetime.now().date(), key="hold_tank_cleaning_commenced_date")
            st.time_input("Commenced Time", datetime.now().time(), key="hold_tank_cleaning_commenced_time")
        with col2:
            st.date_input("Completed Date", datetime.now().date(), key="hold_tank_cleaning_completed_date")
            st.time_input("Completed Time", datetime.now().time(), key="hold_tank_cleaning_completed_time")
        st.checkbox("Stripping / Draining", key="stripping_draining")
        st.text_area("Stripping / Draining Remarks", height=100, key="stripping_draining_remarks")

    with st.expander("Other Operations", expanded=True):
        st.text_area("Description", height=100, key="other_operations_description")
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Commenced Date", datetime.now().date(), key="other_operations_commenced_date")
            st.time_input("Commenced Time", datetime.now().time(), key="other_operations_commenced_time")
        with col2:
            st.date_input("Completed Date", datetime.now().date(), key="other_operations_completed_date")
            st.time_input("Completed Time", datetime.now().time(), key="other_operations_completed_time")
        st.text_input("Action", key="other_operations_action")

def emissions_tab():
    st.header("Emissions in Port")

    with st.expander("General Information", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Vessel Name", key="vessel_name_emission")
            st.text_input("Voyage No", key="voyage_no_emission")
            st.text_input("Port", key="port_emission")
        with col2:
            st.checkbox("Ballast", key="ballast_laden_emission")
            st.checkbox("EU Port", key="eu_port")
        with col3:
            st.date_input("Arrival Date", datetime.now().date(), key="arrival_date_emission")
            st.time_input("Arrival Time", datetime.now().time(), key="arrival_time_emission")
            st.date_input("Departure Date", datetime.now().date(), key="departure_date_emission")
            st.time_input("Departure Time", datetime.now().time(), key="departure_time_emission")
            st.number_input("Total Time in Port (hrs)", min_value=0.0, step=0.01, key="total_time_in_port_emission")
            st.number_input("Total Aggregated CO2 Emitted (T CO2)", min_value=0.0, step=0.01, key="total_aggregated_co2_emitted")

    with st.expander("Consumption (MT)", expanded=True):
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
        st.data_editor(consumption_emissions_df, key="consumption_emissions_editor", hide_index=True)

if __name__ == "__main__":
    main()
