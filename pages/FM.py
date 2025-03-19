import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Vessel Consumption Calculator",
    page_icon="🚢",
    layout="wide"
)

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

    if 'tank_levels' not in st.session_state:
        st.session_state.tank_levels = {
            'ME': {'HFO': 0.0, 'LFO': 0.0, 'MGO': 0.0},
            'AE1': {'HFO': 0.0, 'LFO': 0.0, 'MGO': 0.0},
            'AE2': {'HFO': 0.0, 'LFO': 0.0, 'MGO': 0.0},
            'AE3': {'HFO': 0.0, 'LFO': 0.0, 'MGO': 0.0},
            'BOILER1': {'HFO': 0.0, 'LFO': 0.0, 'MGO': 0.0},
            'BOILER2': {'HFO': 0.0, 'LFO': 0.0, 'MGO': 0.0},
            'OTHERS': {'HFO': 0.0, 'LFO': 0.0, 'MGO': 0.0}
        }

init_session_state()

# Main title
st.title('🚢 Vessel Consumption Calculator')

# Create tabs for Admin and User sections
admin_tab, user_tab = st.tabs(["⚙️ Admin Configuration", "📊 Daily Operations"])

with admin_tab:
    st.header('System Configuration')

    # Flowmeter Management Section
    with st.expander("📝 Flowmeter Management", expanded=True):
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
                    st.rerun()

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
                st.dataframe(fm_df, use_container_width=True)

    # Equipment Configuration Section
    with st.expander("⚡ Equipment Configuration", expanded=True):
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
                st.info("Available variables: F1_TODAY, F1_PREV, F2_TODAY, F2_PREV, etc.")
                custom_formula = st.text_input(
                    'Enter Custom Formula',
                    value=st.session_state.configurations[equipment_type].get('formula', ''),
                    help='Example: (F1_TODAY - F1_PREV) - (F2_TODAY - F2_PREV)'
                )

            if st.button('Save Equipment Configuration'):
                st.session_state.configurations[equipment_type]['flowmeters'] = selected_flowmeters
                if formula_type == 'Custom Formula':
                    st.session_state.configurations[equipment_type]['formula'] = custom_formula
                else:
                    st.session_state.configurations[equipment_type]['formula'] = formula_type
                st.success(f'Configuration saved for {equipment_type}')

