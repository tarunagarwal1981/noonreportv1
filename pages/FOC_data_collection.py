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

# Initialize session state
def initialize_session_state():
    # Define consumers
    if 'consumers' not in st.session_state:
        st.session_state.consumers = [
            'Main Engine', 'Aux Engine1', 'Aux Engine2', 'Aux Engine3',
            'Boiler 1', '    Boiler 1 - Cargo Heating', '    Boiler 1 - Discharge',
            'Boiler 2', '    Boiler 2 - Cargo Heating', '    Boiler 2 - Discharge',
            'IGG', 'Incinerator', 'DPP1', 'DPP2', 'DPP3'
        ]

    # Define fuel types
    if 'fuel_types' not in st.session_state:
        st.session_state.fuel_types = ['HFO', 'LFO', 'MGO/MDO', 'LPG', 'LNG', 'Methanol', 'Ethanol', 'Others', 'Other Fuel Type']

    # Define tanks
    if 'tanks' not in st.session_state:
        st.session_state.tanks = [f'Tank {i}' for i in range(1, 9)]

    # Initialize viscosity and sulfur content
    if 'viscosity' not in st.session_state:
        st.session_state.viscosity = {item: np.random.uniform(20, 100) for item in st.session_state.fuel_types + st.session_state.tanks}
    if 'sulfur' not in st.session_state:
        st.session_state.sulfur = {item: np.random.uniform(0.05, 0.49) for item in st.session_state.fuel_types + st.session_state.tanks}

    # Initialize ROBs for different methods
    if 'previous_rob_fuel' not in st.session_state:
        st.session_state.previous_rob_fuel = pd.Series({fuel: np.random.uniform(100, 1000) for fuel in st.session_state.fuel_types})
    if 'previous_rob_tank' not in st.session_state:
        st.session_state.previous_rob_tank = pd.Series({tank: np.random.uniform(100, 1000) for tank in st.session_state.tanks})
    if 'previous_rob_tank_sounding' not in st.session_state:
        st.session_state.previous_rob_tank_sounding = pd.Series({tank: np.random.uniform(100, 1000) for tank in st.session_state.tanks})

    # Initialize bunker survey corrections
    if 'bunker_survey_correction_fuel' not in st.session_state:
        st.session_state.bunker_survey_correction_fuel = pd.Series({fuel: 0 for fuel in st.session_state.fuel_types})
    if 'bunker_survey_correction_tank' not in st.session_state:
        st.session_state.bunker_survey_correction_tank = pd.Series({tank: 0 for tank in st.session_state.tanks})
    if 'bunker_survey_correction_tank_sounding' not in st.session_state:
        st.session_state.bunker_survey_correction_tank_sounding = pd.Series({tank: 0 for tank in st.session_state.tanks})

    # Initialize consumption data for different methods
    if 'consumption_data_fuel' not in st.session_state:
        st.session_state.consumption_data_fuel = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.fuel_types)
    if 'consumption_data_tank' not in st.session_state:
        st.session_state.consumption_data_tank = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.tanks)
    if 'consumption_data_tank_sounding' not in st.session_state:
        st.session_state.consumption_data_tank_sounding = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.tanks)
    if 'consumption_data_flowmeter' not in st.session_state:
        st.session_state.consumption_data_flowmeter = pd.DataFrame(0, index=st.session_state.consumers, 
                                                                   columns=["Flowmeter In", "Flowmeter Out", "Temp at flowmeter", 
                                                                            "Density @ 15°C", "Fuel Type", "Total Consumption (mT)"])

    # Initialize bunker survey comments
    if 'bunker_survey_comments' not in st.session_state:
        st.session_state.bunker_survey_comments = ""

    # Initialize bunkering and debunkering entries
    if 'bunkering_entries' not in st.session_state:
        st.session_state.bunkering_entries = [{}]
    if 'debunkering_entries' not in st.session_state:
        st.session_state.debunkering_entries = [{}]

    if 'tanks' not in st.session_state:
        st.session_state.tanks = [f'Tank {i}' for i in range(1, 9)]

