import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime Noon Report")

def main():
    st.title("Maritime Noon Report")

    # Add a selectbox for the vessel's current state
    vessel_state = st.selectbox("Vessel's Current State", 
                                ["At Sea", "In Port", "Anchored", "Drifting", "Canal/River Passage"])

    tabs = st.tabs(["General Info", "Navigation", "Weather", "Speed and Consumption", "Engine", "Fuel and Consumables"])

    with tabs[0]:
        general_info_tab(vessel_state)

    with tabs[1]:
        navigation_tab(vessel_state)

    with tabs[2]:
        weather_tab()

    with tabs[3]:
        speed_consumption_tab(vessel_state)

    with tabs[4]:
        engine_tab(vessel_state)

    with tabs[5]:
        fuel_consumables_tab(vessel_state)

    if st.button("Submit Noon Report", type="primary"):
        st.success("Noon Report submitted successfully!")

def general_info_tab(vessel_state):
    st.header("General Information")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Vessel Name")
        st.text_input("Voyage No")
        st.text_input("Cargo No")
        st.text_input("Current Port" if vessel_state == "In Port" else "Last Port")
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

    if vessel_state in ["In Port", "Anchored"]:
        st.text_input("Berth / Anchorage Location")
    
    st.radio("Ballast/Laden", ["Ballast", "Laden"])

def navigation_tab(vessel_state):
    st.header("Navigation Details")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Latitude")
        st.text_input("Longitude")
        if vessel_state == "At Sea":
            st.number_input("Course (°)", min_value=0.0, max_value=360.0, step=1.0)
    with col2:
        st.text_input("Next Port")
        st.date_input("ETA Date", datetime.now())
        st.time_input("ETA Time", datetime.now().time())

    if vessel_state == "At Sea":
        st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1)
    elif vessel_state == "Drifting":
        st.number_input("Drifting Time (hrs)", min_value=0.0, step=0.1)
        st.number_input("Drifting Distance (nm)", min_value=0.0, step=0.1)
    elif vessel_state == "Canal/River Passage":
        st.text_input("Canal/River Name")
        st.number_input("Distance Travelled in Canal/River (nm)", min_value=0.0, step=0.1)

def weather_tab():
    st.header("Weather and Conditions")

    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Wind Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"])
        st.number_input("Wind Force", min_value=0, max_value=12)
        st.number_input("Visibility (nm)", min_value=0.0, step=0.1)
        st.number_input("Sea Height (m)", min_value=0.0, step=0.1)
        st.selectbox("Sea Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"])
    with col2:
        st.number_input("Swell Height (m)", min_value=0.0, step=0.1)
        st.selectbox("Swell Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"])
        st.number_input("Current Set (kts)", min_value=0.0, step=0.1)
        st.selectbox("Current Drift", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"])
        st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1)
        st.checkbox("Icing on Deck?")
    
    st.number_input("Period of bad Weather (beyond BF scale 5, in Hours)", min_value=0.0, step=0.1)

def speed_consumption_tab(vessel_state):
    st.header("Speed and Consumption")

    if vessel_state in ["At Sea", "Canal/River Passage"]:
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1)
            st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1)
            st.number_input("Average Speed (kts)", min_value=0.0, step=0.1)
        with col2:
            st.number_input("Engine Distance (nm)", min_value=0.0, step=0.1)
            st.number_input("Engine Speed (kts)", min_value=0.0, step=0.1)
            st.number_input("Slip (%)", min_value=0.0, max_value=100.0, step=0.1)
    
    st.number_input("Draft F (m)", min_value=0.0, step=0.01)
    st.number_input("Draft A (m)", min_value=0.0, step=0.01)

def engine_tab(vessel_state):
    st.header("Engine Information")

    col1, col2 = st.columns(2)
    with col1:
        st.number_input("ME Rev Counter", min_value=0, step=1)
        st.number_input("Average RPM", min_value=0.0, step=0.1)
        st.radio("Power Output", ["BHP", "KW"])
        st.number_input("Calculated Power", min_value=0, step=1)
    with col2:
        st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1)
        for i in range(1, 5):
            st.number_input(f"A/E No.{i} Generator Load (kw)", min_value=0, step=1)

    if vessel_state in ["At Sea", "Canal/River Passage"]:
        st.number_input("Avg RPM since last noon", min_value=0.0, step=0.1)

def fuel_consumables_tab(vessel_state):
    st.header("Fuel and Consumables")

    st.subheader("Fuel Consumption")
    consumption_data = {
        "Fuel Type": ["HFO", "LSFO", "MGO", "LNG"],
        "Previous ROB": [0.0] * 4,
        f"Consumption ({'At Sea' if vessel_state == 'At Sea' else 'In Port'})": [0.0] * 4,
        "ROB": [0.0] * 4
    }
    consumption_df = pd.DataFrame(consumption_data)
    st.data_editor(consumption_df, key="consumption_editor", hide_index=True)

    st.subheader("Fresh Water")
    fresh_water_data = {
        "Fresh Water": ["Domestic", "Technical", "Boiler"],
        "Previous ROB": [0.0] * 3,
        "Produced": [0.0] * 3,
        "Consumed": [0.0] * 3,
        "ROB": [0.0] * 3
    }
    fresh_water_df = pd.DataFrame(fresh_water_data)
    st.data_editor(fresh_water_df, key="fresh_water_editor", hide_index=True)

    st.subheader("Lub Oil")
    lub_oil_data = {
        "Lub Oil": ["Cylinder Oil", "System Oil"],
        "Previous ROB": [0.0] * 2,
        "Consumed": [0.0] * 2,
        "ROB": [0.0] * 2
    }
    lub_oil_df = pd.DataFrame(lub_oil_data)
    st.data_editor(lub_oil_df, key="lub_oil_editor", hide_index=True)

if __name__ == "__main__":
    main()
