import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Vessel Onboarding")

def create_input_row(labels, keys, col_count=4):
    cols = st.columns(col_count)
    for i, (label, key) in enumerate(zip(labels, keys)):
        with cols[i % col_count]:
            st.text_input(label, key=f"{key}_{i}")

def create_engine_fields(engine_type, num_engines):
    for i in range(1, num_engines + 1):
        st.subheader(f"{engine_type} #{i}")
        create_input_row(
            [f"{engine_type} #{i} Make", f"{engine_type} #{i} Model", f"{engine_type} #{i} SMCR Power", f"{engine_type} #{i} SMCR RPM"],
            [f"{engine_type.lower()}_{i}_make", f"{engine_type.lower()}_{i}_model", f"{engine_type.lower()}_{i}_smcr_power", f"{engine_type.lower()}_{i}_smcr_rpm"]
        )
        create_input_row(
            [f"{engine_type} #{i} NCR Power", f"{engine_type} #{i} NCR RPM", f"{engine_type} #{i} Flowmeter Make", f"{engine_type} #{i} Flowmeter Model"],
            [f"{engine_type.lower()}_{i}_ncr_power", f"{engine_type.lower()}_{i}_ncr_rpm", f"{engine_type.lower()}_{i}_flowmeter_make", f"{engine_type.lower()}_{i}_flowmeter_model"]
        )

def main():
    st.title("Vessel Onboarding")

    with st.expander("Vessel Particulars", expanded=True):
        create_input_row(
            ["Vessel Name", "LOA", "Vessel Type", "LBP"],
            ["vessel_name", "loa", "vessel_type", "lbp"]
        )
        create_input_row(
            ["Vessel Sub type", "Beam", "IMO Number", "Height above keel"],
            ["vessel_subtype", "beam", "imo_number", "height_above_keel"]
        )
        create_input_row(
            ["MMSI Number", "Bridge to bow", "Port Of Registry", "Bridge to stern"],
            ["mmsi_number", "bridge_to_bow", "port_of_registry", "bridge_to_stern"]
        )
        create_input_row(
            ["Call SIGN", "GRT", "NRT", "Lightship"],
            ["call_sign", "grt", "nrt", "lightship"]
        )

    with st.expander("Shipyard Info"):
        create_input_row(
            ["Keel laid", "Date launched", "Delivered", "Hull / Build Number"],
            ["keel_laid", "date_launched", "delivered", "hull_build_number"]
        )
        create_input_row(
            ["Ice class", "Ice class Notation", "EEDI no.", "EEXI value"],
            ["ice_class", "ice_class_notation", "eedi_no", "eexi_value"]
        )

    with st.expander("Deadweight and Freeboard"):
        create_input_row(
            ["Summer Dwt", "Winter Dwt", "Tropical Dwt", "Summer FW Dwt"],
            ["summer_dwt", "winter_dwt", "tropical_dwt", "summer_fw_dwt"]
        )
        create_input_row(
            ["Summer freeboard", "Winter freeboard", "Tropical freeboard", "Summer FW freeboard"],
            ["summer_freeboard", "winter_freeboard", "tropical_freeboard", "summer_fw_freeboard"]
        )
        create_input_row(
            ["Summer draft", "Winter draft", "Tropical draft", "Summer FW draft"],
            ["summer_draft", "winter_draft", "tropical_draft", "summer_fw_draft"]
        )

    with st.expander("Machinery Particulars", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            num_main_engines = st.number_input("Number of Main Engines", min_value=1, max_value=4, value=1, step=1)
        with col2:
            num_aux_engines = st.number_input("Number of Auxiliary Engines", min_value=1, max_value=6, value=1, step=1)
        with col3:
            scrubber_fitted = st.selectbox("Scrubber Fitted", ["No", "Yes"])
        with col4:
            num_boilers = st.number_input("Number of Boilers", min_value=1, max_value=4, value=1, step=1)

        # Main Engines
        create_engine_fields("Main Engine", num_main_engines)

        # Auxiliary Engines
        create_engine_fields("Auxiliary Engine", num_aux_engines)

        # Boilers
        for i in range(1, num_boilers + 1):
            st.subheader(f"Boiler #{i}")
            create_input_row(
                [f"Boiler #{i} Make", f"Boiler #{i} Model", f"Boiler #{i} Capacity", f"Boiler #{i} Working Pressure"],
                [f"boiler_{i}_make", f"boiler_{i}_model", f"boiler_{i}_capacity", f"boiler_{i}_working_pressure"]
            )

        # Scrubber (if fitted)
        if scrubber_fitted == "Yes":
            st.subheader("Scrubber Details")
            create_input_row(
                ["Scrubber Make", "Scrubber Model", "Scrubber Type", "Scrubber Capacity"],
                ["scrubber_make", "scrubber_model", "scrubber_type", "scrubber_capacity"]
            )

    with st.expander("Engine Details"):
        create_input_row(
            ["Shaft Generator Fitted?", "Engine fitted with EPL/Derated Engine?", "Propeller Diameter (mm)", "Propeller Pitch"],
            ["shaft_generator_fitted", "engine_epl_derated", "propeller_diameter", "propeller_pitch"]
        )

    with st.expander("Consumption Details"):
        st.subheader("At Sea")
        create_input_row(
            ["M/E Ballast", "A/E Ballast", "Blr Ballast", "M/E Laden"],
            ["me_ballast", "ae_ballast", "blr_ballast", "me_laden"]
        )
        create_input_row(
            ["A/E Laden", "Blr Laden", "", ""],
            ["ae_laden", "blr_laden", "empty1", "empty2"]
        )

        st.subheader("At Port")
        create_input_row(
            ["AE HSFO", "BLKR HSFO", "AE VLSFO", "BLKR VLSFO"],
            ["ae_hsfo", "blkr_hsfo", "ae_vlsfo", "blkr_vlsfo"]
        )

    with st.expander("Fuel Compatibility"):
        fuels = ["HFO", "LFO", "MGO", "MDO", "LPGP", "LPGB", "LNG", "LNGN2", "Methanol", "Ethanol", "Ethane", "Blend"]
        for i in range(0, len(fuels), 4):
            create_input_row(
                fuels[i:i+4],
                [f"fuel_{fuel.lower()}" for fuel in fuels[i:i+4]]
            )

    if st.button("Submit"):
        st.success("Vessel onboarding information submitted successfully!")

if __name__ == "__main__":
    main()
