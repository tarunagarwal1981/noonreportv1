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
        
        if engine_type == "Main Engine":
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                epl_fitted = st.selectbox(f"EPL Fitted for {engine_type} #{i}", ["No", "Yes"], key=f"{engine_type.lower()}_{i}_epl_fitted")
            with col2:
                if epl_fitted == "Yes":
                    st.text_input(f"EPL Power for {engine_type} #{i}", key=f"{engine_type.lower()}_{i}_epl_power")
            with col3:
                shaft_generator_fitted = st.selectbox(f"Shaft Generator Fitted for {engine_type} #{i}", ["No", "Yes"], key=f"{engine_type.lower()}_{i}_shaft_generator_fitted")
            with col4:
                if shaft_generator_fitted == "Yes":
                    st.text_input(f"Shaft Generator Power for {engine_type} #{i}", key=f"{engine_type.lower()}_{i}_shaft_generator_power")

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

        # Propeller
        st.subheader("Propeller")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Propeller Diameter (mm)", key="propeller_diameter")
        with col2:
            st.number_input("Number of Blades", min_value=1, max_value=10, value=4, step=1, key="propeller_blades")

    with st.expander("Energy Saving Devices (if fitted)"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Pre-Swirl Device")
            pre_swirl_options = [
                "None (selected)", "Pre-Swirl Fins & Stators", "Mitsui Integrated Ducted Propeller",
                "Hatch Zosen Nozzle", "Sumitomo Integrated Lammeren Duct", "Becker Mewis Duct"
            ]
            st.selectbox("Pre-Swirl Device", pre_swirl_options, key="pre_swirl_device")
        
        with col2:
            st.subheader("Post-Swirl Devices")
            post_swirl_options = [
                "None", "Rudder Thruster Fins", "Post Swirl Stators", "Asymmetric Rudders",
                "Rudder (Costa Bulb)", "Propeller Boss Cap Fin (PBCF)", "Divergent Propeller Caps", "Grim Vane Wheels"
            ]
            st.selectbox("Post-Swirl Devices", post_swirl_options, key="post_swirl_devices")
        
        with col3:
            st.subheader("Skin Friction Reduction")
            skin_friction_options = ["None (selected)", "Air Cavity Systems", "Micro Bubbles"]
            st.selectbox("Skin Friction Reduction", skin_friction_options, key="skin_friction_reduction")

    with st.expander("Fuel Compatibility"):
        fuels = [
            "HFO", "eMDO", "NH3", "ULSFO2020", "B10MGO",
            "LFO", "eMGO", "H2", "ULSLFO2020", "B20LFO",
            "MGO", "eLPG", "BioH2", "ULSMDO2020", "B24LFO",
            "MDO", "eDME", "eH2", "ULSMGO2020", "B30LFO",
            "LPGP", "HVO", "eNH3", "VLSFO", "B50MGO",
            "LPGB", "FAME", "LBG", "VLSFO2020", "BioLFO",
            "LNG", "BioLNG", "OtherBio", "VLSLFO2020", "BioMGO",
            "LNGN2", "eLNG", "LSHFO", "B100LFO", "Other",
            "Methanol", "BioMethanol", "LSLFO", "B100MGO",
            "Ethanol", "eMethanol", "LSMGO", "B10LFO",
            "Ethane", "Blend"
        ]
        
        col1, col2, col3, col4 = st.columns(4)
        for i, fuel in enumerate(fuels):
            with col1 if i % 4 == 0 else col2 if i % 4 == 1 else col3 if i % 4 == 2 else col4:
                st.checkbox(fuel, key=f"fuel_{fuel.lower()}")

    with st.expander("Additional Info"):
        create_input_row(
            ["Last Dry Dock Date", "Coating: Silicone Paint Applied?", "Last UW-Coating Application Date", "Surface Preparation (Last Coating Application)"],
            ["last_dry_dock_date", "silicone_paint_applied", "last_uw_coating_date", "surface_preparation"]
        )
        create_input_row(
            ["Last UW Inspection Date", "Intended Next Coating Application", "Last Hull Cleaning Date", "UW-Coating: Paint"],
            ["last_uw_inspection_date", "next_coating_application", "last_hull_cleaning_date", "uw_coating_paint"]
        )
        create_input_row(
            ["Last Propeller Polishing Date", "UW-Coating: Paint Producer", "", ""],
            ["last_propeller_polishing_date", "uw_coating_paint_producer", "empty1", "empty2"]
        )

    if st.button("Submit"):
        st.success("Vessel onboarding information submitted successfully!")

if __name__ == "__main__":
    main()
