import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime Shifting Report")

def main():
    st.title("Maritime Shifting Report")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.header("Filters")
        vessel = st.text_input("Vessel", key="vessel")
        voyage_no = st.text_input("Voyage No", key="voyage_no")
        port = st.text_input("Port", key="port")

    with col2:
        general_info_section()
        detailed_times_section()
        bilge_sludge_section()
        remarks_section()
        counter_section()
        service_remarks_section()
        lube_oil_section()
        consumption_section()

def general_info_section():
    with st.expander("General Information", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Name of Berth Departed", key="berth_departed")
            st.text_input("Name of Berth Arrived", key="berth_arrived")
            st.text_input("Latitude", key="latitude")
            st.text_input("Longitude", key="longitude")
        with col2:
            st.selectbox("Ship Mean Time", ["UTC"], key="ship_mean_time")
            st.number_input("Offset", min_value=-12, max_value=12, step=1, key="offset")
            st.date_input("FWE", datetime.now(), key="fwe_date")
            st.time_input("FWE Time", datetime.now().time(), key="fwe_time")
        with col3:
            st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden")
            st.text_input("Next Port", key="next_port")
            st.text_input("ETC/D", key="etc_d")
            st.date_input("Next Port Operation", datetime.now(), key="next_port_operation_date")

def detailed_times_section():
    with st.expander("Detailed Times", expanded=True):
        col1, col2 = st.columns(2)
        events = [
            "Pilot on Board (POB)", "APS", "Arrival Customary Anchorage",
            "Arrival Drifting Position", "Anchor Aweigh",
            "Commenced Proceeding to Berth from Drifting Position",
            "Standby Engines (SBE)", "All Gone and Clear (LLC)",
            "First Line Ashore (FLA)", "Last Line Ashore (LGA)",
            "All Fast", "Gangway Down", "Finished with Engines (FWE)",
            "Pilot Away (POB)", "Harbour Steaming Dist"
        ]
        
        for i, event in enumerate(events):
            with col1 if i % 2 == 0 else col2:
                st.date_input(f"{event} LT", datetime.now(), key=f"{event.lower().replace(' ', '_')}_lt_date")
                st.time_input(f"{event} UTC", datetime.now().time(), key=f"{event.lower().replace(' ', '_')}_utc_time")

        with col1:
            st.text_input("Shaft Generator Power (kw)", key="shaft_generator_power")
        with col2:
            st.text_input("hrs", key="shaft_generator_hours")

def bilge_sludge_section():
    with st.expander("Bilge, Sludge", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Quantity of Sludge Landed (cu.m)", key="sludge_landed")
        with col2:
            st.text_input("Quantity of Bilge Water Landed (cu.m)", key="bilge_water_landed")
        with col3:
            st.text_input("Quantity of Garbage Landed (cu.m)", key="garbage_landed")
            st.radio("LO Sample Landed?", ["Yes", "No"], key="lo_sample_landed")

def remarks_section():
    with st.expander("Remarks", expanded=True):
        st.text_area("Remarks", key="remarks", height=150)

def counter_section():
    with st.expander("Counter", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("ME Rev Counter @FWE", key="me_rev_counter")
        with col2:
            st.checkbox("Counter Defective / Reset", key="counter_defective")

def service_remarks_section():
    with st.expander("Service Remarks", expanded=True):
        service_data = {
            "Service Type": [
                "FW Received on Owners Account", "Launch services used on Owners account",
                "Stores Received (PO / Reqsn No)", "Spares Received (PO / Reqsn No)",
                "Surveys Carried Out", "Repairs carried out", "Shipments from vessel", "Other Services"
            ],
            "Remarks": [""] * 8
        }
        service_df = pd.DataFrame(service_data)
        st.data_editor(service_df, key="service_editor", hide_index=True, use_container_width=True)

def lube_oil_section():
    with st.expander("Lube Oil (Ltr)", expanded=True):
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
        st.data_editor(lube_oil_df, key="lube_oil_editor", hide_index=True, use_container_width=True)

def consumption_section():
    with st.expander("Consumption (mT)", expanded=True):
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
        st.data_editor(consumption_df, key="consumption_editor", hide_index=True, use_container_width=True)

if __name__ == "__main__":
    main()
