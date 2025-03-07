import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for flowmeters if not exists
if 'flowmeters' not in st.session_state:
    st.session_state.flowmeters = []

def calculate_consumption(current_reading1, previous_reading1, current_reading2=0, previous_reading2=0):
    return (float(current_reading1) - float(previous_reading1)) - (float(current_reading2) - float(previous_reading2))

# App title
st.title('Vessel Flowmeter Configuration and Calculation')

# Sidebar for flowmeter management
with st.sidebar:
    st.header('Flowmeter Management')

    # Add new flowmeter
    new_flowmeter = st.text_input('Enter new flowmeter name')
    if st.button('Add Flowmeter'):
        if new_flowmeter and new_flowmeter not in st.session_state.flowmeters:
            st.session_state.flowmeters.append(new_flowmeter)
            st.success(f'Flowmeter {new_flowmeter} added successfully!')

    # Display existing flowmeters
    st.subheader('Existing Flowmeters')
    for fm in st.session_state.flowmeters:
        st.write(f"- {fm}")

# Main content
st.header('Consumption Calculations')

# Create tabs for different consumption types
tab1, tab2, tab3, tab4 = st.tabs(['ME Consumption', 'AE Consumption', 'BLR Consumption', 'Other Equipment'])

# ME Consumption Tab
with tab1:
    st.subheader('Main Engine Consumption')
    if len(st.session_state.flowmeters) > 0:
        selected_fm = st.selectbox('Select Flowmeter for ME', st.session_state.flowmeters, key='me_fm')
        col1, col2 = st.columns(2)
        with col1:
            current_reading = st.number_input('Current Reading', key='me_current')
        with col2:
            previous_reading = st.number_input('Previous Reading', key='me_previous')

        if st.button('Calculate ME Consumption'):
            consumption = calculate_consumption(current_reading, previous_reading)
            st.success(f'ME Consumption: {consumption:.2f} units')

# AE Consumption Tab
with tab2:
    st.subheader('Auxiliary Engine Consumption')
    if len(st.session_state.flowmeters) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            fm1 = st.selectbox('Select First Flowmeter', st.session_state.flowmeters, key='ae_fm1')
            current1 = st.number_input('Current Reading (FM1)', key='ae_current1')
            previous1 = st.number_input('Previous Reading (FM1)', key='ae_previous1')
        with col2:
            fm2 = st.selectbox('Select Second Flowmeter', st.session_state.flowmeters, key='ae_fm2')
            current2 = st.number_input('Current Reading (FM2)', key='ae_current2')
            previous2 = st.number_input('Previous Reading (FM2)', key='ae_previous2')

        if st.button('Calculate AE Consumption'):
            consumption = calculate_consumption(current1, previous1, current2, previous2)
            st.success(f'AE Consumption: {consumption:.2f} units')
    else:
        st.warning('Add at least 2 flowmeters to calculate AE consumption')

# BLR Consumption Tab
with tab3:
    st.subheader('Boiler Consumption')
    if len(st.session_state.flowmeters) > 0:
        selected_fm = st.selectbox('Select Flowmeter for BLR', st.session_state.flowmeters, key='blr_fm')
        col1, col2 = st.columns(2)
        with col1:
            current_reading = st.number_input('Current Reading', key='blr_current')
        with col2:
            previous_reading = st.number_input('Previous Reading', key='blr_previous')

        if st.button('Calculate BLR Consumption'):
            consumption = calculate_consumption(current_reading, previous_reading)
            st.success(f'BLR Consumption: {consumption:.2f} units')

# Other Equipment Tab
with tab4:
    st.subheader('Other Equipment Consumption')
    if len(st.session_state.flowmeters) > 0:
        selected_fm = st.selectbox('Select Flowmeter for Other Equipment', st.session_state.flowmeters, key='other_fm')
        col1, col2 = st.columns(2)
        with col1:
            current_reading = st.number_input('Current Reading', key='other_current')
        with col2:
            previous_reading = st.number_input('Previous Reading', key='other_previous')

        if st.button('Calculate Other Equipment Consumption'):
            consumption = calculate_consumption(current_reading, previous_reading)
            st.success(f'Other Equipment Consumption: {consumption:.2f} units')
