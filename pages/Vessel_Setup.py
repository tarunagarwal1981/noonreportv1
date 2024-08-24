import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Vessel Setup")

def initialize_session_state():
    if 'fuel_tanks' not in st.session_state:
        st.session_state.fuel_tanks = pd.DataFrame(columns=[
            "Tank Name", "Tank Capacity (100% m3)", "Current ROB (mT)", 
            "Fuel Grade", "BDN Number", "% Sulphur", "Viscosity"
        ])
    if 'lube_oil_tanks' not in st.session_state:
        st.session_state.lube_oil_tanks = pd.DataFrame(columns=[
            "Tank Name", "Tank Capacity (100% m3)", "Current ROB (mT)", 
            "Lube Oil Grade", "BN"
        ])
    if 'water_tanks' not in st.session_state:
        st.session_state.water_tanks = pd.DataFrame(columns=[
            "Tank Name", "Tank Capacity (100% m3)", "Current ROB (mT)", 
            "Water Type"
        ])

def add_tank(tank_type):
    if tank_type == "Fuel":
        new_tank = {
            "Tank Name": st.session_state.fuel_tank_name,
            "Tank Capacity (100% m3)": st.session_state.fuel_tank_capacity,
            "Current ROB (mT)": st.session_state.fuel_current_rob,
            "Fuel Grade": st.session_state.fuel_grade,
            "BDN Number": st.session_state.fuel_bdn_number,
            "% Sulphur": st.session_state.fuel_sulphur,
            "Viscosity": st.session_state.fuel_viscosity
        }
        st.session_state.fuel_tanks = pd.concat([st.session_state.fuel_tanks, pd.DataFrame([new_tank])], ignore_index=True)
    elif tank_type == "Lube Oil":
        new_tank = {
            "Tank Name": st.session_state.lube_tank_name,
            "Tank Capacity (100% m3)": st.session_state.lube_tank_capacity,
            "Current ROB (mT)": st.session_state.lube_current_rob,
            "Lube Oil Grade": st.session_state.lube_grade,
            "BN": st.session_state.lube_bn
        }
        st.session_state.lube_oil_tanks = pd.concat([st.session_state.lube_oil_tanks, pd.DataFrame([new_tank])], ignore_index=True)
    elif tank_type == "Water":
        new_tank = {
            "Tank Name": st.session_state.water_tank_name,
            "Tank Capacity (100% m3)": st.session_state.water_tank_capacity,
            "Current ROB (mT)": st.session_state.water_current_rob,
            "Water Type": st.session_state.water_type
        }
        st.session_state.water_tanks = pd.concat([st.session_state.water_tanks, pd.DataFrame([new_tank])], ignore_index=True)

def main():
    st.title("Vessel Setup")
    initialize_session_state()

    # Fuel Tank Allocation
    st.header("Fuel Tank Allocation")
    st.dataframe(st.session_state.fuel_tanks)
    
    with st.expander("Add New Fuel Tank"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Tank Name", key="fuel_tank_name")
            st.number_input("Tank Capacity (100% m3)", min_value=0.0, key="fuel_tank_capacity")
            st.number_input("Current ROB (mT)", min_value=0.0, key="fuel_current_rob")
            st.text_input("Fuel Grade", key="fuel_grade")
        with col2:
            st.text_input("BDN Number", key="fuel_bdn_number")
            st.number_input("% Sulphur", min_value=0.0, max_value=100.0, key="fuel_sulphur")
            st.number_input("Viscosity", min_value=0.0, key="fuel_viscosity")
        if st.button("Add Fuel Tank"):
            add_tank("Fuel")
            st.success("Fuel tank added successfully!")

    # Lube Oil Tank Allocation
    st.header("Lube Oil Tank Allocation")
    st.dataframe(st.session_state.lube_oil_tanks)
    
    with st.expander("Add New Lube Oil Tank"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Tank Name", key="lube_tank_name")
            st.number_input("Tank Capacity (100% m3)", min_value=0.0, key="lube_tank_capacity")
            st.number_input("Current ROB (mT)", min_value=0.0, key="lube_current_rob")
        with col2:
            st.text_input("Lube Oil Grade", key="lube_grade")
            st.number_input("BN", min_value=0, key="lube_bn")
        if st.button("Add Lube Oil Tank"):
            add_tank("Lube Oil")
            st.success("Lube oil tank added successfully!")

    # Fresh Water/Distilled Water Tank Allocation
    st.header("Fresh Water/Distilled Water Tank Allocation")
    st.dataframe(st.session_state.water_tanks)
    
    with st.expander("Add New Water Tank"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Tank Name", key="water_tank_name")
            st.number_input("Tank Capacity (100% m3)", min_value=0.0, key="water_tank_capacity")
        with col2:
            st.number_input("Current ROB (mT)", min_value=0.0, key="water_current_rob")
            st.selectbox("Water Type", ["Fresh Water", "Distilled Water"], key="water_type")
        if st.button("Add Water Tank"):
            add_tank("Water")
            st.success("Water tank added successfully!")

    # Download buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        csv_fuel = st.session_state.fuel_tanks.to_csv(index=False)
        st.download_button(
            label="Download Fuel Tanks CSV",
            data=csv_fuel,
            file_name="fuel_tanks.csv",
            mime="text/csv",
        )
    with col2:
        csv_lube = st.session_state.lube_oil_tanks.to_csv(index=False)
        st.download_button(
            label="Download Lube Oil Tanks CSV",
            data=csv_lube,
            file_name="lube_oil_tanks.csv",
            mime="text/csv",
        )
    with col3:
        csv_water = st.session_state.water_tanks.to_csv(index=False)
        st.download_button(
            label="Download Water Tanks CSV",
            data=csv_water,
            file_name="water_tanks.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
