import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Noon Reporting Portal")

def main():
    st.title("Noon Reporting Portal")

    sections = [
        "General Information",
        "Voyage Details",
        "Position and Navigation",
        "Weather and Sea Conditions",
        "Time Elapsed",
        "Cargo Operations",
        "Fuel Consumption",
        "Engine Performance",
        "Auxiliary Systems",
        "Environmental Compliance",
        "Fresh Water",
        "Lubricating Oil",
        "Vessel Performance",
        "Special Events and Remarks"
    ]

    for section in sections:
        with st.expander(section, expanded=False):
            globals()[f"display_{section.lower().replace(' ', '_')}"]()

    if st.button("Submit Report", type="primary"):
        st.success("Report submitted successfully!")

def display_general_information():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("IMO Number")
        st.date_input("Date (Local)", value=datetime.now())
        st.time_input("Time (Local)", value=datetime.now().time())
        
    with col2:
        st.text_input("Vessel Name")
        st.date_input("Date (UTC)", value=datetime.now())
        st.time_input("Time (UTC)", value=datetime.now().time())
       
    with col3:
        st.text_input("Vessel Type")
        
def display_voyage_details():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Voyage From")
        st.text_input("Voyage To")
        st.text_input("Voyage ID")
        st.text_input("Segment ID")
    
    with col2:
        st.selectbox("Voyage Type", ["", "One-way", "Round trip", "STS"])
        st.selectbox("Voyage Stage", ["", "East", "West", "Ballast", "Laden"])
        st.date_input("ETA", value=datetime.now())
        st.text_input("Speed Order")
    
    with col3:
        st.text_input("Charter Type")
        st.number_input("Time Since Last Report (hours)", min_value=0.0, step=0.1)
        st.selectbox("Clocks Advanced/Retarded", ["", "Advanced", "Retarded"])
        st.number_input("Clocks Changed By (minutes)", min_value=0, step=1)
    
    with col4:
        offhire = st.checkbox("Off-hire")
        eca_transit = st.checkbox("ECA Transit")
        fuel_changeover = st.checkbox("Fuel Changeover")
        idl_crossing = st.checkbox("IDL Crossing")
        
    if offhire:
        st.subheader("Off-hire Details")
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Off-hire Start Date")
            st.time_input("Off-hire Start Time")
        with col2:
            st.date_input("Off-hire End Date")
            st.time_input("Off-hire End Time")
        st.text_area("Off-hire Reason")
    
    if eca_transit:
        st.subheader("ECA Transit Details")
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("ECA Entry Date")
            st.time_input("ECA Entry Time")
            st.text_input("ECA Entry Latitude")
            st.text_input("ECA Entry Longitude")
        with col2:
            st.date_input("ECA Exit Date")
            st.time_input("ECA Exit Time")
            st.text_input("ECA Exit Latitude")
            st.text_input("ECA Exit Longitude")
        st.text_input("ECA Name")
    
    if fuel_changeover:
        st.subheader("Fuel Changeover Details")
        st.subheader("Start of Changeover")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.date_input("Changeover Start Date")
            st.time_input("Changeover Start Time")
        with col2:
            st.text_input("Changeover Start Latitude")
            st.text_input("Changeover Start Longitude")
        with col3:
            st.number_input("VLSFO ROB at Start (MT)", min_value=0.0, step=0.1)
            st.number_input("LSMGO ROB at Start (MT)", min_value=0.0, step=0.1)
        
        st.subheader("End of Changeover")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.date_input("Changeover End Date")
            st.time_input("Changeover End Time")
        with col2:
            st.text_input("Changeover End Latitude")
            st.text_input("Changeover End Longitude")
        with col3:
            st.number_input("VLSFO ROB at End (MT)", min_value=0.0, step=0.1)
            st.number_input("LSMGO ROB at End (MT)", min_value=0.0, step=0.1)
    
    if idl_crossing:
        st.selectbox("IDL Direction", ["East", "West"])

