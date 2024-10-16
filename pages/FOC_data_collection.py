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
        st.session_state.fuel_types = ['HFO', 'LFO', 'MGO/MDO', 'LPG', 'LNG', 'Methanol', 'Ethanol', 'Others', 'Other Fuel Type']

    if 'tanks' not in st.session_state:
        st.session_state.tanks = [f'Tank {i}' for i in range(1, 9)]

    if 'viscosity' not in st.session_state:
        st.session_state.viscosity = {item: np.random.uniform(20, 100) for item in st.session_state.fuel_types + st.session_state.tanks}

    if 'sulfur' not in st.session_state:
        st.session_state.sulfur = {item: np.random.uniform(0.05, 0.49) for item in st.session_state.fuel_types + st.session_state.tanks}

    if 'previous_rob_fuel' not in st.session_state:
        st.session_state.previous_rob_fuel = pd.Series({fuel: np.random.uniform(100, 1000) for fuel in st.session_state.fuel_types})

    if 'previous_rob_tank' not in st.session_state:
        st.session_state.previous_rob_tank = pd.Series({tank: np.random.uniform(100, 1000) for tank in st.session_state.tanks})

    if 'consumption_data_fuel' not in st.session_state:
        st.session_state.consumption_data_fuel = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.fuel_types)

    if 'consumption_data_tank' not in st.session_state:
        st.session_state.consumption_data_tank = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.tanks)

    if 'consumption_data_flowmeter' not in st.session_state:
        st.session_state.consumption_data_flowmeter = pd.DataFrame(0, index=st.session_state.consumers, 
                                                                   columns=["Flowmeter In", "Flowmeter Out", "Temp at flowmeter", 
                                                                            "Density @ 15°C", "Fuel Type", "Total Consumption (mT)"])

def display_fuel_consumption_report():
    def create_editable_dataframe():
        index = ['Previous ROB'] + st.session_state.consumers + ['Current ROB']
        df = pd.DataFrame(0, index=index, columns=st.session_state.fuel_types)
        df.loc['Previous ROB'] = st.session_state.previous_rob_fuel
        df.loc[st.session_state.consumers] = st.session_state.consumption_data_fuel
        total_consumption = pd.to_numeric(df.loc[st.session_state.consumers].sum(), errors='coerce').fillna(0)
        df.loc['Current ROB'] = pd.to_numeric(df.loc['Previous ROB'], errors='coerce').fillna(0) - total_consumption
        return df

    df = create_editable_dataframe()
    
    st.subheader("Fuel Consumption Data")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=f"fuel_consumption_editor_{uuid.uuid4()}"
    )

    st.session_state.consumption_data_fuel = edited_df.loc[st.session_state.consumers]
    st.session_state.previous_rob_fuel = edited_df.loc['Previous ROB']

def display_bdn_consumption_report():
    def create_editable_dataframe():
        index = ['BDN Number', 'Previous ROB'] + st.session_state.consumers + ['Current ROB']
        df = pd.DataFrame(index=index, columns=st.session_state.tanks)
        bdn_numbers = generate_random_bdn_numbers()
        df.loc['BDN Number'] = [bdn_numbers[i % 3] for i in range(len(st.session_state.tanks))]
        df.loc['Previous ROB'] = st.session_state.previous_rob_tank
        df.loc[st.session_state.consumers] = st.session_state.consumption_data_tank
        total_consumption = pd.to_numeric(df.loc[st.session_state.consumers].sum(), errors='coerce').fillna(0)
        df.loc['Current ROB'] = pd.to_numeric(df.loc['Previous ROB'], errors='coerce').fillna(0) - total_consumption
        return df

    df = create_editable_dataframe()
    
    st.subheader("BDN Based Fuel Consumption Data")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=f"bdn_consumption_editor_{uuid.uuid4()}"
    )

    st.session_state.consumption_data_tank = edited_df.loc[st.session_state.consumers]
    st.session_state.previous_rob_tank = edited_df.loc['Previous ROB']

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
    
    edited_additional_data = st.data_editor(
        additional_data,
        use_container_width=True,
        num_rows="dynamic",
        column_config=column_config,
        key=f"additional_consumption_editor_{uuid.uuid4()}"
    )

    return edited_additional_data