# Fuel based report functionality
def display_fuel_consumption_report(bunker_survey, bunkering_happened, debunkering_happened):
    def create_editable_dataframe():
        index = ['Previous ROB'] + st.session_state.consumers
        if bunkering_happened:
            index.append('Bunkered Qty')
        if debunkering_happened:
            index.append('Debunkered Qty')
        if bunker_survey:
            index.append('Bunker Survey Correction')
        index.append('Current ROB')
        
        # Create DataFrame with fuel types as columns
        df = pd.DataFrame(0, index=index, columns=st.session_state.fuel_types)
        
        # Fill 'Previous ROB' row
        df.loc['Previous ROB'] = st.session_state.previous_rob_fuel
        
        # Fill consumption data for consumers
        df.loc[st.session_state.consumers] = st.session_state.consumption_data_fuel
        
        # Fill bunkering and debunkering quantities if applicable
        if bunkering_happened:
            total_bunkered = sum(entry.get('mass', 0) for entry in st.session_state.bunkering_entries)
            df.loc['Bunkered Qty'] = [total_bunkered] + [0] * (len(st.session_state.fuel_types) - 1)
        if debunkering_happened:
            total_debunkered = sum(entry.get('quantity', 0) for entry in st.session_state.debunkering_entries)
            df.loc['Debunkered Qty'] = [total_debunkered] + [0] * (len(st.session_state.fuel_types) - 1)
        
        # Fill bunker survey correction if needed
        if bunker_survey:
            df.loc['Bunker Survey Correction'] = st.session_state.bunker_survey_correction_fuel
        
        # Ensure total consumption calculation is numeric
        total_consumption = pd.to_numeric(df.loc[st.session_state.consumers].sum(), errors='coerce').fillna(0)
        
        # Calculate Current ROB
        df.loc['Current ROB'] = pd.to_numeric(df.loc['Previous ROB'], errors='coerce').fillna(0) - total_consumption
        
        # Add bunkering and subtract debunkering if applicable
        if bunkering_happened:
            df.loc['Current ROB'] += pd.to_numeric(df.loc['Bunkered Qty'], errors='coerce').fillna(0)
        if debunkering_happened:
            df.loc['Current ROB'] -= pd.to_numeric(df.loc['Debunkered Qty'], errors='coerce').fillna(0)
        
        # Add bunker correction to Current ROB if present
        if bunker_survey:
            df.loc['Current ROB'] += pd.to_numeric(df.loc['Bunker Survey Correction'], errors='coerce').fillna(0)
        
        return df

    df = create_editable_dataframe()
    
    st.subheader("Fuel Consumption Data")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=f"fuel_consumption_editor_{uuid.uuid4()}"
    )

    # Update session state
    st.session_state.consumption_data_fuel = edited_df.loc[st.session_state.consumers]
    st.session_state.previous_rob_fuel = edited_df.loc['Previous ROB']
    if bunker_survey:
        st.session_state.bunker_survey_correction_fuel = edited_df.loc['Bunker Survey Correction']

