import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime Noon Report")

def main():
    st.title("Maritime Noon Report")

    tabs = st.tabs(["General Info", "Navigation", "Weather", "Speed and Consumption", "Engine", "Fuel and Consumables"])

    with tabs[0]:
        general_info_tab()

    with tabs[1]:
        navigation_tab()

    with tabs[2]:
        weather_tab()

    with tabs[3]:
        speed_consumption_tab()

    with tabs[4]:
        engine_tab()

    with tabs[5]:
        fuel_consumables_tab()

    if st.button("Submit Noon Report", type="primary"):
        st.success("Noon Report submitted successfully!")

def general_info_tab():
    st.header("General Information")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Vessel Name")
        st.text_input("Voyage No")
        st.text_input("Cargo No")
        st.selectbox("Vessel's Status", ["At Sea", "In Port"])
        st.text_input("Current Port")
        st.text_input("Last Port")
    with col2:
        st.date_input("Report Date (LT)", datetime.now())
        st.time_input("Report Time (LT)", datetime.now().time())
        st.date_input("Report Date (UTC)", datetime.now())
        st.time_input("Report Time (UTC)", datetime.now().time())
        st.text_input("Ship Mean Time", value="UTC")
        st.number_input("Offset", min_value=-12, max_value=12, step=1)
    with col3:
        st.checkbox("IDL Crossing")
        st.selectbox("IDL Direction", ["--Select--", "East", "West"])
        st.text_input("Berth / Location")
        st.checkbox("Off Port Limits")
        st.radio("Ballast/Laden", ["Ballast", "Laden"])

def navigation_tab():
    st.header("Navigation Details")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Next Port")
        st.date_input("ETA Date", datetime.now())
        st.time_input("ETA Time", datetime.now().time())
        st.number_input("Speed required to achieve Scheduled ETA (kts)", min_value=0.0, step=0.1)
        st.date_input("ETB", datetime.now())
        st.text_input("Latitude")
        st.text_input("Longitude")
    with col2:
        st.date_input("ETC/D", datetime.now())
        st.time_input("ETC/D Time", datetime.now().time())
        st.date_input("Best ETA PBG (LT)", datetime.now())
        st.time_input("Best ETA PBG Time (LT)", datetime.now().time())
        st.date_input("Best ETA PBG (UTC)", datetime.now())
        st.time_input("Best ETA PBG Time (UTC)", datetime.now().time())
        st.number_input("Course (°)", min_value=0.0, max_value=360.0, step=1.0)

    st.subheader("Drifting")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Drifting Start Latitude")
        st.text_input("Drifting Start Longitude")
        st.date_input("Drifting Start Date", datetime.now())
        st.time_input("Drifting Start Time", datetime.now().time())
    with col2:
        st.text_input("Drifting End Latitude")
        st.text_input("Drifting End Longitude")
        st.date_input("Drifting End Date", datetime.now())
        st.time_input("Drifting End Time", datetime.now().time())
        st.number_input("Drifting Distance (nm)", min_value=0.0, step=0.1)
        st.number_input("Drifting Time (hrs)", min_value=0.0, step=0.1)

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

    st.subheader("Forecast next 24 Hrs")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Wind Direction Forecast", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"])
        st.number_input("Wind Force Forecast", min_value=0, max_value=12)
    with col2:
        st.number_input("Sea Height Forecast (m)", min_value=0.0, step=0.1)
        st.selectbox("Sea Direction Forecast", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"])
        st.number_input("Swell Height Forecast (m)", min_value=0.0, step=0.1)

def speed_consumption_tab():
    st.header("Speed and Consumption")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1)
        st.number_input("Full Speed (nm)", min_value=0.0, step=0.1)
        st.number_input("Reduced Speed/Slow Steaming (hrs)", min_value=0.0, step=0.1)
        st.number_input("Reduced Speed/Slow Steaming (nm)", min_value=0.0, step=0.1)
        st.number_input("Stopped (hrs)", min_value=0.0, step=0.1)
        st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1)
    with col2:
        st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1)
        st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1)
        st.number_input("Voyage Average Speed (kts)", min_value=0.0, step=0.1)
        st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1)
        st.number_input("Distance since COSP (nm)", min_value=0.0, step=0.1)
    with col3:
        st.number_input("Voyage Order Speed (kts)", min_value=0.0, step=0.1)
        st.number_input("Voyage Order ME FO Cons (mt)", min_value=0.0, step=0.1)
        st.number_input("Voyage Order ME DO Cons (mt)", min_value=0.0, step=0.1)
        st.number_input("Draft F (m)", min_value=0.0, step=0.01)
        st.number_input("Draft A (m)", min_value=0.0, step=0.01)
        st.number_input("Displacement (mt)", min_value=0.0, step=0.1)

