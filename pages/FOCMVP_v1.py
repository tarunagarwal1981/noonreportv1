import streamlit as st
import pandas as pd
import numpy as np
import random
import string
import uuid

st.set_page_config(layout="wide", page_title="Fuel Consumption Report - Tank Sounding Method")

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

    # Define the specific fuel types for the Tank Sounding table
    if 'fuel_type_columns' not in st.session_state:
        st.session_state.fuel_type_columns = ['HSFO', 'LSFO', 'ULSFO', 'LSMGO', 'LNG']

    # Define all available fuel types for bunkering/debunkering dropdowns
    if 'available_fuel_types' not in st.session_state:
        st.session_state.available_fuel_types = [
            'HSFO', 'VLSFO', 'ULSFO', 'MGO', 'LPG', 'LNG', 'Methanol', 'Ethanol'
        ]

    if 'fuel_types' not in st.session_state:
        st.session_state.fuel_types = ['HFO', 'LFO', 'MGO/MDO', 'LPG', 'LNG', 'Methanol', 'Ethanol', 'Others', 'Other Fuel Type']

    if 'tanks' not in st.session_state:
        st.session_state.tanks = [f'Tank {i}' for i in range(1, 9)]

    # Initialize viscosity and sulfur with default values for all possible keys
    if 'viscosity' not in st.session_state:
        st.session_state.viscosity = {}
        # Initialize for fuel types
        for fuel in st.session_state.fuel_types:
            st.session_state.viscosity[fuel] = np.random.uniform(20, 100)
        # Initialize for tanks
        for tank in st.session_state.tanks:
            st.session_state.viscosity[tank] = np.random.uniform(20, 100)

    if 'sulfur' not in st.session_state:
        st.session_state.sulfur = {}
        # Initialize for fuel types
        for fuel in st.session_state.fuel_types:
            st.session_state.sulfur[fuel] = np.random.uniform(0.05, 0.49)
        # Initialize for tanks
        for tank in st.session_state.tanks:
            st.session_state.sulfur[tank] = np.random.uniform(0.05, 0.49)

    # Initialize consumption_data_tank_sounding with fuel types as columns
    if 'consumption_data_tank_sounding' not in st.session_state:
        index = st.session_state.consumers
        columns = st.session_state.fuel_type_columns
        st.session_state.consumption_data_tank_sounding = pd.DataFrame(0, index=index, columns=columns)
        
    if 'previous_rob_tank_sounding' not in st.session_state:
        # Initialize with random values using fuel type columns
        st.session_state.previous_rob_tank_sounding = pd.Series({fuel: np.random.uniform(100, 1000) 
                                                                 for fuel in st.session_state.fuel_type_columns})
    
    # Initialize fuel grades for tanks (still needed for tank properties section)
    if 'fuel_grades' not in st.session_state:
        st.session_state.fuel_grades = {}
        for tank in st.session_state.tanks:
            st.session_state.fuel_grades[tank] = random.choice(["LFO", "MGO", "HFO"])
    
    # Initialize current_rob for tanks (still needed for tank properties section)
    if 'current_rob' not in st.session_state:
        st.session_state.current_rob = {}
        for tank in st.session_state.tanks:
            st.session_state.current_rob[tank] = np.random.uniform(50, 500)
            
    # Initialize bunkering and debunkering entries
    if 'bunkering_entries' not in st.session_state:
        st.session_state.bunkering_entries = [{}]
        
    if 'debunkering_entries' not in st.session_state:
        st.session_state.debunkering_entries = [{}]

    if 'bdn_numbers' not in st.session_state:
        st.session_state.bdn_numbers = [
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) 
            for _ in range(8)
        ]

