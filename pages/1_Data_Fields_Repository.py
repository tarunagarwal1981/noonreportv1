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
        {"Field": "Shore-Side Electricity", "Mandatory": "No", "Relevant for": "in case of no fuel consumption for any verification"},
        # Non-mandatory fields
        {"Field": "Local date", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Local time", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Event ID", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Sort number", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "From - freetext location", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "To - freetext location", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "ETA", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "RTA", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Speed order", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Number of tugs used", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Reason for deviation", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Charter contract", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Carrier code", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Carrier name", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Service", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Operational condition", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Voyage stage", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Voyage leg name", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Voyage leg type", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Port to port ID", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Area (From/To)", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Position text", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Direction (Course/Heading)", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Weather data (Wind, Sea state, Swell, Current, Temperature)", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Draft data", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Additional Cargo data", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Water data", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Lubes data", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Remarks", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Entry made by", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Contact", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Meta data", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Event type data fields", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"},
        {"Field": "Snapshot type data fields", "Mandatory": "No", "Relevant for": "OPTIONAL INPUT"}
    ]

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Streamlit app
    st.title("Maritime Reporting Data Fields")

    # Display the table
    st.dataframe(df, use_container_width=True)

    # Add filters
    st.sidebar.header("Filters")
    mandatory_filter = st.sidebar.multiselect(
        "Filter by Mandatory Status",
        options=["Yes", "No"],
        default=["Yes", "No"]
    )

    relevance_filter = st.sidebar.multiselect(
        "Filter by Relevance",
        options=df["Relevant for"].unique(),
        default=df["Relevant for"].unique()
    )

    # Apply filters
    filtered_df = df[df["Mandatory"].isin(mandatory_filter) & df["Relevant for"].isin(relevance_filter)]

    # Display filtered table
    st.subheader("Filtered Data")
    st.dataframe(filtered_df, use_container_width=True)

    # Add a download button for the CSV
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="maritime_reporting_fields_filtered.csv",
        mime="text/csv",
    )

if __name__ == "__main__":
    create_maritime_reporting_table()
