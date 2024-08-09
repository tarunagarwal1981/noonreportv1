import streamlit as st
import pandas as pd
import numpy as np

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
    st.session_state.viscosity = {tank: 0.0 for tank in st.session_state.tanks}
if 'sulfur' not in st.session_state:
    st.session_state.sulfur = {tank: 0.0 for tank in st.session_state.tanks}

st.title('Fuel Consumption and Property Tracker')

# Function to create an editable dataframe
def create_editable_dataframe():
    df = st.session_state.consumption_data.copy()
    for consumer in st.session_state.consumers:
        for tank in st.session_state.tanks:
            df.at[consumer, tank] = st.number_input(
                f'{consumer} - {tank}',
                value=float(df.at[consumer, tank]),
                key=f'input_{consumer}_{tank}',
                step=0.1
            )
    return df

# Main content
st.header('Fuel Consumption Data')

# Create tabs for data entry and table view
tab1, tab2 = st.tabs(['Data Entry', 'Table View'])

with tab1:
    st.subheader('Enter Consumption Data')
    st.session_state.consumption_data = create_editable_dataframe()
    
    st.subheader('Enter Fuel Properties')
    cols = st.columns(4)
    for i, tank in enumerate(st.session_state.tanks):
        with cols[i % 4]:
            st.session_state.viscosity[tank] = st.number_input(
                f'{tank} Viscosity',
                value=st.session_state.viscosity[tank],
                key=f'viscosity_{tank}',
                step=0.1
            )
            st.session_state.sulfur[tank] = st.number_input(
                f'{tank} Sulfur (%)',
                value=st.session_state.sulfur[tank],
                key=f'sulfur_{tank}',
                min_value=0.0,
                max_value=100.0,
                step=0.01
            )

    if st.button('Save Data'):
        st.success('Data saved successfully!')

with tab2:
    st.subheader('Fuel Consumption and Property Table')
    
    # Create the table header
    header = ['Consumer'] + [f'{tank}\nViscosity: {st.session_state.viscosity[tank]:.1f}\nSulfur: {st.session_state.sulfur[tank]:.2f}%' for tank in st.session_state.tanks]
    
    # Create the table data
    table_data = [header]
    for consumer in st.session_state.consumers:
        row = [consumer] + [f'{st.session_state.consumption_data.at[consumer, tank]:.1f}' for tank in st.session_state.tanks]
        table_data.append(row)
    
    # Display the table
    df = pd.DataFrame(table_data[1:], columns=table_data[0])
    st.dataframe(df.style.set_properties(**{'text-align': 'center'}))

# Display total consumption
total_consumption = st.session_state.consumption_data.sum().sum()
st.metric('Total Fuel Consumed', f'{total_consumption:.2f} units')

# Footer
st.markdown('---')
st.markdown('Fuel Consumption and Property Tracker - Designed by Claude')
