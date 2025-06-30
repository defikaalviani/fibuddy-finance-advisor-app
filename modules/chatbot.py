# modules/chatbot.py

import streamlit as st
import requests
import json

#OPENROUTER_API_KEY=st.secrets["OPENROUTER_API_KEY"] #or replace with 
OPENROUTER_API_KEY="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"
MODEL = "mistralai/mistral-7b-instruct"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "http://localhost:8501",
    "X-Title": "AI Chatbot Streamlit",
    "Content-Type": "application/json"
}

chatbot_role = """You are a friendly and knowledgeable financial advisor named FinBuddy.
Your goal is to help users understand and manage their personal finances.
You provide simple, clear, practical advice on topics like budgeting, saving, debt, investments, loans, and financial planning.
Always explain things in simple, easy-to-understand language, especially for users who are new to finance.
Focus on financial practices, habits, and tools that are relevant to users in Indonesia.
Ask questions about users’ financial situations to offer more personalized advice.
Offer helpful solutions or referrals when appropriate, but avoid sounding too salesy.
Be supportive, honest, and never make unrealistic promises."""

def render_bubble(role, content):
    if role == "user":
        bubble_color = "#E1BEE7"
        align = "right"
        name = "You"
    elif role == "assistant":
        bubble_color = "#FFF9C4"
        align = "left"
        name = "🐧FinBuddy"
    else:
        return

    st.markdown(
        f"""
        <div style='text-align: {align}; margin: 10px 0;'>
            <div style='
                display: inline-block;
                background-color: {bubble_color};
                padding: 10px 15px;
                border-radius: 12px;
                max-width: 75%;
                font-size: 15px;
                box-shadow: 0px 1px 3px rgba(0,0,0,0.1);
            '>
                <div style='font-weight: bold; margin-bottom: 5px;'>{name}</div>
                {content}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def run(user_id):
    user_data = st.session_state[user_id]
    st.subheader("💬 FinBuddy Chatbot")
    st.markdown("Got financial questions? I’ve got your back — anytime, anywhere.")
    #st.markdown("Powered by **GPT-3.5 via OpenRouter**")

    if "chat_history" not in user_data:
        user_data["chat_history"] = [{"role": "system", "content": chatbot_role}]

    for message in user_data["chat_history"]:
        if message["role"] != "system":
            render_bubble(message["role"], message["content"])

    user_input = st.chat_input("Type your message here...")

    if user_input:
        user_data["chat_history"].append({"role": "user", "content": user_input})
        render_bubble("user", user_input)

        with st.spinner("Thinking..."):
            payload = {
                "model": MODEL,
                "messages": user_data["chat_history"]
            }

            try:
                response = requests.post(API_URL, headers=HEADERS, json=payload)
                if response.status_code == 200:
                    bot_reply = response.json()["choices"][0]["message"]["content"]
                elif response.status_code == 401:
                    bot_reply = "🔐 Access denied. Please check your API key."
                elif response.status_code == 429:
                    bot_reply = "🚦 Too many requests. Please wait a moment and try again."
                elif response.status_code >= 500:
                    bot_reply = "🛠️ Server error. Please try again later."
                else:
                    bot_reply = f"⚠️ Unexpected error {response.status_code}: {response.text[:200]}"
            except requests.exceptions.ConnectionError:
                bot_reply = "🌐 Connection error. Please check your internet connection."
            except Exception as e:
                bot_reply = f"⚠️ An unexpected error occurred: {str(e)}"

        user_data["chat_history"].append({"role": "assistant", "content": bot_reply})
        render_bubble("assistant", bot_reply)
