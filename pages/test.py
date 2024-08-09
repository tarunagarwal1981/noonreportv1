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
    st.session_state.viscosity = {tank: 0.0 for tank in st.session_state.tanks}
if 'sulfur' not in st.session_state:
    st.session_state.sulfur = {tank: 0.0 for tank in st.session_state.tanks}

st.title('Fuel Consumption and Property Tracker')

# Function to create an editable dataframe
def create_editable_dataframe():
    df = st.session_state.consumption_data.copy()
    viscosity_row = pd.Series(st.session_state.viscosity, name='Viscosity')
    sulfur_row = pd.Series(st.session_state.sulfur, name='Sulfur (%)')
    df = pd.concat([viscosity_row.to_frame().T, sulfur_row.to_frame().T, df])
    
    return df

# Create the editable dataframe
df = create_editable_dataframe()

# Display the editable table
st.write("Edit the table below:")
edited_df = st.data_editor(
    df,
    use_container_width=True,
    hide_index=False,
    column_config={
        tank: st.column_config.NumberColumn(
            tank,
            help=f"Enter data for {tank}",
            min_value=0,
            max_value=1000,
            step=0.1,
            format="%.1f"
        ) for tank in st.session_state.tanks
    }
)

# Update session state with edited values
st.session_state.viscosity = edited_df.iloc[0].to_dict()
st.session_state.sulfur = edited_df.iloc[1].to_dict()
st.session_state.consumption_data = edited_df.iloc[2:]

# Calculate and display total consumption
total_consumption = st.session_state.consumption_data.sum().sum()
st.metric('Total Fuel Consumed', f'{total_consumption:.2f} units')

# Footer
st.markdown('---')
st.markdown('Fuel Consumption and Property Tracker - Designed by Claude')
