import streamlit as st
import datetime
import pandas as pd

st.set_page_config(layout="wide", page_title="Voyage Planning Summary")

def main():
    st.title("Voyage Planning Summary")

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
    
    with st.expander("General Information", expanded=False):
        general_info()

    with st.expander("Itinerary", expanded=False):
        itinerary()

    with st.expander("Charterer Info", expanded=False):
        charterer_info()

    with st.expander("Zones", expanded=False):
        zones()

    with st.expander("Log", expanded=False):
        log()

def general_info():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("No", value="VI-KYJO23000006")
        st.text_input("Vessel Code", value="KYJO")
        st.date_input("Voyage Start", value=datetime.date(2023, 4, 11))
    with col2:
        st.text_input("Voyage No", value="74 B")
        st.text_input("Vessel Name", value="KEY JOURNEY")
        st.text_input("Time Zone", value="(UTC+09:00) Osaka, Sapporo, Tokyo")
    with col3:
        st.number_input("Charter Party Speed", value=10.50, format="%.2f")
        st.number_input("Charter Party Consumption", value=14.50, format="%.2f")
        st.selectbox("Status", ["Open", "Closed"], index=1)
    with col4:
        st.selectbox("Vessel Status", ["Laden", "Ballast"], index=1)
        st.number_input("Revision No", value=0, format="%d")
        st.date_input("Revision Date", value=None)
    
    st.text_area("Comments")

def itinerary():
    data = {
        "Port Code": ["JPSGM", "CAPRR"],
        "Port Name": ["Sendaishiogama", "Prince Rupert"],
        "Transit Port": [False, False],
        "Time Zone": ["(UTC+09:00) Osaka, Sapporo, Tokyo", "(UTC-08:00) Pacific Time (US & Canada)"],
        "ETA": ["11/1/2023 5:30 AM", "11/18/2023 5:30 AM"],
        "ETB": ["11/3/2023 5:30 AM", "11/21/2023 5:30 AM"],
        "ETD": ["11/4/2023 5:30 AM", "11/22/2023 5:30 AM"],
        "Actual Arrival(EOSP)": ["11/1/2023 5:30 AM", "11/18/2023 7:30 AM"],
        "Arrival Draft": ["11/1/2023 5:30 AM", "11/21/2023 5:30 AM"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

def charterer_info():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Type", value="Head Charterer")
        st.text_input("Address 1", value="TOKYO, JAPAN")
    with col2:
        st.text_input("Name", value="NYK")
        st.text_input("Address 2", value="")
    with col3:
        st.text_input("Phone No", value="")
        st.text_input("Mobile No", value="")
    with col4:
        st.text_input("Email Id", value="")

def zones():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Zone", value="MAIN_WORLD")
        st.text_input("ETA", value="")
    with col2:
        st.text_input("Area", value="")
        st.text_input("ETD", value="11/4/2023 5:30 AM")
    with col3:
        st.text_input("Latitude(Entry Point)", value="38 ° 09 ' 00 '' N")
        st.text_input("Latitude(Exit Point)", value="")
    with col4:
        st.text_input("Longitude(Entry Point)", value="141 ° 38 ' 00 ''")
        st.text_input("Longitude(Exit Point)", value="")

def log():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Created By", value="2OFF")
    with col2:
        st.date_input("Created Date", value=datetime.date(2024, 6, 23))
    with col3:
        st.text_input("Last Modified by", value="2OFF")
    with col4:
        st.text_input("Last Modified Datetime", value="6/28/2024 4:24 AM")

if __name__ == "__main__":
    main()
