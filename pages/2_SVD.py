import streamlit as st
import pandas as pd

def create_standardised_vessel_dataset_table():
    # Data for the table
    data = [
        {"IMO Data Number": "IMO0597", "Data Element": "Event type, coded", "ISO Universal ID": "jsmea_voy/VoyageInformation/EventType"},
        {"IMO Data Number": "IMO0598", "Data Element": "Operation type, coded", "ISO Universal ID": "jsmea_voy/VoyageInformation/OperationType"},
        {"IMO Data Number": "IMO0599", "Data Element": "Operation, description", "ISO Universal ID": "jsmea_voy/VoyageInformation/OperationType/Remarks"},
        {"IMO Data Number": "IMO0600", "Data Element": "Elapsed Time", "ISO Universal ID": "jsmea_voy/DateAndTime/ElapsedTime"},
        {"IMO Data Number": "IMO0601", "Data Element": "Ship position when reporting, latitude", "ISO Universal ID": "jsmea_voy/ShipPosition/LAT"},
        {"IMO Data Number": "IMO0602", "Data Element": "Ship position when reporting, longitude", "ISO Universal ID": "jsmea_voy/ShipPosition/LON"},
        {"IMO Data Number": "IMO0603", "Data Element": "Ship reporting date time", "ISO Universal ID": "jsmea_voy/DateAndTime"},
        {"IMO Data Number": "IMO0142", "Data Element": "Ship name", "ISO Universal ID": "jsmea_nav/ShipInformation/ShipName"},
        {"IMO Data Number": "IMO0140", "Data Element": "Ship IMO Number", "ISO Universal ID": "jsmea_nav/ShipInformation/IMONumber"},
        {"IMO Data Number": "IMO0326", "Data Element": "Ship MMSI number", "ISO Universal ID": "jsmea_nav/ShipInformation/MMSINumber"},
        {"IMO Data Number": "IMO0160", "Data Element": "Ship type, coded", "ISO Universal ID": "jsmea_nav/ShipInformation/ShipType"},
        {"IMO Data Number": "IMO0086", "Data Element": "Number of crew", "ISO Universal ID": "jsmea_voy/VoyageInformation/CrewList"},
        {"IMO Data Number": "IMO0191", "Data Element": "Voyage number", "ISO Universal ID": "jsmea_voy/VoyageInformation/VoyageNumber"},
        {"IMO Data Number": "IMO0604", "Data Element": "Voyage remarks", "ISO Universal ID": "jsmea_voy/VoyageInformation/Remarks"},
        {"IMO Data Number": "IMO0605", "Data Element": "Voyage leg identifier", "ISO Universal ID": "jsmea_voy/VoyageInformation/LEG"},
        {"IMO Data Number": "IMO0606", "Data Element": "Voyage leg remarks", "ISO Universal ID": "jsmea_voy/VoyageInformation/LEG/Remarks"},
        # Add more rows here...
    ]

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Streamlit app
    st.title("Standardised Vessel Dataset")

    # Add a search box
    search_term = st.text_input("Search for a Data Element or IMO Data Number:")

    # Filter the dataframe based on the search term
    if search_term:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

    # Display the table
    st.dataframe(df, use_container_width=True)

    # Add a download button for the CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="standardised_vessel_dataset.csv",
        mime="text/csv",
    )

if __name__ == "__main__":
    create_standardised_vessel_dataset_table()
