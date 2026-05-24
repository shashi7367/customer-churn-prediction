
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go

# Load model
with open('/Users/shashiranjan/Downloads/Churn_Prevention/model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('/Users/shashiranjan/Downloads/Churn_Prevention/features.pkl', 'rb') as f:
    feature_names = pickle.load(f)

def get_recommendation(churn_prob, monthly_charges, tenure):
    recommendations = []
    revenue_at_risk = monthly_charges * 12
    if churn_prob > 0.7:
        risk_level = "🔴 HIGH RISK"
        recommendations.append("💰 20% discount offer karo 3 months")
        recommendations.append("🎁 Free upgrade to premium plan")
        recommendations.append("📞 Dedicated support assign karo")
        recommendations.append("🎬 Free OTT subscription 3 months")
    elif churn_prob > 0.4:
        risk_level = "🟡 MEDIUM RISK"
        recommendations.append("📧 Special offer email bhejo")
        recommendations.append("💳 Loyalty points double karo")
        recommendations.append("📱 New features showcase karo")
    else:
        risk_level = "🟢 LOW RISK"
        recommendations.append("✅ Customer satisfied hai")
        recommendations.append("🌟 Referral program offer karo")
    retention_cost = monthly_charges * 0.2 * 3
    net_saving = revenue_at_risk - retention_cost
    return risk_level, recommendations, revenue_at_risk, retention_cost, net_saving

st.set_page_config(page_title="Customer Churn Prevention", page_icon="🏢", layout="wide")
st.title("🏢 Customer Churn Prediction System")
st.markdown("---")

# Top metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", "7,043")
col2.metric("High Risk", "892 🔴")
col3.metric("Revenue at Risk", "₹53.5L")
col4.metric("Model Accuracy", "87%")

st.markdown("---")

# Sidebar inputs
st.sidebar.title("Customer Details Bharo")
tenure = st.sidebar.slider("Tenure (Months)", 0, 72, 12)
monthly_charges = st.sidebar.number_input("Monthly Charges (Rs.)", 20.0, 120.0, 65.0)
total_charges = monthly_charges * tenure
contract = st.sidebar.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
internet = st.sidebar.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
online_security = st.sidebar.selectbox("Online Security", ["Yes", "No"])
tech_support = st.sidebar.selectbox("Tech Support", ["Yes", "No"])
paperless = st.sidebar.selectbox("Paperless Billing", ["Yes", "No"])
senior = st.sidebar.selectbox("Senior Citizen", ["No", "Yes"])

contract_map = {"Month-to-month": 0, "One year": 1, "Two year": 2}
internet_map = {"DSL": 0, "Fiber optic": 1, "No": 2}
yes_no = {"Yes": 1, "No": 0}

customer_data = {
    'gender': 1, 'SeniorCitizen': yes_no[senior],
    'Partner': 1, 'Dependents': 0,
    'tenure': tenure, 'PhoneService': 1,
    'MultipleLines': 0,
    'InternetService': internet_map[internet],
    'OnlineSecurity': yes_no[online_security],
    'OnlineBackup': 0, 'DeviceProtection': 0,
    'TechSupport': yes_no[tech_support],
    'StreamingTV': 0, 'StreamingMovies': 0,
    'Contract': contract_map[contract],
    'PaperlessBilling': yes_no[paperless],
    'PaymentMethod': 2,
    'MonthlyCharges': monthly_charges,
    'TotalCharges': total_charges
}

if st.sidebar.button("🔍 Predict Churn", use_container_width=True):
    input_df = pd.DataFrame([customer_data])[feature_names]
    churn_prob = model.predict_proba(input_df)[0][1]
    risk_level, recommendations, revenue_at_risk, retention_cost, net_saving = get_recommendation(
        churn_prob, monthly_charges, tenure
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Prediction Result")
        st.markdown(f"### {risk_level}")

        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=churn_prob * 100,
            title={'text': "Churn Probability"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "red" if churn_prob > 0.7 else "orange" if churn_prob > 0.4 else "green"},
                'steps': [
                    {'range': [0, 40], 'color': "lightgreen"},
                    {'range': [40, 70], 'color': "lightyellow"},
                    {'range': [70, 100], 'color': "lightcoral"}
                ]
            },
            number={'suffix': "%"}
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Business Impact")
        m1, m2, m3 = st.columns(3)
        m1.metric("Revenue at Risk", f"Rs. {revenue_at_risk:,.0f}")
        m2.metric("Retention Cost", f"Rs. {retention_cost:,.0f}")
        m3.metric("Net Saving", f"Rs. {net_saving:,.0f}")

        st.subheader("AI Recommendations")
        for r in recommendations:
            st.write(r)

    st.markdown("---")
    st.subheader("Customer Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tenure", f"{tenure} months")
    c2.metric("Monthly Bill", f"Rs. {monthly_charges:.0f}")
    c3.metric("Contract", contract)
    c4.metric("Internet", internet)

st.markdown("---")
st.caption("Built with XGBoost + SHAP + Streamlit | AI-Powered Churn Prevention")
