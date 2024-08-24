import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

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

def create_editable_grid(df, key):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, resizable=True)
    gb.configure_column("Tank Name", header_name="Tank Name")
    gb.configure_column("Tank Capacity (100% m3)", header_name="Tank Capacity (100% m3)", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2)
    gb.configure_column("Current ROB (mT)", header_name="Current ROB (mT)", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2)
    
    if "Fuel Grade" in df.columns:
        gb.configure_column("Fuel Grade", header_name="Fuel Grade")
        gb.configure_column("BDN Number", header_name="BDN Number")
        gb.configure_column("% Sulphur", header_name="% Sulphur", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=4)
        gb.configure_column("Viscosity", header_name="Viscosity", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2)
    elif "Lube Oil Grade" in df.columns:
        gb.configure_column("Lube Oil Grade", header_name="Lube Oil Grade")
        gb.configure_column("BN", header_name="BN", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1)
    elif "Water Type" in df.columns:
        gb.configure_column("Water Type", header_name="Water Type")
    
    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()
    
    return AgGrid(
        df,
        gridOptions=gridOptions,
        height=300,
        width='100%',
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=False,
        allow_unsafe_jscode=True,
        key=key
    )

def add_tank(tank_type):
    if tank_type == "fuel":
        new_row = pd.DataFrame([['' for _ in range(len(st.session_state.fuel_tanks.columns))]], columns=st.session_state.fuel_tanks.columns)
        st.session_state.fuel_tanks = pd.concat([st.session_state.fuel_tanks, new_row], ignore_index=True)
    elif tank_type == "lube":
        new_row = pd.DataFrame([['' for _ in range(len(st.session_state.lube_oil_tanks.columns))]], columns=st.session_state.lube_oil_tanks.columns)
        st.session_state.lube_oil_tanks = pd.concat([st.session_state.lube_oil_tanks, new_row], ignore_index=True)
    elif tank_type == "water":
        new_row = pd.DataFrame([['' for _ in range(len(st.session_state.water_tanks.columns))]], columns=st.session_state.water_tanks.columns)
        st.session_state.water_tanks = pd.concat([st.session_state.water_tanks, new_row], ignore_index=True)

def main():
    st.title("Vessel Setup")
    initialize_session_state()

    # Fuel Tank Allocation
    st.header("Fuel Tank Allocation")
    fuel_grid_response = create_editable_grid(st.session_state.fuel_tanks, 'fuel_grid')
    st.session_state.fuel_tanks = fuel_grid_response['data']
    if st.button("Add Fuel Tank"):
        add_tank("fuel")

    # Lube Oil Tank Allocation
    st.header("Lube Oil Tank Allocation")
    lube_grid_response = create_editable_grid(st.session_state.lube_oil_tanks, 'lube_grid')
    st.session_state.lube_oil_tanks = lube_grid_response['data']
    if st.button("Add Lube Oil Tank"):
        add_tank("lube")

    # Fresh Water/Distilled Water Tank Allocation
    st.header("Fresh Water/Distilled Water Tank Allocation")
    water_grid_response = create_editable_grid(st.session_state.water_tanks, 'water_grid')
    st.session_state.water_tanks = water_grid_response['data']
    if st.button("Add Water Tank"):
        add_tank("water")

if __name__ == "__main__":
    main()
