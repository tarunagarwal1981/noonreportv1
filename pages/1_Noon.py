import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime Noon Report")

def main():
    st.title("Maritime Noon Report")

    vessel_state = st.selectbox("Vessel's Current State", 
                                ["At Sea", "In Port", "At Anchor", "During Drifting", "At STS", "At Canal/River Passage"],
                                index=0)  # Set "At Sea" as default

    if vessel_state in ["At Sea", "During Drifting", "At Canal/River Passage"]:
        noon_at_sea_report(vessel_state)
    else:
        noon_other_report(vessel_state)

def noon_at_sea_report(vessel_state):
    tabs = st.tabs(["Deck", "Engine"])

    with tabs[0]:
        deck_tab_at_sea(vessel_state)

    with tabs[1]:
        engine_tab_at_sea(vessel_state)

    if st.button(f"Submit Noon {vessel_state} Report", type="primary"):
        st.success(f"Noon {vessel_state} Report submitted successfully!")

def noon_other_report(vessel_state):
    tabs = st.tabs(["Deck", "Engine"])

    with tabs[0]:
        deck_tab_other(vessel_state)

    with tabs[1]:
        engine_tab_other(vessel_state)

    if st.button(f"Submit Noon {vessel_state} Report", type="primary"):
        st.success(f"Noon {vessel_state} Report submitted successfully!")

