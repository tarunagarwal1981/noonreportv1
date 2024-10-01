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

    # Initialize lists for bunkering and debunkering
    if 'bunkering_entries' not in st.session_state:
        st.session_state.bunkering_entries = []
    if 'debunkering_entries' not in st.session_state:
        st.session_state.debunkering_entries = []

    if 'bunker_survey_comments' not in st.session_state:
        st.session_state.bunker_survey_comments = ""

# Function to handle bunkering and debunkering details
def handle_bunkering_debunkering():
    col1, col2, col3 = st.columns(3)
    with col1:
        bunkering_happened = st.checkbox("Bunkering Happened")
    with col2:
        debunkering_happened = st.checkbox("Debunkering Happened")
    with col3:
        bunker_survey = st.checkbox("Bunker Survey")

    if bunkering_happened:
        st.markdown("<h4 style='font-size: 18px;'>Bunkering Details</h4>", unsafe_allow_html=True)
        for i, entry in enumerate(st.session_state.bunkering_entries):
            st.markdown(f"<h5 style='font-size: 16px;'>Bunkering Entry {i+1}</h5>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                entry['bdn_number'] = st.text_input("Bunker Delivery Note Number", key=f"bdn_number_{i}")
                entry['delivery_date'] = st.date_input("Bunker Delivery Date", key=f"delivery_date_{i}")
                entry['delivery_time'] = st.time_input("Bunker Delivery Time", key=f"delivery_time_{i}")
            with col2:
                entry['imo_number'] = st.text_input("IMO number", key=f"imo_number_{i}")
                entry['fuel_type'] = st.text_input("Fuel Type", key=f"fuel_type_{i}")
                entry['mass'] = st.number_input("Mass (mt)", min_value=0.0, step=0.1, key=f"mass_{i}")
            with col3:
                entry['lower_heating_value'] = st.number_input("Lower heating value (MJ/kg)", min_value=0.0, step=0.1, key=f"lower_heating_value_{i}")
                entry['eu_ghg_intensity'] = st.number_input("EU GHG emission intensity (gCO2eq/MJ)", min_value=0.0, step=0.1, key=f"eu_ghg_intensity_{i}")
                entry['imo_ghg_intensity'] = st.number_input("IMO GHG emission intensity (gCO2eq/MJ)", min_value=0.0, step=0.1, key=f"imo_ghg_intensity_{i}")
                entry['lcv_eu'] = st.number_input("Lower Calorific Value (EU) (MJ/kg)", min_value=0.0, step=0.1, key=f"lcv_eu_{i}")
                entry['sustainability'] = st.text_input("Sustainability", key=f"sustainability_{i}")
        if st.button("➕ Add Bunkering Entry"):
            st.session_state.bunkering_entries.append({})
            st.experimental_rerun()

    if debunkering_happened:
        st.markdown("<h4 style='font-size: 18px;'>Debunkering Details</h4>", unsafe_allow_html=True)
        for i, entry in enumerate(st.session_state.debunkering_entries):
            st.markdown(f"<h5 style='font-size: 16px;'>Debunkering Entry {i+1}</h5>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                entry['date'] = st.date_input("Date of Debunkering", key=f"debunker_date_{i}")
                entry['quantity'] = st.number_input("Quantity Debunkered (mt)", min_value=0.0, step=0.1, key=f"debunker_qty_{i}")
            with col2:
                entry['bdn_number'] = st.text_input("BDN Number of Debunkered Oil", key=f"debunker_bdn_{i}")
                entry['receipt_file'] = st.file_uploader("Upload Receipt", type=['pdf', 'jpg', 'png'], key=f"receipt_file_{i}")
        if st.button("➕ Add Debunkering Entry"):
            st.session_state.debunkering_entries.append({})
            st.experimental_rerun()

    if bunker_survey:
        st.text_area("Bunker Survey Comments", key="bunker_survey_comments")

    return bunkering_happened, debunkering_happened, bunker_survey

# Fuel based report functionality
def display_fuel_consumption_report(bunkering_happened, debunkering_happened, bunker_survey):
    def create_editable_dataframe():
        index = ['Previous ROB'] + st.session_state.consumers
        if bunkering_happened:
            index.append('Bunkered Qty')
        if debunkering_happened:
            index.append('Debunkered Qty')
        if bunker_survey:
            index.append('Bunker Survey Correction')
        index.append('Current ROB')

        # Create DataFrame with fuel types as columns
        df = pd.DataFrame(0, index=index, columns=st.session_state.fuel_types)
        
        # Fill 'Previous ROB' row
        df.loc['Previous ROB'] = st.session_state.previous_rob_fuel
        
        # Fill consumption data for consumers
        df.loc[st.session_state.consumers] = st.session_state.consumption_data_fuel
        
        # Handle Bunkered and Debunkered Quantities
        if bunkering_happened:
            total_bunkered = sum(entry.get('mass', 0) for entry in st.session_state.bunkering_entries)
            df.loc['Bunkered Qty'] = total_bunkered
        
        if debunkering_happened:
            total_debunkered = sum(entry.get('quantity', 0) for entry in st.session_state.debunkering_entries)
            df.loc['Debunkered Qty'] = total_debunkered
        
        # Handle Bunker Survey Correction
        if bunker_survey:
            df.loc['Bunker Survey Correction'] = st.session_state.bunker_survey_correction_fuel
        
        # Calculate Current ROB
        total_consumption = pd.to_numeric(df.loc[st.session_state.consumers].sum(), errors='coerce').fillna(0)
        df.loc['Current ROB'] = pd.to_numeric(df.loc['Previous ROB'], errors='coerce').fillna(0) - total_consumption
        
        if bunkering_happened:
            df.loc['Current ROB'] += df.loc['Bunkered Qty']
        if debunkering_happened:
            df.loc['Current ROB'] -= df.loc['Debunkered Qty']
        if bunker_survey:
            df.loc['Current ROB'] += df.loc['Bunker Survey Correction']
        
        return df

    df = create_editable_dataframe()
    
    st.subheader("Fuel Consumption Data")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=f"fuel_consumption_editor_{uuid.uuid4()}"
    )

    # Update session state
    st.session_state.consumption_data_fuel = edited_df.loc[st.session_state.consumers]
    st.session_state.previous_rob_fuel = edited_df.loc['Previous ROB']
    if bunker_survey:
        st.session_state.bunker_survey_correction_fuel = edited_df.loc['Bunker Survey Correction']

# Main app functionality
def main():
    initialize_session_state()

    st.title("Fuel Consumption and BDN Report")

    # Handle bunkering and debunkering inputs
    bunkering_happened, debunkering_happened, bunker_survey = handle_bunkering_debunkering()

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

    # Display corresponding report based on the selected view
    if fuel_type_view:
        display_fuel_consumption_report(bunkering_happened, debunkering_happened, bunker_survey)
    elif bdn_view:
        # Similar function for BDN-based report will be created here
        pass

    # Submit button
    if st.button("Submit Report", type="primary"):
        st.success("Report submitted successfully!")

if __name__ == "__main__":
    main()
