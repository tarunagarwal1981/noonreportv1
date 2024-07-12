import streamlit as st
import random
import string
from datetime import datetime
import pytz

# Set page config
st.set_page_config(layout="wide", page_title="AI-Enhanced Maritime Reporting System")

# Custom CSS for compact layout and field prompts
st.markdown("""
<style>
    .reportSection { padding-right: 1rem; }
    .stButton > button { width: 100%; }
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 100%; }
    h1, h2, h3 { margin-top: 0; font-size: 1.5em; line-height: 1.3; padding: 0.5rem 0; }
    .stAlert { margin-top: 1rem; }
    .stNumberInput, .stTextInput, .stSelectbox { 
        padding-bottom: 0.5rem !important; 
    }
    .stNumberInput input, .stTextInput input, .stSelectbox select {
        padding: 0.3rem !important;
        font-size: 0.9em !important;
    }
    .stExpander { 
        border: none !important; 
        box-shadow: none !important;
        margin-bottom: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Constants
PORTS = [
    "Singapore", "Rotterdam", "Shanghai", "Ningbo-Zhoushan", "Guangzhou Harbor", "Busan",
    "Qingdao", "Hong Kong", "Tianjin", "Port Klang", "Antwerp", "Dubai Ports", "Xiamen",
    "Kaohsiung", "Hamburg", "Los Angeles", "Tanjung Pelepas", "Laem Chabang", "New York-New Jersey",
    "Dalian", "Tanjung Priok", "Valencia", "Colombo", "Ho Chi Minh City", "Algeciras"
]

VESSEL_PREFIXES = ["MV", "SS", "MT", "MSC", "CMA CGM", "OOCL", "Maersk", "Evergreen", "Cosco", "NYK"]
VESSEL_NAMES = ["Horizon", "Voyager", "Pioneer", "Adventurer", "Explorer", "Discovery", "Navigator", "Endeavour", "Challenger", "Trailblazer"]

VESSEL_TYPES = ["Oil Tanker", "LPG Tanker", "LNG Tanker", "Container"]

REPORT_TYPES = [
    "Arrival", "Departure", "Begin of offhire", "End of offhire", "Arrival STS",
    "Departure STS", "STS", "Begin canal passage", "End canal passage",
    "Begin of sea passage", "End of sea passage", "Begin Anchoring/Drifting",
    "End Anchoring/Drifting", "Noon (Position) - Sea passage", "Noon (Position) - Port",
    "Noon (Position) - River", "Noon (Position) - Stoppage", "ETA update",
    "Begin fuel change over", "End fuel change over", "Change destination (Deviation)",
    "Begin of deviation", "End of deviation", "Entering special area", "Leaving special area",
    "Other event", "Bunkering"
]

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
            "IGG": ["IGG LFO (mt)", "IGG MGO (mt)", "IGG LNG (mt)", "IGG Other (mt)", "IGG Other Fuel Type"],
            "Incinerator": ["Incinerator MGO (mt)"]
        },
        "LPG Tanker": {
            "Main Engine": ["ME LFO (mt)", "ME MGO (mt)", "ME LNG (mt)", "ME LPG Propane (mt)", "ME LPG Butane (mt)", "ME Other (mt)", "ME Other Fuel Type"],
            "Auxiliary Engines": ["AE LFO (mt)", "AE MGO (mt)", "AE LNG (mt)", "AE LPG Propane (mt)", "AE LPG Butane (mt)", "AE Other (mt)", "AE Other Fuel Type"],
            "Boilers": ["Boiler LFO (mt)", "Boiler MGO (mt)", "Boiler LNG (mt)", "Boiler LPG Propane (mt)", "Boiler LPG Butane (mt)", "Boiler Other (mt)", "Boiler Other Fuel Type"],
            "IGG": ["IGG LFO (mt)", "IGG MGO (mt)", "IGG LNG (mt)", "IGG LPG Propane (mt)", "IGG LPG Butane (mt)", "IGG Other (mt)", "IGG Other Fuel Type"],
            "Incinerator": ["Incinerator MGO (mt)"]
        },
        "LNG Tanker": {
            "Main Engine": ["ME LFO (mt)", "ME MGO (mt)", "ME LNG (mt)", "ME Other (mt)", "ME Other Fuel Type"],
            "Auxiliary Engines": ["AE LFO (mt)", "AE MGO (mt)", "AE LNG (mt)", "AE Other (mt)", "AE Other Fuel Type"],
            "Boilers": ["Boiler LFO (mt)", "Boiler MGO (mt)", "Boiler LNG (mt)", "Boiler Other (mt)", "Boiler Other Fuel Type"],
            "IGG": ["IGG LFO (mt)", "IGG MGO (mt)", "IGG LNG (mt)", "IGG Other (mt)", "IGG Other Fuel Type"],
            "GCU": ["GCU LFO (mt)", "GCU MGO (mt)", "GCU LNG (mt)", "GCU Other (mt)", "GCU Other Fuel Type"],
            "Incinerator": ["Incinerator MGO (mt)"]
        }
    },
    "ROB": ["LFO ROB (mt)", "MGO ROB (mt)", "LNG ROB (mt)", "Other ROB (mt)", "Other Fuel Type ROB", "Total Fuel ROB (mt)"],
    "Fuel Allocation": {
        "Oil Tanker": {
            "Cargo Heating": [
                "Cargo Heating HFO (mt)", 
                "Cargo Heating MGO (mt)", 
                "Cargo Heating LNG (mt)", 
                "Cargo Heating Other (mt)", 
                "Cargo Heating Other Fuel Type"
            ],
            "Cargo Discharging": [
                "Cargo Discharging HFO (mt)",
                "Cargo Discharging MGO (mt)",
                "Cargo Discharging LNG (mt)",
                "Cargo Discharging Other (mt)",
                "Cargo Discharging Other Fuel Type"
            ],
            "Engine Driven Cargo Pump": ["Engine Driven Cargo Pump MGO (mt)"]
        },
        "LPG Tanker": {
            "Cargo Cooling": [
                "Cargo Cooling LFO (mt)", "Cargo Cooling MGO (mt)", "Cargo Cooling LNG (mt)",
                "Cargo Cooling LPG Propane (mt)", "Cargo Cooling LPG Butane (mt)",
                "Cargo Cooling Other (mt)", "Cargo Cooling Other Fuel Type",
                "Cargo Cooling Work (kWh)", "Cargo Cooling SFOC (g/kWh)"
            ],
            "Discharge Pump": [
                "Discharge Pump LFO (mt)", "Discharge Pump MGO (mt)", "Discharge Pump LNG (mt)",
                "Discharge Pump LPG Propane (mt)", "Discharge Pump LPG Butane (mt)",
                "Discharge Pump Other (mt)", "Discharge Pump Other Fuel Type",
                "Discharge Pump Work (kWh)", "Discharge Pump SFOC (g/kWh)"
            ],
            "Shore-Side Electricity": ["Shore-Side Electricity Work (kWh)"]
        },
        "LNG Tanker": {
            "Cargo Cooling": [
                "Cargo Cooling LFO (mt)", "Cargo Cooling MGO (mt)", "Cargo Cooling LNG (mt)",
                "Cargo Cooling Other (mt)", "Cargo Cooling Other Fuel Type",
                "Cargo Cooling Work (kWh)", "Cargo Cooling SFOC (g/kWh)"
            ],
            "Discharge Pump": [
                "Discharge Pump LFO (mt)", "Discharge Pump MGO (mt)", "Discharge Pump LNG (mt)",
                "Discharge Pump Other (mt)", "Discharge Pump Other Fuel Type",
                "Discharge Pump Work (kWh)", "Discharge Pump SFOC (g/kWh)"
            ],
            "Shore-Side Electricity": ["Shore-Side Electricity Work (kWh)"]
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
    },
    "Bunker": [
        "Bunker Type",
        "Quantity (mt)",
        "Density at 15°C (kg/m3)",
        "Viscosity at 50°C (cSt)",
        "Flash Point (°C)",
        "Sulphur Content (%)",
        "Water Content (%)",
        "Ash Content (%)",
        "Vanadium (mg/kg)",
        "Aluminium + Silicon (mg/kg)",
        "Pour Point (°C)",
        "Supplier Name",
        "Delivery Date",
        "Delivery Port",
        "BDN Number"
    ]
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

def generate_random_vessel_name():
    return f"{random.choice(VESSEL_PREFIXES)} {random.choice(VESSEL_NAMES)}"

def generate_random_imo():
    return ''.join(random.choices(string.digits, k=7))

def create_fields(fields, prefix, report_type, vessel_type):
    cols = st.columns(4)
    for i, field in enumerate(fields):
        with cols[i % 4]:
            field_key = f"{prefix}_{field.lower().replace(' ', '_')}"
            if field == "Vessel Name":
                st.text_input(field, value=generate_random_vessel_name(), key=field_key)
            elif field == "Vessel IMO":
                st.text_input(field, value=generate_random_imo(), key=field_key)
            elif field == "Local Date":
                st.date_input(field, value=datetime.now(), key=field_key)
            elif field == "Local Time":
                st.time_input(field, value=datetime.now().time(), key=field_key)
            elif field == "UTC Offset":
                st.text_input(field, value=datetime.now(pytz.timezone('UTC')).astimezone().strftime('%z'), key=field_key)
            elif field in ["From Port", "To Port"]:
                st.selectbox(field, options=PORTS, key=field_key)
            elif "Latitude" in field or "Longitude" in field:
                if "Degrees" in field:
                    st.number_input(field, min_value=0, max_value=180, key=field_key)
                elif "Minutes" in field:
                    st.number_input(field, min_value=0.0, max_value=59.99, format="%.2f", key=field_key)
                elif "Direction" in field:
                    st.selectbox(field, options=["N", "S"] if "Latitude" in field else ["E", "W"], key=field_key)
            elif any(fuel_type in field for fuel_type in ["LFO", "MGO", "LNG", "LPG Propane", "LPG Butane"]):
                st.number_input(field, min_value=0.0, step=0.1, key=field_key)
            else:
                st.text_input(field, key=field_key)

def create_form(report_type, vessel_type):
    st.header(f"New {report_type} Report for {vessel_type}")
    
    if report_type == "Bunkering":
        # Special form for Bunkering
        create_fields(SECTION_FIELDS["Vessel Data"], f"{report_type}_Vessel_Data", report_type, vessel_type)
        with st.expander("Bunker Details", expanded=True):
            create_fields(SECTION_FIELDS["Bunker"], f"{report_type}_Bunker", report_type, vessel_type)
    else:
        # Regular form for other report types
        for section, fields in SECTION_FIELDS.items():
            if section != "Bunker":  # Skip Bunker section for non-Bunkering reports
                with st.expander(section, expanded=False):
                    st.subheader(section)
                    if isinstance(fields, dict):
                        if section in ["Cargo", "Fuel Consumption", "Fuel Allocation"]:
                            vessel_fields = fields.get(vessel_type, {})
                            if isinstance(vessel_fields, dict):
                                for subsection, subfields in vessel_fields.items():
                                    st.subheader(subsection)
                                    create_fields(subfields, f"{report_type}_{section}_{subsection}", report_type, vessel_type)
                            else:
                                create_fields(vessel_fields, f"{report_type}_{section}", report_type, vessel_type)
                        else:
                            for subsection, subfields in fields.items():
                                st.subheader(subsection)
                                create_fields(subfields, f"{report_type}_{section}_{subsection}", report_type, vessel_type)
                    else:
                        create_fields(fields, f"{report_type}_{section}", report_type, vessel_type)

    if st.button("Submit Report"):
        st.success(f"{report_type} for {vessel_type} submitted successfully!")
        
def main():
    st.title("OptiLog - AI-Enhanced Maritime Reporting System")

    col1, col2 = st.columns([0.7, 0.3])

    with col2:
        st.markdown("### Report Settings")
        vessel_type = st.selectbox("Select Vessel Type:", VESSEL_TYPES, key="vessel_type_selector")
        report_type = st.selectbox("Select Report Type:", REPORT_TYPES, key="report_type_selector")

    with col1:
        create_form(report_type, vessel_type)

if __name__ == "__main__":
    main()
