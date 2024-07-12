import streamlit as st
import random
import string
from datetime import datetime
import pytz

# Constants
PORTS = [
    "Singapore", "Rotterdam", "Shanghai", "Ningbo-Zhoushan", "Guangzhou Harbor", "Busan",
    "Qingdao", "Hong Kong", "Tianjin", "Port Klang", "Antwerp", "Dubai Ports", "Xiamen",
    "Kaohsiung", "Hamburg", "Los Angeles", "Tanjung Pelepas", "Laem Chabang", "New York-New Jersey",
    "Dalian", "Tanjung Priok", "Valencia", "Colombo", "Ho Chi Minh City", "Algeciras"
]

VESSEL_PREFIXES = ["MV", "SS", "MT", "MSC", "CMA CGM", "OOCL", "Maersk", "Evergreen", "Cosco", "NYK"]
VESSEL_NAMES = ["Horizon", "Voyager", "Pioneer", "Adventurer", "Explorer", "Discovery", "Navigator", "Endeavour", "Challenger", "Trailblazer"]
VESSEL_TYPES = ["Oil Tanker", "LPG Tanker", "LNG Tanker"]

REPORT_TYPES = [
    "Arrival", "Departure", "Begin of sea passage", "End of sea passage",
    "Noon (Position) - Sea passage", "Noon (Position) - Port",
    "Noon (Position) - River", "Noon (Position) - Stoppage"
]

# Updated SECTION_FIELDS
SECTION_FIELDS = {
    "Vessel Data": ["Vessel Name", "Vessel IMO", "Vessel Type"],
    "Voyage Data": ["Local Date", "Local Time", "UTC Offset", "Voyage ID", "Segment ID", "From Port", "To Port"],
    "Event Data": ["Event Type", "Time Elapsed (hours)", "Sailing Time (hours)", "Anchor Time (hours)", "Ice Time (hours)", "Maneuvering (hours)", "Loading/Unloading (hours)", "Drifting (hours)"],
    "Position": ["Latitude Degrees", "Latitude Minutes", "Latitude Direction", "Longitude Degrees", "Longitude Minutes", "Longitude Direction"],
    "Cargo": {
        "Oil Tanker": ["Cargo Weight (mt)"],
        "LPG Tanker": ["Cargo Volume (m3)"],
        "LNG Tanker": ["Cargo Volume (m3)"]
    },
    "Fuel Consumption": {
        "Oil Tanker": {
            "Main Engine": ["ME LFO (mt)", "ME MGO (mt)", "ME LNG (mt)", "ME Other (mt)", "ME Other Fuel Type"],
            "Auxiliary Engines": ["AE LFO (mt)", "AE MGO (mt)", "AE LNG (mt)", "AE Other (mt)", "AE Other Fuel Type"],
            "Boilers": ["Boiler LFO (mt)", "Boiler MGO (mt)", "Boiler LNG (mt)", "Boiler Other (mt)", "Boiler Other Fuel Type"],
            "IGG": ["IGG LFO (mt)", "IGG MGO (mt)", "IGG LNG (mt)", "IGG Other (mt)", "IGG Other Fuel Type"]
        },
        "LPG Tanker": {
            "Main Engine": ["ME LFO (mt)", "ME MGO (mt)", "ME LNG (mt)", "ME LPG Propane (mt)", "ME LPG Butane (mt)", "ME Other (mt)", "ME Other Fuel Type"],
            "Auxiliary Engines": ["AE LFO (mt)", "AE MGO (mt)", "AE LNG (mt)", "AE LPG Propane (mt)", "AE LPG Butane (mt)", "AE Other (mt)", "AE Other Fuel Type"],
            "Boilers": ["Boiler LFO (mt)", "Boiler MGO (mt)", "Boiler LNG (mt)", "Boiler LPG Propane (mt)", "Boiler LPG Butane (mt)", "Boiler Other (mt)", "Boiler Other Fuel Type"]
        },
        "LNG Tanker": {
            "Main Engine": ["ME LFO (mt)", "ME MGO (mt)", "ME LNG (mt)", "ME Other (mt)", "ME Other Fuel Type"],
            "Auxiliary Engines": ["AE LFO (mt)", "AE MGO (mt)", "AE LNG (mt)", "AE Other (mt)", "AE Other Fuel Type"],
            "Boilers": ["Boiler LFO (mt)", "Boiler MGO (mt)", "Boiler LNG (mt)", "Boiler Other (mt)", "Boiler Other Fuel Type"],
            "IGG": ["IGG LFO (mt)", "IGG MGO (mt)", "IGG LNG (mt)", "IGG Other (mt)", "IGG Other Fuel Type"],
            "GCU": ["GCU LFO (mt)", "GCU MGO (mt)", "GCU LNG (mt)", "GCU Other (mt)", "GCU Other Fuel Type"]
        }
    },
    "ROB": ["LFO ROB (mt)", "MGO ROB (mt)", "LNG ROB (mt)", "Other ROB (mt)", "Other Fuel Type ROB", "Total Fuel ROB (mt)"],
    "Fuel Allocation": {
        "Oil Tanker": {
            "Cargo Heating": ["Cargo Heating LFO (mt)", "Cargo Heating MGO (mt)", "Cargo Heating LNG (mt)", "Cargo Heating Other (mt)", "Cargo Heating Other Fuel Type"]
        },
        "LPG Tanker": {
            "Cargo Cooling": ["Cargo Cooling LFO (mt)", "Cargo Cooling MGO (mt)", "Cargo Cooling LNG (mt)", "Cargo Cooling LPG Propane (mt)", "Cargo Cooling LPG Butane (mt)", "Cargo Cooling Other (mt)", "Cargo Cooling Other Fuel Type"]
        },
        "LNG Tanker": {
            "Cargo Cooling": ["Cargo Cooling LFO (mt)", "Cargo Cooling MGO (mt)", "Cargo Cooling LNG (mt)", "Cargo Cooling Other (mt)", "Cargo Cooling Other Fuel Type"]
        }
    },
    "Machinery": {
        "Main Engine": ["ME Load (kW)", "ME Load Percentage (%)", "ME Speed (RPM)", "ME Propeller Pitch (m)", "ME Propeller Pitch Ratio", "ME Shaft Generator Power (kW)", "ME Charge Air Inlet Temp (°C)", "ME Scav. Air Pressure (bar)", "ME SFOC (g/kWh)", "ME SFOC ISO Corrected (g/kWh)"],
        "Auxiliary Engines": {
            "Auxiliary Engine 1": ["AE1 Load (kW)", "AE1 Charge Air Inlet Temp (°C)", "AE1 Charge Air Pressure (bar)", "AE1 SFOC (g/kWh)", "AE1 SFOC ISO Corrected (g/kWh)"],
            "Auxiliary Engine 2": ["AE2 Load (kW)", "AE2 Charge Air Inlet Temp (°C)", "AE2 Charge Air Pressure (bar)", "AE2 SFOC (g/kWh)", "AE2 SFOC ISO Corrected (g/kWh)"],
            "Auxiliary Engine 3": ["AE3 Load (kW)", "AE3 Charge Air Inlet Temp (°C)", "AE3 Charge Air Pressure (bar)", "AE3 SFOC (g/kWh)", "AE3 SFOC ISO Corrected (g/kWh)"]
        }
    },
    "Weather": {
        "Wind": ["Wind Direction (degrees)", "Wind Speed (knots)", "Wind Force (Beaufort)"],
        "Sea State": ["Sea State Direction (degrees)", "Sea State Force (Douglas scale)", "Sea State Period (seconds)"],
        "Swell": ["Swell Direction (degrees)", "Swell Height (meters)", "Swell Period (seconds)"],
        "Current": ["Current Direction (degrees)", "Current Speed (knots)"],
        "Temperature": ["Air Temperature (°C)", "Sea Temperature (°C)"]
    },
    "Draft": {
        "Actual": ["Actual Forward Draft (m)", "Actual Aft Draft (m)", "Displacement (mt)", "Water Depth (m)"]
    }
}

