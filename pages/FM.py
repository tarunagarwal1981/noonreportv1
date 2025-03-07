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

    if 'tank_config' not in st.session_state:
        st.session_state.tank_config = {
            'ME': {'tank1': False, 'tank2': False, 'tank3': False},
            'AE1': {'tank1': False, 'tank2': False, 'tank3': False},
            'AE2': {'tank1': False, 'tank2': False, 'tank3': False},
            'AE3': {'tank1': False, 'tank2': False, 'tank3': False},
            'BOILER1': {'tank1': False, 'tank2': False, 'tank3': False},
            'BOILER2': {'tank1': False, 'tank2': False, 'tank3': False},
            'OTHERS': {'tank1': False, 'tank2': False, 'tank3': False}
        }

init_session_state()

# Main title
st.title('🚢 Vessel Consumption Calculator')

# Create tabs for Admin and User sections
admin_tab, user_tab = st.tabs(["⚙️ Admin Configuration", "📊 User Calculations"])

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
        else:
            st.info('No flowmeters added yet. Add a flowmeter using the form above.')

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
                    help='Example: (F1_TODAY - F1_PREV) - (F2_TODAY - F2_PREV)'
                )

            if st.button('Save Equipment Configuration'):
                st.session_state.configurations[equipment_type]['flowmeters'] = selected_flowmeters
                if formula_type == 'Custom Formula':
                    st.session_state.configurations[equipment_type]['formula'] = custom_formula
                else:
                    st.session_state.configurations[equipment_type]['formula'] = formula_type
                st.success(f'Configuration saved for {equipment_type}')
                st.rerun()
        else:
            st.warning('Please add flowmeters first before configuring equipment.')

    # Tank Configuration Section
    st.markdown("---")
    st.header('🛢️ Tank Configuration')

    # Tank Assignment Matrix
    st.subheader('Tank Assignment Matrix')
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        st.markdown("**Equipment**")
    with col2:
        st.markdown("**Tank 1**")
    with col3:
        st.markdown("**Tank 2**")
    with col4:
        st.markdown("**Tank 3**")

    for equipment in st.session_state.tank_config.keys():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

        with col1:
            st.markdown(f"**{equipment}**")
        with col2:
            tank1 = st.checkbox('', key=f'{equipment}_tank1',
                              value=st.session_state.tank_config[equipment]['tank1'])
            st.session_state.tank_config[equipment]['tank1'] = tank1
        with col3:
            tank2 = st.checkbox('', key=f'{equipment}_tank2',
                              value=st.session_state.tank_config[equipment]['tank2'])
            st.session_state.tank_config[equipment]['tank2'] = tank2
        with col4:
            tank3 = st.checkbox('', key=f'{equipment}_tank3',
                              value=st.session_state.tank_config[equipment]['tank3'])
            st.session_state.tank_config[equipment]['tank3'] = tank3

with user_tab:
    st.header('Consumption Calculations')

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

    # Equipment tabs for calculations
    equipment_tabs = st.tabs(['ME', 'AE', 'BLR', 'OTHER'])

    for eq_type, tab in zip(['ME', 'AE', 'BLR', 'OTHER'], equipment_tabs):
        with tab:
            st.subheader(f'{eq_type} Consumption')
            config = st.session_state.configurations[eq_type]

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

                    if fm_details['type'] == 'Volumetric':
                        st.info(f"Mass calculation will be applied")

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
                    st.success(f'{eq_type} Consumption: {result:.2f} units')

                    # Show connected tanks
                    connected_tanks = []
                    for tank_num, connected in st.session_state.tank_config[eq_type].items():
                        if connected:
                            connected_tanks.append(f"Tank {tank_num[-1]}")
                    if connected_tanks:
                        st.info(f"Connected tanks: {', '.join(connected_tanks)}")

# Add save/load functionality
if admin_tab:
    st.sidebar.header("💾 Save/Load Configuration")

    # Save configuration
    if st.sidebar.button("Save Configuration"):
        config_data = {
            'flowmeters': st.session_state.flowmeters,
            'configurations': st.session_state.configurations,
            'tank_config': st.session_state.tank_config
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
            st.session_state.tank_config = config_data['tank_config']
            st.sidebar.success("Configuration loaded successfully!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error loading configuration: {str(e)}")