# BDN based report functionality
def display_bdn_consumption_report(bunker_survey, bunkering_happened, debunkering_happened):
    def create_editable_dataframe():
        # Define the index (now starting with 'BDN Number')
        index = ['BDN Number', 'Previous ROB'] + st.session_state.consumers
        if bunkering_happened:
            index.append('Bunkered Qty')
        if debunkering_happened:
            index.append('Debunkered Qty')
        if bunker_survey:
            index.append('Bunker Survey Correction')
        index.append('Current ROB')
        
        # Create DataFrame
        df = pd.DataFrame(index=index, columns=st.session_state.tanks)
        
        # Generate three random BDN numbers and repeat them across columns
        bdn_numbers = generate_random_bdn_numbers()
        df.loc['BDN Number'] = [bdn_numbers[i % 3] for i in range(len(st.session_state.tanks))]
        
        # Fill 'Previous ROB' row
        df.loc['Previous ROB'] = st.session_state.previous_rob_tank
        
        # Fill consumption data for consumers
        df.loc[st.session_state.consumers] = st.session_state.consumption_data_tank
        
        # Fill bunkering and debunkering quantities if applicable
        if bunkering_happened:
            total_bunkered = sum(entry.get('mass', 0) for entry in st.session_state.bunkering_entries)
            df.loc['Bunkered Qty'] = [total_bunkered] + [0] * (len(st.session_state.tanks) - 1)
        if debunkering_happened:
            total_debunkered = sum(entry.get('quantity', 0) for entry in st.session_state.debunkering_entries)
            df.loc['Debunkered Qty'] = [total_debunkered] + [0] * (len(st.session_state.tanks) - 1)
        
        # Fill bunker survey correction if needed
        if bunker_survey:
            df.loc['Bunker Survey Correction'] = st.session_state.bunker_survey_correction_tank
        
        # Ensure total consumption calculation is numeric
        total_consumption = pd.to_numeric(df.loc[st.session_state.consumers].sum(), errors='coerce').fillna(0)
        
        # Calculate Current ROB
        df.loc['Current ROB'] = pd.to_numeric(df.loc['Previous ROB'], errors='coerce').fillna(0) - total_consumption
        
        # Add bunkering and subtract debunkering if applicable
        if bunkering_happened:
            df.loc['Current ROB'] += pd.to_numeric(df.loc['Bunkered Qty'], errors='coerce').fillna(0)
        if debunkering_happened:
            df.loc['Current ROB'] -= pd.to_numeric(df.loc['Debunkered Qty'], errors='coerce').fillna(0)
        
        # Add bunker correction to Current ROB if present
        if bunker_survey:
            df.loc['Current ROB'] += pd.to_numeric(df.loc['Bunker Survey Correction'], errors='coerce').fillna(0)
        
        return df

    df = create_editable_dataframe()
    
    st.subheader("BDN Based Fuel Consumption Data")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=f"bdn_consumption_editor_{uuid.uuid4()}"
    )

    # Update session state
    st.session_state.consumption_data_tank = edited_df.loc[st.session_state.consumers]
    st.session_state.previous_rob_tank = edited_df.loc['Previous ROB']
    if bunker_survey:
        st.session_state.bunker_survey_correction_tank = edited_df.loc['Bunker Survey Correction']

def display_additional_table(fuel_type_view):
    st.subheader("Additional Consumption Data")
    
    # Determine the last column name based on the selected view
    last_column_name = "Fuel Type" if fuel_type_view else "Fuel BDN No."
    
    additional_data = pd.DataFrame({
        'Work': [0, 0, 0, 0],
        'SFOC': [0, 0, 0, ''],
        last_column_name: ['', '', '', '']
    }, index=['Reefer container', 'Cargo cooling', 'Heating/Discharge pump', 'Shore-Side Electricity'])
    
    # Create column configuration
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
    
    # Add configuration for the last column based on the view
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
    
    edited_additional_data = st.data_editor(
        additional_data,
        use_container_width=True,
        num_rows="dynamic",
        column_config=column_config,
        key=f"additional_consumption_editor_{uuid.uuid4()}"
    )

    return edited_additional_data

def display_bunkering_details():
    st.markdown("<h4 style='font-size: 18px;'>Bunkering Details</h4>", unsafe_allow_html=True)
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
        
        # Add tank selection
        entry['tanks'] = st.multiselect("Select Tanks", st.session_state.tanks, key=f"bunkering_tanks_{i}")

    if st.button("➕ Add Bunkering Entry"):
        st.session_state.bunkering_entries.append({})
        st.experimental_rerun()

