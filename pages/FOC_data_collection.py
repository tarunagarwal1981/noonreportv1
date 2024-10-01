import streamlit as st
import pandas as pd
import numpy as np
import random
import string
import uuid

st.set_page_config(layout="wide", page_title="Fuel Consumption and BDN Report")

def generate_random_bdn_numbers():
    """Generates three unique random alphanumeric BDN numbers (8 characters)."""
    bdn_numbers = [''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) for _ in range(3)]
    return bdn_numbers

# Initialize session state
def initialize_session_state():
    if 'consumers' not in st.session_state:
        st.session_state.consumers = [
            'Main Engine', 'Aux Engine1', 'Aux Engine2', 'Aux Engine3',
            'Boiler 1', '    Boiler 1 - Cargo Heating', '    Boiler 1 - Discharge',
            'Boiler 2', '    Boiler 2 - Cargo Heating', '    Boiler 2 - Discharge',
            'IGG', 'Incinerator', 'DPP1', 'DPP2', 'DPP3'
        ]
    if 'fuel_types' not in st.session_state:
        st.session_state.fuel_types = ['HFO', 'LFO', 'MGO/MDO', 'LPG', 'LNG', 'Methanol', 'Ethanol', 'Others', 'Other Fuel Type']
    if 'tanks' not in st.session_state:
        st.session_state.tanks = [f'Tank {i}' for i in range(1, 9)]
    if 'viscosity' not in st.session_state:
        st.session_state.viscosity = {item: np.random.uniform(20, 100) for item in st.session_state.fuel_types + st.session_state.tanks}
    if 'sulfur' not in st.session_state:
        st.session_state.sulfur = {item: np.random.uniform(0.05, 0.49) for item in st.session_state.fuel_types + st.session_state.tanks}
    
    # Initialize separate previous ROBs for fuel types and tanks
    if 'previous_rob_fuel' not in st.session_state:
        st.session_state.previous_rob_fuel = pd.Series({fuel: np.random.uniform(100, 1000) for fuel in st.session_state.fuel_types})
    if 'previous_rob_tank' not in st.session_state:
        st.session_state.previous_rob_tank = pd.Series({tank: np.random.uniform(100, 1000) for tank in st.session_state.tanks})
    
    if 'bunker_survey_correction_fuel' not in st.session_state:
        st.session_state.bunker_survey_correction_fuel = pd.Series({fuel: 0 for fuel in st.session_state.fuel_types})
    if 'bunker_survey_correction_tank' not in st.session_state:
        st.session_state.bunker_survey_correction_tank = pd.Series({tank: 0 for tank in st.session_state.tanks})
    
    # Initialize consumption data separately for fuel types and tanks
    if 'consumption_data_fuel' not in st.session_state:
        st.session_state.consumption_data_fuel = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.fuel_types)
    if 'consumption_data_tank' not in st.session_state:
        st.session_state.consumption_data_tank = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.tanks)
    
    if 'bunker_survey_comments' not in st.session_state:
        st.session_state.bunker_survey_comments = ""

# BDN based report functionality
def display_bdn_consumption_report(bunker_survey):
    def create_editable_dataframe():
        # Define the index (now starting with 'BDN Number')
        index = ['BDN Number', 'Previous ROB'] + st.session_state.consumers
        if bunker_survey:
            index.append('Bunker Survey Correction')
        index.append('Current ROB')
        
        # Create DataFrame
        df = pd.DataFrame(index=index, columns=st.session_state.tanks)
        
        # Generate three random BDN numbers and repeat them across columns
        bdn_numbers = generate_random_bdn_numbers()
        df.loc['BDN Number'] = [bdn_numbers[i % 3] for i in range(len(st.session_state.tanks))]
        
        # Fill 'Previous ROB' row
        df.loc['Previous ROB'] = st.session_state.previous_rob_tank
        
        # Fill consumption data for consumers
        df.loc[st.session_state.consumers] = st.session_state.consumption_data_tank
        
        # Fill bunker survey correction if needed
        if bunker_survey:
            df.loc['Bunker Survey Correction'] = st.session_state.bunker_survey_correction_tank
        
        # Ensure total consumption calculation is numeric
        total_consumption = pd.to_numeric(df.loc[st.session_state.consumers].sum(), errors='coerce').fillna(0)
        
        # Calculate Current ROB
        df.loc['Current ROB'] = pd.to_numeric(df.loc['Previous ROB'], errors='coerce').fillna(0) - total_consumption
        
        # Add bunker correction to Current ROB if present
        if bunker_survey:
            df.loc['Current ROB'] += pd.to_numeric(df.loc['Bunker Survey Correction'], errors='coerce').fillna(0)
        
        return df

    df = create_editable_dataframe()
    
    st.subheader("BDN Based Fuel Consumption Data")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=f"bdn_consumption_editor_{uuid.uuid4()}"
    )

    # Update session state
    st.session_state.consumption_data_tank = edited_df.loc[st.session_state.consumers]
    st.session_state.previous_rob_tank = edited_df.loc['Previous ROB']
    if bunker_survey:
        st.session_state.bunker_survey_correction_tank = edited_df.loc['Bunker Survey Correction']

def display_additional_table():
    st.subheader("Additional Consumption Data")
    additional_data = pd.DataFrame({
        'Work': [0, 0, 0, 0],
        'SFOC': [0, 0, 0, ''],
        'Fuel Type': ['', '', '', '']
    }, index=['Reefer container', 'Cargo cooling', 'Heating/Discharge pump', 'Shore-Side Electricity'])
    
    edited_additional_data = st.data_editor(
        additional_data,
        use_container_width=True,
        num_rows="dynamic",
        key=f"additional_consumption_editor_{uuid.uuid4()}"
    )

# Main app functionality
def main():
    initialize_session_state()

    st.title("Fuel Consumption and BDN Report")

    # Checkbox for view selection
    col1, col2 = st.columns(2)
    with col1:
        fuel_type_view = st.checkbox("Fuel Type based", value=True)
    with col2:
        bdn_view = st.checkbox("BDN based", value=False)

    # Ensure only one view is selected
    if fuel_type_view and bdn_view:
        st.warning("Please select only one view type.")
        st.stop()
    elif not fuel_type_view and not bdn_view:
        st.warning("Please select a view type.")
        st.stop()

    # Bunker survey checkbox
    bunker_survey = st.checkbox("Bunker Survey")
    if bunker_survey:
        st.session_state.bunker_survey_comments = st.text_area("Bunker Survey Comments", value=st.session_state.bunker_survey_comments, height=100)

    # Display corresponding report based on the selected view
    if fuel_type_view:
        # Call the function for fuel type report (not shown in the question, so it should already exist)
        pass  # Add the existing fuel type report function call here.
    elif bdn_view:
        display_bdn_consumption_report(bunker_survey)

    # Display additional table
    display_additional_table()

    # Submit button
    if st.button("Submit Report", type="primary"):
        st.success("Report submitted successfully!")

if __name__ == "__main__":
    main()
