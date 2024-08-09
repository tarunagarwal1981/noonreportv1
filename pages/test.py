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
            'Boiler 1', 'Boiler 2', 'IGG', 'Incinerator'
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
    if 'bunkering_entries' not in st.session_state:
        st.session_state.bunkering_entries = [{}]

    st.title('Fuel Consumption Tracker')

    # Function to create a formatted column header
    def format_column_header(tank):
        return f"{tank}\nVisc: {st.session_state.viscosity[tank]:.1f}\nSulfur: {st.session_state.sulfur[tank]:.2f}%"

    # Function to create an editable dataframe
    def create_editable_dataframe():
        df = pd.DataFrame(index=['Previous ROB'] + st.session_state.consumers + ['Current ROB'], columns=st.session_state.tanks)
        df.loc['Previous ROB'] = st.session_state.previous_rob
        df.loc[st.session_state.consumers] = st.session_state.consumption_data
        
        # Calculate Current ROB
        total_consumption = df.loc[st.session_state.consumers].sum()
        df.loc['Current ROB'] = df.loc['Previous ROB'] - total_consumption
        
        # Format column headers
        df.columns = [format_column_header(tank) for tank in st.session_state.tanks]
        return df

    # Create the editable dataframe
    df = create_editable_dataframe()

    # Display the editable table
    st.write("Edit the consumption data below:")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        disabled=['Current ROB'],
        column_config={
            column: st.column_config.NumberColumn(
                column,
                help=f"Enter data for {column.split()[0]} {column.split()[1]}",
                min_value=0,
                max_value=1000,
                step=0.1,
                format="%.1f"
            ) for column in df.columns
        }
    )

    # Update session state with edited values
    st.session_state.previous_rob = edited_df.loc['Previous ROB']
    st.session_state.consumption_data = edited_df.loc[st.session_state.consumers]

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

    # Bunkering section
    bunkering_happened = st.checkbox("Bunkering Happened")
    if bunkering_happened:
        st.markdown("<h4 style='font-size: 16px;'>Bunkering Details</h4>", unsafe_allow_html=True)
        
        # Display each bunkering entry without using expander
        for i, entry in enumerate(st.session_state.bunkering_entries):
            st.markdown(f"**Bunkering Entry {i+1}**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                entry['grade'] = st.selectbox("Grade of Fuel Bunkered", 
                                              ["VLSFO", "HFO", "MGO", "LSMGO", "LNG"], 
                                              key=f"grade_{i}")
                entry['grade_bdn'] = st.text_input("Grade as per BDN", key=f"grade_bdn_{i}")
            with col2:
                entry['qty_bdn'] = st.number_input("Quantity as per BDN (mt)", 
                                                   min_value=0.0, step=0.1, key=f"qty_bdn_{i}")
                entry['density'] = st.number_input("Density (kg/m³)", 
                                                   min_value=0.0, step=0.1, key=f"density_{i}")
            with col3:
                entry['viscosity'] = st.number_input("Viscosity (cSt)", 
                                                     min_value=0.0, step=0.1, key=f"viscosity_{i}")
                entry['lcv'] = st.number_input("LCV (MJ/kg)", 
                                               min_value=0.0, step=0.1, key=f"lcv_{i}")
            with col4:
                entry['bdn_file'] = st.file_uploader("Upload BDN", 
                                                     type=['pdf', 'jpg', 'png'], 
                                                     key=f"bdn_file_{i}")
        # Button to add new bunkering entry
        if st.button("➕ Add Bunkering Entry"):
            st.session_state.bunkering_entries.append({})
            st.experimental_rerun()

    # Footer
    st.markdown('---')
    st.markdown('Fuel Consumption Tracker - Designed by Claude')

# Example usage:
if __name__ == "__main__":
    display_fuel_consumption()
