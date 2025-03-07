import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state with proper dictionary structure
if 'flowmeters' not in st.session_state:
    st.session_state.flowmeters = dict()  # Initialize as empty dictionary

if 'configurations' not in st.session_state:
    st.session_state.configurations = {
        'ME': {'flowmeters': [], 'formula': ''},
        'AE': {'flowmeters': [], 'formula': ''},
        'BLR': {'flowmeters': [], 'formula': ''},
        'OTHER': {'flowmeters': [], 'formula': ''}
    }

if 'readings' not in st.session_state:
    st.session_state.readings = dict()

def convert_to_mass(volume, density, temperature):
    temperature_factor = 1 - (0.00065 * (temperature - 15))
    mass = volume * density * temperature_factor
    return mass

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

    # Display existing flowmeters in a table
    if st.session_state.flowmeters:
        st.subheader('Existing Flowmeters')
        fm_data = []
        for fm_name, fm_details in st.session_state.flowmeters.items():
            fm_data.append({
                'Flowmeter Name': fm_name,
                'Type': fm_details['type']
            })
        fm_df = pd.DataFrame(fm_data)
        st.dataframe(fm_df)

# Equipment Configuration
with st.expander("Equipment Configuration", expanded=True):
    equipment_type = st.selectbox('Select Equipment Type', ['ME', 'AE', 'BLR', 'OTHER'])

    st.subheader(f'{equipment_type} Configuration')

    # Select flowmeters for the equipment
    selected_flowmeters = st.multiselect(
        'Select Flowmeters',
        list(st.session_state.flowmeters.keys()),
        default=st.session_state.configurations[equipment_type]['flowmeters']
    )

    # Formula configuration
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

def evaluate_custom_formula(formula, readings):
    variables = {}
    for i, fm in enumerate(readings['flowmeters'], 1):
        variables[f'F{i}_TODAY'] = readings['current'][i-1]
        variables[f'F{i}_PREV'] = readings['previous'][i-1]

    for var_name, value in variables.items():
        formula = formula.replace(var_name, str(value))

    try:
        return eval(formula)
    except Exception as e:
        st.error(f"Error evaluating formula: {str(e)}")
        return None

def calculate_consumption(readings, formula_type):
    if formula_type == 'Simple Difference':
        return float(readings['current'][0]) - float(readings['previous'][0])
    elif formula_type == 'Multiple Flowmeter Difference':
        total = 0
        for i in range(len(readings['current'])):
            total += float(readings['current'][i]) - float(readings['previous'][i])
        return total
    else:
        return evaluate_custom_formula(formula_type, readings)

# Create tabs for different consumption types
tab1, tab2, tab3, tab4 = st.tabs(['ME Consumption', 'AE Consumption', 'BLR Consumption', 'Other Equipment'])

def create_consumption_inputs(equipment_type, tab):
    with tab:
        st.subheader(f'{equipment_type} Consumption')
        config = st.session_state.configurations[equipment_type]

        if not config['flowmeters']:
            st.warning(f'No flowmeters configured for {equipment_type}. Please configure in the Equipment Configuration section.')
            return

        readings = {'current': [], 'previous': [], 'flowmeters': config['flowmeters']}
        mass_flows = []

        for fm in config['flowmeters']:
            st.write(f"### Flowmeter: {fm}")
            fm_details = st.session_state.flowmeters[fm]

            col1, col2 = st.columns(2)
            with col1:
                current = st.number_input(
                    f'Current Reading',
                    key=f'{equipment_type}_{fm}_current'
                )
                readings['current'].append(current)

                if fm_details['type'] == 'Volumetric':
                    density = st.number_input(
                        f'Density (kg/m³)',
                        value=fm_details['density'],
                        key=f'{equipment_type}_{fm}_density'
                    )
                    temperature = st.number_input(
                        f'Temperature (°C)',
                        value=fm_details['temperature'],
                        key=f'{equipment_type}_{fm}_temp'
                    )

            with col2:
                previous = st.number_input(
                    f'Previous Reading',
                    key=f'{equipment_type}_{fm}_previous'
                )
                readings['previous'].append(previous)

            if fm_details['type'] == 'Volumetric':
                current_mass = convert_to_mass(current, density, temperature)
                previous_mass = convert_to_mass(previous, density, temperature)
                mass_flows.append((current_mass, previous_mass))
                st.info(f"Mass flow calculation for {fm}:")
                st.write(f"Current: {current_mass:.2f} kg")
                st.write(f"Previous: {previous_mass:.2f} kg")

        if st.button(f'Calculate {equipment_type} Consumption'):
            if mass_flows:
                for i, (curr_mass, prev_mass) in enumerate(mass_flows):
                    readings['current'][i] = curr_mass
                    readings['previous'][i] = prev_mass

            consumption = calculate_consumption(readings, config['formula'])
            if consumption is not None:
                st.success(f'{equipment_type} Consumption: {consumption:.2f} units')

# Create consumption calculation sections for each equipment type
create_consumption_inputs('ME', tab1)
create_consumption_inputs('AE', tab2)
create_consumption_inputs('BLR', tab3)
create_consumption_inputs('OTHER', tab4)