def display_weather_and_sea_conditions():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Wind Direction (°)", min_value=0, max_value=359)
        st.number_input("Wind Force (knots)", min_value=0.0, step=0.1)
        st.number_input("Sea State Direction (°)", min_value=0, max_value=359)
        st.selectbox("Sea State (Douglas Scale)", [""] + [str(i) for i in range(10)])
        st.number_input("Swell Height (m)", min_value=0.0, step=0.1)
    with col2:
        st.number_input("Current Direction (°)", min_value=0, max_value=359)
        st.number_input("Current Speed (knots)", min_value=0.0, step=0.1)
        st.number_input("Air Temperature (°C)", min_value=-50.0, max_value=50.0, step=0.1)
        st.number_input("Sea Temperature (°C)", min_value=-2.0, max_value=35.0, step=0.1)
        st.number_input("Water Depth (m)", min_value=0.0, step=0.1)

def display_time_elapsed():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Time Since Previous Report (hours)", min_value=0.0, step=0.1)
        st.number_input("Time Elapsed Sailing (hours)", min_value=0.0, step=0.1)
        st.number_input("Time Elapsed Anchoring (hours)", min_value=0.0, step=0.1)
        st.number_input("Time Elapsed DP (hours)", min_value=0.0, step=0.1)
    with col2:
        st.number_input("Time Elapsed Ice (hours)", min_value=0.0, step=0.1)
        st.number_input("Time Elapsed Maneuvering (hours)", min_value=0.0, step=0.1)
        st.number_input("Time Elapsed Waiting (hours)", min_value=0.0, step=0.1)
        st.number_input("Time Elapsed Loading/Unloading (hours)", min_value=0.0, step=0.1)

def display_cargo_operations():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Cargo Weight (MT)", min_value=0.0, step=0.1)
        st.number_input("Cargo Volume (m³)", min_value=0.0, step=0.1)
        st.number_input("Number of Passengers", min_value=0, step=1)
        st.number_input("Total TEU", min_value=0, step=1)
    with col2:
        st.number_input("Reefer TEU", min_value=0, step=1)
        st.number_input("Reefer 20ft Chilled", min_value=0, step=1)
        st.number_input("Reefer 40ft Chilled", min_value=0, step=1)
        st.number_input("Reefer 20ft Frozen", min_value=0, step=1)
        st.number_input("Reefer 40ft Frozen", min_value=0, step=1)

def display_fuel_consumption():
    fuel_types = ["HFO", "LFO", "MGO", "MDO", "LPGP", "LPGB", "LNG", "Methanol", "Ethanol", "Other"]
    consumers = ["ME", "AE", "Boiler", "Inert Gas"]
    
    for consumer in consumers:
        st.subheader(f"{consumer} Consumption")
        cols = st.columns(5)
        for i, fuel in enumerate(fuel_types):
            cols[i % 5].number_input(f"{consumer} {fuel} (MT)", min_value=0.0, step=0.1, key=f"{consumer}_{fuel}")

def display_engine_performance():
    st.subheader("Main Engine")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("ME Load (kW)", min_value=0, step=1)
        st.number_input("ME Load Percentage (%)", min_value=0.0, max_value=100.0, step=0.1)
        st.number_input("ME Speed (RPM)", min_value=0, step=1)
    with col2:
        st.number_input("ME SFOC (g/kWh)", min_value=0.0, step=0.1)
        st.number_input("ME SFOC ISO Corrected (g/kWh)", min_value=0.0, step=0.1)
        st.number_input("ME Running Hours", min_value=0.0, step=0.1)
    with col3:
        st.number_input("ME Work (kWh)", min_value=0, step=1)
        st.number_input("ME Average Load (kW)", min_value=0, step=1)
        st.number_input("ME Average Load Percentage (%)", min_value=0.0, max_value=100.0, step=0.1)

    st.subheader("Auxiliary Engine")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("AE Load (kW)", min_value=0, step=1)
        st.number_input("AE SFOC (g/kWh)", min_value=0.0, step=0.1)
        st.number_input("AE SFOC ISO Corrected (g/kWh)", min_value=0.0, step=0.1)
    with col2:
        st.number_input("AE Running Hours", min_value=0.0, step=0.1)
        st.number_input("AE Average Load (kW)", min_value=0, step=1)
        st.number_input("AE Work (kWh)", min_value=0, step=1)