with user_tab:
    st.header('Daily Consumption Recording')

    def convert_to_mass(volume, density, temperature):
        temperature_factor = 1 - (0.00065 * (temperature - 15))
        return volume * density * temperature_factor

    def calculate_consumption(readings, formula_type):
        try:
            if formula_type == 'Simple Difference':
                return float(readings['current'][0]) - float(readings['previous'][0])
            elif formula_type == 'Multiple Flowmeter Difference':
                total = 0
                for curr, prev in zip(readings['current'], readings['previous']):
                    total += float(curr) - float(prev)
                return total
            elif isinstance(formula_type, str) and 'F' in formula_type:
                variables = {}
                for i, (curr, prev) in enumerate(zip(readings['current'], readings['previous']), 1):
                    variables[f'F{i}_TODAY'] = float(curr)
                    variables[f'F{i}_PREV'] = float(prev)
                formula = formula_type
                for var_name, value in variables.items():
                    formula = formula.replace(var_name, str(value))
                return eval(formula)
        except Exception as e:
            st.error(f"Calculation error: {str(e)}")
            return None

    # Flowmeter Readings Section
    st.subheader('📊 Flowmeter Readings')

    # Equipment tabs for calculations
    equipment_tabs = st.tabs(['ME', 'AE', 'BLR', 'OTHER'])

    calculation_results = {}  # Store calculation results for display

    for eq_type, tab in zip(['ME', 'AE', 'BLR', 'OTHER'], equipment_tabs):
        with tab:
            config = st.session_state.configurations[eq_type]

            # Add datetime and fuel type fields
            col1, col2 = st.columns(2)
            with col1:
                reading_date = st.date_input(
                    "Date",
                    value=datetime.now().date(),
                    key=f'{eq_type}_date'
                )
                reading_time = st.time_input(
                    "Time",
                    value=datetime.now().time(),
                    key=f'{eq_type}_time'
                )
            with col2:
                fuel_type = st.selectbox(
                    "Fuel Type",
                    options=['HFO', 'LFO', 'MGO'],
                    key=f'{eq_type}_fuel_type'
                )

            st.markdown("---")  # Add a separator between datetime/fuel type and flowmeter readings

            if not config['flowmeters']:
                st.warning(f'No flowmeters configured for {eq_type}. Please configure in Admin section.')
                continue

            readings = {'current': [], 'previous': []}

            for fm in config['flowmeters']:
                fm_details = st.session_state.flowmeters[fm]

                st.markdown(f"#### {fm}")
                col1, col2 = st.columns(2)

                with col1:
                    current = st.number_input(
                        'Current Reading',
                        value=0.0,
                        key=f'{eq_type}_{fm}_current'
                    )
                    readings['current'].append(current)

                    if fm_details['type'] == 'Volumetric':
                        density = st.number_input(
                            'Density (kg/m³)',
                            value=0.0,
                            key=f'{eq_type}_{fm}_density'
                        )
                        temperature = st.number_input(
                            'Temperature (°C)',
                            value=15.0,
                            key=f'{eq_type}_{fm}_temp'
                        )

                with col2:
                    previous = st.number_input(
                        'Previous Reading',
                        value=0.0,
                        key=f'{eq_type}_{fm}_previous'
                    )
                    readings['previous'].append(previous)

            if st.button(f'Calculate {eq_type} Consumption'):
                # Apply mass conversion if needed
                for i, fm in enumerate(config['flowmeters']):
                    if st.session_state.flowmeters[fm]['type'] == 'Volumetric':
                        density = st.session_state[f'{eq_type}_{fm}_density']
                        temperature = st.session_state[f'{eq_type}_{fm}_temp']
                        readings['current'][i] = convert_to_mass(readings['current'][i], density, temperature)
                        readings['previous'][i] = convert_to_mass(readings['previous'][i], density, temperature)

                result = calculate_consumption(readings, config['formula'])
                if result is not None:
                    calculation_results[eq_type] = result
                    st.success(f'{eq_type} Consumption: {result:.2f} units')

    # Tank Levels Section
    st.markdown("---")
    st.subheader('🛢️ Tank Levels')

    # Create columns for the table header
    cols = st.columns([2, 1, 1, 1])
    cols[0].markdown("**Equipment**")
    cols[1].markdown("**HFO**")
    cols[2].markdown("**LFO**")
    cols[3].markdown("**MGO**")

    # Create input fields for each equipment's tank levels
    for equipment in ['ME', 'AE1', 'AE2', 'AE3', 'BOILER1', 'BOILER2', 'OTHERS']:
        cols = st.columns([2, 1, 1, 1])
        cols[0].markdown(f"**{equipment}**")

        # Ensure the tank_levels dictionary has the correct structure
        if equipment not in st.session_state.tank_levels:
            st.session_state.tank_levels[equipment] = {'HFO': 0.0, 'LFO': 0.0, 'MGO': 0.0}

        # Tank level inputs
        for tank_type in ['HFO', 'LFO', 'MGO']:
            tank_level = cols[['HFO', 'LFO', 'MGO'].index(tank_type) + 1].number_input(
                f"Level",
                value=st.session_state.tank_levels[equipment].get(tank_type, 0.0),
                key=f'{equipment}_{tank_type}_level',
                label_visibility="collapsed"
            )
            st.session_state.tank_levels[equipment][tank_type] = tank_level

    # Save button for tank levels
    if st.button('Save Tank Levels'):
        st.success('Tank levels saved successfully!')

# Add save/load functionality in sidebar
st.sidebar.header("💾 Save/Load Configuration")

# Save configuration
if st.sidebar.button("Save Configuration"):
    config_data = {
        'flowmeters': st.session_state.flowmeters,
        'configurations': st.session_state.configurations,
        'tank_levels': st.session_state.tank_levels
    }
    json_str = json.dumps(config_data)
    st.sidebar.download_button(
        label="Download Configuration",
        data=json_str,
        file_name="vessel_config.json",
        mime="application/json"
    )

# Load configuration
uploaded_file = st.sidebar.file_uploader("Load Configuration", type=['json'])
if uploaded_file is not None:
    try:
        config_data = json.loads(uploaded_file.getvalue())
        st.session_state.flowmeters = config_data['flowmeters']
        st.session_state.configurations = config_data['configurations']
        st.session_state.tank_levels = config_data['tank_levels']
        st.sidebar.success("Configuration loaded successfully!")
        st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error loading configuration: {str(e)}")
