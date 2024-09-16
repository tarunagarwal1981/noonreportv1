import streamlit as st
import datetime
import pandas as pd
import random
import string

st.set_page_config(layout="wide", page_title="Voyage Manifest")

# Initialize session state variables
if 'voyages' not in st.session_state:
    st.session_state.voyages = []
if 'current_voyage' not in st.session_state:
    st.session_state.current_voyage = None
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

def generate_voyage_id():
    return f"VI-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"

def create_new_voyage():
    new_voyage = {
        'id': generate_voyage_id(),
        'status': 'Draft',
        'itinerary': pd.DataFrame(columns=[
            "Segment ID", "Port Code", "Port Name", "Transit Port", "ETA", "ETB", "ETD", 
            "Actual Arrival(EOSP)", "Arrival Date(AB)", "Departure Date(DB)", "Actual Departure(COSP)"
        ]),
        'general_info': {},
        'charterer_info': [],
        'agent_info': [],
        'zones': {},
        'port_details': {},
        'log': {
            'created_by': 'System',
            'created_date': datetime.date.today(),
            'last_modified_by': 'System',
            'last_modified_datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    st.session_state.voyages.append(new_voyage)
    st.session_state.current_voyage = new_voyage

def display_voyage_manifest():
    voyage = st.session_state.current_voyage
    st.write(f"Voyage ID: {voyage['id']}")
    st.write(f"Current Voyage Status: {voyage['status']}")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("Start New Voyage Manifest"):
            if voyage['status'] == 'Closed':
                create_new_voyage()
                st.success(f"New Voyage Manifest started in Draft mode! Voyage ID: {st.session_state.current_voyage['id']}")
            else:
                st.error("Cannot start a new voyage. Current voyage is not closed.")

    with col2:
        if st.button("Toggle Edit Mode"):
            st.session_state.edit_mode = not st.session_state.edit_mode
            st.experimental_rerun()

    with col3:
        if st.button("Open Voyage"):
            if voyage['status'] == 'Draft':
                voyage['status'] = 'Open'
                st.success("Voyage opened successfully!")
            else:
                st.error("Can only open a voyage in Draft status.")

    with col4:
        if st.button("Close Voyage"):
            if voyage['status'] == 'Open':
                voyage['status'] = 'Closed'
                st.success("Voyage closed successfully!")
            else:
                st.error("Can only close an open voyage.")

    with col5:
        if st.button("Save Draft"):
            if voyage['status'] == 'Draft':
                voyage['log']['last_modified_by'] = 'User'  # Replace with actual user info
                voyage['log']['last_modified_datetime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.success("Draft saved successfully!")
            else:
                st.error("Can only save drafts for voyages in Draft status.")

    with st.expander("General Information", expanded=False):
        general_info()

    with st.expander("Voyage Itinerary", expanded=False):
        voyage_itinerary()

    with st.expander("Charterer Info", expanded=False):
        charterer_info()

    with st.expander("Agent Info", expanded=False):
        agent_info()

    with st.expander("Zones", expanded=False):
        zones()

    with st.expander("Log", expanded=False):
        log()

def general_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    
    st.subheader("General Information")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        voyage['general_info']['vessel_code'] = st.text_input("Vessel Code", value=voyage['general_info'].get('vessel_code', ''), key="vessel_code", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['general_info']['voyage_start'] = st.date_input("Voyage Start", value=voyage['general_info'].get('voyage_start', datetime.date.today()), key="voyage_start", disabled=not edit_mode or voyage['status'] == 'Closed')
    with col2:
        voyage['general_info']['vessel_name'] = st.text_input("Vessel Name", value=voyage['general_info'].get('vessel_name', ''), key="vessel_name", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['general_info']['charter_party_speed'] = st.number_input("Charter Party Speed", value=float(voyage['general_info'].get('charter_party_speed', 0)), format="%.2f", key="charter_party_speed", disabled=not edit_mode or voyage['status'] == 'Closed')
    with col3:
        voyage['general_info']['voyage_no'] = st.text_input("Voyage No", value=voyage['general_info'].get('voyage_no', ''), key="voyage_no", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['general_info']['charter_party_consumption'] = st.number_input("Charter Party Consumption", value=float(voyage['general_info'].get('charter_party_consumption', 0)), format="%.2f", key="charter_party_consumption", disabled=not edit_mode or voyage['status'] == 'Closed')
    with col4:
        voyage['general_info']['vessel_status'] = st.selectbox("Vessel Status", ["Laden", "Ballast"], index=0 if voyage['general_info'].get('vessel_status', '') == 'Laden' else 1, key="vessel_status", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['general_info']['revision_no'] = st.number_input("Revision No", value=int(voyage['general_info'].get('revision_no', 0)), format="%d", key="revision_no", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['general_info']['revision_date'] = st.date_input("Revision Date", value=voyage['general_info'].get('revision_date', datetime.date.today()), key="revision_date", disabled=not edit_mode or voyage['status'] == 'Closed')
    
    voyage['general_info']['comments'] = st.text_area("Comments", value=voyage['general_info'].get('comments', ''), key="comments", disabled=not edit_mode or voyage['status'] == 'Closed')

    st.subheader("Additional Information")
    st.write("MCR/RPM Range")

    col1, col2 = st.columns(2)
    with col1:
        st.write("Continuous Operable Range")
        voyage['general_info']['continuous_operable_min'] = st.number_input("Min", value=float(voyage['general_info'].get('continuous_operable_min', 0)), format="%.2f", key="continuous_operable_min", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['general_info']['continuous_operable_max'] = st.number_input("Max", value=float(voyage['general_info'].get('continuous_operable_max', 0)), format="%.2f", key="continuous_operable_max", disabled=not edit_mode or voyage['status'] == 'Closed')

        st.write("Prohibited Range")
        voyage['general_info']['prohibited_range_min'] = st.number_input("Min", value=float(voyage['general_info'].get('prohibited_range_min', 0)), format="%.2f", key="prohibited_range_min", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['general_info']['prohibited_range_max'] = st.number_input("Max", value=float(voyage['general_info'].get('prohibited_range_max', 0)), format="%.2f", key="prohibited_range_max", disabled=not edit_mode or voyage['status'] == 'Closed')

    with col2:
        st.write("Prohibited Range-2")
        voyage['general_info']['prohibited_range_2_min'] = st.number_input("Min", value=float(voyage['general_info'].get('prohibited_range_2_min', 0)), format="%.2f", key="prohibited_range_2_min", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['general_info']['prohibited_range_2_max'] = st.number_input("Max", value=float(voyage['general_info'].get('prohibited_range_2_max', 0)), format="%.2f", key="prohibited_range_2_max", disabled=not edit_mode or voyage['status'] == 'Closed')

        st.write("Ultra slow steaming range")
        voyage['general_info']['ultra_slow_steaming_min'] = st.number_input("Min", value=float(voyage['general_info'].get('ultra_slow_steaming_min', 0)), format="%.2f", key="ultra_slow_steaming_min", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['general_info']['ultra_slow_steaming_max'] = st.number_input("Max", value=float(voyage['general_info'].get('ultra_slow_steaming_max', 0)), format="%.2f", key="ultra_slow_steaming_max", disabled=not edit_mode or voyage['status'] == 'Closed')

def voyage_itinerary():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode

    if len(voyage['itinerary']) == 0:
        voyage['itinerary'] = pd.DataFrame([
            {"Segment ID": 0, "Port Code": "", "Port Name": "", "Transit Port": False, "ETA": "", "ETB": "", "ETD": "", "Actual Arrival(EOSP)": "", "Arrival Date(AB)": "", "Departure Date(DB)": "", "Actual Departure(COSP)": ""},
            {"Segment ID": 1, "Port Code": "", "Port Name": "", "Transit Port": False, "ETA": "", "ETB": "", "ETD": "", "Actual Arrival(EOSP)": "", "Arrival Date(AB)": "", "Departure Date(DB)": "", "Actual Departure(COSP)": ""}
        ])

    st.subheader("Voyage Itinerary")

    # Display the itinerary table
    edited_df = st.data_editor(
        voyage['itinerary'],
        disabled=not edit_mode or voyage['status'] == 'Closed',
        num_rows="dynamic",
        key="itinerary_editor"
    )

    # Update the voyage itinerary with edited data
    voyage['itinerary'] = edited_df

    # Add intermediate port functionality
    if edit_mode and voyage['status'] != 'Closed':
        col1, col2 = st.columns([1, 3])
        with col1:
            insert_index = st.number_input("Insert after row:", min_value=0, max_value=len(voyage['itinerary'])-1, value=0, step=1)
        with col2:
            if st.button("Add Intermediate Port"):
                new_row = pd.DataFrame([{"Segment ID": insert_index + 0.5}])
                voyage['itinerary'] = pd.concat([voyage['itinerary'].iloc[:insert_index+1], new_row, voyage['itinerary'].iloc[insert_index+1:]], ignore_index=True)
                voyage['itinerary']['Segment ID'] = range(len(voyage['itinerary']))
                st.experimental_rerun()

    # Display segment details
    st.subheader("Segment Details")
    segment_options = [f"Segment {index} - {row['Port Name']}" for index, row in voyage['itinerary'].iterrows()]
    selected_segment = st.selectbox("Select a segment to view details:", segment_options)
    
    if selected_segment:
        segment_index = int(selected_segment.split(" - ")[0].split(" ")[1])
        segment_details(segment_index)

def segment_details(segment_id):
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    
    if 'segment_details' not in voyage:
        voyage['segment_details'] = {}
    
    if segment_id not in voyage['segment_details']:
        voyage['segment_details'][segment_id] = {}
    
    segment_info = voyage['segment_details'][segment_id]
    
    st.write(f"Detailed Information for Segment {segment_id}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        segment_info['latitude'] = st.text_input("Latitude", value=segment_info.get('latitude', ''), key=f"lat_{segment_id}", disabled=not edit_mode or voyage['status'] == 'Closed')
        segment_info['forward_draft'] = st.number_input("Forward Draft (mtr)", value=float(segment_info.get('forward_draft', 0)), format="%.2f", key=f"fwd_draft_{segment_id}", disabled=not edit_mode or voyage['status'] == 'Closed')
        segment_info['gm'] = st.number_input("GM (mtr)", value=float(segment_info.get('gm', 0)), format="%.2f", key=f"gm_{segment_id}", disabled=not edit_mode or voyage['status'] == 'Closed')
    with col2:
        segment_info['longitude'] = st.text_input("Longitude", value=segment_info.get('longitude', ''), key=f"long_{segment_id}", disabled=not edit_mode or voyage['status'] == 'Closed')
        segment_info['after_draft'] = st.number_input("After Draft (mtr)", value=float(segment_info.get('after_draft', 0)), format="%.2f", key=f"aft_draft_{segment_id}", disabled=not edit_mode or voyage['status'] == 'Closed')
        segment_info['displacement'] = st.number_input("Displacement (MT)", value=float(segment_info.get('displacement', 0)), format="%.2f", key=f"disp_{segment_id}", disabled=not edit_mode or voyage['status'] == 'Closed')
    with col3:
        segment_info['cargo_quantity'] = st.number_input("Cargo Quantity (mt)", value=float(segment_info.get('cargo_quantity', 0)), format="%.2f", key=f"cargo_{segment_id}", disabled=not edit_mode or voyage['status'] == 'Closed')
        segment_info['roll_period'] = st.number_input("Roll Period (sec)", value=float(segment_info.get('roll_period', 0)), format="%.2f", key=f"roll_{segment_id}", disabled=not edit_mode or voyage['status'] == 'Closed')
        segment_info['freeboard'] = st.number_input("Freeboard (mtr)", value=float(segment_info.get('freeboard', 0)), format="%.2f", key=f"freeboard_{segment_id}", disabled=not edit_mode or voyage['status'] == 'Closed')
        
def charterer_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    st.subheader("Charterer Information")
    
    for i, charterer in enumerate(voyage['charterer_info']):
        st.markdown(f"**Charterer {i+1}**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            charterer['type'] = st.text_input("Type", value=charterer.get('type', ''), key=f"charterer_type_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
            charterer['address_1'] = st.text_input("Address 1", value=charterer.get('address_1', ''), key=f"charterer_address1_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
        with col2:
            charterer['name'] = st.text_input("Name", value=charterer.get('name', ''), key=f"charterer_name_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
            charterer['address_2'] = st.text_input("Address 2", value=charterer.get('address_2', ''), key=f"charterer_address2_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
        with col3:
            charterer['phone'] = st.text_input("Phone No", value=charterer.get('phone', ''), key=f"charterer_phone_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
            charterer['mobile'] = st.text_input("Mobile No", value=charterer.get('mobile', ''), key=f"charterer_mobile_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
        with col4:
            charterer['email'] = st.text_input("Email Id", value=charterer.get('email', ''), key=f"charterer_email_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
        st.markdown("---")

    if edit_mode and voyage['status'] != 'Closed' and st.button("Add Charterer", key="add_charterer"):
        voyage['charterer_info'].append({})

def agent_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    st.subheader("Agent Information")
    
    for i, agent in enumerate(voyage['agent_info']):
        st.markdown(f"**Agent {i+1}**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            agent['type'] = st.text_input("Type", value=agent.get('type', ''), key=f"agent_type_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
            agent['address_1'] = st.text_input("Address 1", value=agent.get('address_1', ''), key=f"agent_address1_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
        with col2:
            agent['name'] = st.text_input("Name", value=agent.get('name', ''), key=f"agent_name_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
            agent['address_2'] = st.text_input("Address 2", value=agent.get('address_2', ''), key=f"agent_address2_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
        with col3:
            agent['phone'] = st.text_input("Phone No", value=agent.get('phone', ''), key=f"agent_phone_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
            agent['mobile'] = st.text_input("Mobile No", value=agent.get('mobile', ''), key=f"agent_mobile_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
        with col4:
            agent['email'] = st.text_input("Email Id", value=agent.get('email', ''), key=f"agent_email_{i}", disabled=not edit_mode or voyage['status'] == 'Closed')
        st.markdown("---")

    if edit_mode and voyage['status'] != 'Closed' and st.button("Add Agent", key="add_agent"):
        voyage['agent_info'].append({})

def zones():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        voyage['zones']['zone'] = st.text_input("Zone", value=voyage['zones'].get('zone', ''), key="zone", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['zones']['eta'] = st.text_input("ETA", value=voyage['zones'].get('eta', ''), key="eta", disabled=not edit_mode or voyage['status'] == 'Closed')
    with col2:
        voyage['zones']['area'] = st.text_input("Area", value=voyage['zones'].get('area', ''), key="area", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['zones']['etd'] = st.text_input("ETD", value=voyage['zones'].get('etd', ''), key="etd", disabled=not edit_mode or voyage['status'] == 'Closed')
    with col3:
        voyage['zones']['latitude_entry'] = st.text_input("Latitude(Entry Point)", value=voyage['zones'].get('latitude_entry', ''), key="lat_entry", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['zones']['latitude_exit'] = st.text_input("Latitude(Exit Point)", value=voyage['zones'].get('latitude_exit', ''), key="lat_exit", disabled=not edit_mode or voyage['status'] == 'Closed')
    with col4:
        voyage['zones']['longitude_entry'] = st.text_input("Longitude(Entry Point)", value=voyage['zones'].get('longitude_entry', ''), key="long_entry", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['zones']['longitude_exit'] = st.text_input("Longitude(Exit Point)", value=voyage['zones'].get('longitude_exit', ''), key="long_exit", disabled=not edit_mode or voyage['status'] == 'Closed')

def log():
    voyage = st.session_state.current_voyage
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Created By", value=voyage['log'].get('created_by', ''), key="created_by", disabled=True)
    with col2:
        st.date_input("Created Date", value=voyage['log'].get('created_date', datetime.date.today()), key="created_date", disabled=True)
    with col3:
        st.text_input("Last Modified by", value=voyage['log'].get('last_modified_by', ''), key="last_modified_by", disabled=True)
    with col4:
        st.text_input("Last Modified Datetime", value=voyage['log'].get('last_modified_datetime', ''), key="last_modified_datetime", disabled=True)

def display_past_voyages():
    st.subheader("Past Voyages")
    for voyage in st.session_state.voyages:
        if voyage != st.session_state.current_voyage:
            col1, col2, col3 = st.columns([2,2,1])
            with col1:
                st.write(f"Voyage ID: {voyage['id']}")
            with col2:
                st.write(f"Status: {voyage['status']}")
            with col3:
                if st.button("View", key=f"view_{voyage['id']}"):
                    st.session_state.current_voyage = voyage
                    st.experimental_rerun()

def main():
    st.title("Voyage Manifest")

    if st.session_state.current_voyage is None:
        st.write("No active voyage. Start a new voyage manifest.")
        if st.button("Start New Voyage Manifest"):
            create_new_voyage()
            st.success(f"New Voyage Manifest started in Draft mode! Voyage ID: {st.session_state.current_voyage['id']}")
    else:
        display_voyage_manifest()

    display_past_voyages()

if __name__ == "__main__":
    main()
