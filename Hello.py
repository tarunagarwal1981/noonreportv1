import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(layout="wide", page_title="Maritime Reporting System")

def main():
    st.title("Maritime Reporting System")

    report_type = st.sidebar.selectbox("Select Report Type", ["Noon Report", "Departure Report"])

    if report_type == "Noon Report":
        noon_report()
    elif report_type == "Departure Report":
        departure_report()

def noon_report():
    st.header("Noon Report")
    
    tabs = st.tabs(["General Info", "Navigation", "Weather", "Engine", "Consumables"])
    
    with tabs[0]:
        general_info_section()
    
    with tabs[1]:
        navigation_section()
    
    with tabs[2]:
        weather_section()
    
    with tabs[3]:
        engine_section()
    
    with tabs[4]:
        consumables_section()

    if st.button("Submit Noon Report"):
        st.success("Noon Report submitted successfully!")

def departure_report():
    st.header("Departure Report")
    
    tabs = st.tabs(["Departure Info", "Cargo", "Bunkers", "Voyage Plan"])
    
    with tabs[0]:
        departure_info_section()
    
    with tabs[1]:
        cargo_section()
    
    with tabs[2]:
        bunkers_section()
    
    with tabs[3]:
        voyage_plan_section()

    if st.button("Submit Departure Report"):
        st.success("Departure Report submitted successfully!")

def general_info_section():
    st.subheader("General Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Vessel Name")
        st.text_input("IMO Number")
        st.date_input("Date (UTC)")
    with col2:
        st.time_input("Time (UTC)")
        st.number_input("Time Zone", min_value=-12, max_value=12)
        st.text_input("Master's Name")
    with col3:
        st.text_input("Voyage Number")
        st.selectbox("Report Type", ["Daily", "Arrival", "Departure", "Noon", "Midnight"])

def navigation_section():
    st.subheader("Navigation Details")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Latitude")
        st.text_input("Longitude")
        st.number_input("Course", min_value=0, max_value=359)
    with col2:
        st.number_input("Speed (knots)", min_value=0.0, step=0.1)
        st.number_input("Distance Run (NM)", min_value=0.0, step=0.1)
        st.text_input("Next Port")

def weather_section():
    st.subheader("Weather and Environmental Conditions")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.selectbox("Wind Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
        st.number_input("Wind Speed (knots)", min_value=0)
        st.number_input("Sea State (Douglas Scale)", min_value=0, max_value=9)
    with col2:
        st.number_input("Air Temperature (°C)", step=0.1)
        st.number_input("Water Temperature (°C)", step=0.1)
        st.number_input("Atmospheric Pressure (hPa)", min_value=900, max_value=1100)
    with col3:
        st.selectbox("Visibility", ["Good", "Moderate", "Poor"])
        st.multiselect("Weather Conditions", ["Clear", "Partly Cloudy", "Overcast", "Rain", "Snow", "Fog"])

def engine_section():
    st.subheader("Engine and Performance Data")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Main Engine RPM")
        st.number_input("Main Engine Power (%)", min_value=0, max_value=100)
        st.number_input("Shaft Generator Power (kW)")
    with col2:
        st.number_input("Auxiliary Engine 1 Load (%)", min_value=0, max_value=100)
        st.number_input("Auxiliary Engine 2 Load (%)", min_value=0, max_value=100)
        st.number_input("Boiler Steam Production (t/h)")

def consumables_section():
    st.subheader("Fuel and Consumables")
    
    fuel_data = {
        "Fuel Type": ["HFO", "LSFO", "MGO", "LNG"],
        "Consumption (mt)": [0.0, 0.0, 0.0, 0.0],
        "ROB (mt)": [0.0, 0.0, 0.0, 0.0]
    }
    st.dataframe(pd.DataFrame(fuel_data).set_index("Fuel Type"))
    
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Fresh Water Consumption (m³)")
        st.number_input("Fresh Water ROB (m³)")
    with col2:
        st.number_input("Lube Oil Consumption (L)")
        st.number_input("Lube Oil ROB (L)")

def departure_info_section():
    st.subheader("Departure Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Port of Departure")
        st.date_input("Date of Departure (UTC)")
        st.time_input("Time of Departure (UTC)")
    with col2:
        st.text_input("Berth/Terminal")
        st.number_input("Draft Forward (m)", min_value=0.0, step=0.01)
        st.number_input("Draft Aft (m)", min_value=0.0, step=0.01)
    with col3:
        st.text_input("Next Port")
        st.date_input("ETA Next Port")
        st.time_input("ETA Time Next Port")

def cargo_section():
    st.subheader("Cargo Information")
    cargo_types = st.multiselect("Cargo Types", ["Containers", "Bulk", "Liquid", "Break Bulk", "Ro-Ro"])
    
    for cargo in cargo_types:
        st.number_input(f"{cargo} Cargo Quantity", min_value=0.0)
    
    st.number_input("Total Cargo Weight (mt)", min_value=0.0)
    st.number_input("Deadweight (mt)", min_value=0.0)

def bunkers_section():
    st.subheader("Bunkers on Departure")
    bunker_data = {
        "Fuel Type": ["HFO", "LSFO", "MGO", "LNG"],
        "Quantity (mt)": [0.0, 0.0, 0.0, 0.0],
        "Sulphur Content (%)": [0.0, 0.0, 0.0, 0.0]
    }
    st.dataframe(pd.DataFrame(bunker_data).set_index("Fuel Type"))

def voyage_plan_section():
    st.subheader("Voyage Plan")
    st.text_area("Route Description")
    st.number_input("Estimated Distance (NM)", min_value=0.0)
    st.number_input("Estimated Average Speed (knots)", min_value=0.0, step=0.1)
    st.text_input("Estimated Fuel Consumption (mt)")
    st.text_area("Additional Remarks")

if __name__ == "__main__":
    main()