# Helper functions
def generate_random_position():
    lat_deg = random.randint(0, 89)
    lat_min = round(random.uniform(0, 59.99), 2)
    lat_dir = random.choice(['N', 'S'])
    lon_deg = random.randint(0, 179)
    lon_min = round(random.uniform(0, 59.99), 2)
    lon_dir = random.choice(['E', 'W'])
    return lat_deg, lat_min, lat_dir, lon_deg, lon_min, lon_dir

def generate_random_consumption():
    me_lfo = round(random.uniform(20, 25), 1)
    ae_lfo = round(random.uniform(2, 3), 1)
    return me_lfo, ae_lfo

def generate_random_vessel_name():
    return f"{random.choice(VESSEL_PREFIXES)} {random.choice(VESSEL_NAMES)}"

def generate_random_imo():
    return ''.join(random.choices(string.digits, k=7))

def create_fields(fields, prefix, report_type, vessel_type):
    cols = st.columns(4)
    for i, field in enumerate(fields):
        with cols[i % 4]:
            field_key = f"{prefix}_{field.lower().replace(' ', '_')}"
            if field == "Vessel Type":
                st.selectbox(field, options=VESSEL_TYPES, key=field_key)
            elif "LFO (mt)" in field or "MGO (mt)" in field or "LNG (mt)" in field or "Other (mt)" in field or "LPG Propane (mt)" in field or "LPG Butane (mt)" in field:
                st.number_input(field, min_value=0.0, step=0.1, key=field_key)
            elif any(unit in field for unit in ["(%)", "(mt)", "(kW)", "(°C)", "(bar)", "(g/kWh)", "(knots)", "(meters)", "(seconds)", "(degrees)"]):
                st.number_input(field, key=field_key)
            elif "Direction" in field and "degrees" not in field:
                st.selectbox(field, options=["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=field_key)
            else:
                st.text_input(field, key=field_key)

def create_form(report_type, vessel_type):
    st.header(f"New {report_type} Report for {vessel_type}")
    
    for section, fields in SECTION_FIELDS.items():
        with st.expander(section, expanded=False):
            st.subheader(section)
            if isinstance(fields, dict):
                if section in ["Cargo", "Fuel Consumption", "Fuel Allocation"]:
                    fields = fields.get(vessel_type, {})
                for subsection, subfields in fields.items():
                    st.subheader(subsection)
                    create_fields(subfields, f"{report_type}_{section}_{subsection}", report_type, vessel_type)
            elif isinstance(fields, list):
                create_fields(fields, f"{report_type}_{section}", report_type, vessel_type)

    if st.button("Submit Report"):
        st.success(f"{report_type} for {vessel_type} submitted successfully!")

def main():
    st.set_page_config(layout="wide", page_title="Maritime Reporting System")
    st.title("Maritime Reporting System")

    # Vessel Type Selector
    vessel_type = st.selectbox("Select Vessel Type", options=VESSEL_TYPES)

    # Report Type Selector
    report_type = st.selectbox("Select Report Type", options=REPORT_TYPES)

    # Create Form
    create_form(report_type, vessel_type)

if __name__ == "__main__":
    main()
