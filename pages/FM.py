import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for flowmeters and configurations if not exists
if 'flowmeters' not in st.session_state:
    st.session_state.flowmeters = []
if 'configurations' not in st.session_state:
    st.session_state.configurations = {
        'ME': {'flowmeters': [], 'formula': ''},
        'AE': {'flowmeters': [], 'formula': ''},
        'BLR': {'flowmeters': [], 'formula': ''},
        'OTHER': {'flowmeters': [], 'formula': ''}
    }

# App title
st.title('Vessel Flowmeter Configuration and Calculation')

# Configuration Section
st.header('System Configuration')

# Flowmeter Management
with st.expander("Flowmeter Management", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        new_flowmeter = st.text_input('Enter new flowmeter name')
    with col2:
        if st.button('Add Flowmeter'):
            if new_flowmeter and new_flowmeter not in st.session_state.flowmeters:
                st.session_state.flowmeters.append(new_flowmeter)
                st.success(f'Flowmeter {new_flowmeter} added successfully!')

    # Display existing flowmeters in a table
    if st.session_state.flowmeters:
        st.subheader('Existing Flowmeters')
        fm_df = pd.DataFrame(st.session_state.flowmeters, columns=['Flowmeter Name'])
        st.dataframe(fm_df)

# Equipment Configuration
with st.expander("Equipment Configuration", expanded=True):
    equipment_type = st.selectbox('Select Equipment Type', ['ME', 'AE', 'BLR', 'OTHER'])

    st.subheader(f'{equipment_type} Configuration')

    # Select flowmeters for the equipment
    selected_flowmeters = st.multiselect(
        'Select Flowmeters',
        st.session_state.flowmeters,
        default=st.session_state.configurations[equipment_type]['flowmeters']
    )

    # Formula configuration
    formula_type = st.selectbox(
        'Select Formula Type',
        ['Simple Difference', 'Multiple Flowmeter Difference', 'Custom Formula'],
        key=f'{equipment_type}_formula'
    )

    if formula_type == 'Custom Formula':
        custom_formula = st.text_input(
            'Enter Custom Formula',
            help='Use F1, F2, etc. to refer to flowmeters in order of selection'
        )

    if st.button('Save Configuration'):
        st.session_state.configurations[equipment_type]['flowmeters'] = selected_flowmeters
        if formula_type == 'Custom Formula':
            st.session_state.configurations[equipment_type]['formula'] = custom_formula
        else:
            st.session_state.configurations[equipment_type]['formula'] = formula_type
        st.success(f'Configuration saved for {equipment_type}')

# Display current configurations
with st.expander("Current Configurations", expanded=True):
    for eq_type, config in st.session_state.configurations.items():
        st.subheader(f'{eq_type} Configuration')
        st.write(f"Assigned Flowmeters: {', '.join(config['flowmeters']) if config['flowmeters'] else 'None'}")
        st.write(f"Formula Type: {config['formula'] if config['formula'] else 'Not configured'}")

# Calculation Section
st.header('Consumption Calculations')

def calculate_consumption(readings, formula_type):
    if formula_type == 'Simple Difference':
        return float(readings['current'][0]) - float(readings['previous'][0])
    elif formula_type == 'Multiple Flowmeter Difference':
        total = 0
        for i in range(len(readings['current'])):
            total += float(readings['current'][i]) - float(readings['previous'][i])
        return total
    else:
        # Handle custom formula here
        return 0  # Placeholder

# Create tabs for different consumption types
tab1, tab2, tab3, tab4 = st.tabs(['ME Consumption', 'AE Consumption', 'BLR Consumption', 'Other Equipment'])

def create_consumption_inputs(equipment_type, tab):
    with tab:
        st.subheader(f'{equipment_type} Consumption')
        config = st.session_state.configurations[equipment_type]

        if not config['flowmeters']:
            st.warning(f'No flowmeters configured for {equipment_type}. Please configure in the Equipment Configuration section.')
            return

        readings = {'current': [], 'previous': []}

        for fm in config['flowmeters']:
            col1, col2 = st.columns(2)
            with col1:
                current = st.number_input(f'Current Reading - {fm}', key=f'{equipment_type}_{fm}_current')
                readings['current'].append(current)
            with col2:
                previous = st.number_input(f'Previous Reading - {fm}', key=f'{equipment_type}_{fm}_previous')
                readings['previous'].append(previous)

        if st.button(f'Calculate {equipment_type} Consumption'):
            consumption = calculate_consumption(readings, config['formula'])
            st.success(f'{equipment_type} Consumption: {consumption:.2f} units')

# Create consumption calculation sections for each equipment type
create_consumption_inputs('ME', tab1)
create_consumption_inputs('AE', tab2)
create_consumption_inputs('BLR', tab3)
create_consumption_inputs('OTHER', tab4)
