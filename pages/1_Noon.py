import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime Noon at Sea Report")

def main():
    st.title("Maritime Noon at Sea Report")

    vessel_state = st.selectbox("Vessel's Current State", 
                                ["At Sea", "In Port", "At Anchor", "During Drifting", "At STS", "At Canal/River Passage"])

    if vessel_state == "At Sea":
        tabs = st.tabs(["Deck", "Engine"])

        with tabs[0]:
            deck_tab()

        with tabs[1]:
            engine_tab()

        if st.button("Submit Noon at Sea Report", type="primary"):
            st.success("Noon at Sea Report submitted successfully!")
    else:
        st.warning("Please select 'At Sea' to fill out the Noon at Sea Report.")

def deck_tab():
    st.header("Deck Information")

    with st.expander("General Information", expanded=True):
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

    st.radio("Ballast/Laden", ["Ballast", "Laden"])

    with st.expander("Navigation Details", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Latitude")
            st.text_input("Longitude")
            st.number_input("Course (°)", min_value=0.0, max_value=360.0, step=1.0)
        with col2:
            st.text_input("Next Port")
            st.date_input("ETA Date", datetime.now())
            st.time_input("ETA Time", datetime.now().time())
            st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1)
            st.number_input("Distance Traveled Since Last Noon (nm)", min_value=0.0, step=0.1)

    with st.expander("Weather and Conditions", expanded=True):
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

    with st.expander("Speed and Consumption", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1)
            st.number_input("Reduced Speed (hrs)", min_value=0.0, step=0.1)
            st.number_input("Stopped (hrs)", min_value=0.0, step=0.1)
        with col2:
            st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1)
            st.number_input("Average Speed (kts)", min_value=0.0, step=0.1)
            st.number_input("Engine Speed (kts)", min_value=0.0, step=0.1)
        with col3:
            st.number_input("Slip (%)", min_value=0.0, max_value=100.0, step=0.1)
            st.number_input("Draft F (m)", min_value=0.0, step=0.01)
            st.number_input("Draft A (m)", min_value=0.0, step=0.01)

def engine_tab():
    st.header("Engine Information")

    with st.expander("Main Engine", expanded=True):
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

    with st.expander("Auxiliary Engines", expanded=True):
        col1, col2 = st.columns(2)
        for i in range(1, 5):
            with col1:
                st.number_input(f"A/E No.{i} Generator Load (kw)", min_value=0, step=1)
            with col2:
                st.number_input(f"A/E No.{i} Running Hours", min_value=0.0, step=0.1)
        st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1)

    with st.expander("Fuel Consumption", expanded=True):
        consumption_data = {
            "Fuel Type": ["HFO", "LSFO", "MGO", "LNG"],
            "Previous ROB": [0.0] * 4,
            "Consumption (At Sea)": [0.0] * 4,
            "ROB": [0.0] * 4
        }
        consumption_df = pd.DataFrame(consumption_data)
        st.data_editor(consumption_df, key="consumption_editor", hide_index=True)

    with st.expander("Lube Oil Consumption", expanded=True):
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
