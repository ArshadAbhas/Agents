import streamlit as st




import pandas as pd



import pandas as pd

def prepare_prompt(df: pd.DataFrame):
    summary = {}

    # Basic metadata
    summary["columns"] = df.dtypes.astype(str).to_dict()
    summary["nulls"] = df.isnull().sum().to_dict()
    summary["uniques"] = df.nunique().to_dict()

    # Describe numeric columns
    numeric_desc = df.describe(include='number').to_dict()
    summary["numeric_summary"] = numeric_desc

    # Sample top values
    for col in df.columns:
        summary[f"top_{col}"] = df[col].value_counts().head(5).to_dict()

    # Entity-level analysis
    summary["top_items"] = df["Items"].value_counts().head(10).to_dict()
    summary["top_combinations"] = (
        df.groupby("TransactionNo")["Items"]
        .apply(list)
        .value_counts()
        .head(5)
        .to_dict()
    )

    # Return formatted prompt
    import json
    return f"Analyze this dataset and suggest insights and patterns:\n{json.dumps(summary, indent=2)}"


st.set_page_config(page_title="Excel Insight Agent", layout="wide")

st.title("💬 Excel Insight Agent")
st.markdown("Upload your file and ask anything. Your data assistant is ready!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# File upload
uploaded_file = st.file_uploader("📁 Upload a CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    st.success(f"File `{uploaded_file.name}` uploaded successfully.")

    # 📄 Read the uploaded file
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # ✅ Display the dataframe (optional)
        st.subheader("📊 Uploaded Data Preview:")
        st.dataframe(df.head())  # Show first 5 rows

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
# Show chat history
    if "initial_insight_done" not in st.session_state:
        txt = prepare_prompt(df)
        print(txt)
        st.session_state.chat_history.append({"role": "assistant", "message": txt})
        st.session_state.initial_insight_done = True
st.markdown("---")
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["message"])

# Chat input
if uploaded_file:
    user_input = st.chat_input("Ask something about your uploaded data...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "message": user_input})

        # Placeholder for model/insight response
        fake_response = "🤖 This is a placeholder response from the model."
        st.session_state.chat_history.append({"role": "assistant", "message": fake_response})
        st.experimental_rerun()
else:
    st.info("Please upload a file to start the conversation.")

