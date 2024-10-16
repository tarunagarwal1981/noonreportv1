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

def initialize_session_state():
    if 'consumers' not in st.session_state:
        st.session_state.consumers = [
            'Main Engine', 'Aux Engine1', 'Aux Engine2', 'Aux Engine3',
            'Boiler 1', '    Boiler 1 - Cargo Heating', '    Boiler 1 - Discharge',
            'Boiler 2', '    Boiler 2 - Cargo Heating', '    Boiler 2 - Discharge',
            'IGG', 'Incinerator', 'DPP1', 'DPP2', 'DPP3'
        ]
    if 'fuel_types' not in st.session_state:
        st.session_state.fuel_types = ['VLSFO', 'MGO', 'HFO']
    if 'tanks' not in st.session_state:
        st.session_state.tanks = [f'Tank {i}' for i in range(1, 9)]
    if 'viscosity' not in st.session_state:
        st.session_state.viscosity = {tank: np.random.uniform(20, 100) for tank in st.session_state.tanks}
    if 'sulfur' not in st.session_state:
        st.session_state.sulfur = {tank: np.random.uniform(0.05, 0.49) for tank in st.session_state.tanks}

def edit_tank_properties():
    st.write("Edit tank properties:")
    
    tank_props = pd.DataFrame({
        'Fuel Grade': [random.choice(st.session_state.fuel_types) for _ in st.session_state.tanks],
        'Viscosity': [st.session_state.viscosity[tank] for tank in st.session_state.tanks],
        'Sulfur (%)': [st.session_state.sulfur[tank] for tank in st.session_state.tanks],
        'Current ROB': [np.random.uniform(50, 500) for _ in st.session_state.tanks]
    }, index=st.session_state.tanks)

    col1, col2, col3 = st.columns(3)
    with col1:
        bunkering_happened = st.checkbox("Bunkering Happened", key="bunkering_checkbox")
    with col2:
        debunkering_happened = st.checkbox("Debunkering Happened", key="debunkering_checkbox")
    with col3:
        bunker_survey = st.checkbox("Bunker Survey", key="bunker_survey_checkbox")

    tank_transfer = st.checkbox("Enable Tank-to-Tank Transfer")

    if bunkering_happened:
        tank_props['Bunkered Qty (mT)'] = [0.0] * len(st.session_state.tanks)
    if debunkering_happened:
        tank_props['Debunkered Qty (mT)'] = [0.0] * len(st.session_state.tanks)
    if bunker_survey:
        tank_props['Correction Qty (mT)'] = [0.0] * len(st.session_state.tanks)
    if tank_transfer:
        tank_props['Qty (mT) Transferred From Tank'] = [0.0] * len(st.session_state.tanks)
        tank_props['Qty (mT) Transferred To Tank'] = [0.0] * len(st.session_state.tanks)

    column_config = {
        'Fuel Grade': st.column_config.SelectboxColumn(
            'Fuel Grade',
            options=st.session_state.fuel_types,
            required=True
        ),
        'Viscosity': st.column_config.NumberColumn(
            'Viscosity', min_value=20.0, max_value=100.0, step=0.1, format="%.1f"
        ),
        'Sulfur (%)': st.column_config.NumberColumn(
            'Sulfur (%)', min_value=0.05, max_value=0.49, step=0.01, format="%.2f"
        ),
        'Current ROB': st.column_config.NumberColumn(
            'Current ROB', min_value=0.0, step=0.1, format="%.1f"
        )
    }

    if bunkering_happened:
        column_config['Bunkered Qty (mT)'] = st.column_config.NumberColumn(
            'Bunkered Qty (mT)', min_value=0.0, step=0.1, format="%.1f"
        )
    if debunkering_happened:
        column_config['Debunkered Qty (mT)'] = st.column_config.NumberColumn(
            'Debunkered Qty (mT)', min_value=0.0, step=0.1, format="%.1f"
        )
    if bunker_survey:
        column_config['Correction Qty (mT)'] = st.column_config.NumberColumn(
            'Correction Qty (mT)', min_value=-100.0, max_value=100.0, step=0.1, format="%.1f"
        )
    if tank_transfer:
        column_config.update({
            'Qty (mT) Transferred From Tank': st.column_config.NumberColumn(
                'Transferred From', min_value=0.0, step=0.1, format="%.1f"
            ),
            'Qty (mT) Transferred To Tank': st.column_config.NumberColumn(
                'Transferred To', min_value=0.0, step=0.1, format="%.1f"
            )
        })

    edited_props = st.data_editor(
        tank_props,
        use_container_width=True,
        column_config=column_config,
        key=f"edit_tank_properties_editor_{uuid.uuid4()}"
    )
    
    for tank in st.session_state.tanks:
        st.session_state.viscosity[tank] = edited_props.loc[tank, 'Viscosity']
        st.session_state.sulfur[tank] = edited_props.loc[tank, 'Sulfur (%)']

    if tank_transfer:
        transfers_from = edited_props['Qty (mT) Transferred From Tank']
        transfers_to = edited_props['Qty (mT) Transferred To Tank']
        if transfers_from.sum() != transfers_to.sum():
            st.warning("The total quantity transferred from tanks must equal the total quantity transferred to tanks.")
        else:
            st.success(f"Total quantity transferred: {transfers_from.sum()} mT")

    return edited_props, bunkering_happened, debunkering_happened, bunker_survey

