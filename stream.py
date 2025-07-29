import streamlit as st
import pandas as pd
from model import get_model_response, input_User

from io import StringIO
from model import get_model_response,input_User # your custom function

st.title("📊 CSV Insight Generator")

# Step 1: Upload CSV file
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

# Step 2: Ask user for a query
user_query = st.text_input("🔍 Ask a question about the data (e.g., 'Give me a summary'):")

if uploaded_file is not None:
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(uploaded_file)

        st.subheader("📌 Preview of Uploaded Data")
        st.dataframe(df.head())

        # Combine user's question with a summary of the data
        if user_query:
            st.subheader("🧠 Generating Insight...")
            prompt = input_User(df.to_json, user_query)
            insight = get_model_response(prompt)

            # Display and allow download
            st.subheader("📝 Insight from AI")
            st.write(insight)

            # Prepare downloadable text file
            download_text = StringIO()
            download_text.write(insight)
            download_text.seek(0)

            st.download_button(
                label="📥 Download Insight as .txt",
                data=download_text,
                file_name="insight_report.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"❌ Error reading CSV file: {e}")