def display_auxiliary_systems():
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Boiler 1 Operation Mode")
        st.number_input("Boiler 1 Feed Water Flow (m³/min)", min_value=0.0, step=0.1)
        st.number_input("Boiler 1 Steam Pressure (bar)", min_value=0.0, step=0.1)
        st.number_input("Boiler 1 Running Hours", min_value=0.0, step=0.1)
    with col2:
        st.number_input("Air Compressor 1 Running Time (hours)", min_value=0.0, step=0.1)
        st.number_input("Air Compressor 2 Running Time (hours)", min_value=0.0, step=0.1)
        st.number_input("Thruster 1 Running Time (hours)", min_value=0.0, step=0.1)
        st.number_input("Thruster 2 Running Time (hours)", min_value=0.0, step=0.1)

def display_environmental_compliance():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Total Fuel ROB (MT)", min_value=0.0, step=0.1)
        st.number_input("HFO ROB (MT)", min_value=0.0, step=0.1)
        st.number_input("LFO ROB (MT)", min_value=0.0, step=0.1)
        st.number_input("MGO ROB (MT)", min_value=0.0, step=0.1)
    with col2:
        st.number_input("MDO ROB (MT)", min_value=0.0, step=0.1)
        st.number_input("LNG ROB (MT)", min_value=0.0, step=0.1)
        st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1)
        st.number_input("Shore Side Electricity Reception (kWh)", min_value=0, step=1)

def display_fresh_water():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Fresh Water Bunkered (m³)", min_value=0.0, step=0.1)
        st.number_input("Fresh Water Consumption - Drinking (m³)", min_value=0.0, step=0.1)
        st.number_input("Fresh Water Consumption - Technical (m³)", min_value=0.0, step=0.1)
    with col2:
        st.number_input("Fresh Water Consumption - Washing (m³)", min_value=0.0, step=0.1)
        st.number_input("Fresh Water Produced (m³)", min_value=0.0, step=0.1)
        st.number_input("Fresh Water ROB (m³)", min_value=0.0, step=0.1)

def display_lubricating_oil():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("ME Cylinder Oil ROB (liters)", min_value=0, step=1)
        st.number_input("ME Cylinder Oil High BN ROB (liters)", min_value=0, step=1)
        st.number_input("ME Cylinder Oil Low BN ROB (liters)", min_value=0, step=1)
        st.number_input("ME System Oil ROB (liters)", min_value=0, step=1)
    with col2:
        st.number_input("AE System Oil ROB (liters)", min_value=0, step=1)
        st.number_input("ME Cylinder Oil Consumption (liters)", min_value=0, step=1)
        st.number_input("ME Cylinder Oil Feed Rate (g/kWh)", min_value=0.0, step=0.1)
        st.number_input("ME System Oil Consumption (liters)", min_value=0, step=1)

def display_vessel_performance():
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Draft Actual Fore (m)", min_value=0.0, step=0.01)
        st.number_input("Draft Actual Aft (m)", min_value=0.0, step=0.01)
        st.number_input("Draft Recommended Fore (m)", min_value=0.0, step=0.01)
        st.number_input("Draft Recommended Aft (m)", min_value=0.0, step=0.01)
    with col2:
        st.number_input("Propeller Pitch (m)", min_value=0.0, step=0.01)
        st.number_input("Propeller Pitch Ratio", min_value=0.0, step=0.01)
        st.number_input("Average Propeller Speed (RPM)", min_value=0, step=1)
        st.number_input("Slip (%)", min_value=0.0, max_value=100.0, step=0.1)
        st.number_input("ME Projected Consumption (MT/day)", min_value=0.0, step=0.1)
        st.number_input("AE Projected Consumption (MT/day)", min_value=0.0, step=0.1)

def display_special_events_and_remarks():
    st.selectbox("Operation Mode", ["", "At Sea", "In Port", "Maneuvering", "Anchoring", "Drifting"])
    st.selectbox("Cleaning Event", ["", "Propeller Cleaning", "Hull Cleaning", "Tank Cleaning"])
    st.number_input("Number of Tugs", min_value=0, step=1)
    st.text_input("Reason for Schedule Deviation")
    st.text_area("Remarks")
    st.text_input("Entry Made By (Deck)")
    st.text_input("Entry Made By (Engine)")
    st.text_input("Contact Email")
    st.date_input("Reporting Date", value=datetime.now())

if __name__ == "__main__":
    main()
