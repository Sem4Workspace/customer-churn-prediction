import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --- Page config ---
st.set_page_config(
    page_title="Telecom Customer Churn Prediction",
    page_icon=None,
    layout="wide",
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 700;
        color: #4fc3f7;
        text-align: center;
        padding: 1rem 0 0.3rem 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #ce93d8;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 1rem;
    }
    .churn-yes {
        background-color: #ffeaea;
        border: 2px solid #e74c3c;
    }
    .churn-no {
        background-color: #eafff1;
        border: 2px solid #27ae60;
    }
    .result-label {
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .result-prob {
        font-size: 1.1rem;
        color: #444;
    }
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a1a2e;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.4rem;
        margin-bottom: 1rem;
    }
    div.stButton > button {
        width: 100%;
        background-color: #1a1a2e;
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.6rem 2rem;
        border-radius: 8px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #16213e;
        color: #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)


# --- Load model artifacts ---
@st.cache_resource
def load_artifacts():
    model = joblib.load("models/xgboost_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
    feature_names = joblib.load("models/feature_names.pkl")
    return model, scaler, feature_names


model, scaler, feature_names = load_artifacts()

# --- Header ---
st.markdown('<div class="main-header">Telecom Customer Churn Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Predict whether a customer is likely to churn using an XGBoost model trained on telco data</div>', unsafe_allow_html=True)

st.markdown("---")

# ========== INPUT FORM ==========
col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown('<div class="section-title">Customer Information</div>', unsafe_allow_html=True)

    gender = st.selectbox("Gender", ["Female", "Male"])
    senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
    partner = st.selectbox("Partner", ["No", "Yes"])
    dependents = st.selectbox("Dependents", ["No", "Yes"])

    st.markdown('<div class="section-title">Account Information</div>', unsafe_allow_html=True)

    tenure = st.slider("Tenure (months)", min_value=0, max_value=72, value=12)
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    paperless_billing = st.selectbox("Paperless Billing", ["No", "Yes"])
    payment_method = st.selectbox("Payment Method", [
        "Bank transfer (automatic)",
        "Credit card (automatic)",
        "Electronic check",
        "Mailed check",
    ])
    monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, value=50.0, step=0.5)
    total_charges = st.number_input("Total Charges ($)", min_value=0.0, max_value=10000.0, value=600.0, step=1.0)

with col_right:
    st.markdown('<div class="section-title">Phone Service</div>', unsafe_allow_html=True)

    phone_service = st.selectbox("Phone Service", ["No", "Yes"])
    if phone_service == "Yes":
        multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes"])
    else:
        multiple_lines = "No phone service"
        st.info("Multiple Lines: Not applicable (no phone service)")

    st.markdown('<div class="section-title">Internet Service</div>', unsafe_allow_html=True)

    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

    if internet_service != "No":
        online_security = st.selectbox("Online Security", ["No", "Yes"])
        online_backup = st.selectbox("Online Backup", ["No", "Yes"])
        device_protection = st.selectbox("Device Protection", ["No", "Yes"])
        tech_support = st.selectbox("Tech Support", ["No", "Yes"])
        streaming_tv = st.selectbox("Streaming TV", ["No", "Yes"])
        streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes"])
    else:
        st.info("Internet-dependent services: Not applicable (no internet service)")
        online_security = "No internet service"
        online_backup = "No internet service"
        device_protection = "No internet service"
        tech_support = "No internet service"
        streaming_tv = "No internet service"
        streaming_movies = "No internet service"

st.markdown("---")


# ========== FEATURE ENCODING ==========
def encode_input():
    """Encode raw form inputs into the 30-feature vector matching training data."""
    yn = {"Yes": 1, "No": 0}

    row = {
        "gender": 1 if gender == "Male" else 0,
        "SeniorCitizen": yn[senior_citizen],
        "Partner": yn[partner],
        "Dependents": yn[dependents],
        "tenure": tenure,
        "PhoneService": yn[phone_service],
        "PaperlessBilling": yn[paperless_billing],
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,

        # MultipleLines
        "MultipleLines_Yes": 1 if multiple_lines == "Yes" else 0,
        "MultipleLines_NoService": 1 if multiple_lines == "No phone service" else 0,

        # Internet-dependent services
        "OnlineSecurity_Yes": 1 if online_security == "Yes" else 0,
        "OnlineSecurity_NoInternet": 1 if online_security == "No internet service" else 0,
        "OnlineBackup_Yes": 1 if online_backup == "Yes" else 0,
        "OnlineBackup_NoInternet": 1 if online_backup == "No internet service" else 0,
        "DeviceProtection_Yes": 1 if device_protection == "Yes" else 0,
        "DeviceProtection_NoInternet": 1 if device_protection == "No internet service" else 0,
        "TechSupport_Yes": 1 if tech_support == "Yes" else 0,
        "TechSupport_NoInternet": 1 if tech_support == "No internet service" else 0,
        "StreamingTV_Yes": 1 if streaming_tv == "Yes" else 0,
        "StreamingTV_NoInternet": 1 if streaming_tv == "No internet service" else 0,
        "StreamingMovies_Yes": 1 if streaming_movies == "Yes" else 0,
        "StreamingMovies_NoInternet": 1 if streaming_movies == "No internet service" else 0,

        # One-hot encoded (drop_first: DSL is reference for InternetService,
        # Month-to-month for Contract, Bank transfer for PaymentMethod)
        "InternetService_Fiber optic": 1 if internet_service == "Fiber optic" else 0,
        "InternetService_No": 1 if internet_service == "No" else 0,
        "Contract_One year": 1 if contract == "One year" else 0,
        "Contract_Two year": 1 if contract == "Two year" else 0,
        "PaymentMethod_Credit card (automatic)": 1 if payment_method == "Credit card (automatic)" else 0,
        "PaymentMethod_Electronic check": 1 if payment_method == "Electronic check" else 0,
        "PaymentMethod_Mailed check": 1 if payment_method == "Mailed check" else 0,
    }

    df = pd.DataFrame([row])
    # Ensure column order matches training
    df = df[feature_names]
    return df


# ========== PREDICTION ==========
_, center_col, _ = st.columns([1, 2, 1])
with center_col:
    predict_clicked = st.button("Predict Churn")

if predict_clicked:
    input_df = encode_input()
    input_scaled = scaler.transform(input_df)

    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0]

    churn_prob = probability[1] * 100
    no_churn_prob = probability[0] * 100

    st.markdown("---")

    res_left, res_right = st.columns(2, gap="large")

    with res_left:
        if prediction == 1:
            st.markdown(f"""
            <div class="result-box churn-yes">
                <div class="result-label" style="color: #e74c3c;">CHURN PREDICTED</div>
                <div class="result-prob">This customer is likely to leave the service.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-box churn-no">
                <div class="result-label" style="color: #27ae60;">NO CHURN</div>
                <div class="result-prob">This customer is likely to stay with the service.</div>
            </div>
            """, unsafe_allow_html=True)

    with res_right:
        st.markdown(f"""
        <div class="result-box" style="background-color: #f7f9fc; border: 2px solid #d0d7de;">
            <div class="result-label" style="color: #1a1a2e;">Prediction Confidence</div>
            <div class="result-prob">
                Churn Probability: <strong>{churn_prob:.1f}%</strong><br>
                Retention Probability: <strong>{no_churn_prob:.1f}%</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Progress bar visualization
    st.markdown("")
    st.markdown("**Churn Risk Meter**")
    st.progress(churn_prob / 100)

    if churn_prob >= 70:
        risk_level = "HIGH RISK"
        risk_color = "#e74c3c"
    elif churn_prob >= 40:
        risk_level = "MEDIUM RISK"
        risk_color = "#f39c12"
    else:
        risk_level = "LOW RISK"
        risk_color = "#27ae60"

    st.markdown(f'<p style="text-align:center; font-size:1.2rem; font-weight:600; color:{risk_color};">{risk_level} -- {churn_prob:.1f}% churn probability</p>', unsafe_allow_html=True)

    # Feature summary
    with st.expander("View Input Feature Summary"):
        input_df_display = encode_input()
        st.dataframe(input_df_display, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown(
    '<p style="text-align:center; color:#888; font-size:0.85rem;">'
    'Telecom Churn Prediction -- Built with XGBoost and Streamlit'
    '</p>',
    unsafe_allow_html=True,
)
