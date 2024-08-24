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

def add_row(df):
    return pd.concat([df, pd.DataFrame([[''] * len(df.columns)], columns=df.columns)], ignore_index=True)

def main():
    st.title("Vessel Setup")
    initialize_session_state()

    # Fuel Tank Allocation
    st.header("Fuel Tank Allocation")
    edited_fuel_df = st.data_editor(
        st.session_state.fuel_tanks,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Tank Name": st.column_config.TextColumn(required=True),
            "Tank Capacity (100% m3)": st.column_config.NumberColumn(required=True, min_value=0, format="%.2f"),
            "Current ROB (mT)": st.column_config.NumberColumn(required=True, min_value=0, format="%.2f"),
            "Fuel Grade": st.column_config.TextColumn(required=True),
            "BDN Number": st.column_config.TextColumn(required=True),
            "% Sulphur": st.column_config.NumberColumn(required=True, min_value=0, max_value=100, format="%.4f"),
            "Viscosity": st.column_config.NumberColumn(required=True, min_value=0, format="%.2f"),
        }
    )
    st.session_state.fuel_tanks = edited_fuel_df

    # Lube Oil Tank Allocation
    st.header("Lube Oil Tank Allocation")
    edited_lube_df = st.data_editor(
        st.session_state.lube_oil_tanks,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Tank Name": st.column_config.TextColumn(required=True),
            "Tank Capacity (100% m3)": st.column_config.NumberColumn(required=True, min_value=0, format="%.2f"),
            "Current ROB (mT)": st.column_config.NumberColumn(required=True, min_value=0, format="%.2f"),
            "Lube Oil Grade": st.column_config.TextColumn(required=True),
            "BN": st.column_config.NumberColumn(required=True, min_value=0, format="%.1f"),
        }
    )
    st.session_state.lube_oil_tanks = edited_lube_df

    # Fresh Water/Distilled Water Tank Allocation
    st.header("Fresh Water/Distilled Water Tank Allocation")
    edited_water_df = st.data_editor(
        st.session_state.water_tanks,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Tank Name": st.column_config.TextColumn(required=True),
            "Tank Capacity (100% m3)": st.column_config.NumberColumn(required=True, min_value=0, format="%.2f"),
            "Current ROB (mT)": st.column_config.NumberColumn(required=True, min_value=0, format="%.2f"),
            "Water Type": st.column_config.SelectboxColumn(
                required=True,
                options=["Fresh Water", "Distilled Water"],
            ),
        }
    )
    st.session_state.water_tanks = edited_water_df

if __name__ == "__main__":
    main()
