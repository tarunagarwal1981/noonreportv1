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

    if 'consumption_data_tank' not in st.session_state:
        st.session_state.consumption_data_tank = pd.DataFrame(0, 
            index=st.session_state.consumers, 
            columns=st.session_state.tanks)

def display_tank_sounding_report():
    def create_editable_dataframe():
        # Initialize key rows for the sounding data table
        index = [
            'Fuel Type',
            'BDN Number',
            'Sounding Level (m)',
            'Temperature (°C)',
            'Density @ 15°C',
            'Volume (m³)',
            'Mass (MT)',
            'Previous ROB',
            'Current ROB'
        ]
        tanks = st.session_state.tanks
        df = pd.DataFrame(index=index, columns=tanks)
        
        # Set default values
        fuel_types = ["VLSFO", "MGO", "HFO"]
        df.loc['Fuel Type'] = [random.choice(fuel_types) for _ in tanks]
        bdn_numbers = generate_random_bdn_numbers()
        df.loc['BDN Number'] = [bdn_numbers[i % 3] for i in range(len(tanks))]
        df.loc['Previous ROB'] = [np.random.uniform(100, 1000) for _ in tanks]
        
        # Set reasonable default values for sounding data
        df.loc['Sounding Level (m)'] = [np.random.uniform(1, 10) for _ in tanks]
        df.loc['Temperature (°C)'] = [np.random.uniform(20, 40) for _ in tanks]
        df.loc['Density @ 15°C'] = [np.random.uniform(0.9, 1.0) for _ in tanks]
        df.loc['Volume (m³)'] = [np.random.uniform(50, 200) for _ in tanks]
        
        # Calculate mass based on volume and density
        df.loc['Mass (MT)'] = df.loc['Volume (m³)'] * df.loc['Density @ 15°C']
        
        # For consumer consumption data
        for consumer in st.session_state.consumers:
            df.loc[consumer] = [np.random.uniform(0, 5) for _ in tanks]
        
        # Calculate current ROB
        total_consumption = df.loc[st.session_state.consumers].sum()
        df.loc['Current ROB'] = df.loc['Previous ROB'] - total_consumption
        
        return df

    st.title("Tank Sounding Method")
    
    # Tank Sounding Data Table
    st.subheader("Tank Sounding Data")
    tank_data = create_editable_dataframe()
    edited_tank_data = st.data_editor(
        tank_data,
        use_container_width=True,
        key=f"tank_sounding_editor_{uuid.uuid4()}"
    )

    # Consumer Consumption Section
    st.subheader("Consumer Consumption Data")
    consumption_data = edited_tank_data.loc[st.session_state.consumers]
    edited_consumption = st.data_editor(
        consumption_data,
        use_container_width=True,
        key=f"consumption_editor_{uuid.uuid4()}"
    )

    # Additional consumption data for special equipment
    st.subheader("Additional Consumption Data")
    additional_data = pd.DataFrame({
        'Work (kWh)': [0, 0, 0, 0],
        'SFOC': [0, 0, 0, ''],
        'Tank Number': ['', '', '', '']
    }, index=['Reefer container', 'Cargo cooling', 'Heating/Discharge pump', 'Shore-Side Electricity'])
    
    edited_additional = st.data_editor(
        additional_data,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Work (kWh)": st.column_config.NumberColumn(
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
            "Tank Number": st.column_config.TextColumn(
                "Tank Number",
                help="Enter the tank number",
                max_chars=50
            )
        },
        key=f"additional_consumption_editor_{uuid.uuid4()}"
    )

    # Summary section
    st.subheader("Summary")
    total_consumption = consumption_data.sum().sum()
    total_rob = edited_tank_data.loc['Current ROB'].sum()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Fuel Consumption", f"{total_consumption:.2f} MT")
    with col2:
        st.metric("Total Remaining On Board", f"{total_rob:.2f} MT")

    if st.button("Submit Report", type="primary"):
        st.success("Tank sounding report submitted successfully!")
        
        # Save data to session state
        st.session_state.consumption_data_tank = edited_consumption
        st.session_state.tank_data = edited_tank_data
        st.session_state.additional_consumption = edited_additional

def main():
    initialize_session_state()
    display_tank_sounding_report()

if __name__ == "__main__":
    main()