def display_fuel_consumption_report(edited_props, bunkering_happened, debunkering_happened, bunker_survey):
    st.subheader("Fuel Consumption Data")

    fuel_consumption = edited_props.groupby('Fuel Grade').agg({
        'Current ROB': 'sum',
        'Bunkered Qty (mT)': 'sum' if 'Bunkered Qty (mT)' in edited_props.columns else (lambda x: 0),
        'Debunkered Qty (mT)': 'sum' if 'Debunkered Qty (mT)' in edited_props.columns else (lambda x: 0),
        'Correction Qty (mT)': 'sum' if 'Correction Qty (mT)' in edited_props.columns else (lambda x: 0)
    }).reset_index()

    fuel_consumption['Previous ROB'] = (
        fuel_consumption['Current ROB'] - 
        fuel_consumption['Bunkered Qty (mT)'] + 
        fuel_consumption['Debunkered Qty (mT)'] - 
        fuel_consumption['Correction Qty (mT)']
    )

    columns = ['Fuel Grade', 'Previous ROB']
    if bunkering_happened:
        columns.append('Bunkered Qty (mT)')
    if debunkering_happened:
        columns.append('Debunkered Qty (mT)')
    if bunker_survey:
        columns.append('Correction Qty (mT)')
    columns.append('Current ROB')

    fuel_consumption = fuel_consumption[columns]
    st.dataframe(fuel_consumption, use_container_width=True)

def display_bdn_consumption_report(edited_props, bunkering_happened, debunkering_happened, bunker_survey):
    st.subheader("BDN Based Fuel Consumption Data")
    
    bdn_numbers = generate_random_bdn_numbers()
    edited_props['BDN Number'] = [bdn_numbers[i % 3] for i in range(len(edited_props))]
    
    columns = ['BDN Number', 'Fuel Grade', 'Previous ROB', 'Current ROB']
    if bunkering_happened:
        columns.insert(-1, 'Bunkered Qty (mT)')
    if debunkering_happened:
        columns.insert(-1, 'Debunkered Qty (mT)')
    if bunker_survey:
        columns.insert(-1, 'Correction Qty (mT)')
    
    bdn_consumption = edited_props[columns]
    st.dataframe(bdn_consumption, use_container_width=True)

def display_flowmeter_method_report(edited_props, bunkering_happened, debunkering_happened, bunker_survey):
    st.subheader("Flowmeter Method Fuel Consumption Data")
    
    flowmeter_data = pd.DataFrame({
        "Flowmeter In": np.random.uniform(10, 50, len(st.session_state.consumers)),
        "Flowmeter Out": np.random.uniform(10, 50, len(st.session_state.consumers)),
        "Temp at flowmeter": np.random.uniform(20, 80, len(st.session_state.consumers)),
        "Density @ 15°C": np.random.uniform(0.8, 1.0, len(st.session_state.consumers)),
        "Fuel Type": [random.choice(st.session_state.fuel_types) for _ in st.session_state.consumers],
        "Total Consumption (mT)": np.random.uniform(1, 10, len(st.session_state.consumers))
    }, index=st.session_state.consumers)
    
    st.dataframe(flowmeter_data, use_container_width=True)