def display_flowmeter_method_report():
    def create_editable_dataframe():
        index = st.session_state.consumers
        flowmeter_columns = [
            "Flowmeter In", "Flowmeter Out", "Temp at flowmeter", 
            "Density @ 15°C", "Fuel Type", "Total Consumption (mT)"
        ]
        df = pd.DataFrame(0, index=index, columns=flowmeter_columns)
        fuel_types = ["LFO", "MGO", "HFO"]
        for consumer in st.session_state.consumers:
            row_data = [np.random.uniform(10, 50) for _ in range(len(flowmeter_columns) - 2)]
            row_data.append(random.choice(fuel_types))
            row_data.append(np.random.uniform(1, 10))
            df.loc[consumer] = row_data
        return df

    df = create_editable_dataframe()
    
    st.subheader("Flowmeter Method Fuel Consumption Data")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",
        key=f"flowmeter_consumption_editor_{uuid.uuid4()}"
    )

    st.session_state.consumption_data_flowmeter = edited_df

def display_tank_sounding_report():
    def create_editable_dataframe():
        index = ['Fuel Type', 'BDN Number', 'Previous ROB'] + st.session_state.consumers + ['Current ROB']
        tanks = [f'Tank {i}' for i in range(1, 9)]
        df = pd.DataFrame(index=index, columns=tanks)
        fuel_types = ["LFO", "MGO", "HFO"]
        df.loc['Fuel Type'] = [random.choice(fuel_types) for _ in tanks]
        bdn_numbers = generate_random_bdn_numbers()
        df.loc['BDN Number'] = [bdn_numbers[i % 3] for i in range(len(tanks))]
        df.loc['Previous ROB'] = [np.random.uniform(100, 1000) for _ in tanks]
        for consumer in st.session_state.consumers:
            df.loc[consumer] = [np.random.uniform(0, 50) for _ in tanks]
        consumption = df.loc[st.session_state.consumers].sum()
        df.loc['Current ROB'] = df.loc['Previous ROB'] - consumption
        return df

    df = create_editable_dataframe()
    
    st.subheader("Tank Sounding Method Fuel Consumption Data")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=f"tank_sounding_editor_{uuid.uuid4()}"
    )

    st.session_state.consumption_data_tank_sounding = edited_df.loc[st.session_state.consumers]
    st.session_state.previous_rob_tank_sounding = edited_df.loc['Previous ROB']

def display_ctms_method_report():
    def create_editable_dataframe():
        index = ['Previous ROB'] + st.session_state.consumers + ['Current ROB']
        columns = ['HFO', 'LFO', 'MGO/MDO']
        df = pd.DataFrame(0, index=index, columns=columns)
        df.loc['Previous ROB'] = [np.random.uniform(100, 1000) for _ in range(len(columns))]
        for consumer in st.session_state.consumers:
            df.loc[consumer] = [np.random.uniform(0, 50) for _ in range(len(columns))]
        df.loc['Current ROB'] = df.loc['Previous ROB'] - df.loc[st.session_state.consumers].sum()
        return df

    def create_ctms_specific_dataframe():
        index = ['CTMS qty (m3)', 'Cargo loaded (m3)', 'Cargo discharged (m3)', 'Density', 'N2 correction', 'Total LNG consumption (mT)']
        df = pd.DataFrame(0, index=index, columns=['Value'])
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

        st.session_state.consumption_data_ctms = edited_df.loc[st.session_state.consumers]
        st.session_state.previous_rob_ctms = edited_df.loc['Previous ROB']

    with col2:
        ctms_df = create_ctms_specific_dataframe()
        edited_ctms_df = st.data_editor(
            ctms_df,
            use_container_width=True,
            num_rows="fixed",
            key=f"ctms_specific_editor_{uuid.uuid4()}"
        )

        st.session_state.ctms_specific_data = edited_ctms_df

    return edited_df, edited_ctms_df

