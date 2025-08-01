import streamlit as st

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
    if "file_uploaded" not in st.session_state:
        st.session_state.file_uploaded = True
        # You can store file contents in session state here if needed

    if "initial_insight_done" not in st.session_state:
        # Placeholder for backend-generated insight
        insight = "🔍 Sample insight will be shown here from backend."
        st.session_state.chat_history.append({"role": "assistant", "message": insight})
        st.session_state.initial_insight_done = True

# Show chat history
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
