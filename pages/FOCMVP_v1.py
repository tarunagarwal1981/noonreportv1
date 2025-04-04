import streamlit as st
import pandas as pd
import numpy as np
import random
import string
import uuid

st.set_page_config(layout="wide", page_title="Fuel Consumption Report")

def generate_random_bdn_numbers():
    """Generates three unique random alphanumeric BDN numbers (8 characters)."""
    return [''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) for _ in range(3)]

def initialize_session_state():
    if 'consumers' not in st.session_state:
        st.session_state.consumers = [
            'Main Engine', 'Aux Engine1', 'Aux Engine2', 'Aux Engine3',
            'Boiler 1', '    Boiler 1 - Cargo Heating', '    Boiler 1 - Discharge',
            'Boiler 2', '    Boiler 2 - Cargo Heating', '    Boiler 2 - Discharge',
            'IGG', 'Incinerator', 'DPP1', 'DPP2', 'DPP3'
        ]

    if 'fuel_types' not in st.session_state:
        st.session_state.fuel_types = ['HSFO', 'LSFO', 'ULSFO', 'LSMGO', 'LNG']

    if 'viscosity' not in st.session_state:
        st.session_state.viscosity = {fuel: np.random.uniform(20, 100) for fuel in st.session_state.fuel_types}

    if 'sulfur' not in st.session_state:
        st.session_state.sulfur = {fuel: np.random.uniform(0.05, 0.49) for fuel in st.session_state.fuel_types}

def display_tank_sounding_report():
    def create_editable_dataframe():
        # Define the row indices, including 'Fuel Type' as the first row
        index = ['Fuel Type', 'BDN Number', 'Previous ROB'] + st.session_state.consumers + ['Current ROB']

        # Create DataFrame with generic column names
        num_columns = 5  # For HSFO, LSFO, ULSFO, LSMGO, LNG
        df = pd.DataFrame(index=index, columns=[f'Column {i+1}' for i in range(num_columns)])

        # Set fuel types in the first row
        df.loc['Fuel Type'] = ['HSFO', 'LSFO', 'ULSFO', 'LSMGO', 'LNG']

        # Generate BDN numbers
        bdn_numbers = generate_random_bdn_numbers()
        df.loc['BDN Number'] = [bdn_numbers[i % 3] for i in range(num_columns)]

        # Generate random Previous ROB values
        df.loc['Previous ROB'] = [np.random.uniform(100, 1000) for _ in range(num_columns)]

        # Initialize consumption values
        for consumer in st.session_state.consumers:
            df.loc[consumer] = [np.random.uniform(0, 50) for _ in range(num_columns)]

        # Calculate Current ROB
        consumption = pd.DataFrame(df.loc[st.session_state.consumers], dtype=float).sum()
        df.loc['Current ROB'] = pd.to_numeric(df.loc['Previous ROB']) - consumption

        return df

    df = create_editable_dataframe()

    st.subheader("Tank Sounding Method Fuel Consumption Data")

    # Configure column properties
    column_config = {
        col: st.column_config.NumberColumn(
            col,
            help=f"Values for {col}",
            min_value=0.0,
            format="%.3f"
        ) for col in df.columns
    }

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        column_config=column_config,
        key=f"tank_sounding_editor_{uuid.uuid4()}"
    )

    st.session_state.consumption_data_tank_sounding = edited_df.loc[st.session_state.consumers]
    st.session_state.previous_rob_tank_sounding = edited_df.loc['Previous ROB']
def display_additional_table():
    st.subheader("Additional Consumption Data")

    additional_data = pd.DataFrame({
        'Work': [0, 0, 0, 0],
        'SFOC': [0, 0, 0, ''],
        'Fuel Type': ['', '', '', '']
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
        ),
        "Fuel Type": st.column_config.SelectboxColumn(
            "Fuel Type",
            help="Select the fuel type",
            options=st.session_state.fuel_types
        )
    }

    edited_additional_data = st.data_editor(
        additional_data,
        use_container_width=True,
        num_rows="dynamic",
        column_config=column_config,
        key=f"additional_consumption_editor_{uuid.uuid4()}"
    )

    return edited_additional_data

