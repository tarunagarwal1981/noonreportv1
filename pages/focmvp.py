import streamlit as st
import pandas as pd
import numpy as np
import random
import string
import uuid

st.set_page_config(layout="wide", page_title="Tank Sounding Method")

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
    
    if 'tanks' not in st.session_state:
        st.session_state.tanks = [f'Tank {i}' for i in range(1, 9)]

def display_tank_sounding_report():
    def create_editable_dataframe():
        index = ['Fuel Type', 'BDN Number', 'Previous ROB'] + st.session_state.consumers + ['Current ROB']
        tanks = [f'Tank {i}' for i in range(1, 9)]
        df = pd.DataFrame(index=index, columns=tanks)
        fuel_types = ["VLSFO", "MGO", "HFO"]
        df.loc['Fuel Type'] = [random.choice(fuel_types) for _ in tanks]
        bdn_numbers = generate_random_bdn_numbers()
        df.loc['BDN Number'] = [bdn_numbers[i % 3] for i in range(len(tanks))]
        df.loc['Previous ROB'] = [np.random.uniform(100, 1000) for _ in tanks]
        for consumer in st.session_state.consumers:
            df.loc[consumer] = [np.random.uniform(0, 50) for _ in tanks]
        consumption = df.loc[st.session_state.consumers].sum()
        df.loc['Current ROB'] = df.loc['Previous ROB'] - consumption
        return df

    # Checkboxes for operations
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        bunkering_record = st.checkbox("Bunkering Record")
    with col2:
        debunkering_record = st.checkbox("Debunkering Record")
    with col3:
        bunker_survey = st.checkbox("Bunker Survey")
    with col4:
        tank_transfer = st.checkbox("Tank-to-Tank Transfer")

    # Display bunkering details if checked
    if bunkering_record:
        st.markdown("<h4 style='font-size: 18px;'>Bunkering Details</h4>", unsafe_allow_html=True)
        if 'bunkering_entries' not in st.session_state:
            st.session_state.bunkering_entries = [{}]
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
            entry['tanks'] = st.multiselect("Select Tanks", st.session_state.tanks, key=f"bunkering_tanks_{i}")
        if st.button("➕ Add Bunkering Entry"):
            st.session_state.bunkering_entries.append({})
            st.experimental_rerun()

    # Display debunkering details if checked
    if debunkering_record:
        st.markdown("<h4 style='font-size: 18px;'>Debunkering Details</h4>", unsafe_allow_html=True)
        if 'debunkering_entries' not in st.session_state:
            st.session_state.debunkering_entries = [{}]
        for i, entry in enumerate(st.session_state.debunkering_entries):
            st.markdown(f"<h5 style='font-size: 16px;'>Debunkering Entry {i+1}</h5>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                entry['date'] = st.date_input("Date of Debunkering", key=f"debunker_date_{i}")
                entry['quantity'] = st.number_input("Quantity Debunkered (mt)", min_value=0.0, step=0.1, key=f"debunker_qty_{i}")
            with col2:
                entry['bdn_number'] = st.text_input("BDN Number of Debunkered Oil", key=f"debunker_bdn_{i}")
                entry['receipt_file'] = st.file_uploader("Upload Receipt", type=['pdf', 'jpg', 'png'], key=f"receipt_file_{i}")
            entry['tanks'] = st.multiselect("Select Tanks", st.session_state.tanks, key=f"debunkering_tanks_{i}")
        if st.button("➕ Add Debunkering Entry"):
            st.session_state.debunkering_entries.append({})
            st.experimental_rerun()

    # Tank sounding data table
    st.subheader("Tank Sounding Method Fuel Consumption Data")
    df = create_editable_dataframe()
    
    # Add columns for bunker survey if checked
    if bunker_survey:
        df.loc['Bunker Survey Correction'] = [0.0] * len(df.columns)
        df.loc['Current ROB'] = df.loc['Previous ROB'] - df.loc[st.session_state.consumers].sum() + df.loc['Bunker Survey Correction']
    
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=f"tank_sounding_editor_{uuid.uuid4()}"
    )

    # Tank transfer section if checked
    if tank_transfer:
        st.subheader("Tank-to-Tank Transfer")
        transfer_df = pd.DataFrame({
            'From Tank': [''] * 3,
            'To Tank': [''] * 3,
            'Quantity (MT)': [0.0] * 3
        })
        
        edited_transfer = st.data_editor(
            transfer_df,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "From Tank": st.column_config.SelectboxColumn(
                    "From Tank",
                    options=st.session_state.tanks,
                ),
                "To Tank": st.column_config.SelectboxColumn(
                    "To Tank",
                    options=st.session_state.tanks,
                ),
                "Quantity (MT)": st.column_config.NumberColumn(
                    "Quantity (MT)",
                    min_value=0,
                    format="%.1f"
                )
            },
            key=f"tank_transfer_editor_{uuid.uuid4()}"
        )

    # Store data in session state
    st.session_state.consumption_data_tank_sounding = edited_df.loc[st.session_state.consumers]
    st.session_state.previous_rob_tank_sounding = edited_df.loc['Previous ROB']

    # Additional consumption data table
    st.subheader("Additional Consumption Data")
    additional_data = pd.DataFrame({
        'Work': [0, 0, 0, 0],
        'SFOC': [0, 0, 0, ''],
        'Tank Name': ['', '', '', '']
    }, index=['Reefer container', 'Cargo cooling', 'Heating/Discharge pump', 'Shore-Side Electricity'])
    
    edited_additional = st.data_editor(
        additional_data,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
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
            "Tank Name": st.column_config.TextColumn(
                "Tank Name",
                help="Enter the tank name",
                max_chars=50
            )
        },
        key=f"additional_consumption_editor_{uuid.uuid4()}"
    )

    if st.button("Submit Report", type="primary"):
        st.success("Report submitted successfully!")

def main():
    initialize_session_state()
    display_tank_sounding_report()

if __name__ == "__main__":
    main()