def engine_tab():
    st.header("Engine Information")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("ME Rev Counter", min_value=0, step=1)
        st.number_input("Average RPM", min_value=0.0, step=0.1)
        st.number_input("Avg RPM since COSP", min_value=0.0, step=0.1)
        st.radio("Power Output", ["BHP", "KW"])
        st.number_input("Calculated BHP", min_value=0, step=1)
    with col2:
        st.number_input("Governor Setting or Fuel rack Setting (%)", min_value=0.0, max_value=100.0, step=0.1)
        st.number_input("Speed Setting", min_value=0.0, step=0.1)
        st.number_input("Scav Air Temp (°C)", min_value=0.0, step=0.1)
        st.number_input("Scav Air Press (bar)", min_value=0.0, step=0.1)
        st.number_input("FO Inlet Temp (°C)", min_value=0.0, step=0.1)
    with col3:
        st.number_input("FO Cat Fines (ppm)", min_value=0.0, step=0.1)
        st.number_input("FO Press (bar)", min_value=0.0, step=0.1)
        st.number_input("Exh Temp Max (°C)", min_value=0.0, step=0.1)
        st.number_input("Exh Temp Min (°C)", min_value=0.0, step=0.1)
        st.number_input("Exh Press (bar)", min_value=0.0, step=0.1)

    st.subheader("Auxiliary Engines")
    col1, col2 = st.columns(2)
    with col1:
        for i in range(1, 5):
            st.number_input(f"A/E No.{i} Generator Load (kw)", min_value=0, step=1)
    with col2:
        for i in range(1, 5):
            st.number_input(f"A/E No.{i} Generator Hours of Operation (hrs)", min_value=0.0, step=0.1)
    st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1)
    st.number_input("Earth Fault Monitor 440 Volts (MΩ)", min_value=0.0, step=0.1)
    st.number_input("Earth Fault Monitor 230/110 Volts (MΩ)", min_value=0.0, step=0.1)

