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
        'leg_details': {},
        'log': {
            'created_by': 'System',
            'created_date': datetime.date.today(),
            'last_modified_by': 'System',
            'last_modified_datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    st.session_state.voyages.append(new_voyage)
    st.session_state.current_voyage = new_voyage

def voyage_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    
    st.subheader("Voyage Information")
    
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

def display_past_voyages():
    st.subheader("Past Voyages")
    if len(st.session_state.voyages) > 1:  # More than just the current voyage
        for voyage in st.session_state.voyages:
            if voyage != st.session_state.current_voyage:
                col1, col2, col3, col4 = st.columns([2,2,1,1])
                with col1:
                    st.write(f"Voyage ID: {voyage['id']}")
                with col2:
                    st.write(f"Status: {voyage['status']}")
                with col3:
                    st.write(f"Created: {voyage['log']['created_date']}")
                with col4:
                    if st.button("View", key=f"view_{voyage['id']}"):
                        st.session_state.current_voyage = voyage
                        st.experimental_rerun()
    else:
        st.write("No past voyages available.")

def main():
    st.title("Voyage Manifest")

    if st.session_state.current_voyage is None:
        st.write("No active voyage. Start a new voyage manifest.")
        if st.button("Start New Voyage Manifest"):
            create_new_voyage()
            st.success(f"New Voyage Manifest started in Draft mode!")
    else:
        display_voyage_manifest()
        st.markdown("---")
        display_past_voyages()

if __name__ == "__main__":
    main()
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

    with col4:
        voyage['general_info']['comments'] = st.text_area(
            "Comments",
            value=voyage['general_info'].get('comments', ''),
            disabled=not edit_mode or voyage['status'] == 'Closed'
        )

def voyage_itinerary():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode

    st.subheader("Voyage Itinerary")

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

    # Add intermediate leg functionality
    if edit_mode and voyage['status'] != 'Closed':
        col1, col2 = st.columns([1, 3])
        with col1:
            insert_index = st.number_input("Insert after leg:", min_value=0, max_value=len(voyage['itinerary'])-1, value=0, step=1)
        with col2:
            if st.button("Add Intermediate Leg"):
                new_row = pd.DataFrame([{"Leg ID": insert_index + 0.5}])
                voyage['itinerary'] = pd.concat([voyage['itinerary'].iloc[:insert_index+1], new_row, voyage['itinerary'].iloc[insert_index+1:]], ignore_index=True)
                voyage['itinerary']['Leg ID'] = range(len(voyage['itinerary']))
                st.experimental_rerun()

    # Display leg details
    show_leg_details = st.checkbox("Show Leg Details", value=voyage.get('show_leg_details', False))
    voyage['show_leg_details'] = show_leg_details

    if show_leg_details:
        st.subheader("Leg Details")
        leg_options = [f"Leg {index} - {row['Port Name']}" for index, row in voyage['itinerary'].iterrows()]
        selected_leg = st.selectbox("Select a leg to view details:", leg_options)
        
        if selected_leg:
            leg_index = int(selected_leg.split(" - ")[0].split(" ")[1])
            leg_details(leg_index)

def leg_details(leg_id):
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    
    if 'leg_details' not in voyage:
        voyage['leg_details'] = {}
    
    if leg_id not in voyage['leg_details']:
        voyage['leg_details'][leg_id] = {}
    
    leg_info = voyage['leg_details'][leg_id]
    
    st.write(f"Detailed Information for Leg {leg_id}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        leg_info['latitude'] = st.text_input("Latitude", value=leg_info.get('latitude', ''), key=f"lat_{leg_id}")
        leg_info['forward_draft'] = st.number_input("Forward Draft (mtr)", value=float(leg_info.get('forward_draft', 0)), format="%.2f", key=f"fwd_draft_{leg_id}")
        leg_info['gm'] = st.number_input("GM (mtr)", value=float(leg_info.get('gm', 0)), format="%.2f", key=f"gm_{leg_id}")
    with col2:
        leg_info['longitude'] = st.text_input("Longitude", value=leg_info.get('longitude', ''), key=f"long_{leg_id}")
        leg_info['after_draft'] = st.number_input("After Draft (mtr)", value=float(leg_info.get('after_draft', 0)), format="%.2f", key=f"aft_draft_{leg_id}")
        leg_info['roll_period'] = st.number_input("Roll Period (sec)", value=float(leg_info.get('roll_period', 0)), format="%.2f", key=f"roll_{leg_id}")
    with col3:
        leg_info['cargo_quantity'] = st.number_input("Cargo Quantity (mt)", value=float(leg_info.get('cargo_quantity', 0)), format="%.2f", key=f"cargo_{leg_id}")
        leg_info['displacement'] = st.number_input("Displacement (MT)", value=float(leg_info.get('displacement', 0)), format="%.2f", key=f"disp_{leg_id}")
        leg_info['freeboard'] = st.number_input("Freeboard (mtr)", value=float(leg_info.get('freeboard', 0)), format="%.2f", key=f"freeboard_{leg_id}")
    with col4:
        leg_info['additional_notes'] = st.text_area("Additional Notes", value=leg_info.get('additional_notes', ''), key=f"notes_{leg_id}")

def additional_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode

    st.subheader("MCR/RPM Ranges")
    
    for range_type in [
        "Continuous Operable Range", "Prohibited Range 1",
        "Prohibited Range 2", "Ultra Slow Steaming"
    ]:
        st.write(range_type)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.number_input(f"Min kW", key=f"{range_type}_min_kw")
        with col2:
            st.number_input(f"Max kW", key=f"{range_type}_max_kw")
        with col3:
            st.number_input(f"Min RPM", key=f"{range_type}_min_rpm")
        with col4:
            st.number_input(f"Max RPM", key=f"{range_type}_max_rpm")

    st.subheader("Additional Parameters")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.text_input("Optimization Objective")
        st.number_input("Min Voyage Cost (Hire + Bunker)")
        st.number_input("Vertex Limit")
        st.number_input("Instructed Speed")
        
    with col2:
        st.text_input("Required Time to Arrive")
        st.number_input("Estimated ROBs on Dep Berth")
        st.number_input("USD Cost")
        st.number_input("Limit FOC in Rough Wx")
        
    with col3:
        st.text_input("Variable Speed")
        st.number_input("Fuel Used")
        st.number_input("Min FOC")
        st.text_input("Control Mode")
        
    with col4:
        st.number_input("Biofuel")
        st.text_area("Additional Notes")

def charterer_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    
    st.subheader("Charterer Information")
    
    for i, charterer in enumerate(voyage['charterer_info']):
        st.markdown(f"**Charterer {i+1}**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            charterer['type'] = st.text_input("Type", value=charterer.get('type', ''), key=f"charterer_type_{i}")
            charterer['name'] = st.text_input("Name", value=charterer.get('name', ''), key=f"charterer_name_{i}")
        with col2:
            charterer['phone'] = st.text_input("Phone No", value=charterer.get('phone', ''), key=f"charterer_phone_{i}")
            charterer['email'] = st.text_input("Email Id", value=charterer.get('email', ''), key=f"charterer_email_{i}")
        with col3:
            charterer['address_1'] = st.text_input("Address 1", value=charterer.get('address_1', ''), key=f"charterer_addr1_{i}")
            charterer['address_2'] = st.text_input("Address 2", value=charterer.get('address_2', ''), key=f"charterer_addr2_{i}")
        with col4:
            charterer['mobile'] = st.text_input("Mobile No", value=charterer.get('mobile', ''), key=f"charterer_mobile_{i}")
        
        st.markdown("---")

    if edit_mode and voyage['status'] != 'Closed' and st.button("Add Charterer"):
        voyage['charterer_info'].append({})

def agent_info():
    voyage = st.session_state.current_voyage
    edit_mode = st.session_state.edit_mode
    
    st.subheader("Agent Information")
    
    for i, agent in enumerate(voyage['agent_info']):
        st.markdown(f"**Agent {i+1}**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            agent['type'] = st.text_input("Type", value=agent.get('type', ''), key=f"agent_type_{i}")
            agent['name'] = st.text_input("Name", value=agent.get('name', ''), key=f"agent_name_{i}")
        with col2:
            agent['phone'] = st.text_input("Phone No", value=agent.get('phone', ''), key=f"agent_phone_{i}")
            agent['email'] = st.text_input("Email Id", value=agent.get('email', ''), key=f"agent_email_{i}")
        with col3:
            agent['address_1'] = st.text_input("Address 1", value=agent.get('address_1', ''), key=f"agent_addr1_{i}")
            agent['address_2'] = st.text_input("Address 2", value=agent.get('address_2', ''), key=f"agent_addr2_{i}")
        with col4:
            agent['mobile'] = st.text_input("Mobile No", value=agent.get('mobile', ''), key=f"agent_mobile_{i}")
        
        st.markdown("---")

    if edit_mode and voyage['status'] != 'Closed' and st.button("Add Agent"):
        voyage['agent_info'].append({})

def log():
    voyage = st.session_state.current_voyage
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_input("Created By", value=voyage['log']['created_by'], disabled=True)
    with col2:
        st.date_input("Created Date", value=voyage['log']['created_date'], disabled=True)
    with col3:
        st.text_input("Last Modified by", value=voyage['log']['last_modified_by'], disabled=True)
    with col4:
        st.text_input("Last Modified Datetime", value=voyage['log']['last_modified_datetime'], disabled=True)

def display_voyage_manifest():
    voyage = st.session_state.current_voyage
    st.write(f"Voyage ID: {voyage['id']}")
    st.write(f"Current Voyage Status: {voyage['status']}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
