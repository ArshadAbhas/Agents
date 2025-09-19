import streamlit as st
from csv_agent import NewTable
from corechain import PolicyChecker


st.title("Excel to Smart Expense - Policy Checker")

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully ✅")

    try:
        # Step 1: Add uploaded Excel as DuckDB table
        new_table = NewTable(uploaded_file)
        table_name = new_table.addtable()
        st.success(f"Table '{table_name}' created successfully in DuckDB 🎉")

        # Step 2: Run PolicyChecker
        checker = PolicyChecker()
        report = checker.run_policy_check(output_file="expense_report.json")

        # Step 3: Show JSON in app
        st.subheader("📊 Policy Check Report")
        st.json(report)

        # Step 4: Download button
        st.download_button(
            label="⬇️ Download JSON Report",
            data=open("expense_report.json", "r").read(),
            file_name="expense_report.json",
            mime="application/json"
        )

    except Exception as e:
        st.error(f"⚠️ Error while processing: {e}")
