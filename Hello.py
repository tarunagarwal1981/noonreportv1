import streamlit as st
import psycopg2
import pandas as pd
from psycopg2 import sql
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="Optilog - DB Schema Viewer")

# Apply custom CSS for better visual appeal
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stSelectbox {
        min-width: 200px;
    }
    .stDownloadButton {
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Database connection
@st.cache_resource
def init_connection():
    return psycopg2.connect(
        host=st.secrets["db_connection"]["host"],
        port=st.secrets["db_connection"]["port"],
        dbname=st.secrets["db_connection"]["dbname"],
        user=st.secrets["db_connection"]["user"],
        password=st.secrets["db_connection"]["password"]
    )

conn = init_connection()

# Database query functions
def run_query(query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()

def get_table_columns(table_name, schema):
    query = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = %s AND table_name = %s
    """
    return [col[0] for col in run_query(query, (schema, table_name))]

def get_metadata_fields():
    query = """
    SELECT table_name, column_name, data_element_name, definition, standard_unit, additional_info
    FROM public.column_metadata
    """
    return run_query(query)

# Streamlit app title
st.title('Optilog - DB Schema, Table, Fields & Metadata')

# Sidebar for filters
with st.sidebar:
    st.header('Filters')

    # Get all schemas, including 'public'
    schemas = run_query("""
        SELECT schema_name 
        FROM information_schema.schemata 
        WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
    """)
    schema_list = [schema[0] for schema in schemas]
    default_schema_index = schema_list.index('public') if 'public' in schema_list else 0
    selected_schema = st.selectbox('Select a schema', schema_list, index=default_schema_index)

    # Get tables for selected schema
    tables = run_query("SELECT table_name FROM information_schema.tables WHERE table_schema = %s", (selected_schema,))
    selected_table = st.selectbox('Select a table', [table[0] for table in tables])

    # Option to show only mandatory fields
    show_mandatory = st.checkbox('Show only mandatory fields')

# Main content area
if selected_table:
    columns = get_table_columns(selected_table, selected_schema)
    
    if columns:
        # Construct and execute query
        columns_str = ', '.join(columns)
        query = f"SELECT {columns_str} FROM {selected_schema}.{selected_table}"
        data = run_query(query)
        
        # Display data using AgGrid
        df = pd.DataFrame(data, columns=columns)
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(resizable=True, sorteable=True, filter=True, wrapText=True, autoHeight=True)
        gb.configure_grid_options(domLayout='normal')
        gb.configure_side_bar()
        gridOptions = gb.build()
        
        st.subheader(f'Data from {selected_schema}.{selected_table}')
        AgGrid(df, 
               gridOptions=gridOptions, 
               height=500, 
               width='100%',
               theme='streamlit', 
               update_mode=GridUpdateMode.SELECTION_CHANGED,
               allow_unsafe_jscode=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f'{selected_schema}_{selected_table}.csv',
            mime='text/csv',
        )
    else:
        st.warning("No columns found or accessible.")
else:
    st.info("Please select a table to view data.")

# Display table metadata
metadata = get_metadata_fields()

if metadata:
    metadata_df = pd.DataFrame(metadata, columns=['Table Name', 'Column', 'Data Element', 'Definition', 'Unit', 'Additional Info'])
    filtered_metadata_df = metadata_df[metadata_df['Table Name'] == selected_table]
    
    if show_mandatory:
        filtered_metadata_df = filtered_metadata_df[filtered_metadata_df['Additional Info'].str.contains('mandatory', case=False, na=False)]
    
    if not filtered_metadata_df.empty:
        st.subheader(f'Metadata for {selected_table}')
        gb = GridOptionsBuilder.from_dataframe(filtered_metadata_df)
        gb.configure_default_column(resizable=True, wrapText=True, autoHeight=True)
        gb.configure_grid_options(domLayout='normal')
        gb.configure_side_bar()
        gridOptions = gb.build()
        
        AgGrid(filtered_metadata_df, 
               gridOptions=gridOptions, 
               height=300, 
               width='100%',
               theme='streamlit',
               update_mode=GridUpdateMode.SELECTION_CHANGED,
               allow_unsafe_jscode=True)
    else:
        st.warning("No metadata found for this table.")
else:
    st.warning("No metadata found.")

# Footer
st.markdown("---")
st.markdown("© 2023 Optilog. All rights reserved.")