def deck_tab_at_sea(vessel_state):
    st.header("Deck Information")

    with st.expander("General Information", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Vessel Name")
            st.text_input("Voyage No")
            st.text_input("Last Port")
        with col2:
            st.date_input("Report Date (LT)", datetime.now())
            st.time_input("Report Time (LT)", datetime.now().time())
            st.date_input("Report Date (UTC)", datetime.now())
            st.time_input("Report Time (UTC)", datetime.now().time())
        with col3:
            st.text_input("Ship Mean Time", value="UTC")
            st.number_input("Offset", min_value=-12, max_value=12, step=1)
            st.checkbox("IDL Crossing")
            st.selectbox("IDL Direction", ["--Select--", "East", "West"])

    with st.expander("Voyage Details", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Voyage From")
            st.text_input("Voyage To")
            st.selectbox("Voyage Stage", ["", "East", "West", "Ballast", "Laden"])
        with col2:
            st.text_input("Speed Order")
            st.text_input("ETA")
            st.radio("Ballast/Laden", ["Ballast", "Laden"])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.checkbox("Off-hire")
        with col2:
            st.checkbox("ECA Transit")
        with col3:
            st.checkbox("Fuel Changeover")
        with col4:
            st.checkbox("Deviation")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Ice Navigation")
        with col2:
            st.checkbox("IDL Crossing")
        
        st.checkbox("Transiting Special Area")

    with st.expander("Speed, Position and Navigation", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1)
            st.number_input("Reduced Speed (hrs)", min_value=0.0, step=0.1)
            st.number_input("Stopped (hrs)", min_value=0.0, step=0.1)
            st.text_input("Latitude")
            st.text_input("Longitude")
        with col2:
            st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1)
            st.number_input("Distance Through Water (nm)", min_value=0.0, step=0.1)
            st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1)
            st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1)
        with col3:
            st.number_input("Course (°)", min_value=0.0, max_value=360.0, step=1.0)
            st.number_input("Heading (°)", min_value=0.0, max_value=360.0, step=1.0)

    with st.expander("Weather and Conditions", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
            st.number_input("Wind Force (Beaufort)", min_value=0, max_value=12)
            st.number_input("Sea Height (m)", min_value=0.0, step=0.1)
            st.selectbox("Sea Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
        with col2:
            st.number_input("Swell Height (m)", min_value=0.0, step=0.1)
            st.selectbox("Swell Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
            st.number_input("Current Speed (kts)", min_value=0.0, step=0.1)
            st.selectbox("Current Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
            st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1)
            st.number_input("Sea Temp (°C)", min_value=-2.0, max_value=35.0, step=0.1)

        st.number_input("Visibility (nm)", min_value=0.0, step=0.1)
        st.checkbox("Icing on Deck?")

    with st.expander("Cargo and Stability", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Draft F (m)", min_value=0.0, step=0.01)
            st.number_input("Draft A (m)", min_value=0.0, step=0.01)
            st.number_input("Draft M (m)", min_value=0.0, step=0.01)
        with col2:
            st.number_input("Displacement (MT)", min_value=0.0, step=0.1)
            st.number_input("Deadweight (MT)", min_value=0.0, step=0.1)
        with col3:
            st.number_input("GM (m)", min_value=0.0, step=0.01)
            st.number_input("Trim (m)", min_value=-10.0, max_value=10.0, step=0.01)

def engine_tab_at_sea(vessel_state):
    st.header("Engine Information")

    with st.expander("Main Engine", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("ME Rev Counter", min_value=0, step=1)
            st.number_input("Average RPM", min_value=0.0, step=0.1)
            st.number_input("Avg RPM since COSP", min_value=0.0, step=0.1)
            st.radio("Power Output", ["BHP", "KW"])
            st.number_input("Calculated Power", min_value=0, step=1)
        with col2:
            st.number_input("Governor Setting (%)", min_value=0.0, max_value=100.0, step=0.1)
            st.number_input("Scav Air Temp (°C)", min_value=0.0, step=0.1)
            st.number_input("Scav Air Press (bar)", min_value=0.0, step=0.1)
        with col3:
            st.number_input("FO Inlet Temp (°C)", min_value=0.0, step=0.1)
            st.number_input("FO Press (bar)", min_value=0.0, step=0.1)
            st.number_input("Exh Temp Avg (°C)", min_value=0.0, step=0.1)

    with st.expander("Auxiliary Engines", expanded=False):
        col1, col2 = st.columns(2)
        for i in range(1, 5):
            with col1:
                st.number_input(f"A/E No.{i} Generator Load (kw)", min_value=0, step=1)
            with col2:
                st.number_input(f"A/E No.{i} Running Hours", min_value=0.0, step=0.1)
        st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1)

    with st.expander("Fuel Consumption", expanded=False):
        consumption_data = {
            "Fuel Type": ["HFO", "LSFO", "MGO", "LNG"],
            "Previous ROB": [0.0] * 4,
            "Consumption (At Sea)": [0.0] * 4,
            "ROB": [0.0] * 4
        }
        consumption_df = pd.DataFrame(consumption_data)
        st.data_editor(consumption_df, key="consumption_editor", hide_index=True)

    with st.expander("Fuel Allocation", expanded=False):
        allocation_data = {
            "Fuel Type": ["HFO", "LSFO", "MGO", "LNG"],
            "Main Engine": [0.0] * 4,
            "Auxiliary Engine": [0.0] * 4,
            "Boilers": [0.0] * 4,
            "Others": [0.0] * 4
        }
        allocation_df = pd.DataFrame(allocation_data)
        st.data_editor(allocation_df, key="allocation_editor", hide_index=True)

    with st.expander("Environmental Compliance", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1)
            st.number_input("Sludge Burnt in Incinerator (MT)", min_value=0.0, step=0.1)
            st.number_input("Sludge Landed Ashore (MT)", min_value=0.0, step=0.1)
        with col2:
            st.number_input("Bilge Water Quantity (m³)", min_value=0.0, step=0.1)
            st.number_input("Bilge Water Pumped Out through 15ppm Equipment (m³)", min_value=0.0, step=0.1)
            st.number_input("Bilge Water Landed Ashore (m³)", min_value=0.0, step=0.1)

def deck_tab_other(vessel_state):
    st.header("Deck Information")

    with st.expander("General Information", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Vessel Name")
            st.text_input("Voyage No")
            st.text_input("Last Port")
        with col2:
            st.date_input("Report Date (LT)", datetime.now())
            st.time_input("Report Time (LT)", datetime.now().time())
            st.date_input("Report Date (UTC)", datetime.now())
            st.time_input("Report Time (UTC)", datetime.now().time())
        with col3:
            st.text_input("Ship Mean Time", value="UTC")
            st.number_input("Offset", min_value=-12, max_value=12, step=1)
            st.checkbox("IDL Crossing")
            st.selectbox("IDL Direction", ["--Select--", "East", "West"])

    with st.expander("Voyage Details", expanded=False):
        st.text_input("Port Name")
        st.radio("Ballast/Laden", ["Ballast", "Laden"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.checkbox("Off-hire")
        with col2:
            st.checkbox("ECA Transit")
        with col3:
            st.checkbox("Fuel Changeover")

    with st.expander("Speed, Position and Navigation", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Latitude")
            st.text_input("Longitude")
        with col2:
            st.number_input("True Heading (°)", min_value=0.0, max_value=360.0, step=1.0)

    with st.expander("Weather and Conditions", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
            st.number_input("Wind Force (Beaufort)", min_value=0, max_value=12)
            st.number_input("Sea Height (m)", min_value=0.0, step=0.1)
            st.selectbox("Sea Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
        with col2:
            st.number_input("Swell Height (m)", min_value=0.0, step=0.1)
            st.selectbox("Swell Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
            st.number_input("Current Speed (kts)", min_value=0.0, step=0.1)
            st.selectbox("Current Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
            st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1)
            st.number_input("Sea Temp (°C)", min_value=-2.0, max_value=35.0, step=0.1)

        st.number_input("Visibility (nm)", min_value=0.0, step=0.1)
        st.checkbox("Icing on Deck?")

    with st.expander("Cargo and Stability", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Draft F (m)", min_value=0.0, step=0.01)
            st.number_input("Draft A (m)", min_value=0.0, step=0.01)
            st.number_input("Draft M (m)", min_value=0.0, step=0.01)
        with col2:
            st.number_input("Displacement (MT)", min_value=0.0, step=0.1)
            st.number_input("Deadweight (MT)", min_value=0.0, step=0.1)
        with col3:
            st.number_input("GM (m)", min_value=0.0, step=0.01)
            st.number_input("Trim (m)", min_value=-10.0, max_value=10.0, step=0.01)

def engine_tab_other(vessel_state):
    st.header("Engine Information")

    with st.expander("Main Engine", expanded=False):
        st.number_input("ME Rev Counter", min_value=0, step=1)

    with st.expander("Auxiliary Engines", expanded=False):
        col1, col2 = st.columns(2)
        for i in range(1, 5):
            with col1:
                st.number_input(f"A/E No.{i} Generator Load (kw)", min_value=0, step=1)
            with col2:
                st.number_input(f"A/E No.{i} Running Hours", min_value=0.0, step=0.1)
        st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1)

    with st.expander("Fuel Consumption", expanded=False):
        consumption_data = {
            "Fuel Type": ["HFO", "LSFO", "MGO", "LNG"],
            "Previous ROB": [0.0] * 4,
            "Consumption (In Port)": [0.0] * 4,
            "ROB": [0.0] * 4
        }
        consumption_df = pd.DataFrame(consumption_data)
        st.data_editor(consumption_df, key="consumption_editor", hide_index=True)

    with st.expander("Fuel Allocation", expanded=False):
        allocation_data = {
            "Fuel Type": ["HFO", "LSFO", "MGO", "LNG"],
            "Main Engine": [0.0] * 4,
            "Auxiliary Engine": [0.0] * 4,
            "Boilers": [0.0] * 4,
            "Others": [0.0] * 4
        }
        allocation_df = pd.DataFrame(allocation_data)
        st.data_editor(allocation_df, key="allocation_editor", hide_index=True)

    with st.expander("Environmental Compliance", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1)
            st.number_input("Sludge Landed Ashore (MT)", min_value=0.0, step=0.1)
        with col2:
            st.number_input("Bilge Water Quantity (m³)", min_value=0.0, step=0.1)
            st.number_input("Bilge Water Landed Ashore (m³)", min_value=0.0, step=0.1)

    with st.expander("Fresh Water", expanded=False):
        fresh_water_data = {
            "Fresh Water": ["Domestic Fresh Water", "Drinking Water", "Boiler Water", "Tank Cleaning Water"],
            "Previous ROB": [0.0] * 4,
            "Produced": [0.0] * 4,
            "ROB": [0.0] * 4,
            "Consumption": [0.0] * 4
        }
        fresh_water_df = pd.DataFrame(fresh_water_data)
        st.data_editor(fresh_water_df, key="fresh_water_editor", hide_index=True)

    with st.expander("Lubricating Oil", expanded=False):
        lube_oil_data = {
            "Lube Oil": ["ME Cylinder Oil", "ME System Oil", "AE System Oil"],
            "Previous ROB": [0.0] * 3,
            "Consumption": [0.0] * 3,
            "ROB": [0.0] * 3
        }
        lube_oil_df = pd.DataFrame(lube_oil_data)
        st.data_editor(lube_oil_df, key="lube_oil_editor", hide_index=True)

if __name__ == "__main__":
    main()