def display_tank_sounding_report(edited_props, bunkering_happened, debunkering_happened, bunker_survey):
    st.subheader("Tank Sounding Method Fuel Consumption Data")
    st.dataframe(edited_props, use_container_width=True)

def display_ctms_method_report(edited_props, bunkering_happened, debunkering_happened, bunker_survey):
    st.subheader("CTMS Method Fuel Consumption Data")
    
    ctms_data = pd.DataFrame({
        'Value': [
            np.random.uniform(1000, 5000),
            np.random.uniform(500, 2000),
            np.random.uniform(500, 2000),
            np.random.uniform(0.4, 0.5),
            np.random.uniform(-5, 5),
            np.random.uniform(50, 200)
        ]
    }, index=['CTMS qty (m3)', 'Cargo loaded (m3)', 'Cargo discharged (m3)', 'Density', 'N2 correction', 'Total LNG consumption (mT)'])
    
    st.dataframe(ctms_data, use_container_width=True)

def display_additional_table(fuel_type_view):
    st.subheader("Additional Consumption Data")
    
    last_column_name = "Fuel Type" if fuel_type_view else "Fuel BDN No."
    
    additional_data = pd.DataFrame({
        'Work': [0, 0, 0, 0],
        'SFOC': [0, 0, 0, ''],
        last_column_name: ['', '', '', '']
    }, index=['Reefer container', 'Cargo cooling', 'Heating/Discharge pump', 'Shore-Side Electricity'])
    
    column_config = {
        "Work": st.column_config.NumberColumn(
            "Work",
            help="Work done in kWh",
            min_value=0,
            format="%d kWh"
        ),
        "SFOC": st.column_config.NumberColumn(
            "SFOC",
            help="Specific Fuel Oil Consumption",
            min_value=0,
            format="%.2f"
        )
    }
    
    if fuel_type_view:
        column_config[last_column_name] = st.column_config.SelectboxColumn(
            "Fuel Type",
            help="Select the fuel type",
            options=st.session_state.fuel_types
        )
    else:
        column_config[last_column_name] = st.column_config.TextColumn(
            "Fuel BDN No.",
            help="Enter the Fuel BDN Number",
            max_chars=50
        )
    
    st.data_editor(
        additional_data,
        use_container_width=True,
        num_rows="dynamic",
        column_config=column_config,
        key=f"additional_consumption_editor_{uuid.uuid4()}"
    )

def main():
    initialize_session_state()

    st.title("Fuel Consumption and BDN Report")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        fuel_type_view = st.checkbox("Fuel Type based", value=True)
    with col2:
        bdn_view = st.checkbox("BDN based", value=False)
    with col3:
        flowmeter_method = st.checkbox("Flowmeter Method", value=False)
    with col4:
        tank_sounding_method = st.checkbox("Tank Sounding Method", value=False)
    with col5:
        ctms_method = st.checkbox("CTMS Method", value=False)

    if sum([fuel_type_view, bdn_view, flowmeter_method, tank_sounding_method, ctms_method]) > 1:
        st.warning("Please select only one view type.")
        st.stop()
    elif not any([fuel_type_view, bdn_view, flowmeter_method, tank_sounding_method, ctms_method]):
        st.warning("Please select a view type.")
        st.stop()

    edited_props, bunkering_happened, debunkering_happened, bunker_survey = edit_tank_properties()

    if fuel_type_view:
        display_fuel_consumption_report(edited_props, bunkering_happened, debunkering_happened, bunker_survey)
    elif bdn_view:
        display_bdn_consumption_report(edited_props, bunkering_happened, debunkering_happened, bunker_survey)
    elif flowmeter_method:
        display_flowmeter_method_report(edited_props, bunkering_happened, debunkering_happened, bunker_survey)
    elif tank_sounding_method:
        display_tank_sounding_report(edited_props, bunkering_happened, debunkering_happened, bunker_survey)
    elif ctms_method:
        display_ctms_method_report(edited_props, bunkering_happened, debunkering_happened, bunker_survey)

    display_additional_table(fuel_type_view)

    if st.button("Submit Report", type="primary"):
        st.success("Report submitted successfully!")

if __name__ == "__main__":
    main()