def display_debunkering_details():
    st.markdown("<h4 style='font-size: 18px;'>Debunkering Details</h4>", unsafe_allow_html=True)
    for i, entry in enumerate(st.session_state.debunkering_entries):
        st.markdown(f"<h5 style='font-size: 16px;'>Debunkering Entry {i+1}</h5>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            entry['date'] = st.date_input("Date of Debunkering", key=f"debunker_date_{i}")
            entry['quantity'] = st.number_input("Quantity Debunkered (mt)", min_value=0.0, step=0.1, key=f"debunker_qty_{i}")
        with col2:
            entry['bdn_number'] = st.text_input("BDN Number of Debunkered Oil", key=f"debunker_bdn_{i}")
            entry['receipt_file'] = st.file_uploader("Upload Receipt", type=['pdf', 'jpg', 'png'], key=f"receipt_file_{i}")
        
        # Add tank selection
        entry['tanks'] = st.multiselect("Select Tanks", st.session_state.tanks, key=f"debunkering_tanks_{i}")

    if st.button("➕ Add Debunkering Entry"):
        st.session_state.debunkering_entries.append({})
        st.experimental_rerun()



def display_fuel_type_summary(bunker_survey, bunkering_happened, debunkering_happened):
    st.subheader("Fuel Type Summary")
    
    # Define row names and column names
    row_names = ["HFO", "LFO", "MGO", "MDO", "LPG", "LNG", "Methanol", "Ethanol"]
    columns = ["Previous ROB (mT)", "Current ROB (mT)"]
    
    # Dynamically adjust columns based on bunker survey, bunkering, or debunkering
    if bunker_survey:
        columns.insert(1, "Survey Correction (mT)")
    elif bunkering_happened:
        columns.insert(1, "Bunkered Qty (mT)")
    elif debunkering_happened:
        columns.insert(1, "Debunkered Qty (mT)")
    
    # Initialize the DataFrame for the summary table
    df_summary = pd.DataFrame(0, index=row_names, columns=columns)
    
    # Fill the table with random data (replace with actual data logic)
    df_summary["Previous ROB (mT)"] = [np.random.uniform(100, 500) for _ in range(len(row_names))]
    df_summary["Current ROB (mT)"] = [np.random.uniform(50, 450) for _ in range(len(row_names))]
    
    # Fill Bunkered Qty / Survey Correction / Debunkered Qty if applicable
    if "Survey Correction (mT)" in columns:
        df_summary["Survey Correction (mT)"] = [np.random.uniform(-5, 5) for _ in range(len(row_names))]
    elif "Bunkered Qty (mT)" in columns:
        df_summary["Bunkered Qty (mT)"] = [np.random.uniform(10, 50) for _ in range(len(row_names))]
    elif "Debunkered Qty (mT)" in columns:
        df_summary["Debunkered Qty (mT)"] = [np.random.uniform(10, 30) for _ in range(len(row_names))]
    
    # Display the summary table
    st.dataframe(df_summary)

# Function to display Flowmeter Method table similar to BDN-based method

def display_flowmeter_method_report(bunker_survey, bunkering_happened, debunkering_happened):
    def create_editable_dataframe():
        # Define the index (only consumers)
        index = st.session_state.consumers

        # Create DataFrame with the Flowmeter columns
        flowmeter_columns = [
            "Flowmeter In", "Flowmeter Out", "Temp at flowmeter", 
            "Density @ 15°C", "Fuel Type", "Total Consumption (mT)"
        ]
        
        # Initialize the DataFrame for the flowmeter method with zeros
        df = pd.DataFrame(0, index=index, columns=flowmeter_columns)

        # List of fuel types to randomly choose from
        fuel_types = ["LFO", "MGO", "HFO"]

        # Fill consumption data for consumers with random data
        for consumer in st.session_state.consumers:
            row_data = [np.random.uniform(10, 50) for _ in range(len(flowmeter_columns) - 2)]  # -2 because we'll set Fuel Type and Total Consumption separately
            row_data.append(random.choice(fuel_types))  # Randomly choose a fuel type
            row_data.append(np.random.uniform(1, 10))  # Random Total Consumption
            df.loc[consumer] = row_data

        return df

    # Create the editable DataFrame for the Flowmeter method
    df = create_editable_dataframe()
    
    st.subheader("Flowmeter Method Fuel Consumption Data")
    
    # Display the DataFrame in editable format
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",  # This ensures no new rows can be added
        key=f"flowmeter_consumption_editor_{uuid.uuid4()}"
    )

    # Update session state based on the edited data
    st.session_state.consumption_data_flowmeter = edited_df

