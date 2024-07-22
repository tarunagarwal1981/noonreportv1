import streamlit as st
from datetime import datetime
import pandas as pd

# Set up the page layout
st.set_page_config(layout="wide", page_title="Shifting Report")

def main():
    st.title("Shifting Report")

    # General Information Section
    st.header("General Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Vessel", key="vessel")
        st.text_input("Voyage No", key="voyage_no")
        st.text_input("Port", key="port")
        st.text_input("Name of Berth Departed", key="berth_departed")
        st.text_input("Name of Berth Arrived", key="berth_arrived")
    with col2:
        st.text_input("Latitude", key="latitude")
        st.text_input("Longitude", key="longitude")
        st.selectbox("Ship Mean Time", ["UTC"], key="ship_mean_time")
        st.number_input("Offset", min_value=-12, max_value=12, step=1, key="offset")
    with col3:
        st.date_input("FWE", datetime.now(), key="fwe_date")
        st.time_input("FWE Time", datetime.now().time(), key="fwe_time")

    # Detailed Times Section
    st.subheader("Detailed Times")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.date_input("Pilot on Board (POB) LT", datetime.now(), key="pob_lt_date")
        st.time_input("Pilot on Board (POB) UTC", datetime.now().time(), key="pob_utc_time")
        st.date_input("APS LT", datetime.now(), key="aps_lt_date")
        st.time_input("APS UTC", datetime.now().time(), key="aps_utc_time")
        st.date_input("Arrival Customary Anchorage LT", datetime.now(), key="arrival_customary_anchorage_lt_date")
        st.time_input("Arrival Customary Anchorage UTC", datetime.now().time(), key="arrival_customary_anchorage_utc_time")
        st.date_input("Arrival Drifting Position LT", datetime.now(), key="arrival_drifting_position_lt_date")
        st.time_input("Arrival Drifting Position UTC", datetime.now().time(), key="arrival_drifting_position_utc_time")
    with col2:
        st.date_input("Anchor Aweigh LT", datetime.now(), key="anchor_aweigh_lt_date")
        st.time_input("Anchor Aweigh UTC", datetime.now().time(), key="anchor_aweigh_utc_time")
        st.date_input("Commenced Proceeding to Berth from Drifting Position LT", datetime.now(), key="proceeding_berth_lt_date")
        st.time_input("Commenced Proceeding to Berth from Drifting Position UTC", datetime.now().time(), key="proceeding_berth_utc_time")
        st.date_input("Standby Engines (SBE) LT", datetime.now(), key="sbe_lt_date")
        st.time_input("Standby Engines (SBE) UTC", datetime.now().time(), key="sbe_utc_time")
        st.date_input("All Gone and Clear (LLC) LT", datetime.now(), key="llc_lt_date")
        st.time_input("All Gone and Clear (LLC) UTC", datetime.now().time(), key="llc_utc_time")
    with col3:
        st.date_input("First Line Ashore (FLA) LT", datetime.now(), key="fla_lt_date")
        st.time_input("First Line Ashore (FLA) UTC", datetime.now().time(), key="fla_utc_time")
        st.date_input("Last Line Ashore (LGA) LT", datetime.now(), key="lga_lt_date")
        st.time_input("Last Line Ashore (LGA) UTC", datetime.now().time(), key="lga_utc_time")
        st.date_input("All Fast LT", datetime.now(), key="all_fast_lt_date")
        st.time_input("All Fast UTC", datetime.now().time(), key="all_fast_utc_time")
        st.date_input("Gangway Down LT", datetime.now(), key="gangway_down_lt_date")
        st.time_input("Gangway Down UTC", datetime.now().time(), key="gangway_down_utc_time")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.date_input("Finished with Engines (FWE) LT", datetime.now(), key="finished_engines_lt_date")
        st.time_input("Finished with Engines (FWE) UTC", datetime.now().time(), key="finished_engines_utc_time")
        st.date_input("Pilot Away (POB) LT", datetime.now(), key="pilot_away_lt_date")
        st.time_input("Pilot Away (POB) UTC", datetime.now().time(), key="pilot_away_utc_time")
    with col2:
        st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden")
        st.date_input("Harbour Steaming Dist LT", datetime.now(), key="harbour_steaming_dist_lt_date")
        st.time_input("Harbour Steaming Dist UTC", datetime.now().time(), key="harbour_steaming_dist_utc_time")
        st.text_input("ETC/D", key="etc_d")
        st.date_input("Next Port Operation", datetime.now(), key="next_port_operation_date")
    with col3:
        st.text_input("Next Port", key="next_port")
        st.text_input("Shaft Generator Power (kw)", key="shaft_generator_power")
        st.text_input("hrs", key="shaft_generator_hours")

    # Bilge, Sludge Section
    st.subheader("Bilge, Sludge")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Quantity of Sludge Landed (cu.m)", key="sludge_landed")
    with col2:
        st.text_input("Quantity of Bilge Water Landed (cu.m)", key="bilge_water_landed")
    with col3:
        st.text_input("Quantity of Garbage Landed (cu.m)", key="garbage_landed")
        st.radio("LO Sample Landed?", ["Yes", "No"], key="lo_sample_landed")

    # Remarks Section
    st.subheader("Remarks")
    st.text_area("Remarks", key="remarks")

    # Counter Section
    st.subheader("Counter")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("ME Rev Counter @FWE", key="me_rev_counter")
    with col2:
        st.checkbox("Counter Defective / Reset", key="counter_defective")

    # Service Remarks Section
    st.subheader("Service Remarks")
    service_data = {
        "Service Type": [
            "FW Received on Owners Account", "Launch services used on Owners account", "Stores Received (PO / Reqsn No)",
            "Spares Received (PO / Reqsn No)", "Surveys Carried Out", "Repairs carried out", "Shipments from vessel", "Other Services"
        ],
        "Remarks": [""] * 8
    }
    service_df = pd.DataFrame(service_data)
    st.data_editor(service_df, key="service_editor", hide_index=True)

    # Lube Oil Section
    st.subheader("Lube Oil (Ltr)")
    lube_oil_data = {
        "Lube Oil": [
            "ME Cylinder Oil", "ME Cylinder Oil 15 TBN", "ME Cylinder Oil 40 TBN",
            "ME Cylinder Oil 70 TBN", "ME Cylinder Oil 100 TBN", "ME/MT System Oil",
            "AE System Oil", "AE System Oil 15TBN", "TG System Oil", "Other Lub Oils"
        ],
        "Prev. ROB": [0.0] * 10,
        "Consumption": [0.0] * 10,
        "Received": [0.0] * 10,
        "ROB": [0.0] * 10
    }
    lube_oil_df = pd.DataFrame(lube_oil_data)
    st.data_editor(lube_oil_df, key="lube_oil_editor", hide_index=True)

    # Consumption Section
    st.subheader("Consumption (mT)")
    consumption_data = {
        "Item": [
            "Heavy Fuel Oil RME-RMK >80cSt", "Heavy Fuel Oil RMA-RMD <80cSt",
            "VLSFO RME-RMK Visc >80cSt 0.5%S Max", "VLSFO RMA-RMD Visc >80cSt 0.5%S Max",
            "ULSFO RME-RMK <80cSt 0.1%S Max", "ULSFO RMA-RMD <80cSt 0.1%S Max",
            "VLSMGO 0.5%S Max", "ULSMGO 0.1%S Max", "Biofuel - 30", "Biofuel Distillate FO",
            "LPG - Propane", "LPG - Butane", "LNG Boil Off", "LNG (Bunkered)"
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
        "ROB @ BILGE": [0.0] * 14,
        "AT HARBOUR M/E": [0.0] * 14,
        "AT HARBOUR A/E": [0.0] * 14,
        "AT HARBOUR BLR": [0.0] * 14,
        "AT HARBOUR IGG": [0.0] * 14,
        "AT HARBOUR C/ENG": [0.0] * 14,
        "AT HARBOUR OTH": [0.0] * 14,
        "ROB @ FWE": [0.0] * 14
    }
    consumption_df = pd.DataFrame(consumption_data)
    st.data_editor(consumption_df, key="consumption_editor", hide_index=True)

if __name__ == "__main__":
    main()
