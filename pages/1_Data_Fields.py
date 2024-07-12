import streamlit as st
import pandas as pd

def create_maritime_reporting_table():
    # Data for the table
    data = [
        {"Field": "IMO Number", "Mandatory": "Yes", "Relevant for": "mandatory for MRV&DCS"},
        {"Field": "UTC date", "Mandatory": "Yes", "Relevant for": "mandatory for MRV&DCS"},
        {"Field": "UTC time", "Mandatory": "Yes", "Relevant for": "mandatory for MRV&DCS"},
        {"Field": "From - port code (Departure port)", "Mandatory": "No", "Relevant for": "mandatory for MRV&DCS"},
        {"Field": "To - port code (Arrival port)", "Mandatory": "No", "Relevant for": "mandatory for MRV&DCS"},
        {"Field": "Voyage type", "Mandatory": "No", "Relevant for": "for CII correction"},
        {"Field": "Voyage Number", "Mandatory": "No", "Relevant for": "recommended for voyage level verification schemes"},
        {"Field": "Offhire reasons", "Mandatory": "No", "Relevant for": "for CII correction, voluntary wrt MRV"},
        {"Field": "Event name", "Mandatory": "No", "Relevant for": "mandatory for MRV&DCS"},
        {"Field": "Time elapsed since previous event report", "Mandatory": "Yes", "Relevant for": "mandatory for MRV&DCS"},
        {"Field": "Time elapsed sailing", "Mandatory": "No", "Relevant for": "DSC only, voluntary wrt MRV"},
        {"Field": "Time elapsed at anchor", "Mandatory": "No", "Relevant for": "mandatory for MRV&DCS"},
        {"Field": "Time elapsed in dynamic positioning", "Mandatory": "No", "Relevant for": "recommended for MRV&DCS"},
        {"Field": "Time elapsed operating in ice", "Mandatory": "No", "Relevant for": "for CII correction, voluntary wrt MRV"},
        {"Field": "Time elapsed maneuvering", "Mandatory": "No", "Relevant for": "recommended for MRV&DCS"},
        {"Field": "Time elapsed waiting", "Mandatory": "No", "Relevant for": "not in use"},
        {"Field": "Time elapsed loading/unloading", "Mandatory": "No", "Relevant for": "mandatory for MRV"},
        {"Field": "Time elapsed drifting", "Mandatory": "No", "Relevant for": "recommended for MRV&DCS"},
        {"Field": "Distance over Ground", "Mandatory": "No", "Relevant for": "mandatory for MRV&DCS"},
        {"Field": "Position (Latitude, Longitude)", "Mandatory": "No", "Relevant for": "mandatory for MRV&DCS"},
        {"Field": "Cargo Weight", "Mandatory": "No", "Relevant for": "mandatory for MRV"},
        {"Field": "Cargo Volume", "Mandatory": "No", "Relevant for": "mandatory for MRV"},
        {"Field": "Number of passengers", "Mandatory": "No", "Relevant for": "mandatory for MRV"},
        {"Field": "Reefer Containers", "Mandatory": "No", "Relevant for": "for CII correction"},
        {"Field": "Fuel Consumption (ME, AE, Boilers, etc.)", "Mandatory": "No", "Relevant for": "mandatory for MRV&DCS"},
        {"Field": "Remaining on Board (ROB) for different fuel types", "Mandatory": "No", "Relevant for": "mandatory for MRV&DCS"},
        {"Field": "Allocation of fuel for different purposes", "Mandatory": "No", "Relevant for": "for CII correction, voluntary wrt MRV"},
        {"Field": "Machinery data (Reefer container, Cargo cooling, etc.)", "Mandatory": "No", "Relevant for": "for CII correction, voluntary wrt MRV"},
        {"Field": "Shore-Side Electricity", "Mandatory": "No", "Relevant for": "in case of no fuel consumption for any verification"}
    ]

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Streamlit app
    st.title("Maritime Reporting Data Fields")

    # Display the table
    st.dataframe(df, use_container_width=True)

    # Add a download button for the CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="maritime_reporting_fields.csv",
        mime="text/csv",
    )

if __name__ == "__main__":
    create_maritime_reporting_table()
