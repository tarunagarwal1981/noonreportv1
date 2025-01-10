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

def round_to_one(value):
    """Round a number to one decimal place."""
    return round(value, 1)

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
    st.title("Tank Sounding Method")

    # Tank metadata section
    st.subheader("Tank Information")
    tank_info = pd.DataFrame({
        'Fuel Type': ["VLSFO", "MGO", "HFO", "VLSFO", "MGO", "HFO", "VLSFO", "MGO"],
        'BDN Number': generate_random_bdn_numbers() * 3,
    }, index=st.session_state.tanks)
    
    edited_tank_info = st.data_editor(
        tank_info,
        use_container_width=True,
        key=f"tank_info_editor_{uuid.uuid4()}"
    )

    # Tank sounding measurements section
    st.subheader("Tank Sounding Measurements")
    sounding_data = pd.DataFrame({
        'Sounding Level (m)': [round_to_one(np.random.uniform(1, 10)) for _ in range(8)],
        'Temperature (°C)': [round_to_one(np.random.uniform(20, 40)) for _ in range(8)],
        'Density @ 15°C': [round_to_one(np.random.uniform(0.9, 1.0)) for _ in range(8)],
        'Volume (m³)': [round_to_one(np.random.uniform(50, 200)) for _ in range(8)],
        'Mass (MT)': [0.0] * 8,  # Will be calculated
        'Previous ROB (MT)': [round_to_one(np.random.uniform(100, 1000)) for _ in range(8)],
        'Current ROB (MT)': [0.0] * 8,  # Will be calculated
    }, index=st.session_state.tanks)

    # Convert columns to numeric and format to one decimal
    numeric_columns = ['Sounding Level (m)', 'Temperature (°C)', 'Density @ 15°C', 
                      'Volume (m³)', 'Mass (MT)', 'Previous ROB (MT)', 'Current ROB (MT)']
    for col in numeric_columns:
        sounding_data[col] = pd.to_numeric(sounding_data[col], errors='coerce').round(1)

    # Calculate mass with one decimal
    sounding_data['Mass (MT)'] = (sounding_data['Volume (m³)'] * sounding_data['Density @ 15°C']).round(1)
    
    edited_sounding_data = st.data_editor(
        sounding_data,
        use_container_width=True,
        column_config={col: st.column_config.NumberColumn(
            col, format="%.1f"
        ) for col in numeric_columns},
        key=f"sounding_editor_{uuid.uuid4()}"
    )

    # Consumer consumption section
    st.subheader("Consumer Consumption Data")
    consumption_df = pd.DataFrame(
        np.round(np.random.uniform(0, 5, size=(len(st.session_state.consumers), len(st.session_state.tanks))), 1),
        index=st.session_state.consumers,
        columns=st.session_state.tanks
    )
    
    edited_consumption = st.data_editor(
        consumption_df,
        use_container_width=True,
        column_config={tank: st.column_config.NumberColumn(
            tank, format="%.1f"
        ) for tank in st.session_state.tanks},
        key=f"consumption_editor_{uuid.uuid4()}"
    )

    # Calculate current ROB
    total_consumption = edited_consumption.sum().round(1)
    current_rob = (edited_sounding_data['Previous ROB (MT)'] - total_consumption).round(1)
    edited_sounding_data['Current ROB (MT)'] = current_rob

    # Additional consumption data for special equipment
    st.subheader("Additional Consumption Data")
    additional_data = pd.DataFrame({
        'Work (kWh)': [0.0, 0.0, 0.0, 0.0],
        'SFOC': [0.0, 0.0, 0.0, 0.0],
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
                format="%.1f"
            ),
            "SFOC": st.column_config.NumberColumn(
                "SFOC",
                help="Specific Fuel Oil Consumption",
                min_value=0,
                format="%.1f"
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
    total_consumption = round_to_one(edited_consumption.astype(float).sum().sum())
    total_rob = round_to_one(edited_sounding_data['Current ROB (MT)'].sum())
    total_mass = round_to_one(edited_sounding_data['Mass (MT)'].sum())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Fuel Consumption", f"{total_consumption} MT")
    with col2:
        st.metric("Total Mass from Sounding", f"{total_mass} MT")
    with col3:
        st.metric("Total Remaining On Board", f"{total_rob} MT")

    # Validation warnings
    if total_consumption > edited_sounding_data['Previous ROB (MT)'].sum():
        st.warning("⚠️ Total consumption exceeds previous ROB!")

    mass_rob_diff = round_to_one(abs(edited_sounding_data['Mass (MT)'].sum() - total_rob))
    if mass_rob_diff > 5:  # 5 MT tolerance
        st.warning(f"⚠️ Large discrepancy ({mass_rob_diff} MT) between sounding mass and calculated ROB!")

    # Submit button
    if st.button("Submit Report", type="primary"):
        # Store data in session state for future reference
        st.session_state.tank_info = edited_tank_info
        st.session_state.sounding_data = edited_sounding_data
        st.session_state.consumption_data = edited_consumption
        st.session_state.additional_consumption = edited_additional
        
        st.success("Tank sounding report submitted successfully!")
        st.balloons()

def main():
    initialize_session_state()
    display_tank_sounding_report()

if __name__ == "__main__":
    main()