def display_tank_sounding_report(bunker_survey, bunkering_happened, debunkering_happened):
    def create_editable_dataframe():
        # Define the index
        index = ['Fuel Type', 'BDN Number', 'Previous ROB'] + st.session_state.consumers
        if bunkering_happened:
            index.append('Bunkered Qty')
        if debunkering_happened:
            index.append('Debunkered Qty')
        if bunker_survey:
            index.append('Bunker Survey Correction')
        index.append('Current ROB')
        
        # Create DataFrame with tank columns
        tanks = [f'Tank {i}' for i in range(1, 9)]
        df = pd.DataFrame(index=index, columns=tanks)
        
        # Fill 'Fuel Type' row
        fuel_types = ["LFO", "MGO", "HFO"]
        df.loc['Fuel Type'] = [random.choice(fuel_types) for _ in tanks]
        
        # Fill 'BDN Number' row
        bdn_numbers = generate_random_bdn_numbers()
        df.loc['BDN Number'] = [bdn_numbers[i % 3] for i in range(len(tanks))]
        
        # Fill 'Previous ROB' row
        df.loc['Previous ROB'] = [np.random.uniform(100, 1000) for _ in tanks]
        
        # Fill consumption data for consumers
        for consumer in st.session_state.consumers:
            df.loc[consumer] = [np.random.uniform(0, 50) for _ in tanks]
        
        # Fill bunkering and debunkering quantities if applicable
        if bunkering_happened:
            total_bunkered = sum(entry.get('mass', 0) for entry in st.session_state.bunkering_entries)
            df.loc['Bunkered Qty'] = [total_bunkered / len(tanks)] * len(tanks)
        if debunkering_happened:
            total_debunkered = sum(entry.get('quantity', 0) for entry in st.session_state.debunkering_entries)
            df.loc['Debunkered Qty'] = [total_debunkered / len(tanks)] * len(tanks)
        
        # Fill bunker survey correction if needed
        if bunker_survey:
            df.loc['Bunker Survey Correction'] = [np.random.uniform(-5, 5) for _ in tanks]
        
        # Calculate Current ROB
        consumption = df.loc[st.session_state.consumers].sum()
        df.loc['Current ROB'] = df.loc['Previous ROB'] - consumption
        if bunkering_happened:
            df.loc['Current ROB'] += df.loc['Bunkered Qty']
        if debunkering_happened:
            df.loc['Current ROB'] -= df.loc['Debunkered Qty']
        if bunker_survey:
            df.loc['Current ROB'] += df.loc['Bunker Survey Correction']
        
        return df

    df = create_editable_dataframe()
    
    st.subheader("Tank Sounding Method Fuel Consumption Data")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=f"tank_sounding_editor_{uuid.uuid4()}"
    )

    # Update session state
    st.session_state.consumption_data_tank_sounding = edited_df.loc[st.session_state.consumers]
    st.session_state.previous_rob_tank_sounding = edited_df.loc['Previous ROB']
    if bunker_survey:
        st.session_state.bunker_survey_correction_tank_sounding = edited_df.loc['Bunker Survey Correction']

