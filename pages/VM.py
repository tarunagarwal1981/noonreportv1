import streamlit as st
import datetime
import pandas as pd

st.set_page_config(layout="wide", page_title="Voyage Manifest")

# Initialize session state variables
if 'voyage_status' not in st.session_state:
    st.session_state.voyage_status = 'Draft'
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = pd.DataFrame(columns=["Segment ID", "Port Code", "Port Name", "Transit Port", "Time Zone", "ETA", "ETB", "ETD", "Actual Arrival(EOSP)", "Arrival Date(AB)", "Departure Date(DB)", "Actual Departure(COSP)"])

def main():
    st.title("Voyage Manifest")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Start New Voyage Manifest"):
            if st.session_state.voyage_status == 'Closed':
                st.session_state.voyage_status = 'Draft'
                st.success("New Voyage Manifest started in Draft mode!")
            else:
                st.error("Cannot start a new voyage. Current voyage is not closed.")
    with col2:
        edit_mode = st.button("Edit")
    with col3:
        if st.button("Open Voyage"):
            if st.session_state.voyage_status == 'Draft':
                st.session_state.voyage_status = 'Open'
                st.success("Voyage opened successfully!")
            else:
                st.error("Can only open a voyage in Draft status.")
    with col4:
        if st.button("Close Voyage"):
            if st.session_state.voyage_status == 'Open':
                st.session_state.voyage_status = 'Closed'
                st.success("Voyage closed successfully!")
            else:
                st.error("Can only close an open voyage.")

    st.write(f"Current Voyage Status: {st.session_state.voyage_status}")

    voyage_id = st.text_input("Voyage ID", value="VI-KYJO23000006", disabled=st.session_state.voyage_status == 'Closed')
    
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

def general_info(edit_mode):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("No", value="VI-KYJO23000006", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.text_input("Vessel Code", value="KYJO", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.date_input("Voyage Start", value=datetime.date(2023, 4, 11), disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.text_input("From Port", value="", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
    with col2:
        st.text_input("Voyage No", value="74 B", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.text_input("Vessel Name", value="KEY JOURNEY", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.text_input("Time Zone", value="(UTC+09:00) Osaka, Sapporo, Tokyo", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.text_input("To Port", value="", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
    with col3:
        st.number_input("Charter Party Speed", value=10.50, format="%.2f", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.number_input("Charter Party Consumption", value=14.50, format="%.2f", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.selectbox("Status", ["Draft", "Open", "Closed"], index=["Draft", "Open", "Closed"].index(st.session_state.voyage_status), disabled=True)
    with col4:
        st.selectbox("Vessel Status", ["Laden", "Ballast"], index=1, disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.number_input("Revision No", value=0, format="%d", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.date_input("Revision Date", value=None, disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
    
    st.text_area("Comments", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')

def voyage_itinerary(edit_mode):
    if len(st.session_state.itinerary) == 0:
        # Initialize with departure and arrival ports
        st.session_state.itinerary = pd.DataFrame([
            {"Segment ID": 0, "Port Code": "", "Port Name": "", "Transit Port": False, "Time Zone": "", "ETA": "", "ETB": "", "ETD": "", "Actual Arrival(EOSP)": "", "Arrival Date(AB)": "", "Departure Date(DB)": "", "Actual Departure(COSP)": ""},
            {"Segment ID": 1, "Port Code": "", "Port Name": "", "Transit Port": False, "Time Zone": "", "ETA": "", "ETB": "", "ETD": "", "Actual Arrival(EOSP)": "", "Arrival Date(AB)": "", "Departure Date(DB)": "", "Actual Departure(COSP)": ""}
        ])

    edited_df = st.data_editor(st.session_state.itinerary, disabled=not edit_mode or st.session_state.voyage_status == 'Closed', num_rows="dynamic")
    
    if edit_mode and st.session_state.voyage_status != 'Closed':
        if st.button("Add Intermediate Port"):
            new_row = pd.DataFrame([{"Segment ID": len(st.session_state.itinerary) - 1}])
            st.session_state.itinerary = pd.concat([st.session_state.itinerary.iloc[:-1], new_row, st.session_state.itinerary.iloc[-1:]], ignore_index=True)
            st.session_state.itinerary['Segment ID'] = range(len(st.session_state.itinerary))
    
    st.session_state.itinerary = edited_df

def charterer_info(edit_mode):
    st.subheader("Charterer Information")
    if 'charterer_count' not in st.session_state:
        st.session_state.charterer_count = 1

    for i in range(st.session_state.charterer_count):
        st.markdown(f"**Charterer {i+1}**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.text_input("Type", key=f"charterer_type_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
            st.text_input("Address 1", key=f"charterer_address1_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        with col2:
            st.text_input("Name", key=f"charterer_name_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
            st.text_input("Address 2", key=f"charterer_address2_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        with col3:
            st.text_input("Phone No", key=f"charterer_phone_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
            st.text_input("Mobile No", key=f"charterer_mobile_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        with col4:
            st.text_input("Email Id", key=f"charterer_email_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.markdown("---")

    if edit_mode and st.session_state.voyage_status != 'Closed' and st.button("Add Charterer"):
        st.session_state.charterer_count += 1
        st.experimental_rerun()

def agent_info(edit_mode):
    st.subheader("Agent Information")
    if 'agent_count' not in st.session_state:
        st.session_state.agent_count = 1

    for i in range(st.session_state.agent_count):
        st.markdown(f"**Agent {i+1}**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.text_input("Type", key=f"agent_type_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
            st.text_input("Address 1", key=f"agent_address1_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        with col2:
            st.text_input("Name", key=f"agent_name_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
            st.text_input("Address 2", key=f"agent_address2_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        with col3:
            st.text_input("Phone No", key=f"agent_phone_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
            st.text_input("Mobile No", key=f"agent_mobile_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        with col4:
            st.text_input("Email Id", key=f"agent_email_{i}", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.markdown("---")

    if edit_mode and st.session_state.voyage_status != 'Closed' and st.button("Add Agent"):
        st.session_state.agent_count += 1
        st.experimental_rerun()

def zones(edit_mode):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Zone", value="MAIN_WORLD", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.text_input("ETA", value="", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
    with col2:
        st.text_input("Area", value="", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.text_input("ETD", value="11/4/2023 5:30 AM", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
    with col3:
        st.text_input("Latitude(Entry Point)", value="38 ° 09 ' 00 '' N", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.text_input("Latitude(Exit Point)", value="", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
    with col4:
        st.text_input("Longitude(Entry Point)", value="141 ° 38 ' 00 ''", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')
        st.text_input("Longitude(Exit Point)", value="", disabled=not edit_mode or st.session_state.voyage_status == 'Closed')

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
