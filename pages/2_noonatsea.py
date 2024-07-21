elif field_type == "selectbox":
        return st.selectbox(label, key=label, help=kwargs.get("help", ""), options=kwargs.get("options", []), index=kwargs.get("options", []).index(st.session_state.form_data.get(label, kwargs.get("options", [""])[0])))
    elif field_type == "radio":
        return st.radio(label, key=label, help=kwargs.get("help", ""), options=kwargs.get("options", []), index=kwargs.get("options", []).index(st.session_state.form_data.get(label, kwargs.get("options", [""])[0])))
    elif field_type == "checkbox":
        return st.checkbox(label, key=label, help=kwargs.get("help", ""), value=st.session_state.form_data.get(label, False))

def create_summary():
    summary = {}
    for key, value in st.session_state.items():
        if not key.startswith('_') and key != 'form_data':
            summary[key] = value
    return summary

def display_summary():
    st.title("Report Summary")
    summary = create_summary()
    for section, fields in summary.items():
        st.header(section)
        for field, value in fields.items():
            st.write(f"{field}: {value}")

def save_report():
    summary = create_summary()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"maritime_report_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(summary, f)
    st.success(f"Report saved as {filename}")

# Add keyboard shortcuts
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 's') {
        document.querySelector('button:contains("Save Current Report")').click();
        e.preventDefault();
    } else if (e.ctrlKey && e.key === 'r') {
        document.querySelector('button:contains("Review Summary")').click();
        e.preventDefault();
    }
});
</script>
""", unsafe_allow_html=True)

# Main function (updated)
def main():
    st.set_page_config(layout="wide", page_title="Maritime Report")
    
    # Dark mode toggle
    if st.sidebar.checkbox("Dark Mode"):
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("Maritime Report")

    # Progress indicator
    st.progress(st.session_state.progress)

    # Quick Fill and Save buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Quick Fill from Previous Report"):
            load_form_data()
    with col2:
        if st.button("Save Current Report"):
            save_form_data()
    with col3:
        if st.button("Review Summary"):
            display_summary()

    # Search function
    search_term = st.sidebar.text_input("Search fields")

    tabs = st.tabs(["Deck", "Engine"])

    with tabs[0]:
        deck_tab(search_term)

    with tabs[1]:
        engine_tab(search_term)

    if st.button("Submit Report", type="primary"):
        save_report()
        st.success("Report submitted and saved successfully!")

    # Auto-save every 5 minutes
    if tm.time() % 300 < 1:  # Every 5 minutes
        save_form_data()

    # Update progress
    update_progress()

if __name__ == "__main__":
    main()
