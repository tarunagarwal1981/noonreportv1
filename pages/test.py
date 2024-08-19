import streamlit as st
import pandas as pd
from datetime import datetime

# Mock data
fields_data = {
    'Field Name': ['Vessel Name', 'IMO Number', 'Departure Port', 'Arrival Port', 'Fuel Consumption'],
    'Definition': ['Name of the vessel', 'IMO ship identification number', 'Port of departure', 'Port of arrival', 'Total fuel consumed during voyage'],
    'Unit': ['N/A', 'N/A', 'N/A', 'N/A', 'Metric Tons'],
    'Vessel Type': ['All', 'All', 'All', 'All', 'All'],
    'Version': ['1.0', '1.0', '1.0', '1.0', '1.1']
}

reports_data = {
    'Report Name': ['Noon Report', 'Arrival Report', 'Departure Report'],
    'Description': ['Daily report at noon', 'Report upon arrival at port', 'Report upon departure from port'],
    'Category': ['Daily', 'Event', 'Event']
}

def main():
    st.title("Maritime Reporting System Mockup")

    menu = st.sidebar.selectbox("Select a feature", 
                                ["Data Field Library", "Standard Reports", "Company-Specific Reports"])

    if menu == "Data Field Library":
        data_field_library()
    elif menu == "Standard Reports":
        standard_reports()
    elif menu == "Company-Specific Reports":
        company_specific_reports()

def data_field_library():
    st.header("Data Field Library")
    
    fields_df = pd.DataFrame(fields_data)
    
    st.subheader("View Fields")
    st.dataframe(fields_df)
    
    st.subheader("Add New Field")
    new_field_name = st.text_input("Field Name")
    new_field_definition = st.text_input("Definition")
    new_field_unit = st.text_input("Unit")
    new_field_vessel_type = st.multiselect("Applicable Vessel Types", ["All", "Oil Tanker", "Container Ship", "Bulk Carrier"])
    
    if st.button("Add Field"):
        st.success(f"Field '{new_field_name}' added successfully!")

def standard_reports():
    st.header("Standard Reports")
    
    reports_df = pd.DataFrame(reports_data)
    
    st.subheader("View Reports")
    st.dataframe(reports_df)
    
    st.subheader("Create New Report")
    new_report_name = st.text_input("Report Name")
    new_report_description = st.text_area("Description")
    new_report_category = st.selectbox("Category", ["Daily", "Event", "Environmental"])
    new_report_fields = st.multiselect("Select Fields", fields_data['Field Name'])
    
    if st.button("Create Report"):
        st.success(f"Report '{new_report_name}' created successfully!")

def company_specific_reports():
    st.header("Company-Specific Reports")
    
    company = st.selectbox("Select Company", ["Company A", "Company B", "Company C"])
    vessel_type = st.selectbox("Select Vessel Type", ["Oil Tanker", "Container Ship", "Bulk Carrier"])
    
    st.subheader("Customize Report")
    base_report = st.selectbox("Select Base Report", reports_data['Report Name'])
    custom_fields = st.multiselect("Select Fields", fields_data['Field Name'])
    
    if st.button("Save Customized Report"):
        st.success(f"Customized report for {company} ({vessel_type}) saved successfully!")

if __name__ == "__main__":
    main()
