import streamlit as st
import pandas as pd

# Define the data structure (same as before)
data = {
    "General": [
        {"name": "Vessel Name", "type": "text", "validation": "Trimmed and unique per vessel"},
        {"name": "Date (Local ship Time)", "type": "date"},
        {"name": "Time Zone", "type": "number", "min": -12, "max": 12},
        {"name": "UTC Time", "type": "time", "derived": "Time zone + Local Time"},
        {"name": "Event Type", "type": "select", "options": ["Sailing", "Anchorage", "Drifting", "Maneuvering (FWE, SBE, COSP, EOSP)"]},
        {"name": "Event Time", "type": "time", "derived": "Difference between two event times should not be more than 25hrs"}
    ],
    # ... (include all other sections as before)
}

def create_dataframe(section_data):
    rows = []
    for field in section_data:
        row = {
            "Field Name": field["name"],
            "Data Type": field["type"],
            "Min": field.get("min", ""),
            "Max": field.get("max", ""),
            "Validation/Derivation": field.get("validation", field.get("derived", ""))
        }
        rows.append(row)
    return pd.DataFrame(rows)

def main():
    st.title("Maritime Data Fields Overview")

    for section, fields in data.items():
        st.header(section)
        df = create_dataframe(fields)
        st.table(df)

if __name__ == "__main__":
    main()
