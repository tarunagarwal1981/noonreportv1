import streamlit as st
import datetime

st.set_page_config(layout="wide", page_title="Voyage Manifest")

def main():
    st.title("Voyage Manifest")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("Edit")
    with col2:
        st.button("Share")
    with col3:
        st.button("Add")
    with col4:
        st.button("Delete")

    voyage_id = st.text_input("Voyage ID", value="VI-KYJO23000006")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["General", "Itinerary", "Charterer Info", "Zones", "Log"])

    with tab1:
        general_info()

    with tab2:
        itinerary()

    with tab3:
        charterer_info()

    with tab4:
        zones()

    with tab5:
        log()

def general_info():
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("No", value="VI-KYJO23000006")
        st.text_input("Voyage No", value="74 B")
        st.text_input("Vessel Code", value="KYJO")
        st.text_input("Vessel Name", value="KEY JOURNEY")
        st.date_input("Voyage Start", value=datetime.date(2023, 4, 11))
        st.text_input("Time Zone", value="(UTC+09:00) Osaka, Sapporo, Tokyo")
        st.number_input("Charter Party Speed", value=10.50, format="%.2f")
    with col2:
        st.number_input("Charter Party Consumption", value=14.50, format="%.2f")
        st.selectbox("Status", ["Open", "Closed"], index=1)
        st.selectbox("Vessel Status", ["Laden", "Ballast"], index=1)
        st.number_input("Revision No", value=0, format="%d")
        st.date_input("Revision Date", value=None)
        st.text_area("Comments")

def itinerary():
    st.subheader("Itinerary")
    data = [
        {"Port Code": "JPSGM", "Port Name": "Sendaishiogama", "Transit Port": False, 
         "Time Zone": "(UTC+09:00) Osaka, Sapporo, Tokyo", "ETA": "11/1/2023 5:30 AM", 
         "ETB": "11/3/2023 5:30 AM", "ETD": "11/4/2023 5:30 AM", 
         "Actual Arrival(EOSP)": "11/1/2023 5:30 AM", "Arrival Draft": "11/1/2023 5:30 AM"},
        {"Port Code": "CAPRR", "Port Name": "Prince Rupert", "Transit Port": False, 
         "Time Zone": "(UTC-08:00) Pacific Time (US & Canada)", "ETA": "11/18/2023 5:30 AM", 
         "ETB": "11/21/2023 5:30 AM", "ETD": "11/22/2023 5:30 AM", 
         "Actual Arrival(EOSP)": "11/18/2023 7:30 AM", "Arrival Draft": "11/21/2023 5:30 AM"}
    ]
    st.table(data)

def charterer_info():
    st.subheader("Charterer Info")
    data = {
        "Type": "Head Charterer",
        "Name": "NYK",
        "Address 1": "TOKYO, JAPAN",
        "Address 2": "",
        "Phone No": "",
        "Mobile No": "",
        "Email Id": ""
    }
    for key, value in data.items():
        st.text_input(key, value=value)

def zones():
    st.subheader("Zones")
    data = {
        "Zone": "MAIN_WORLD",
        "Area": "",
        "ETA": "",
        "ETD": "11/4/2023 5:30 AM",
        "Latitude(Entry Point)": "38 ° 09 ' 00 '' N",
        "Latitude(Exit Point)": "",
        "Longitude(Entry Point)": "141 ° 38 ' 00 ''",
        "Longitude(Exit Point)": ""
    }
    for key, value in data.items():
        st.text_input(key, value=value)

def log():
    st.subheader("Log")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Created By", value="2OFF")
        st.date_input("Created Date", value=datetime.date(2024, 6, 23))
    with col2:
        st.text_input("Last Modified by", value="2OFF")
        st.text_input("Last Modified Datetime", value="6/28/2024 4:24 AM")

if __name__ == "__main__":
    main()
