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
            "Leg ID", "Vessel Status", "Port Code", "Port Name", "Charter Party Speed", "Charter Party Consumption",
            "Transit Port", "Time Zone", "ETA (LT)", "ETB (LT)", "ETD (LT)", "Actual EOSP", "Actual Arrival Berth",
            "Actual Departure", "Actual COSP", "Berth/Terminal Name"
        ]),
        'segment_details': pd.DataFrame(columns=[
            "Lat", "Long", "Cargo qty (mT/m3)", "Fwd draft", "Aft Draft", "Roll period (sec)", "GM (mtr)",
            "Displacement (mT)", "Freeboard (mtr)"
        ]),
        'general_info': {},
        'additional_info': {
            "optimization_objective": "",
            "instructed_speed": 0.0,
            "min_voyage_cost": 0.0
        },
        'charterer_info': [],
        'agent_info': [],
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

    with st.expander("Segment Details", expanded=False):
        segment_details()

    with st.expander("Additional Information", expanded=False):
        additional_information()

    with st.expander("Charterer Information", expanded=False):
        charterer_info()

    with st.expander("Agent Information", expanded=False):
        agent_info()

    with st.expander("Log", expanded=False):
        log()

def general_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    
    st.subheader("General Information")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        voyage['general_info']['vessel_code'] = st.text_input("Vessel Code", value=voyage['general_info'].get('vessel_code', ''), key="vessel_code", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['general_info']['voyage_id'] = st.text_input("Voyage ID", value=voyage['general_info'].get('voyage_id', ''), key="voyage_id", disabled=True)
    with col2:
        voyage['general_info']['vessel_name'] = st.text_input("Vessel Name", value=voyage['general_info'].get('vessel_name', ''), key="vessel_name", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['general_info']['revision_no'] = st.number_input("Revision No", value=int(voyage['general_info'].get('revision_no', 0)), key="revision_no", disabled=not edit_mode or voyage['status'] == 'Closed')
    with col3:
        voyage['general_info']['voyage_no'] = st.text_input("Voyage No.", value=voyage['general_info'].get('voyage_no', ''), key="voyage_no", disabled=not edit_mode or voyage['status'] == 'Closed')
        voyage['general_info']['revision_date'] = st.date_input("Revision Date", value=voyage['general_info'].get('revision_date', datetime.date.today()), key="revision_date", disabled=not edit_mode or voyage['status'] == 'Closed')
    with col4:
        voyage['general_info']['comments'] = st.text_area("Comments", value=voyage['general_info'].get('comments', ''), key="comments", disabled=not edit_mode or voyage['status'] == 'Closed')

def voyage_itinerary():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode

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

def segment_details():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode

    # Ensure 'segment_details' is initialized
    if 'segment_details' not in voyage or voyage['segment_details'] is None:
        voyage['segment_details'] = pd.DataFrame(columns=[
            "Lat", "Long", "Cargo qty (mT/m3)", "Fwd draft", "Aft Draft", "Roll period (sec)", "GM (mtr)",
            "Displacement (mT)", "Freeboard (mtr)"
        ])

    st.subheader("Segment Details")

    edited_df = st.data_editor(
        voyage['segment_details'],
        disabled=not edit_mode or voyage['status'] == 'Closed',
        num_rows="dynamic",
        key="segment_details_editor"
    )

    voyage['segment_details'] = edited_df

def additional_information():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode

    # Ensure 'additional_info' is initialized
    if 'additional_info' not in voyage or voyage['additional_info'] is None:
        voyage['additional_info'] = {
            "optimization_objective": "",
            "instructed_speed": 0.0,
            "min_voyage_cost": 0.0
        }

    st.subheader("Additional Information")
    col1, col2, col3, col4 = st.columns(4)

    voyage['additional_info']['optimization_objective'] = st.text_input("Optimization Objective", value=voyage['additional_info'].get('optimization_objective', ''), key="optimization_objective", disabled=not edit_mode or voyage['status'] == 'Closed')
    voyage['additional_info']['instructed_speed'] = st.number_input("Instructed Speed", value=float(voyage['additional_info'].get('instructed_speed', 0)), format="%.2f", key="instructed_speed", disabled=not edit_mode or voyage['status'] == 'Closed')
    voyage['additional_info']['min_voyage_cost'] = st.number_input("Min Voyage Cost (Hire + Bunker)", value=float(voyage['additional_info'].get('min_voyage_cost', 0)), format="%.2f", key="min_voyage_cost", disabled=not edit_mode or voyage['status'] == 'Closed')

def charterer_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode

    st.subheader("Charterer Information")
    if edit_mode and st.button("Add Charterer"):
        voyage['charterer_info'].append({})

    for idx, charterer in enumerate(voyage['charterer_info']):
        col1, col2 = st.columns(2)
        charterer['name'] = st.text_input(f"Name {idx + 1}", value=charterer.get('name', ''), key=f"charterer_name_{idx}", disabled=not edit_mode)
        charterer['type'] = st.text_input(f"Type {idx + 1}", value=charterer.get('type', ''), key=f"charterer_type_{idx}", disabled=not edit_mode)

def agent_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode

    st.subheader("Agent Information")
    if edit_mode and st.button("Add Agent"):
        voyage['agent_info'].append({})

    for idx, agent in enumerate(voyage['agent_info']):
        col1, col2 = st.columns(2)
        agent['name'] = st.text_input(f"Name {idx + 1}", value=agent.get('name', ''), key=f"agent_name_{idx}", disabled=not edit_mode)
        agent['type'] = st.text_input(f"Type {idx + 1}", value=agent.get('type', ''), key=f"agent_type_{idx}", disabled=not edit_mode)

def log():
    voyage = st.session_state.current_voyage
    st.text_input("Created By", value=voyage['log'].get('created_by', ''), disabled=True)
    st.text_input("Last Modified By", value=voyage['log'].get('last_modified_by', ''), disabled=True)
    st.text_input("Last Modified Datetime", value=voyage['log'].get('last_modified_datetime', ''), disabled=True)

def main():
    st.title("Voyage Manifest")

    if st.session_state.current_voyage is None:
        st.write("No active voyage. Start a new voyage manifest.")
        if st.button("Start New Voyage Manifest"):
            create_new_voyage()
            st.success(f"New Voyage Manifest started in Draft mode! Voyage ID: {st.session_state.current_voyage['id']}")
    else:
        display_voyage_manifest()

if __name__ == "__main__":
    main()
