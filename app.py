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

# Sidebar: ID Pengguna
with st.sidebar:
    st.markdown("## 👤 Identitas Pengguna")
    user_id = st.text_input("Masukkan Nama atau ID Kamu", key="user_id", placeholder="contoh: defika123")
    if not user_id:
        st.warning("Harap isi ID pengguna untuk menggunakan aplikasi.")
        st.stop()

# Inisialisasi data per user
if user_id not in st.session_state:
    st.session_state[user_id] = {
        "quiz_score": 0,
        "quiz_answers": {},
        "simulator_result": {},
        "chat_history": []
    }

# Sidebar: Navigasi fitur
menu = st.sidebar.selectbox(
    "Pilih Fitur",
    ["🏠 Home", "📊 Simulasi Kredit Mobil", "🧠 Cek Kesiapan Finansial", "💬 Tanya Chatbot"]
)

if menu == "🏠 Home":
    st.subheader(f"Halo, {user_id} 👋")
    st.markdown("""
    Aplikasi ini membantumu mengambil keputusan kredit mobil yang lebih bijak.
    
    **Fitur yang tersedia:**
    - 📊 Simulasi cicilan kredit mobil
    - 🧠 Kuis kesiapan finansial
    - 💬 Chatbot keuangan pribadi
    """)
elif menu == "📊 Simulasi Kredit Mobil":
    simulator.run(user_id)
elif menu == "🧠 Cek Kesiapan Finansial":
    quiz.run(user_id)
elif menu == "💬 Tanya Chatbot":
    chatbot.run(user_id)