def fuel_consumables_tab():
    st.header("Fuel and Consumables")

    st.subheader("Fuel Consumption")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("FO Cons Rate (mt/day)", min_value=0.0, step=0.1)
        st.number_input("DO Cons Rate (mt/day)", min_value=0.0, step=0.1)
        st.number_input("Density @ 15°C", min_value=0.0, step=0.001)
        st.number_input("Sulphur Content %", min_value=0.0, max_value=100.0, step=0.01)
    with col2:
        st.number_input("FO Cons since COSP (mt/day)", min_value=0.0, step=0.1)
        st.number_input("DO Cons since COSP (mt/day)", min_value=0.0, step=0.1)
        st.number_input("Bilge Tank ROB (cu.m)", min_value=0.0, step=0.1)
        st.number_input("Total Sludge Retained onboard (cu.m)", min_value=0.0, step=0.1)

    st.subheader("Detailed Fuel Consumption")
    consumption_data = {
        "Fuel Type": [
            "Heavy Fuel Oil RME-RMK - 380cSt", "Heavy Fuel Oil RMA-RMD - 80cSt",
            "VLSFO RME-RMK Visc >380cSt 0.5%S Max", "VLSFO RMA-RMD Visc >80cSt 0.5%S Max",
            "ULSFO RME-RMK <380cSt 0.1%S Max", "ULSFO RMA-RMD <80cSt 0.1%S Max",
            "VLSMGO 0.5%S Max", "ULSMGO 0.1%S Max",
            "Biofuel - 30", "Biofuel Distillate FO",
            "LPG - Propane", "LPG - Butane",
            "LNG Boil Off", "LNG (Bunkered)"
        ],
        "Previous ROB": [0.0] * 14,
        "At Sea M/E": [0.0] * 14,
        "At Sea A/E": [0.0] * 14,
        "At Sea BLR": [0.0] * 14,
        "At Sea IGG": [0.0] * 14,
        "At Sea GE/EG": [0.0] * 14,
        "At Sea OTH": [0.0] * 14,
        "In Port M/E": [0.0] * 14,
        "In Port A/E": [0.0] * 14,
        "In Port BLR": [0.0] * 14,
        "In Port IGG": [0.0] * 14,
        "In Port GE/EG": [0.0] * 14,
        "In Port OTH": [0.0] * 14,
        "Bunker Qty": [0.0] * 14,
        "Sulphur %": [0.0] * 14,
        "Total": [0.0] * 14,
        "ROB at Noon": [0.0] * 14
    }
    consumption_df = pd.DataFrame(consumption_data)
    st.data_editor(consumption_df, key="consumption_editor", hide_index=True)

    st.subheader("Fresh Water")
    fresh_water_data = {
        "Fresh Water": ["Domestic Fresh Water", "Drinking Water", "Boiler Water", "Tank Cleaning Water"],
        "Previous ROB": [0.0] * 4,
        "Produced": [0.0] * 4,
        "ROB": [0.0] * 4,
        "Consumption": [0.0] * 4
    }
    fresh_water_df = pd.DataFrame(fresh_water_data)
    st.data_editor(fresh_water_df, key="fresh_water_editor", hide_index=True)
    st.number_input("Boiler water Chlorides (ppm)", min_value=0.0, step=0.1)

    st.subheader("Lube Oil Consumptions")
    lube_oil_data = {
        "Lube Oil": ["ME Cylinder Oil", "ME Cylinder Oil 40 TBN", "ME Cylinder Oil 70 TBN", "ME Cylinder Oil 100 TBN", "ME/MT System Oil", "AE System Oil", "AE System Oil 15TBN", "TG System Oil", "Other Lub Oils"],
        "Prev.ROB": [0.0] * 9,
        "Cons": [0.0] * 9,
        "Received": [0.0] * 9,
        "ROB": [0.0] * 9
    }
    lube_oil_df = pd.DataFrame(lube_oil_data)
    st.data_editor(lube_oil_df, key="lube_oil_editor", hide_index=True)

    st.subheader("Bilge and Sludge")
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Last landing of Bilge Water", datetime.now())
        st.number_input("Days since last Bilge Water landing", min_value=0, step=1)
    with col2:
        st.date_input("Last landing of Sludge", datetime.now())
        st.number_input("Days since last Sludge landing", min_value=0, step=1)

    st.subheader("Purifier")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("HFO PFR 1 Operation Hrs", min_value=0.0, step=0.1)
        st.number_input("HFO PFR 2 Operation Hrs", min_value=0.0, step=0.1)
        st.number_input("DO PFR Operation Hrs", min_value=0.0, step=0.1)
    with col2:
        st.number_input("ME LO PFR Operation Hrs", min_value=0.0, step=0.1)
        st.number_input("AE LO PFR Operation Hrs", min_value=0.0, step=0.1)

    st.subheader("Environmental Control Area")
    st.text_input("Fuel Used in ECA")
    st.number_input("Fuel CO Time (hrs)", min_value=0.0, step=0.01)

if __name__ == "__main__":
    main()