def display_tank_sounding_report():
    def create_editable_dataframe():
        # New structure with fuel types as columns but WITHOUT the BDN Number row
        index = ['Previous ROB'] + st.session_state.consumers + ['Current ROB']
        columns = st.session_state.fuel_type_columns  # Use the fuel type columns
        
        df = pd.DataFrame(index=index, columns=columns)
        
        # Set Previous ROB from session state or initialize with random values
        df.loc['Previous ROB'] = st.session_state.previous_rob_tank_sounding
        
        # Set consumption data from session state
        df.loc[st.session_state.consumers] = st.session_state.consumption_data_tank_sounding
        
        # Calculate Current ROB
        consumption = pd.to_numeric(df.loc[st.session_state.consumers].sum(), errors='coerce').fillna(0)
        df.loc['Current ROB'] = pd.to_numeric(df.loc['Previous ROB'], errors='coerce').fillna(0) - consumption
        
        return df

    df = create_editable_dataframe()
    
    st.subheader("Tank Sounding Method Fuel Consumption Data")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=f"tank_sounding_editor_{uuid.uuid4()}"
    )

    # Save edited data back to session state
    st.session_state.consumption_data_tank_sounding = edited_df.loc[st.session_state.consumers]
    st.session_state.previous_rob_tank_sounding = edited_df.loc['Previous ROB']
    
    return edited_df

