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
            "Leg ID", "Vessel Status", "Port Code", "Port Name", 
            "Charter Party Speed", "Charter Party Consumption", "Transit Port",
            "Time Zone", "ETA (LT)", "ETB (LT)", "ETD (LT)", 
            "Actual EOSP", "Actual Arrival Berth", "Actual Departure", 
            "Actual COSP", "Berth/Terminal Name"
        ]),
        'general_info': {},
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
                st.success(f"New Voyage Manifest started in Draft mode!")
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
                voyage['log']['last_modified_by'] = 'User'
                voyage['log']['last_modified_datetime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.success("Draft saved successfully!")
            else:
                st.error("Can only save drafts for voyages in Draft status.")

    with st.expander("Voyage Information", expanded=False):
        voyage_info()

    with st.expander("Voyage Itinerary", expanded=False):
        voyage_itinerary()

    with st.expander("Additional Information", expanded=False):
        additional_info()
    
    with st.expander("Charterer Information", expanded=False):
        charterer_info()

    with st.expander("Agent Information", expanded=False):
        agent_info()

    with st.expander("Log", expanded=False):
        log()

def voyage_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        voyage['general_info']['vessel_code'] = st.text_input(
            "Vessel Code", 
            value=voyage['general_info'].get('vessel_code', ''), 
            disabled=not edit_mode or voyage['status'] == 'Closed'
        )
        voyage['general_info']['vessel_name'] = st.text_input(
            "Vessel Name",
            value=voyage['general_info'].get('vessel_name', ''),
            disabled=not edit_mode or voyage['status'] == 'Closed'
        )

    with col2:
        voyage['general_info']['voyage_id'] = st.text_input(
            "Voyage ID",
            value=voyage['general_info'].get('voyage_id', ''),
            disabled=not edit_mode or voyage['status'] == 'Closed'
        )
        voyage['general_info']['voyage_no'] = st.text_input(
            "Voyage No.",
            value=voyage['general_info'].get('voyage_no', ''),
            disabled=not edit_mode or voyage['status'] == 'Closed'
        )

    with col3:
        voyage['general_info']['revision_no'] = st.number_input(
            "Revision No",
            value=int(voyage['general_info'].get('revision_no', 0)),
            disabled=not edit_mode or voyage['status'] == 'Closed'
        )
        voyage['general_info']['revision_date'] = st.date_input(
            "Revision Date",
            value=voyage['general_info'].get('revision_date', datetime.date.today()),
            disabled=not edit_mode or voyage['status'] == 'Closed'
        )

    voyage['general_info']['comments'] = st.text_area(
        "Comments",
        value=voyage['general_info'].get('comments', ''),
        disabled=not edit_mode or voyage['status'] == 'Closed'
    )

def voyage_itinerary():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode

    if len(voyage['itinerary']) == 0:
        voyage['itinerary'] = pd.DataFrame([
            {col: "" for col in voyage['itinerary'].columns}
            for _ in range(2)
        ])

    edited_df = st.data_editor(
        voyage['itinerary'],
        disabled=not edit_mode or voyage['status'] == 'Closed',
        num_rows="dynamic"
    )

    voyage['itinerary'] = edited_df

    show_segment_details = st.checkbox(
        "Show Segment Details",
        value=voyage.get('show_segment_details', False)
    )

    if show_segment_details:
        segment_details()

def segment_details():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    
    if 'segment_details' not in voyage:
        voyage['segment_details'] = {}
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Latitude")
        st.number_input("Forward Draft (mtr)")
        st.number_input("Roll Period (sec)")
        
    with col2:
        st.text_input("Longitude")
        st.number_input("After Draft (mtr)")
        st.number_input("GM (mtr)")
        
    with col3:
        st.number_input("Cargo Quantity (mt)")
        st.number_input("Displacement (MT)")
        st.number_input("Freeboard (mtr)")

def additional_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode

    # MCR/RPM Ranges
    st.subheader("MCR/RPM Ranges")
    
    for range_type in [
        "Continuous Operable Range", "Prohibited Range 1",
        "Prohibited Range 2", "Ultra Slow Steaming"
    ]:
        st.write(range_type)
        col1, col2 = st.columns(2)
        with col1:
            st.number_input(f"Min kW", key=f"{range_type}_min_kw")
            st.number_input(f"Max kW", key=f"{range_type}_max_kw")
        with col2:
            st.number_input(f"Min RPM", key=f"{range_type}_min_rpm")
            st.number_input(f"Max RPM", key=f"{range_type}_max_rpm")

    # Additional Parameters
    st.subheader("Additional Parameters")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Optimization Objective")
        st.number_input("Min Voyage Cost (Hire + Bunker)")
        st.number_input("Vertex Limit")
        
    with col2:
        st.number_input("Instructed Speed")
        st.text_input("Required Time to Arrive")
        st.number_input("Estimated ROBs on Dep Berth")
        
    with col3:
        st.number_input("USD Cost")
        st.number_input("Limit FOC in Rough Wx")
        st.text_input("Variable Speed")
        st.number_input("Fuel Used")
        st.number_input("Min FOC")
        st.text_input("Control Mode")
        st.number_input("Biofuel")

def charterer_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    
    for i, charterer in enumerate(voyage['charterer_info']):
        st.markdown(f"**Charterer {i+1}**")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Type", key=f"charterer_type_{i}")
            st.text_input("Name", key=f"charterer_name_{i}")
            st.text_input("Phone No", key=f"charterer_phone_{i}")
            st.text_input("Email Id", key=f"charterer_email_{i}")
            
        with col2:
            st.text_input("Address 1", key=f"charterer_addr1_{i}")
            st.text_input("Address 2", key=f"charterer_addr2_{i}")
            st.text_input("Mobile No", key=f"charterer_mobile_{i}")
        
        st.markdown("---")

    if edit_mode and st.button("Add Charterer"):
        voyage['charterer_info'].append({})

def agent_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    
    for i, agent in enumerate(voyage['agent_info']):
        st.markdown(f"**Agent {i+1}**")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Type", key=f"agent_type_{i}")
            st.text_input("Name", key=f"agent_name_{i}")
            st.text_input("Phone No", key=f"agent_phone_{i}")
            st.text_input("Email Id", key=f"agent_email_{i}")
            
        with col2:
            st.text_input("Address 1", key=f"agent_addr1_{i}")
            st.text_input("Address 2", key=f"agent_addr2_{i}")
            st.text_input("Mobile No", key=f"agent_mobile_{i}")
        
        st.markdown("---")

    if edit_mode and st.button("Add Agent"):
        voyage['agent_info'].append({})

def log():
    voyage = st.session_state.current_voyage
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Created By", value=voyage['log']['created_by'], disabled=True)
        st.date_input("Created Date", value=voyage['log']['created_date'], disabled=True)
    with col2:
        st.text_input("Last Modified by", value=voyage['log']['last_modified_by'], disabled=True)
        st.text_input("Last Modified Datetime", value=voyage['log']['last_modified_datetime'], disabled=True)

def main():
    st.title("Voyage Manifest")

    if st.session_state.current_voyage is None:
        st.write("No active voyage. Start a new voyage manifest.")
        if st.button("Start New Voyage Manifest"):
            create_new_voyage()
            st.success(f"New Voyage Manifest started in Draft mode!")
    else:
        display_voyage_manifest()

if __name__ == "__main__":
    main()
