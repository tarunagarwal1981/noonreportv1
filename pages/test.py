import streamlit as st
import pandas as pd
import numpy as np

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
    cols = st.columns(len(st.session_state.tanks))
    for i, tank in enumerate(st.session_state.tanks):
        with cols[i]:
            st.session_state.viscosity[tank] = st.number_input(
                f"{tank} Viscosity",
                min_value=20.0,
                max_value=100.0,
                value=st.session_state.viscosity[tank],
                step=0.1,
                key=f"visc_{tank}"
            )
            st.session_state.sulfur[tank] = st.number_input(
                f"{tank} Sulfur (%)",
                min_value=0.05,
                max_value=0.49,
                value=st.session_state.sulfur[tank],
                step=0.01,
                format="%.2f",
                key=f"sulfur_{tank}"
            )

# Add a section to edit tank properties
if st.checkbox("Edit Tank Properties"):
    edit_tank_properties()

# Calculate and display total consumption
total_consumption = st.session_state.consumption_data.sum().sum()
st.metric('Total Fuel Consumed', f'{total_consumption:.2f} units')

# Footer
st.markdown('---')
st.markdown('Fuel Consumption Tracker - Designed by Claude')
