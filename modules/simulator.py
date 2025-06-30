import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def run(user_id):
    if user_id not in st.session_state:
        st.session_state[user_id] = {}

    st.subheader("🚗 Car Credit Simulator")
    st.markdown("Estimate your monthly installment based on car price, down payment, interest rate, and loan term.")

    # Input fields
    car_price = st.number_input("Car Price (IDR)", min_value=10000000, step=1000000, value=150000000)
    down_payment = st.number_input("Down Payment (IDR)", min_value=0, max_value=car_price, step=1000000, value=30000000)

    # Show formatted amounts
    st.markdown(f"**Selected Car Price:** IDR {car_price:,.0f}")
    st.markdown(f"**Down Payment:** IDR {down_payment:,.0f}")

    # Reference note for effective interest rate in Indonesia (Adira, OTO, etc.)
    st.markdown("""
    _Effective interest rates for car loans in Indonesia typically range between **8% - 14%** per year depending on credit score, down payment, and provider (e.g., Adira, OTO)._  
    _This simulator uses **effective interest** calculation, which reflects actual costs more accurately._
    """)
    interest_rate = st.slider("Effective Annual Interest Rate (%)", min_value=6.0, max_value=18.0, value=12.0)

    loan_years = st.slider("Loan Term (Years)", min_value=1, max_value=6, value=3)

    if st.button("Calculate Installment"):
        loan_amount = car_price - down_payment
        total_months = loan_years * 12
        monthly_interest_rate = interest_rate / 12 / 100

        # Using annuity formula (effective interest)
        monthly_installment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_months) / ((1 + monthly_interest_rate) ** total_months - 1)
        total_payment = monthly_installment * total_months
        total_interest = total_payment - loan_amount

        st.markdown("---")
        st.subheader("💰 Estimated Monthly Installment")
        st.success(f"IDR {monthly_installment:,.0f} / month for {total_months} months")

        st.markdown("**📈 Summary**")
        st.markdown(f"- **Loan Amount:** IDR {loan_amount:,.0f}")
        st.markdown(f"- **Total Interest Paid:** IDR {total_interest:,.0f}")
        st.markdown(f"- **Total Payment:** IDR {total_payment:,.0f}")

        # 📉 Monthly Principal & Interest Breakdown
        st.markdown("---")
        st.subheader("📉 Monthly Breakdown: Interest vs. Principal")

        # Amortization breakdown
        principal_paid = []
        interest_paid = []
        remaining_balance = loan_amount

        for _ in range(total_months):
            interest = remaining_balance * monthly_interest_rate
            principal = monthly_installment - interest
            remaining_balance -= principal

            interest_paid.append(interest)
            principal_paid.append(principal)

        cumulative_interest = pd.Series(interest_paid).cumsum()
        cumulative_principal = pd.Series(principal_paid).cumsum()

        df_monthly = pd.DataFrame({
            "Month": list(range(1, total_months + 1)),
            "Monthly Principal": principal_paid,
            "Monthly Interest": interest_paid
        })

        fig, ax = plt.subplots()
        ax.plot(df_monthly["Month"], df_monthly["Monthly Principal"], label="Principal", color='green')
        ax.plot(df_monthly["Month"], df_monthly["Monthly Interest"], label="Interest", color='red')
        ax.set_title("Monthly Interest and Principal Payment")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount (IDR)")
        ax.legend()
        ax.grid(True)

        # Format y-axis to currency
        ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('IDR {x:,.0f}'))

        st.pyplot(fig)
