import streamlit as st
from modules import simulator, quiz, chatbot

st.set_page_config(page_title="FinBuddy Virtual Advisor", layout="centered", page_icon="🐧")
st.title("🐧 FinBuddy Virtual Advisor 🐧")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #E3F2FD;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar: User Identification
with st.sidebar:
    st.markdown("## 👤 User Identification")
    user_id = st.text_input("Enter Your Name or ID", key="user_id", placeholder="e.g. defika123")

    # Sidebar: Feature Navigation (always visible)
    st.markdown("## 🔍 Navigate Features")
    menu = st.radio(
        "Select Feature",
        ["🏠 Home", "🧠 Financial Readiness Quiz", "📊 Car Loan Simulator", "💬 Ask the Chatbot"]
    )

# Set display name
display_name = user_id if user_id else "Guest"

# Routing based on menu selection
if menu == "🏠 Home":
    st.subheader(f"Hi, {display_name} 👋")
    st.markdown("""
    **Welcome to FinBuddy!** 🐧  
    FinBuddy is your virtual financial assistant — here to help you make smarter car loan decisions.

    With FinBuddy, you can:
    - 🧠 Take a quiz to assess your financial readiness
    - 📊 Simulate monthly car loan installments
    - 💬 Chat with a smart finance assistant

    Just select a feature from the sidebar to get started!
    """)
else:
    if not user_id:
        st.warning("Please enter your ID in the sidebar to use this feature.")
        st.stop()

    # Initialize per-user data if not already set
    if user_id not in st.session_state:
        st.session_state[user_id] = {
            "quiz_score": 0,
            "quiz_answers": {},
            "simulator_result": {},
            "chat_history": []
        }

    # Run selected module
    if menu == "📊 Car Loan Simulator":
        simulator.run(user_id)
    elif menu == "🧠 Financial Readiness Quiz":
        quiz.run(user_id)
    elif menu == "💬 Ask the Chatbot":
        chatbot.run(user_id)
