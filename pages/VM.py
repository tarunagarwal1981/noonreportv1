import streamlit as st
import datetime
import pandas as pd

st.set_page_config(layout="wide", page_title="Voyage Manifest")

def main():
    st.title("Voyage Manifest")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("Start New Voyage Manifest"):
            st.success("New Voyage Manifest started!")
    with col2:
        edit_mode = st.button("Edit")
    with col3:
        st.button("Share")
    with col4:
        st.button("Add")
    with col5:
        st.button("Delete")

    voyage_id = st.text_input("Voyage ID", value="VI-KYJO23000006", disabled=not edit_mode)
    
    with st.expander("General Information", expanded=False):
        general_info(edit_mode)

    with st.expander("Voyage Itinerary", expanded=False):
        voyage_itinerary(edit_mode)

    with st.expander("Charterer Info", expanded=False):
        charterer_info(edit_mode)

    with st.expander("Agent Info", expanded=False):
        agent_info(edit_mode)

    with st.expander("Zones", expanded=False):
        zones(edit_mode)

    with st.expander("Log", expanded=False):
        log(edit_mode)

    if st.button("Close this Voyage"):
        st.success("Voyage closed successfully!")

def general_info(edit_mode):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("No", value="VI-KYJO23000006", disabled=not edit_mode)
        st.text_input("Vessel Code", value="KYJO", disabled=not edit_mode)
        st.date_input("Voyage Start", value=datetime.date(2023, 4, 11), disabled=not edit_mode)
    with col2:
        st.text_input("Voyage No", value="74 B", disabled=not edit_mode)
        st.text_input("Vessel Name", value="KEY JOURNEY", disabled=not edit_mode)
        st.text_input("Time Zone", value="(UTC+09:00) Osaka, Sapporo, Tokyo", disabled=not edit_mode)
    with col3:
        st.number_input("Charter Party Speed", value=10.50, format="%.2f", disabled=not edit_mode)
        st.number_input("Charter Party Consumption", value=14.50, format="%.2f", disabled=not edit_mode)
        st.selectbox("Status", ["Open", "Closed"], index=1, disabled=not edit_mode)
    with col4:
        st.selectbox("Vessel Status", ["Laden", "Ballast"], index=1, disabled=not edit_mode)
        st.number_input("Revision No", value=0, format="%d", disabled=not edit_mode)
        st.date_input("Revision Date", value=None, disabled=not edit_mode)
    
    st.text_area("Comments", disabled=not edit_mode)

def voyage_itinerary(edit_mode):
    data = {
        "Segment ID": [0, 1],
        "Port Code": ["JPSGM", "CAPRR"],
        "Port Name": ["Sendaishiogama", "Prince Rupert"],
        "Transit Port": [False, False],
        "Time Zone": ["(UTC+09:00) Osaka, Sapporo, Tokyo", "(UTC-08:00) Pacific Time (US & Canada)"],
        "ETA": ["11/1/2023 5:30 AM", "11/18/2023 5:30 AM"],
        "ETB": ["11/3/2023 5:30 AM", "11/21/2023 5:30 AM"],
        "ETD": ["11/4/2023 5:30 AM", "11/22/2023 5:30 AM"],
        "Actual Arrival(EOSP)": ["11/1/2023 5:30 AM", "11/18/2023 7:30 AM"],
        "Arrival Date(AB)": ["11/1/2023 5:30 AM", "11/21/2023 4:06 AM"],
        "Departure Date(DB)": ["11/4/2023 5:30 AM", ""],
        "Actual Departure(COSP)": ["11/5/2023 3:00 AM", ""]
    }
    df = pd.DataFrame(data)
    edited_df = st.data_editor(df, disabled=not edit_mode, num_rows="dynamic")
    if edit_mode:
        st.button("Add Itinerary")