def display_ctms_method_report(bunker_survey, bunkering_happened, debunkering_happened):
    def create_editable_dataframe():
        index = ['Previous ROB'] + st.session_state.consumers
        if bunkering_happened:
            index.append('Bunkered Qty')
        if debunkering_happened:
            index.append('Debunkered Qty')
        if bunker_survey:
            index.append('Bunker Survey Correction')
        index.append('Current ROB')
        
        columns = ['HFO', 'LFO', 'MGO/MDO']
        
        df = pd.DataFrame(0, index=index, columns=columns)
        
        # Fill 'Previous ROB' row
        df.loc['Previous ROB'] = [np.random.uniform(100, 1000) for _ in range(len(columns))]
        
        # Fill consumption data for consumers
        for consumer in st.session_state.consumers:
            df.loc[consumer] = [np.random.uniform(0, 50) for _ in range(len(columns))]
        
        # Fill bunkering and debunkering quantities if applicable
        if bunkering_happened:
            df.loc['Bunkered Qty'] = [np.random.uniform(50, 200) for _ in range(len(columns))]
        if debunkering_happened:
            df.loc['Debunkered Qty'] = [np.random.uniform(10, 50) for _ in range(len(columns))]
        
        # Fill bunker survey correction if needed
        if bunker_survey:
            df.loc['Bunker Survey Correction'] = [np.random.uniform(-5, 5) for _ in range(len(columns))]
        
        # Calculate Current ROB
        df.loc['Current ROB'] = df.loc['Previous ROB'] - df.loc[st.session_state.consumers].sum()
        if bunkering_happened:
            df.loc['Current ROB'] += df.loc['Bunkered Qty']
        if debunkering_happened:
            df.loc['Current ROB'] -= df.loc['Debunkered Qty']
        if bunker_survey:
            df.loc['Current ROB'] += df.loc['Bunker Survey Correction']
        
        return df

    def create_ctms_specific_dataframe():
        index = ['CTMS qty (m3)', 'Cargo loaded (m3)', 'Cargo discharged (m3)', 'Density', 'N2 correction', 'Total LNG consumption (mT)']
        df = pd.DataFrame(0, index=index, columns=['Value'])
        
        # Fill with random data for demonstration
        df.loc['CTMS qty (m3)'] = np.random.uniform(1000, 5000)
        df.loc['Cargo loaded (m3)'] = np.random.uniform(500, 2000)
        df.loc['Cargo discharged (m3)'] = np.random.uniform(500, 2000)
        df.loc['Density'] = np.random.uniform(0.4, 0.5)
        df.loc['N2 correction'] = np.random.uniform(-5, 5)
        df.loc['Total LNG consumption (mT)'] = np.random.uniform(50, 200)
        
        return df

    st.subheader("CTMS Method Fuel Consumption Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        df = create_editable_dataframe()
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
            key=f"ctms_method_editor_{uuid.uuid4()}"
        )

        # Update session state
        st.session_state.consumption_data_ctms = edited_df.loc[st.session_state.consumers]
        st.session_state.previous_rob_ctms = edited_df.loc['Previous ROB']
        if bunker_survey:
            st.session_state.bunker_survey_correction_ctms = edited_df.loc['Bunker Survey Correction']

    with col2:
        ctms_df = create_ctms_specific_dataframe()
        edited_ctms_df = st.data_editor(
            ctms_df,
            use_container_width=True,
            num_rows="fixed",
            key=f"ctms_specific_editor_{uuid.uuid4()}"
        )

        # Update session state for CTMS specific data
        st.session_state.ctms_specific_data = edited_ctms_df

    return edited_df, edited_ctms_df
# Main app functionality
def main():
    initialize_session_state()

    st.title("Fuel Consumption and BDN Report")

    # Checkbox for view selection
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

    # Ensure only one view is selected
    if sum([fuel_type_view, bdn_view, flowmeter_method, tank_sounding_method, ctms_method]) > 1:
        st.warning("Please select only one view type.")
        st.stop()
    elif not fuel_type_view and not bdn_view and not flowmeter_method and not tank_sounding_method and not ctms_method:
        st.warning("Please select a view type.")
        st.stop()
        
    # Additional checkboxes for bunkering, debunkering, and bunker survey
    st.markdown("### Additional Options")
    col1, col2, col3 = st.columns(3)
    with col1:
        bunkering_happened = st.checkbox("Bunkering Happened", key="bunkering_checkbox")
    with col2:
        debunkering_happened = st.checkbox("Debunkering Happened", key="debunkering_checkbox")
    with col3:
        bunker_survey = st.checkbox("Bunker Survey", key="bunker_survey_checkbox")

    # Display bunkering details if bunkering happened
    if bunkering_happened:
        display_bunkering_details()

    # Display debunkering details if debunkering happened
    if debunkering_happened:
        display_debunkering_details()

    # Bunker survey comments
    if bunker_survey:
        st.session_state.bunker_survey_comments = st.text_area("Bunker Survey Comments", value=st.session_state.bunker_survey_comments, height=100)

    # Display corresponding report based on the selected view
    if fuel_type_view:
        display_fuel_consumption_report(bunker_survey, bunkering_happened, debunkering_happened)
    elif bdn_view:
        display_bdn_consumption_report(bunker_survey, bunkering_happened, debunkering_happened)
    elif flowmeter_method:
        display_flowmeter_method_report(False, False, False)
        display_fuel_type_summary(bunker_survey, bunkering_happened, debunkering_happened)
    elif tank_sounding_method:
        display_tank_sounding_report(bunker_survey, bunkering_happened, debunkering_happened)
    elif ctms_method:
        display_ctms_method_report(bunker_survey, bunkering_happened, debunkering_happened)
    
    # Display additional table with the correct view type
    display_additional_table(fuel_type_view)

    # Submit button
    if st.button("Submit Report", type="primary"):
        st.success("Report submitted successfully!")

if __name__ == "__main__":
    main()