def display_additional_table():
    st.subheader("Additional Consumption Data")
    
    last_column_name = "Fuel BDN No."
    
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
        ),
        last_column_name: st.column_config.TextColumn(
            "Fuel BDN No.",
            help="Enter the Fuel BDN Number",
            max_chars=50
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

def classify_fuel_by_viscosity(fuel_type, viscosity):
    """Classifies the fuel based on type and viscosity."""
    if fuel_type in ['HSFO', 'VLSFO', 'ULSFO']:
        if viscosity > 80:
            return 'HFO'
        else:
            return 'LFO'
    return fuel_type

def display_bunkering_details():
    st.markdown("<h4 style='font-size: 18px;'>Bunkering Details</h4>", unsafe_allow_html=True)
    
    for i, entry in enumerate(st.session_state.bunkering_entries):
        st.markdown(f"<h5 style='font-size: 16px;'>Bunkering Entry {i+1}</h5>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            entry['bdn_number'] = st.text_input("Bunker Delivery Note Number", value=entry.get('bdn_number', ''), key=f"bdn_number_{i}")
            entry['delivery_date'] = st.date_input("Bunker Delivery Date", value=entry.get('delivery_date', pd.Timestamp.now().date()), key=f"delivery_date_{i}")
            entry['delivery_time'] = st.time_input("Bunker Delivery Time", value=entry.get('delivery_time', pd.Timestamp.now().time()), key=f"delivery_time_{i}")
            
            # Add fuel type dropdown with the expanded list
            entry['fuel_type'] = st.selectbox(
                "Fuel Type", 
                options=st.session_state.available_fuel_types,
                index=st.session_state.available_fuel_types.index(entry.get('fuel_type', st.session_state.available_fuel_types[0])) 
                if entry.get('fuel_type') in st.session_state.available_fuel_types else 0,
                key=f"fuel_type_select_{i}"
            )
            
            # Add viscosity field
            entry['viscosity'] = st.number_input(
                "Viscosity (cSt)",
                min_value=0.0,
                max_value=1000.0,
                value=entry.get('viscosity', 50.0),
                step=0.1,
                key=f"viscosity_{i}"
            )
            
            # Classify the fuel type based on viscosity
            if entry['fuel_type'] in ['HSFO', 'VLSFO', 'ULSFO']:
                fuel_classification = "HFO" if entry['viscosity'] > 80 else "LFO"
                st.info(f"Based on viscosity, this will be classified as {fuel_classification}")
                entry['classified_as'] = fuel_classification
            
        with col2:
            entry['imo_number'] = st.text_input("IMO number", value=entry.get('imo_number', ''), key=f"imo_number_{i}")
            entry['mass'] = st.number_input("Mass (mt)", value=entry.get('mass', 0.0), min_value=0.0, step=0.1, key=f"mass_{i}")
            entry['lower_heating_value'] = st.number_input("Lower heating value (MJ/kg)", value=entry.get('lower_heating_value', 0.0), min_value=0.0, step=0.1, key=f"lower_heating_value_{i}")
            entry['eu_ghg_intensity'] = st.number_input("EU GHG emission intensity (gCO2eq/MJ)", value=entry.get('eu_ghg_intensity', 0.0), min_value=0.0, step=0.1, key=f"eu_ghg_intensity_{i}")
            
        with col3:
            entry['imo_ghg_intensity'] = st.number_input("IMO GHG emission intensity (gCO2eq/MJ)", value=entry.get('imo_ghg_intensity', 0.0), min_value=0.0, step=0.1, key=f"imo_ghg_intensity_{i}")
            entry['lcv_eu'] = st.number_input("Lower Calorific Value (EU) (MJ/kg)", value=entry.get('lcv_eu', 0.0), min_value=0.0, step=0.1, key=f"lcv_eu_{i}")
            entry['sustainability'] = st.text_input("Sustainability", value=entry.get('sustainability', ''), key=f"sustainability_{i}")
            
            # Add tank selection
            entry['tanks'] = st.multiselect("Select Tanks", st.session_state.tanks, default=entry.get('tanks', []), key=f"bunkering_tanks_{i}")
        
        # Updating tank fuel grades based on selection
        if entry.get('tanks') and entry.get('fuel_type') and entry.get('viscosity'):
            for tank in entry['tanks']:
                st.session_state.fuel_grades[tank] = classify_fuel_by_viscosity(entry['fuel_type'], entry['viscosity'])
    
    if st.button("➕ Add Bunkering Entry"):
        st.session_state.bunkering_entries.append({})
        st.experimental_rerun()

def display_debunkering_details():
    st.markdown("<h4 style='font-size: 18px;'>Debunkering Details</h4>", unsafe_allow_html=True)
    
    for i, entry in enumerate(st.session_state.debunkering_entries):
        st.markdown(f"<h5 style='font-size: 16px;'>Debunkering Entry {i+1}</h5>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            entry['date'] = st.date_input("Date of Debunkering", value=entry.get('date', pd.Timestamp.now().date()), key=f"debunker_date_{i}")
            entry['quantity'] = st.number_input("Quantity Debunkered (mt)", value=entry.get('quantity', 0.0), min_value=0.0, step=0.1, key=f"debunker_qty_{i}")
            
            # Add fuel type dropdown with the expanded list
            entry['fuel_type'] = st.selectbox(
                "Fuel Type", 
                options=st.session_state.available_fuel_types,
                index=st.session_state.available_fuel_types.index(entry.get('fuel_type', st.session_state.available_fuel_types[0])) 
                if entry.get('fuel_type') in st.session_state.available_fuel_types else 0,
                key=f"debunker_fuel_type_select_{i}"
            )
            
            # Add viscosity field for debunkering
            entry['viscosity'] = st.number_input(
                "Viscosity (cSt)",
                min_value=0.0,
                max_value=1000.0,
                value=entry.get('viscosity', 50.0),
                step=0.1,
                key=f"debunker_viscosity_{i}"
            )
            
            # Classify the fuel type based on viscosity
            if entry['fuel_type'] in ['HSFO', 'VLSFO', 'ULSFO']:
                fuel_classification = "HFO" if entry['viscosity'] > 80 else "LFO"
                st.info(f"Based on viscosity, this will be classified as {fuel_classification}")
                entry['classified_as'] = fuel_classification
                
        with col2:
            entry['bdn_number'] = st.text_input("BDN Number of Debunkered Oil", value=entry.get('bdn_number', ''), key=f"debunker_bdn_{i}")
            entry['receipt_file'] = st.file_uploader("Upload Receipt", type=['pdf', 'jpg', 'png'], key=f"receipt_file_{i}")
            
            # Add tank selection
            entry['tanks'] = st.multiselect("Select Tanks", st.session_state.tanks, default=entry.get('tanks', []), key=f"debunkering_tanks_{i}")
    
    if st.button("➕ Add Debunkering Entry"):
        st.session_state.debunkering_entries.append({})
        st.experimental_rerun()

def edit_tank_properties():
    # Add checkboxes for bunkering record, debunkering record, and Bunker Survey
    col1, col2, col3 = st.columns(3)
    with col1:
        bunkering_record = st.checkbox("Bunkering Record")
    with col2:
        debunkering_record = st.checkbox("Debunkering Record")
    with col3:
        bunker_survey = st.checkbox("Bunker Survey")

    # Display bunkering details if bunkering record is checked
    if bunkering_record:
        display_bunkering_details()

    # Display debunkering details if debunkering record is checked
    if debunkering_record:
        display_debunkering_details()

    fuel_grade_options = ['VLSFO', 'MGO', 'HFO']
    
    # Ensure all tanks have viscosity, sulfur, and fuel grade values
    for i in range(1, 9):
        tank_name = f'Tank {i}'
        if tank_name not in st.session_state.viscosity:
            st.session_state.viscosity[tank_name] = np.random.uniform(20, 100)
        if tank_name not in st.session_state.sulfur:
            st.session_state.sulfur[tank_name] = np.random.uniform(0.05, 0.49)
        if tank_name not in st.session_state.fuel_grades:
            st.session_state.fuel_grades[tank_name] = random.choice(fuel_grade_options)
        if tank_name not in st.session_state.current_rob:
            st.session_state.current_rob[tank_name] = np.random.uniform(50, 500)
    
    # Generate BDN numbers (one for each tank)
    if 'bdn_numbers' not in st.session_state:
        st.session_state.bdn_numbers = [
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) 
            for _ in range(8)
        ]
    
    # Create the base DataFrame - Add BDN number column
    tank_props = pd.DataFrame({
        'Fuel Grade': [st.session_state.fuel_grades.get(f'Tank {i}', random.choice(fuel_grade_options)) for i in range(1, 9)],
        'BDN Number': st.session_state.bdn_numbers,
        'Viscosity': [st.session_state.viscosity[f'Tank {i}'] for i in range(1, 9)],
        'Sulfur (%)': [st.session_state.sulfur[f'Tank {i}'] for i in range(1, 9)],
        'Current ROB': [st.session_state.current_rob.get(f'Tank {i}', np.random.uniform(50, 500)) for i in range(1, 9)]
    }, index=[f'Tank {i}' for i in range(1, 9)])

    # Add columns based on checked options
    if bunkering_record:
        tank_props.insert(4, 'Bunkered qty(mT)', [0.0] * 8)
    if debunkering_record:
        tank_props.insert(4, 'Debunkered qty(mT)', [0.0] * 8)
    if bunker_survey:
        tank_props.insert(4, 'Survey Correction qty(mT)', [0.0] * 8)

    tank_transfer = st.checkbox("Enable Tank-to-Tank Transfer")

    if tank_transfer:
        tank_props['Qty (mT) Transferred From Tank'] = [0.0] * 8
        tank_props['Qty (mT) Transferred To Tank'] = [0.0] * 8

    column_config = {
        'Fuel Grade': st.column_config.SelectboxColumn(
            'Fuel Grade',
            options=fuel_grade_options,
            required=True
        ),
        'BDN Number': st.column_config.TextColumn(
            'BDN Number',
            max_chars=15,
            help="Bunker Delivery Note Number"
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
    
    # Update session state with edited values
    for i in range(1, 9):
        tank_name = f'Tank {i}'
        st.session_state.viscosity[tank_name] = edited_props.loc[tank_name, 'Viscosity']
        st.session_state.sulfur[tank_name] = edited_props.loc[tank_name, 'Sulfur (%)']
        st.session_state.fuel_grades[tank_name] = edited_props.loc[tank_name, 'Fuel Grade']
        st.session_state.current_rob[tank_name] = edited_props.loc[tank_name, 'Current ROB']
        st.session_state.bdn_numbers[i-1] = edited_props.loc[tank_name, 'BDN Number']

    if tank_transfer:
        transfers_from = edited_props['Qty (mT) Transferred From Tank']
        transfers_to = edited_props['Qty (mT) Transferred To Tank']
        
        if transfers_from.sum() != transfers_to.sum():
            st.warning("The total quantity transferred from tanks must equal the total quantity transferred to tanks.")
        else:
            st.success(f"Total quantity transferred: {transfers_from.sum()} mT")

    return edited_props

def main():
    initialize_session_state()

    st.title("Fuel Consumption Report - Tank Sounding Method")

    # Display the tank sounding method report with fuel types as columns
    display_tank_sounding_report()
    
    # Display additional table for other consumption data
    display_additional_table()

    # Tank properties editor is always shown (no checkbox needed)
    st.subheader("Tank Properties")
    edit_tank_properties()

    if st.button("Submit Report", type="primary"):
        st.success("Report submitted successfully!")

if __name__ == "__main__":
    main()
