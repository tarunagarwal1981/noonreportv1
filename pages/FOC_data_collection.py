import streamlit as st
import pandas as pd
import numpy as np
import uuid

st.set_page_config(layout="wide", page_title="Fuel Consumption Report")

def main():
    if 'consumers' not in st.session_state:
        st.session_state.consumers = [
            'Main Engine', 'Aux Engine1', 'Aux Engine2', 'Aux Engine3',
            'Boiler 1',
            '    Boiler 1 - Cargo Heating',
            '    Boiler 1 - Discharge',
            'Boiler 2',
            '    Boiler 2 - Cargo Heating',
            '    Boiler 2 - Discharge',
            'IGG', 'Incinerator',
            'DPP1', 'DPP2', 'DPP3'
        ]
    if 'fuel_types' not in st.session_state:
        st.session_state.fuel_types = ['HFO', 'LFO', 'MGO/MDO', 'LPG', 'LNG', 'Methanol', 'Ethanol', 'Others']
    if 'consumption_data' not in st.session_state:
        st.session_state.consumption_data = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.fuel_types + ['Other Fuel Type'])
    if 'viscosity' not in st.session_state:
        st.session_state.viscosity = {fuel: np.random.uniform(20, 100) for fuel in st.session_state.fuel_types}
    if 'sulfur' not in st.session_state:
        st.session_state.sulfur = {fuel: np.random.uniform(0.05, 0.49) for fuel in st.session_state.fuel_types}
    if 'previous_rob' not in st.session_state:
        st.session_state.previous_rob = pd.Series({fuel: np.random.uniform(100, 1000) for fuel in st.session_state.fuel_types + ['Other Fuel Type']})
    if 'bunker_survey_correction' not in st.session_state:
        st.session_state.bunker_survey_correction = pd.Series({fuel: 0 for fuel in st.session_state.fuel_types + ['Other Fuel Type']})
    if 'bunker_survey_comments' not in st.session_state:
        st.session_state.bunker_survey_comments = ""

    st.title('Fuel Consumption Report')

    # Add bunker survey checkbox
    bunker_survey = st.checkbox("Bunker Survey")

    # Add comment box right after the checkbox
    if bunker_survey:
        st.session_state.bunker_survey_comments = st.text_area(
            "Bunker Survey Comments",
            value=st.session_state.bunker_survey_comments,
            height=100
        )

    def format_column_header(fuel):
        if fuel == 'Other Fuel Type':
            return fuel
        return f"{fuel}\nVisc: {st.session_state.viscosity[fuel]:.1f}\nSulfur: {st.session_state.sulfur[fuel]:.2f}%"

    def create_editable_dataframe():
        index = ['Previous ROB'] + st.session_state.consumers
        if bunker_survey:
            index.append('Bunker Survey Correction')
        index.append('Current ROB')
        df = pd.DataFrame(index=index, columns=st.session_state.fuel_types + ['Other Fuel Type'])
        df.loc['Previous ROB'] = st.session_state.previous_rob
        df.loc[st.session_state.consumers] = st.session_state.consumption_data
        if bunker_survey:
            df.loc['Bunker Survey Correction'] = st.session_state.bunker_survey_correction
        total_consumption = df.loc[st.session_state.consumers].sum()
        df.loc['Current ROB'] = df.loc['Previous ROB'] - total_consumption
        if bunker_survey:
            df.loc['Current ROB'] += df.loc['Bunker Survey Correction']
        df.columns = [format_column_header(fuel) for fuel in st.session_state.fuel_types + ['Other Fuel Type']]
        return df

    df = create_editable_dataframe()

    st.subheader("Fuel Consumption Data")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Other Fuel Type": st.column_config.TextColumn(
                "Other Fuel Type",
                help="Specify the type of other fuel used",
                max_chars=50,
            )
        },
        key=f"fuel_consumption_editor_{uuid.uuid4()}"
    )

    # Update session state with edited values
    st.session_state.consumption_data = edited_df.loc[st.session_state.consumers, st.session_state.fuel_types + ['Other Fuel Type']]
    st.session_state.previous_rob = edited_df.loc['Previous ROB']
    if bunker_survey:
        st.session_state.bunker_survey_correction = edited_df.loc['Bunker Survey Correction']

    def display_additional_table():
        st.subheader("Additional Consumption Data")
        additional_data = pd.DataFrame({
            'Work': [0, 0, 0, 0],
            'SFOC': [0, 0, 0, ''],
            'Fuel Type': ['', '', '', '']
        }, index=['Reefer container', 'Cargo cooling', 'Heating/Discharge pump', 'Shore-Side Electricity'])
        
        edited_additional_data = st.data_editor(
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
                "Fuel Type": st.column_config.SelectboxColumn(
                    "Fuel Type",
                    help="Select the fuel type",
                    options=st.session_state.fuel_types + ['Other']
                )
            },
            key=f"additional_consumption_editor_{uuid.uuid4()}"
        )

    display_additional_table()

    def edit_fuel_properties():
        st.subheader("Edit Fuel Properties")
        fuel_props = pd.DataFrame({
            'Viscosity': st.session_state.viscosity,
            'Sulfur (%)': st.session_state.sulfur
        })
        edited_props = st.data_editor(
            fuel_props,
            use_container_width=True,
            column_config={
                'Viscosity': st.column_config.NumberColumn(
                    'Viscosity', min_value=20.0, max_value=100.0, step=0.1, format="%.1f"
                ),
                'Sulfur (%)': st.column_config.NumberColumn(
                    'Sulfur (%)', min_value=0.05, max_value=0.49, step=0.01, format="%.2f"
                )
            },
            key=f"fuel_properties_editor_{uuid.uuid4()}"
        )
        st.session_state.viscosity = edited_props['Viscosity'].to_dict()
        st.session_state.sulfur = edited_props['Sulfur (%)'].to_dict()

    if st.checkbox("Edit Fuel Properties"):
        edit_fuel_properties()

    if st.button("Submit Report", type="primary"):
        st.success("Fuel consumption report submitted successfully!")

if __name__ == "__main__":
    main()
