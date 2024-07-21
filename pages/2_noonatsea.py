import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime Report")

def main():
    st.title("Maritime Report")

    tabs = st.tabs(["Deck", "Engine"])

    with tabs[0]:
        deck_tab()

    with tabs[1]:
        engine_tab()

    if st.button("Submit Report", type="primary"):
        st.success("Report submitted successfully!")

def deck_tab():
    st.header("Deck Information")

    with st.expander("General Information", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Vessel Name")
            st.text_input("Voyage No")
            st.text_input("Cargo No")
            st.selectbox("Vessel's Status", ["At Sea", "In Port"])
            st.text_input("Current Port")
            st.text_input("Last Port")
            st.text_input("Berth / Location")
        with col2:
            st.date_input("Report Date (LT)", datetime.now().date())
            st.time_input("Report Time (LT)", datetime.now().time())
            st.date_input("Report Date (UTC)", datetime.now().date())
            st.time_input("Report Time (UTC)", datetime.now().time())
            st.text_input("IDL Crossing")
            st.selectbox("IDL Direction", ["--Select--", "East", "West"])
            st.checkbox("Off Port Limits")
        with col3:
            st.text_input("Next Port")
            st.date_input("ETA Date", datetime.now().date())
            st.time_input("ETA Time", datetime.now().time())
            st.number_input("Speed required to achieve Scheduled ETA (kts)", min_value=0.0, step=0.1)
            st.date_input("ETB", datetime.now().date())
            st.date_input("ETC/D", datetime.now().date())
            st.radio("Ballast/Laden", ["Ballast", "Laden"])

    with st.expander("Speed and Consumption", expanded=True):
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
            st.number_input("Course (°)", min_value=0.0, step=1.0)
            st.number_input("Draft F (m)", min_value=0.0, step=0.01)
            st.number_input("Draft A (m)", min_value=0.0, step=0.01)
            st.number_input("Displacement (mt)", min_value=0.0, step=0.1)

    with st.expander("Position and Navigation"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Latitude")
            st.text_input("Longitude")
        with col2:
            st.date_input("Best ETA PBG (LT)", datetime.now().date())
            st.time_input("Best ETA PBG Time (LT)", datetime.now().time())
            st.date_input("Best ETA PBG (UTC)", datetime.now().date())
            st.time_input("Best ETA PBG Time (UTC)", datetime.now().time())

    with st.expander("Weather"):
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
            st.number_input("Air Temp (°C)", min_value=-50.0, step=0.1)
            st.checkbox("Icing on Deck?")
        st.number_input("Period of bad Weather (beyond BF scale 5, in Hours)", min_value=0.0, step=0.1)

    with st.expander("Special Areas"):
        col1, col2 = st.columns(2)
        with col1:
            st.radio("Is vessel currently in Gulf of Aden / HRA or will be Transiting Gulf of Aden / HRA within next 14 days?", ["Yes", "No"])
            st.date_input("Entry into HRA Date", datetime.now().date())
            st.time_input("Entry into HRA Time", datetime.now().time())
            st.date_input("Exit from HRA Date", datetime.now().date())
            st.time_input("Exit from HRA Time", datetime.now().time())
        with col2:
            st.radio("Is vessel in an ECA area or will enter ECA area within next 3 days?", ["Yes", "No"])
            st.date_input("Entry into ECA Date", datetime.now().date())
            st.time_input("Entry into ECA Time", datetime.now().time())
            st.date_input("Exit from ECA Date", datetime.now().date())
            st.time_input("Exit from ECA Time", datetime.now().time())
            st.text_input("Latitude (ECA)")
            st.text_input("Longitude (ECA)")
            st.text_input("Fuel used in ECA")
            st.time_input("Fuel C/O Time", datetime.now().time())

    with st.expander("Breaching International Navigating Limits"):
        col1, col2 = st.columns(2)
        with col1:
            st.radio("Is the vessel in IWL Breach area or will enter IWL Breach area within next 7 days?", ["Yes", "No"])
            st.date_input("Entry into IWL Breach Date", datetime.now().date())
            st.time_input("Entry into IWL Breach Time", datetime.now().time())
        with col2:
            st.date_input("Exit from IWL Breach Date", datetime.now().date())
            st.time_input("Exit from IWL Breach Time", datetime.now().time())

    with st.expander("Drifting"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Drifting Start Latitude")
            st.text_input("Drifting Start Longitude")
            st.date_input("Drifting Start Date", datetime.now().date())
            st.time_input("Drifting Start Time", datetime.now().time())
            st.number_input("Drifting Distance (nm)", min_value=0.0, step=0.1)
        with col2:
            st.text_input("Drifting End Latitude")
            st.text_input("Drifting End Longitude")
            st.date_input("Drifting End Date", datetime.now().date())
            st.time_input("Drifting End Time", datetime.now().time())
            st.number_input("Drifting Time (hrs)", min_value=0.0, step=0.1)


def engine_tab():
    st.header("Engine Information")

    with st.expander("Main Engine", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("ME Rev Counter", min_value=0, step=1)
            st.number_input("Average RPM", min_value=0.0, step=0.1)
            st.number_input("Avg RPM since COSP", min_value=0.0, step=0.1)
            st.radio("Power Output", ["BHP", "KW"])
            st.number_input("Calculated BHP", min_value=0, step=1)
        with col2:
            st.number_input("Governor Setting or Fuel rack Setting (%)", min_value=0.0, step=0.1)
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

    with st.expander("Auxiliary Engines"):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("A/E No.1 Generator Load (kw)", min_value=0, step=1)
            st.number_input("A/E No.2 Generator Load (kw)", min_value=0, step=1)
            st.number_input("A/E No.3 Generator Load (kw)", min_value=0, step=1)
            st.number_input("A/E No.4 Generator Load (kw)", min_value=0, step=1)
        with col2:
            st.number_input("A/E No.1 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1)
            st.number_input("A/E No.2 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1)
            st.number_input("A/E No.3 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1)
            st.number_input("A/E No.4 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1)
        st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1)

    with st.expander("Lube Oil Consumptions"):
        lube_oil_data = {
            "Lube Oil": ["ME Cylinder Oil", "ME Cylinder Oil 40 TBN", "ME Cylinder Oil 70 TBN", "ME Cylinder Oil 100 TBN", "ME/MT System Oil", "AE System Oil", "AE System Oil 15TBN", "TG System Oil", "Other Lub Oils"],
            "Prev.ROB": [0.0] * 9,
            "Cons": [0.0] * 9,
            "Received": [0.0] * 9,
            "ROB": [0.0] * 9
        }
        lube_oil_df = pd.DataFrame(lube_oil_data)
        st.data_editor(lube_oil_df)

    with st.expander("Fresh Water"):
        fresh_water_data = {
            "Fresh Water": ["Domestic Fresh Water", "Drinking Water", "Boiler Water", "Tank Cleaning Water"],
            "Previous ROB": [0.0] * 4,
            "Produced": [0.0] * 4,
            "ROB": [0.0] * 4,
            "Consumption": [0.0] * 4
        }
        fresh_water_df = pd.DataFrame(fresh_water_data)
        st.data_editor(fresh_water_df)

    with st.expander("Fuel Consumption"):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("FO Cons Rate (mt/day)", min_value=0.0, step=0.1)
            st.number_input("DO Cons Rate (mt/day)", min_value=0.0, step=0.1)
            st.number_input("Density @ 15°C", min_value=0.0, step=0.001)
            st.number_input("Sulphur Content %", min_value=0.0, step=0.01)
        with col2:
            st.number_input("FO Cons since COSP (mt/day)", min_value=0.0, step=0.1)
            st.number_input("DO Cons since COSP (mt/day)", min_value=0.0, step=0.1)
            st.number_input("Bilge Tank ROB (cu.m)", min_value=0.0, step=0.1)
            st.number_input("Total Sludge Retained onboard (cu.m)", min_value=0.0, step=0.1)

    with st.expander("Detailed Fuel Consumption"):
        consumptions_data = {
            "Oil Type": [
                "Heavy Fuel Oil RME-RMK - 80cSt", "Heavy Fuel Oil RMA-RMD - 80cSt",
                "VLSFO RME-RMK Visc >80cSt 0.5%S Max", "VLSFO RMA-RMD Visc >80cSt 0.5%S Max",
                "ULSFO RME-RMK <80cSt 0.1%S Max", "ULSFO RMA-RMD <80cSt 0.1%S Max",
                "VLSMGO 0.5%S Max", "ULSMGO 0.1%S Max",
                "Biofuel - 30", "Biofuel Distillate FO",
                "LPG - Propane", "LPG - Butane",
                "LNG Boil Off", "LNG (Bunkered)"
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
            "Total": [0.0] * 14,
            "ROB at Noon": [0.0] * 14
        }
        consumptions_df = pd.DataFrame(consumptions_data)
        st.data_editor(consumptions_df)

if __name__ == "__main__":
    main()