def edit_tank_properties():
    st.write("Edit tank properties:")

    col1, col2, col3 = st.columns(3)
    with col1:
        bunkering_record = st.checkbox("Bunkering Record")
    with col2:
        debunkering_record = st.checkbox("Debunkering Record")
    with col3:
        bunker_survey = st.checkbox("Bunker Survey")

    # Create the base DataFrame with fuel types as columns
    tank_props = pd.DataFrame({
        'Viscosity': [st.session_state.viscosity[fuel] for fuel in st.session_state.fuel_types],
        'Sulfur (%)': [st.session_state.sulfur[fuel] for fuel in st.session_state.fuel_types],
        'Current ROB': [np.random.uniform(50, 500) for _ in st.session_state.fuel_types]
    }, index=st.session_state.fuel_types)

    if bunkering_record:
        tank_props.insert(2, 'Bunkered qty(mT)', [0.0] * len(st.session_state.fuel_types))
    if debunkering_record:
        tank_props.insert(2, 'Debunkered qty(mT)', [0.0] * len(st.session_state.fuel_types))
    if bunker_survey:
        tank_props.insert(2, 'Survey Correction qty(mT)', [0.0] * len(st.session_state.fuel_types))

    tank_transfer = st.checkbox("Enable Fuel Transfer")

    if tank_transfer:
        tank_props['Qty (mT) Transferred From'] = [0.0] * len(st.session_state.fuel_types)
        tank_props['Qty (mT) Transferred To'] = [0.0] * len(st.session_state.fuel_types)

    column_config = {
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

    if bunkering_record:
        column_config['Bunkered qty(mT)'] = st.column_config.NumberColumn(
            'Bunkered qty(mT)', min_value=0.0, step=0.1, format="%.1f"
        )
    if debunkering_record:
        column_config['Debunkered qty(mT)'] = st.column_config.NumberColumn(
            'Debunkered qty(mT)', min_value=0.0, step=0.1, format="%.1f"
        )
    if bunker_survey:
        column_config['Survey Correction qty(mT)'] = st.column_config.NumberColumn(
            'Survey Correction qty(mT)', min_value=-100.0, max_value=100.0, step=0.1, format="%.1f"
        )

    if tank_transfer:
        column_config.update({
            'Qty (mT) Transferred From': st.column_config.NumberColumn(
                'Transferred From', min_value=0.0, step=0.1, format="%.1f"
            ),
            'Qty (mT) Transferred To': st.column_config.NumberColumn(
                'Transferred To', min_value=0.0, step=0.1, format="%.1f"
            )
        })

    edited_props = st.data_editor(
        tank_props,
        use_container_width=True,
        column_config=column_config,
        key=f"edit_tank_properties_editor_{uuid.uuid4()}"
    )

    # Update session state
    for fuel in st.session_state.fuel_types:
        st.session_state.viscosity[fuel] = edited_props.loc[fuel, 'Viscosity']
        st.session_state.sulfur[fuel] = edited_props.loc[fuel, 'Sulfur (%)']
        
    if 'current_rob' not in st.session_state:
        st.session_state.current_rob = {}
    for fuel in st.session_state.fuel_types:
        st.session_state.current_rob[fuel] = edited_props.loc[fuel, 'Current ROB']

    if tank_transfer:
        transfers_from = edited_props['Qty (mT) Transferred From']
        transfers_to = edited_props['Qty (mT) Transferred To']

        if transfers_from.sum() != transfers_to.sum():
            st.warning("The total quantity transferred from must equal the total quantity transferred to.")
        else:
            st.success(f"Total quantity transferred: {transfers_from.sum()} mT")

    return edited_props

def main():
    initialize_session_state()

    st.title("Fuel Consumption Report - Tank Sounding Method")

    display_tank_sounding_report()
    display_additional_table()

    if st.checkbox("Edit Fuel Properties"):
        edit_tank_properties()

    if st.button("Submit Report", type="primary"):
        st.success("Report submitted successfully!")

if __name__ == "__main__":
    main()
