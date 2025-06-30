import streamlit as st

questions = [
    {
        "question": "Do you currently have any emergency savings (Dana Darurat)?",
        "options": ["Yes, more than 6 months of expenses", "Yes, 3-6 months of expenses", "Less than 3 months", "No savings at all"],
        "scores": [4, 3, 2, 1]
    },
    {
        "question": "How much of your income do you save or invest monthly?",
        "options": ["More than 30%", "15-30%", "5-15%", "Less than 5%"],
        "scores": [4, 3, 2, 1]
    },
    {
        "question": "Do you have any unpaid debt (not including mortgage/car loan)?",
        "options": ["No debt at all", "Less than 30% of monthly income", "30-50% of monthly income", "More than 50%"],
        "scores": [4, 3, 2, 1]
    },
    {
        "question": "How stable is your current income?",
        "options": ["Very stable (fixed salary)", "Stable but with variable bonus", "Freelance / business income", "Unstable or irregular"],
        "scores": [4, 3, 2, 1]
    },
    {
        "question": "How familiar are you with credit interest and loan terms?",
        "options": ["Very familiar", "Somewhat familiar", "Only basic knowledge", "Not familiar at all"],
        "scores": [4, 3, 2, 1]
    },
    {
        "question": "Have you ever checked your credit score or SLIK?",
        "options": ["Yes, regularly", "Yes, once or twice", "I know what it is, but never checked", "I don't know what that is"],
        "scores": [4, 3, 2, 1]
    },
    {
        "question": "When receiving a big bonus or THR, what do you usually do?",
        "options": ["Invest/save majority", "Pay off debt, then save", "Split evenly with spending", "Spend most of it"],
        "scores": [4, 3, 2, 1]
    },
    {
        "question": "How do you usually track your spending?",
        "options": ["Use budgeting app/spreadsheet", "Track manually", "Occasionally review bank statement", "Don’t track at all"],
        "scores": [4, 3, 2, 1]
    },
    {
        "question": "What is your main reason for wanting to buy a car on credit?",
        "options": ["Need it for work or family & have a plan", "Need it soon, still figuring out finances", "Want it for convenience", "Just want a car now"],
        "scores": [4, 3, 2, 1]
    },
    {
        "question": "How would you describe your overall financial discipline?",
        "options": ["Very disciplined", "Fairly disciplined", "Trying to improve", "Not disciplined"],
        "scores": [4, 3, 2, 1]
    }
]

def run(user_id):
    # Initialize navigation state if not set
    if "nav" not in st.session_state:
        st.session_state["nav"] = "quiz"

    # Initialize user_data for the current user_id if not exists
    if user_id not in st.session_state:
        st.session_state[user_id] = {"chat_history": []}

    user_data = st.session_state[user_id]
    st.subheader("📝 Mini Quiz: Are You Ready for a Car Loan?")
    st.markdown("Answer the following 10 questions to find out your financial readiness.")

    total_score = 0
    for i, q in enumerate(questions):
        st.markdown(f"**{i+1}. {q['question']}**")
        selected = st.radio("", q["options"], key=f"q{i}", index=None)
        if selected:
            score = q["scores"][q["options"].index(selected)]
            total_score += score

    if st.button("Check My Result"):
        st.markdown("---")
        st.subheader("📊 Your Financial Readiness Result:")

        if total_score >= 30:
            st.success("""✅ You're financially ready for a car loan! Just make sure to choose the right terms and budget wisely.
                       You seem well-prepared! If you'd like to simulate your car credit, go ahead and try our simulator.""")
        elif total_score >= 20:
            st.info("""🟡 You're getting there. Work on building savings and understanding credit better.
                    You're close! Try asking FinBuddy chatbot for more tips or simulate a car loan to explore your options.""")
        elif total_score >= 10:
            st.warning("""⚠️ You're not quite ready yet. Strengthen your finances before taking on a loan.
                       We recommend talking to FinBuddy for budgeting advice, or simulate a loan to understand the costs.""")
        else:
            st.error("""❌ It’s risky to take a loan now. Focus on building stability and knowledge first.
                     Start by chatting with FinBuddy for personalized financial advice.""")

        st.markdown(f"**Your Score: {total_score} / 40**")
