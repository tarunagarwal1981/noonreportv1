import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Define the data structure
data = {
    "General": [
        {"name": "Vessel Name", "type": "text", "validation": "Trimmed and unique per vessel"},
        {"name": "Date (Local ship Time)", "type": "date"},
        {"name": "Time Zone", "type": "number", "min": -12, "max": 12},
        {"name": "UTC Time", "type": "time", "derived": "Time zone + Local Time"},
        {"name": "Event Type", "type": "select", "options": ["Sailing", "Anchorage", "Drifting", "Maneuvering (FWE, SBE, COSP, EOSP)"]},
        {"name": "Event Time", "type": "time", "derived": "Difference between two event times should not be more than 25hrs"}
    ],
    "Voyage Details": [
        {"name": "Voy No", "type": "text", "validation": "Unique for one voyage"},
        {"name": "Leg No", "type": "text", "validation": "Unique for one leg"},
        {"name": "IDL Crossing Tag", "type": "select", "options": ["Yes", "No"]},
        {"name": "STS Voyage Tag", "type": "select", "options": ["Yes", "No"]},
        {"name": "Ice Voyage Tag", "type": "select", "options": ["Yes", "No"]},
        {"name": "Emergency Voyage", "type": "select", "options": ["Yes", "No"]},
        {"name": "EU voyage Tag", "type": "select", "options": ["Yes", "No"]},
        {"name": "From port", "type": "text", "validation": "Should match with UNLOCODE"},
        {"name": "To Port", "type": "text", "validation": "Should match with UNLOCODE"},
        {"name": "Displacement", "type": "number", "min": 0, "validation": "0.9*Ballast Displacement to 1.1*scantling displacement"},
        {"name": "Draft fore", "type": "number", "min": 0, "validation": "0.9 * Ballast Draft to 1.1 * Scantling draft"},
        {"name": "Draft mid", "type": "number", "min": 0, "validation": "0.9 * Ballast Draft to 1.1 * Scantling draft"},
        {"name": "Draft aft", "type": "number", "min": 0, "validation": "0.9 * Ballast Draft to 1.1 * Scantling draft"},
        {"name": "Total Cargo Onboard", "type": "number", "min": 0, "max": "vessel DWT capacity"},
        {"name": "Vessel Condition", "type": "select", "options": ["Ballast", "Laden"]},
        {"name": "C/P Speed", "type": "number", "min": 0, "max": 27},
        {"name": "C/P Consumption Total (per Fuel Type)", "type": "number", "min": 0, "validation": "Max: 1.3 * avg Fuel consumption"}
    ],
    "Deck": [
        {"name": "GPS Latitude", "type": "text", "validation": "Decimal or DMS format"},
        {"name": "GPS Longitude", "type": "text", "validation": "Decimal or DMS format"},
        {"name": "Ship Heading", "type": "number", "min": 0, "max": 360},
        {"name": "Engine Distance", "type": "number", "min": 0, "validation": "<= straight line distance between last report Lat, Long"},
        {"name": "Distance sailed since last event (DOG)", "type": "number", "min": 0, "validation": "<= straight line distance between last report Lat, Long"},
        {"name": "Distance to Go", "type": "number", "min": 0, "derived": "Sum of all day distance reported from Voyage start - sum of voyage Distance using the Way points from Voyage plan"},
        {"name": "Avg Speed Observed (SOG)", "type": "number", "min": 0, "max": 27},
        {"name": "STW (Log Speed)", "type": "number", "min": 0, "max": 27, "derived": "Engine Distance * ME Run hrs"},
        {"name": "Maneuvering Hrs", "type": "number", "min": 0, "validation": "<= event time"},
        {"name": "Anchorage hrs", "type": "number", "min": 0, "validation": "<= event time"},
        {"name": "Drifting hrs", "type": "number", "min": 0, "validation": "<= event time"},
        {"name": "STS hrs", "type": "number", "min": 0, "validation": "<= event time"}
    ],
    "Engine": [
        {"name": "RPM", "type": "number", "min": 0, "validation": "< MCR RPM"},
        {"name": "Slip (%)", "type": "number", "min": 0, "max": 100, "derived": "(Engine Distance – Observed Distance) / Engine Distance x 100"},
        {"name": "T/C RPM", "type": "number", "min": 0, "validation": "< 110% T/C RPM"},
        {"name": "Scav. Air Pressure", "type": "number", "min": 0, "validation": "<110%mcr scv pr in shop test"},
        {"name": "Scav. Air Temp", "type": "number", "min": 25, "max": 70},
        {"name": "ME (kw)", "type": "number", "min": 0, "validation": "< MCR Power"},
        {"name": "DG(kw)", "type": "number", "min": 0, "validation": "< AE MCR Power"},
        {"name": "Framo Engines (kw)", "type": "number", "min": 0, "validation": "< Framo Max kW"},
        {"name": "Shaft Generator(kw)", "type": "number", "min": 0},
        {"name": "Cargo Refer (kw) (if Electrically driven)", "type": "number", "min": 0},
        {"name": "Cargo Pump(kw) (if Electrically driven)", "type": "number", "min": 0},
        {"name": "No. Refer Containers in use", "type": "number", "min": 0},
        {"name": "ME SFOC", "type": "number", "min": 140, "max": 280, "derived": "ME Consumption * 10^6 / (ME power * Run hrs)"},
        {"name": "AE SFOC", "type": "number", "min": 170, "max": 320, "derived": "AE Consumption * 10^6 / (AE power * Run hrs)"}
    ],
    "Running Hrs": [
        {"name": "ME steaming hrs", "type": "number", "min": 0, "max": 26, "validation": "Should be equal or Less than Event time"},
        {"name": "DG run hrs", "type": "number", "min": 0, "max": 26, "validation": "If AE Consumption > 0, then AE Run hrs should be > 0"},
        {"name": "SG run hrs", "type": "number", "min": 0, "max": 26}
    ],
    "Consumption": [
        {"name": "ME Total Consumption", "type": "number", "min": 0, "validation": "Max: 1.5 * avg Fuel consumption"},
        {"name": "DG total Consumption", "type": "number", "min": 0, "validation": "Max: 1.5 * avg Fuel consumption"},
        {"name": "DG Cons for Cargo Operations", "type": "number", "min": 0, "validation": "Cannot be greater than total DG Consumption"},
        {"name": "Boiler Total Consumption", "type": "number", "min": 0},
        {"name": "Boiler Consumption for Cargo Operations", "type": "number", "min": 0, "validation": "Cannot be greater than total Boiler consumption"},
        {"name": "Framo Engines consumption", "type": "number", "min": 0},
        {"name": "IGS", "type": "number", "min": 0},
        {"name": "Incinerator", "type": "number", "min": 0},
        {"name": "While in DP Consumption", "type": "number", "min": 0},
        {"name": "Sludge generated", "type": "number", "min": 0, "max": "5% of that day's Consumption"}
    ],
    "ROBs": [
        {"name": "HFO", "type": "number", "min": 0, "validation": "Max: Max Fuel Type Capacity"},
        {"name": "LFO", "type": "number", "min": 0, "validation": "Max: Max Fuel Type Capacity"},
        {"name": "DO/GO", "type": "number", "min": 0, "validation": "Max: Max Fuel Type Capacity"},
        {"name": "LNG", "type": "number", "min": 0, "validation": "Max: Max Fuel Type Capacity"},
        {"name": "LPG", "type": "number", "min": 0, "validation": "Max: Max Fuel Type Capacity"},
        {"name": "Methanol", "type": "number", "min": 0, "validation": "Max: Max Fuel Type Capacity"},
        {"name": "Ethanol", "type": "number", "min": 0, "validation": "Max: Max Fuel Type Capacity"},
        {"name": "Others fuels (Bio Fuels)", "type": "number", "min": 0, "validation": "Max: Max Fuel Type Capacity"}
    ],
    "Weather Service": [
        {"name": "Wind Direction", "type": "number", "min": 0, "max": 360},
        {"name": "Wind Speed", "type": "number", "min": 0, "max": 64},
        {"name": "Windforce (Bft)", "type": "number", "min": 0, "max": 12, "derived": True},
        {"name": "DSS Scale", "type": "number", "min": 0, "max": 9, "derived": True},
        {"name": "Wave Height", "type": "number", "min": 0, "max": 14},
        {"name": "Current Speed", "type": "number", "min": 0, "max": 4},
        {"name": "Current Direction", "type": "number", "min": 0, "max": 360}
    ],
    "Bunker Details": [
        {"name": "Grade Name (Lab Test) IMO Grades", "type": "text", "validation": "As per ISO 8217 for HFO, LFO & Gas Oil Diesel Oil"},
        {"name": "Sulphur % (BDN)", "type": "number", "min": 0, "max": 5},
        {"name": "Density (BDN)", "type": "number", "min": 0.7, "max": 0.99},
        {"name": "Viscosity (BDN)", "type": "number", "min": 0, "max": 380},
        {"name": "Bunker Received Quantity", "type": "number", "min": 0, "validation": "Max: sum of all fuel tank capacity"}
    ]
}

def create_input_field(field):
    if field["type"] == "text":
        return st.text_input(field["name"])
    elif field["type"] == "number":
        return st.number_input(field["name"], min_value=field.get("min"), max_value=field.get("max"))
    elif field["type"] == "date":
        return st.date_input(field["name"])
    elif field["type"] == "time":
        return st.time_input(field["name"])
    elif field["type"] == "select":
        return st.selectbox(field["name"], field["options"])

def main():
    st.title("Maritime Data Entry Form")

    for section, fields in data.items():
        st.header(section)
        for field in fields:
            value = create_input_field(field)
            if "validation" in field:
                st.info(f"Validation: {field['validation']}")
            if "derived" in field:
                st.info(f"Derived: {field['derived']}")

    if st.button("Submit Form"):
        st.success("Form submitted successfully!")

if __name__ == "__main__":
    main()
