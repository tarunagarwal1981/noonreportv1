import streamlit as st
import pandas as pd
import numpy as np

def display_fuel_consumption():
    # Set page to wide mode
    st.set_page_config(layout="wide")

    # Initialize session state variables
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
    if 'tanks' not in st.session_state:
        st.session_state.tanks = [f'Tank {i}' for i in range(1, 9)]
    if 'consumption_data' not in st.session_state:
        st.session_state.consumption_data = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.tanks)
    if 'viscosity' not in st.session_state:
        st.session_state.viscosity = {tank: np.random.uniform(20, 100) for tank in st.session_state.tanks}
    if 'sulfur' not in st.session_state:
        st.session_state.sulfur = {tank: np.random.uniform(0.05, 0.49) for tank in st.session_state.tanks}
    if 'previous_rob' not in st.session_state:
        st.session_state.previous_rob = pd.Series({tank: np.random.uniform(100, 1000) for tank in st.session_state.tanks})
    if 'bunkered_qty' not in st.session_state:
        st.session_state.bunkered_qty = pd.Series({tank: 0 for tank in st.session_state.tanks})
    if 'bunkering_entries' not in st.session_state:
        st.session_state.bunkering_entries = []

    st.title('Fuel Consumption Tracker')

    # Bunkering checkbox at the top
    bunkering_happened = st.checkbox("Bunkering Happened")

    # Bunkering details section
    if bunkering_happened:
        st.markdown("<h4 style='font-size: 18px;'>Bunkering Details</h4>", unsafe_allow_html=True)
        
        # Display each bunkering entry
        for i, entry in enumerate(st.session_state.bunkering_entries):
            st.markdown(f"<h5 style='font-size: 16px;'>Bunkering Entry {i+1}</h5>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                entry['grade'] = st.selectbox("Grade of Fuel Bunkered", 
                                              ["VLSFO", "HFO", "MGO", "LSMGO", "LNG"], 
                                              key=f"grade_{i}")
                entry['grade_bdn'] = st.text_input("Grade as per BDN", key=f"grade_bdn_{i}")
                entry['total_qty'] = st.number_input("Total Quantity Bunkered (mt)", 
                                                     min_value=0.0, step=0.1, key=f"total_qty_{i}")
            with col2:
                entry['density'] = st.number_input("Density (kg/m³)", 
                                                   min_value=0.0, step=0.1, key=f"density_{i}")
                entry['viscosity'] = st.number_input("Viscosity (cSt)", 
                                                     min_value=0.0, step=0.1, key=f"viscosity_{i}")
            with col3:
                entry['lcv'] = st.number_input("LCV (MJ/kg)", 
                                               min_value=0.0, step=0.1, key=f"lcv_{i}")
                entry['bdn_file'] = st.file_uploader("Upload BDN", 
                                                     type=['pdf', 'jpg', 'png'], 
                                                     key=f"bdn_file_{i}")

        # Button to add new bunkering entry
        if st.button("➕ Add Bunkering Entry"):
            st.session_state.bunkering_entries.append({})
            st.experimental_rerun()

    # Function to create a formatted column header
    def format_column_header(tank):
        return f"{tank}\nVisc: {st.session_state.viscosity[tank]:.1f}\nSulfur: {st.session_state.sulfur[tank]:.2f}%"

    # Function to create an editable dataframe
    def create_editable_dataframe():
        index = ['Previous ROB'] + st.session_state.consumers
        if bunkering_happened:
            index += ['Bunkered Qty']
        index += ['Current ROB']
        
        df = pd.DataFrame(index=index, columns=st.session_state.tanks)
        df.loc['Previous ROB'] = st.session_state.previous_rob
        df.loc[st.session_state.consumers] = st.session_state.consumption_data
        if bunkering_happened:
            total_bunkered = sum(entry.get('total_qty', 0) for entry in st.session_state.bunkering_entries)
            df.loc['Bunkered Qty'] = [total_bunkered] + [0] * (len(st.session_state.tanks) - 1)
        
        # Calculate Current ROB
        total_consumption = df.loc[st.session_state.consumers].sum()
        df.loc['Current ROB'] = df.loc['Previous ROB'] - total_consumption
        if bunkering_happened:
            df.loc['Current ROB'] += df.loc['Bunkered Qty']
        
        # Format column headers
        df.columns = [format_column_header(tank) for tank in st.session_state.tanks]
        return df

    # Create the editable dataframe
    df = create_editable_dataframe()

    # Display the editable table
    st.write("Fuel Consumption Data:")
    
    # Custom CSS to style the dataframe
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

    # Convert dataframe to HTML and apply custom styling
    df_html = df.to_html(classes='dataframe', escape=False)
    df_html = df_html.replace('<th>', '<th style="text-align: center;">')
    
    italic_rows = ['Boiler 1', 'Boiler 2', 'DPP1', 'DPP2', 'DPP3']
    for consumer in st.session_state.consumers:
        if consumer.startswith('    '):
            df_html = df_html.replace(f'<td>{consumer}</td>', f'<td class="boiler-subsection">{consumer.strip()}</td>')
        elif consumer in italic_rows:
            df_html = df_html.replace(f'<td>{consumer}</td>', f'<td class="italic-row">{consumer}</td>')

    # Display the styled dataframe
    st.markdown(df_html, unsafe_allow_html=True)

    # Function to create and display the additional table
    def display_additional_table():
        st.write("Additional Consumption Data:")
        
        # Create the dataframe for the additional table
        additional_data = pd.DataFrame({
            'Work': [0, 0, 0, 0],
            'SFOC': [0, 0, 0, ''],
            'Tank Name': ['', '', '', '']
        }, index=['Reefer container', 'Cargo cooling', 'Heating/Discharge pump', 'Shore-Side Electricity'])
        
        # Custom CSS for the additional table
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
        
        # Convert dataframe to HTML and apply custom styling
        table_html = additional_data.to_html(classes='additional-table', escape=False)
        table_html = table_html.replace('<td></td>', '<td>-</td>')  # Replace empty cells with '-'
        table_html = table_html.replace('<td>Shore-Side Electricity</td><td>0</td><td></td><td></td>', 
                                        '<td>Shore-Side Electricity</td><td>0</td><td class="grey-out">-</td><td class="grey-out">-</td>')
        
        # Display the styled table
        st.markdown(table_html, unsafe_allow_html=True)

    # Display the additional table
    display_additional_table()

    # Function to edit tank properties
    def edit_tank_properties():
        st.write("Edit tank properties:")
        
        # Create a dataframe for tank properties
        tank_props = pd.DataFrame({
            'Viscosity': st.session_state.viscosity,
            'Sulfur (%)': st.session_state.sulfur
        })
        
        # Display editable dataframe for tank properties
        edited_props = st.data_editor(
            tank_props,
            use_container_width=True,
            column_config={
                'Viscosity': st.column_config.NumberColumn(
                    'Viscosity',
                    min_value=20.0,
                    max_value=100.0,
                    step=0.1,
                    format="%.1f"
                ),
                'Sulfur (%)': st.column_config.NumberColumn(
                    'Sulfur (%)',
                    min_value=0.05,
                    max_value=0.49,
                    step=0.01,
                    format="%.2f"
                )
            }
        )
        
        # Update session state with edited values
        st.session_state.viscosity = edited_props['Viscosity'].to_dict()
        st.session_state.sulfur = edited_props['Sulfur (%)'].to_dict()

    # Add a section to edit tank properties
    if st.checkbox("Edit Tank Properties"):
        edit_tank_properties()

    # Calculate and display total consumption
    total_consumption = st.session_state.consumption_data.sum().sum()
    st.metric('Total Fuel Consumed', f'{total_consumption:.2f} units')

    # Footer
    st.markdown('---')
    st.markdown('Fuel Consumption Tracker - Designed by Claude')

# Run the Streamlit app
if __name__ == "__main__":
    display_fuel_consumption()
