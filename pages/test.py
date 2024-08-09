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

    # ... (previous code for fuel consumption table remains unchanged)

    # Bunkering section
    bunkering_happened = st.checkbox("Bunkering Happened")
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
                entry['qty_bdn'] = st.number_input("Total Quantity as per BDN (mt)", 
                                                   min_value=0.0, step=0.1, key=f"qty_bdn_{i}")
            with col2:
                entry['density'] = st.number_input("Density (kg/m³)", 
                                                   min_value=0.0, step=0.1, key=f"density_{i}")
                entry['viscosity'] = st.number_input("Viscosity (cSt)", 
                                                     min_value=0.0, step=0.1, key=f"viscosity_{i}")
                entry['lcv'] = st.number_input("LCV (MJ/kg)", 
                                               min_value=0.0, step=0.1, key=f"lcv_{i}")
            with col3:
                entry['bdn_file'] = st.file_uploader("Upload BDN", 
                                                     type=['pdf', 'jpg', 'png'], 
                                                     key=f"bdn_file_{i}")

            # Tank allocation section
            st.markdown("<h6 style='font-size: 14px;'>Allocate Bunkered Fuel to Tanks</h6>", unsafe_allow_html=True)
            if 'tank_allocation' not in entry:
                entry['tank_allocation'] = []

            # Display current allocations
            total_allocated = sum(alloc['quantity'] for alloc in entry['tank_allocation'])
            remaining_to_allocate = entry['qty_bdn'] - total_allocated

            if entry['tank_allocation']:
                st.markdown("**Current Allocations:**")
                for alloc in entry['tank_allocation']:
                    st.markdown(f"- {alloc['tank']}: {alloc['quantity']:.2f} mt")
                st.markdown(f"**Remaining to allocate: {remaining_to_allocate:.2f} mt**")

            # New allocation input
            if remaining_to_allocate > 0:
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_tank = st.selectbox("Select Tank", 
                                            [tank for tank in st.session_state.tanks if tank not in [alloc['tank'] for alloc in entry['tank_allocation']]], 
                                            key=f"new_tank_{i}")
                with col2:
                    new_quantity = st.number_input("Quantity (mt)", 
                                                   min_value=0.0, 
                                                   max_value=remaining_to_allocate, 
                                                   step=0.1, 
                                                   key=f"new_quantity_{i}")
                with col3:
                    if st.button("Add Allocation", key=f"add_allocation_{i}"):
                        entry['tank_allocation'].append({'tank': new_tank, 'quantity': new_quantity})
                        st.experimental_rerun()

            # Option to clear allocations
            if entry['tank_allocation'] and st.button("Clear All Allocations", key=f"clear_allocations_{i}"):
                entry['tank_allocation'] = []
                st.experimental_rerun()

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
