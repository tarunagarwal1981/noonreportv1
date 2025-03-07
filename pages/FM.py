import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state variables
def init_session_state():
    if 'flowmeters' not in st.session_state:
        st.session_state.flowmeters = {}

    if 'configurations' not in st.session_state:
        st.session_state.configurations = {
            'ME': {'flowmeters': [], 'formula': ''},
            'AE': {'flowmeters': [], 'formula': ''},
            'BLR': {'flowmeters': [], 'formula': ''},
            'OTHER': {'flowmeters': [], 'formula': ''}
        }

    if 'readings' not in st.session_state:
        st.session_state.readings = {}

# Call initialization function
init_session_state()

# App title
st.title('Vessel Flowmeter Configuration and Calculation')

# Configuration Section
st.header('System Configuration')

# Flowmeter Management
with st.expander("Flowmeter Management", expanded=True):
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        new_flowmeter = st.text_input('Enter new flowmeter name')
    with col2:
        flowmeter_type = st.selectbox(
            'Flowmeter Type',
            ['Volumetric', 'Mass'],
            key='new_flowmeter_type'
        )
    with col3:
        if st.button('Add Flowmeter'):
            if new_flowmeter and new_flowmeter not in st.session_state.flowmeters:
                st.session_state.flowmeters[new_flowmeter] = {
                    'type': flowmeter_type,
                    'current_reading': 0.0,
                    'previous_reading': 0.0,
                    'density': 0.0,
                    'temperature': 0.0
                }
                st.success(f'Flowmeter {new_flowmeter} added successfully!')
                st.rerun()  # Rerun the app to update the state

    # Display existing flowmeters
    if st.session_state.flowmeters:
        st.subheader('Existing Flowmeters')
        fm_data = []
        for name, details in st.session_state.flowmeters.items():
            fm_data.append({
                'Flowmeter Name': name,
                'Type': details['type']
            })
        if fm_data:
            fm_df = pd.DataFrame(fm_data)
            st.dataframe(fm_df)
    else:
        st.info('No flowmeters added yet. Add a flowmeter using the form above.')

# Equipment Configuration
with st.expander("Equipment Configuration", expanded=True):
    equipment_type = st.selectbox('Select Equipment Type', ['ME', 'AE', 'BLR', 'OTHER'])

    if len(st.session_state.flowmeters) > 0:
        selected_flowmeters = st.multiselect(
            'Select Flowmeters',
            options=list(st.session_state.flowmeters.keys()),
            default=st.session_state.configurations[equipment_type]['flowmeters']
        )

        formula_type = st.selectbox(
            'Select Formula Type',
            ['Simple Difference', 'Multiple Flowmeter Difference', 'Custom Formula'],
            key=f'{equipment_type}_formula'
        )

        if formula_type == 'Custom Formula':
            st.write("Available variables for formula:")
            st.write("- Use F1_TODAY, F1_PREV for first flowmeter's readings")
            st.write("- Use F2_TODAY, F2_PREV for second flowmeter's readings, etc.")
            custom_formula = st.text_input(
                'Enter Custom Formula',
                help='Example: (F1_TODAY - F1_PREV) - (F2_TODAY - F2_PREV)'
            )

        if st.button('Save Configuration'):
            st.session_state.configurations[equipment_type]['flowmeters'] = selected_flowmeters
            if formula_type == 'Custom Formula':
                st.session_state.configurations[equipment_type]['formula'] = custom_formula
            else:
                st.session_state.configurations[equipment_type]['formula'] = formula_type
            st.success(f'Configuration saved for {equipment_type}')
            st.rerun()
    else:
        st.warning('Please add flowmeters first before configuring equipment.')

# Calculation Section
st.header('Consumption Calculations')

def calculate_consumption(readings, formula_type):
    try:
        if formula_type == 'Simple Difference':
            return float(readings['current'][0]) - float(readings['previous'][0])
        elif formula_type == 'Multiple Flowmeter Difference':
            total = 0
            for curr, prev in zip(readings['current'], readings['previous']):
                total += float(curr) - float(prev)
            return total
        elif isinstance(formula_type, str) and 'F' in formula_type:  # Custom formula
            # Create variables dictionary
            variables = {}
            for i, (curr, prev) in enumerate(zip(readings['current'], readings['previous']), 1):
                variables[f'F{i}_TODAY'] = float(curr)
                variables[f'F{i}_PREV'] = float(prev)

            # Replace variables in formula
            formula = formula_type
            for var_name, value in variables.items():
                formula = formula.replace(var_name, str(value))

            return eval(formula)
    except Exception as e:
        st.error(f"Calculation error: {str(e)}")
        return None

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
            fm_details = st.session_state.flowmeters[fm]

            st.write(f"### {fm}")
            col1, col2 = st.columns(2)

            with col1:
                current = st.number_input(
                    'Current Reading',
                    value=0.0,
                    key=f'{equipment_type}_{fm}_current'
                )
                readings['current'].append(current)

                if fm_details['type'] == 'Volumetric':
                    density = st.number_input(
                        'Density (kg/m³)',
                        value=0.0,
                        key=f'{equipment_type}_{fm}_density'
                    )
                    temperature = st.number_input(
                        'Temperature (°C)',
                        value=15.0,
                        key=f'{equipment_type}_{fm}_temp'
                    )

            with col2:
                previous = st.number_input(
                    'Previous Reading',
                    value=0.0,
                    key=f'{equipment_type}_{fm}_previous'
                )
                readings['previous'].append(previous)

        if st.button(f'Calculate {equipment_type} Consumption'):
            result = calculate_consumption(readings, config['formula'])
            if result is not None:
                st.success(f'{equipment_type} Consumption: {result:.2f} units')

# Create consumption calculation sections
create_consumption_inputs('ME', tab1)
create_consumption_inputs('AE', tab2)
create_consumption_inputs('BLR', tab3)
create_consumption_inputs('OTHER', tab4)
