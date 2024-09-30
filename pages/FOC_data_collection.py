import streamlit as st
import pandas as pd
import numpy as np
import uuid

def display_fuel_consumption():
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
        st.session_state.consumption_data = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.fuel_types)
    if 'viscosity' not in st.session_state:
        st.session_state.viscosity = {fuel: np.random.uniform(20, 100) for fuel in st.session_state.fuel_types}
    if 'sulfur' not in st.session_state:
        st.session_state.sulfur = {fuel: np.random.uniform(0.05, 0.49) for fuel in st.session_state.fuel_types}
    if 'previous_rob' not in st.session_state:
        st.session_state.previous_rob = pd.Series({fuel: np.random.uniform(100, 1000) for fuel in st.session_state.fuel_types})
    if 'bunker_survey_correction' not in st.session_state:
        st.session_state.bunker_survey_correction = pd.Series({fuel: 0 for fuel in st.session_state.fuel_types})
    if 'bunker_survey_comments' not in st.session_state:
        st.session_state.bunker_survey_comments = ""
    if 'other_fuel_type' not in st.session_state:
        st.session_state.other_fuel_type = ""

    st.title('Fuel Consumption Tracker')

    # Add bunker survey checkbox
    bunker_survey = st.checkbox("Bunker Survey")

    # Add comment box right after the checkbox
    if bunker_survey:
        st.session_state.bunker_survey_comments = st.text_area(
            "Bunker Survey Comments",
            value=st.session_state.bunker_survey_comments,
            height=100
        )

    # Input for 'Other' fuel type
    st.session_state.other_fuel_type = st.text_input("Specify 'Other' fuel type", value=st.session_state.other_fuel_type)

    def format_column_header(fuel):
        return f"{fuel}\nVisc: {st.session_state.viscosity[fuel]:.1f}\nSulfur: {st.session_state.sulfur[fuel]:.2f}%"

    def create_editable_dataframe():
        index = ['Previous ROB'] + st.session_state.consumers
        if bunker_survey:
            index.append('Bunker Survey Correction')
        index.append('Current ROB')
        df = pd.DataFrame(index=index, columns=st.session_state.fuel_types)
        df.loc['Previous ROB'] = st.session_state.previous_rob
        df.loc[st.session_state.consumers] = st.session_state.consumption_data
        if bunker_survey:
            df.loc['Bunker Survey Correction'] = st.session_state.bunker_survey_correction
        total_consumption = df.loc[st.session_state.consumers].sum()
        df.loc['Current ROB'] = df.loc['Previous ROB'] - total_consumption
        if bunker_survey:
            df.loc['Current ROB'] += df.loc['Bunker Survey Correction']
        df.columns = [format_column_header(fuel) for fuel in st.session_state.fuel_types]
        return df

    df = create_editable_dataframe()

    st.write("Fuel Consumption Data:")
    custom_css = """
    <style>
        .dataframe td:first-child {
            font-weight: bold;
        }
        .dataframe td.italic-row {
            font-style: italic;
        }
        .dataframe td.boiler-subsection {
            padding-left: 30px !important;
            font-style: italic;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    df_html = df.to_html(classes='dataframe', escape=False)
    df_html = df_html.replace('<th>', '<th style="text-align: center;">')
    italic_rows = ['Boiler 1', 'Boiler 2', 'DPP1', 'DPP2', 'DPP3']
    for consumer in st.session_state.consumers:
        if consumer.startswith('    '):
            df_html = df_html.replace(f'<td>{consumer}</td>', f'<td class="boiler-subsection">{consumer.strip()}</td>')
        elif consumer in italic_rows:
            df_html = df_html.replace(f'<td>{consumer}</td>', f'<td class="italic-row">{consumer}</td>')
    st.markdown(df_html, unsafe_allow_html=True)

    def display_additional_table():
        st.write("Additional Consumption Data:")
        additional_data = pd.DataFrame({
            'Work': [0, 0, 0, 0],
            'SFOC': [0, 0, 0, ''],
            'Fuel Type': ['', '', '', '']
        }, index=['Reefer container', 'Cargo cooling', 'Heating/Discharge pump', 'Shore-Side Electricity'])
        custom_css = """
        <style>
            .additional-table th {
                text-align: center !important;
            }
            .additional-table td {
                text-align: center !important;
            }
            .grey-out {
                background-color: #f0f0f0 !important;
                color: #888 !important;
            }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
        table_html = additional_data.to_html(classes='additional-table', escape=False)
        table_html = table_html.replace('<td></td>', '<td>-</td>')
        table_html = table_html.replace('<td>Shore-Side Electricity</td><td>0</td><td></td><td></td>', 
                                        '<td>Shore-Side Electricity</td><td>0</td><td class="grey-out">-</td><td class="grey-out">-</td>')
        st.markdown(table_html, unsafe_allow_html=True)

    display_additional_table()

    def edit_fuel_properties():
        st.write("Edit fuel properties:")
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
            }
        )
        st.session_state.viscosity = edited_props['Viscosity'].to_dict()
        st.session_state.sulfur = edited_props['Sulfur (%)'].to_dict()

    if st.checkbox("Edit Fuel Properties"):
        edit_fuel_properties()

# You can call this function in your main app
# display_fuel_consumption()