def display_bunkering_details():
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
        
        # Add tank selection
        entry['tanks'] = st.multiselect("Select Tanks", st.session_state.tanks, key=f"bunkering_tanks_{i}")
    if st.button("➕ Add Bunkering Entry"):
        st.session_state.bunkering_entries.append({})
        st.experimental_rerun()

def edit_tank_properties():
    st.write("Edit tank properties:")
    
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

    fuel_grade_options = ['VLSFO', 'MGO', 'HFO']
    
    tank_props = pd.DataFrame({
        'Fuel Grade': [random.choice(fuel_grade_options) for _ in range(8)],
        'Viscosity': [st.session_state.viscosity[f'Tank {i}'] for i in range(1, 9)],
        'Sulfur (%)': [st.session_state.sulfur[f'Tank {i}'] for i in range(1, 9)],
        'Bunkered qty(mT)': [0.0] * 8,  # New column
        'Current ROB': [np.random.uniform(50, 500) for _ in range(8)]
    }, index=[f'Tank {i}' for i in range(1, 9)])

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
        'Viscosity': st.column_config.NumberColumn(
            'Viscosity', min_value=20.0, max_value=100.0, step=0.1, format="%.1f"
        ),
        'Sulfur (%)': st.column_config.NumberColumn(
            'Sulfur (%)', min_value=0.05, max_value=0.49, step=0.01, format="%.2f"
        ),
        'Bunkered qty(mT)': st.column_config.NumberColumn(
            'Bunkered qty(mT)', min_value=0.0, step=0.1, format="%.1f"
        ),
        'Current ROB': st.column_config.NumberColumn(
            'Current ROB', min_value=0.0, step=0.1, format="%.1f"
        )
    }

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
    
    for i in range(1, 9):
        tank_name = f'Tank {i}'
        st.session_state.viscosity[tank_name] = edited_props.loc[tank_name, 'Viscosity']
        st.session_state.sulfur[tank_name] = edited_props.loc[tank_name, 'Sulfur (%)']
    
    if 'fuel_grades' not in st.session_state:
        st.session_state.fuel_grades = {}
    for tank_name, row in edited_props.iterrows():
        st.session_state.fuel_grades[tank_name] = row['Fuel Grade']

    if 'current_rob' not in st.session_state:
        st.session_state.current_rob = {}
    for tank_name, row in edited_props.iterrows():
        st.session_state.current_rob[tank_name] = row['Current ROB']

    if tank_transfer:
        transfers_from = edited_props['Qty (mT) Transferred From Tank']
        transfers_to = edited_props['Qty (mT) Transferred To Tank']
        
        if transfers_from.sum() != transfers_to.sum():
            st.warning("The total quantity transferred from tanks must equal the total quantity transferred to tanks.")
        else:
            st.success(f"Total quantity transferred: {transfers_from.sum()} mT")

    return edited_props

# Update the main function to include the new edit_tank_properties function
def main():
    initialize_session_state()

    st.title("Fuel Consumption Report")

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
    elif not fuel_type_view and not bdn_view and not flowmeter_method and not tank_sounding_method and not ctms_method:
        st.warning("Please select a view type.")
        st.stop()

    if fuel_type_view:
        display_fuel_consumption_report()
    elif bdn_view:
        display_bdn_consumption_report()
    elif flowmeter_method:
        display_flowmeter_method_report()
    elif tank_sounding_method:
        display_tank_sounding_report()
    elif ctms_method:
        display_ctms_method_report()
    
    display_additional_table(fuel_type_view)

    if st.checkbox("Edit Tank Properties"):
        edit_tank_properties()

    if st.button("Submit Report", type="primary"):
        st.success("Report submitted successfully!")

if __name__ == "__main__":
    main()