def charterer_info(edit_mode):
    st.subheader("Charterer Information")
    charterer_data = st.session_state.get('charterer_data', [{}])
    for i, charterer in enumerate(charterer_data):
        with st.expander(f"Charterer {i+1}", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                charterer['Type'] = st.text_input("Type", value=charterer.get('Type', ''), key=f"charterer_type_{i}", disabled=not edit_mode)
                charterer['Address 1'] = st.text_input("Address 1", value=charterer.get('Address 1', ''), key=f"charterer_address1_{i}", disabled=not edit_mode)
            with col2:
                charterer['Name'] = st.text_input("Name", value=charterer.get('Name', ''), key=f"charterer_name_{i}", disabled=not edit_mode)
                charterer['Address 2'] = st.text_input("Address 2", value=charterer.get('Address 2', ''), key=f"charterer_address2_{i}", disabled=not edit_mode)
            with col3:
                charterer['Phone No'] = st.text_input("Phone No", value=charterer.get('Phone No', ''), key=f"charterer_phone_{i}", disabled=not edit_mode)
                charterer['Mobile No'] = st.text_input("Mobile No", value=charterer.get('Mobile No', ''), key=f"charterer_mobile_{i}", disabled=not edit_mode)
            with col4:
                charterer['Email Id'] = st.text_input("Email Id", value=charterer.get('Email Id', ''), key=f"charterer_email_{i}", disabled=not edit_mode)
    if edit_mode:
        if st.button("Add Charterer"):
            charterer_data.append({})
    st.session_state['charterer_data'] = charterer_data

def agent_info(edit_mode):
    st.subheader("Agent Information")
    agent_data = st.session_state.get('agent_data', [{}])
    for i, agent in enumerate(agent_data):
        with st.expander(f"Agent {i+1}", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                agent['Type'] = st.text_input("Type", value=agent.get('Type', ''), key=f"agent_type_{i}", disabled=not edit_mode)
                agent['Address 1'] = st.text_input("Address 1", value=agent.get('Address 1', ''), key=f"agent_address1_{i}", disabled=not edit_mode)
            with col2:
                agent['Name'] = st.text_input("Name", value=agent.get('Name', ''), key=f"agent_name_{i}", disabled=not edit_mode)
                agent['Address 2'] = st.text_input("Address 2", value=agent.get('Address 2', ''), key=f"agent_address2_{i}", disabled=not edit_mode)
            with col3:
                agent['Phone No'] = st.text_input("Phone No", value=agent.get('Phone No', ''), key=f"agent_phone_{i}", disabled=not edit_mode)
                agent['Mobile No'] = st.text_input("Mobile No", value=agent.get('Mobile No', ''), key=f"agent_mobile_{i}", disabled=not edit_mode)
            with col4:
                agent['Email Id'] = st.text_input("Email Id", value=agent.get('Email Id', ''), key=f"agent_email_{i}", disabled=not edit_mode)
    if edit_mode:
        if st.button("Add Agent"):
            agent_data.append({})
    st.session_state['agent_data'] = agent_data

def zones(edit_mode):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Zone", value="MAIN_WORLD", disabled=not edit_mode)
        st.text_input("ETA", value="", disabled=not edit_mode)
    with col2:
        st.text_input("Area", value="", disabled=not edit_mode)
        st.text_input("ETD", value="11/4/2023 5:30 AM", disabled=not edit_mode)
    with col3:
        st.text_input("Latitude(Entry Point)", value="38 ° 09 ' 00 '' N", disabled=not edit_mode)
        st.text_input("Latitude(Exit Point)", value="", disabled=not edit_mode)
    with col4:
        st.text_input("Longitude(Entry Point)", value="141 ° 38 ' 00 ''", disabled=not edit_mode)
        st.text_input("Longitude(Exit Point)", value="", disabled=not edit_mode)

def log(edit_mode):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Created By", value="2OFF", disabled=True)
    with col2:
        st.date_input("Created Date", value=datetime.date(2024, 6, 23), disabled=True)
    with col3:
        st.text_input("Last Modified by", value="2OFF", disabled=True)
    with col4:
        st.text_input("Last Modified Datetime", value="6/28/2024 4:24 AM", disabled=True)

if __name__ == "__main__":
    main()
