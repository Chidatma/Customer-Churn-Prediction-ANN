import streamlit as st
import pandas as pd
import numpy as np
import pickle

from tensorflow.keras.models import load_model

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="European Bank Customer Churn Prediction",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_ann_model():
    model = load_model("european_bank.model.keras", compile=False)
    return model

model = load_ann_model()

# =====================================================
# LOAD SCALER
# =====================================================

with open("scaler.pkl","rb") as file:
    scaler = pickle.load(file)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

.title{
    font-size:42px;
    color:#003366;
    text-align:center;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:18px;
    margin-bottom:25px;
}

.section{
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0px 0px 8px rgba(0,0,0,0.15);
    margin-bottom:20px;
}

</style>
""",unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("European Bank")


page = st.sidebar.radio(
    "Navigation",
    [
        "Customer Prediction",
        "About Project",
        "Model Information"
    ]
)






st.sidebar.success("")

# =====================================================
# CUSTOMER PREDICTION PAGE
# =====================================================

if page == "Customer Prediction":

    st.markdown(
        "<div class='title'>European Bank Customer Churn Prediction</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>AI Powered Customer Retention Analytics Dashboard</div>",
        unsafe_allow_html=True
    )

    left_column,right_column = st.columns([2,1])

    # =====================================================
    # LEFT COLUMN
    # =====================================================

    with left_column:


        st.subheader("Customer Information")

        col1,col2 = st.columns(2)

        with col1:

            credit_score = st.slider(
                "Credit Score",
                300,
                900,
                650
            )

            age = st.slider(
                "Age",
                18,
                100,
                35
            )

            gender = st.selectbox(
                "Gender",
                ["Male","Female"]
            )

            geography = st.selectbox(
                "Geography",
                ["France","Germany","Spain"]
            )

            tenure = st.slider(
                "Tenure",
                0,
                10,
                5
            )

        with col2:

            balance = st.number_input(
                "Balance",
                min_value=0.0,
                value=50000.0,
                step=1000.0
            )

            num_products = st.selectbox(
                "Number of Products",
                [1,2,3,4]
            )

            has_card = st.selectbox(
                "Has Credit Card",
                ["Yes","No"]
            )

            active_member = st.selectbox(
                "Is Active Member",
                ["Yes","No"]
            )

            salary = st.number_input(
                "Estimated Salary",
                min_value=0.0,
                value=50000.0,
                step=1000.0
            )

        predict_button = st.button(
            "Predict Customer Churn",
            use_container_width=True
        )

        st.markdown("</div>",unsafe_allow_html=True)

    # =====================================================
    # PREPROCESSING
    # =====================================================

    probability = None

    if predict_button:

        gender = 1 if gender=="Male" else 0

        geo_germany = 1 if geography=="Germany" else 0
        geo_spain = 1 if geography=="Spain" else 0

        has_card = 1 if has_card=="Yes" else 0
        active_member = 1 if active_member=="Yes" else 0

        input_df = pd.DataFrame({

            "CreditScore":[credit_score],
            "Gender":[gender],
            "Age":[age],
            "Tenure":[tenure],
            "Balance":[balance],
            "NumOfProducts":[num_products],
            "HasCrCard":[has_card],
            "IsActiveMember":[active_member],
            "EstimatedSalary":[salary],
            "Geography_Germany":[geo_germany],
            "Geography_Spain":[geo_spain]

        })

        input_scaled = scaler.transform(input_df)

        prediction = model.predict(input_scaled)

        probability = float(prediction[0][0])

        churn = probability >= 0.5

    # =====================================================
    # RIGHT COLUMN
    # =====================================================

    with right_column:


        st.subheader("Prediction Dashboard")

        if probability is not None:

            # Prediction
            if churn:
                st.error("Customer is likely to CHURN")
            else:
                st.success("Customer is likely to STAY")

            # Probability
            st.metric(
                "Churn Probability",
                f"{probability*100:.2f}%"
            )

            # Progress Bar
            st.progress(probability)

            st.markdown("---")

            # Risk Level
            if probability < 0.30:

                st.success("🟢 LOW RISK")

            elif probability < 0.70:

                st.warning("🟡 MEDIUM RISK")

            else:

                st.error("🔴 HIGH RISK")

            st.markdown("---")

            # AI Recommendation
            st.subheader("AI Recommendation")

            if probability >= 0.70:

                st.write("Offer a customer retention campaign.")
                st.write("Assign a relationship manager.")
                st.write("Recommend additional banking products.")
                st.write("Provide personalized offers.")

            elif probability >= 0.30:

                st.write("Increase customer engagement.")
                st.write("Offer loyalty rewards.")
                st.write("Recommend product bundles.")

            else:

                st.write("Customer relationship is healthy.")
                st.write("Maintain regular engagement.")
                st.write("Continue existing banking services.")

            st.markdown("---")

            # Customer Summary
            st.subheader("Customer Summary")

            st.write(f"Credit Score : {credit_score}")
            st.write(f"Age : {age}")
            st.write(f"Geography : {geography}")
            st.write(f"Products : {num_products}")
            st.write(f"Balance : ₹ {balance:,.2f}")
            st.write(f"Estimated Salary : ₹ {salary:,.2f}")

            st.write(
                f"Active Member : {'Yes' if active_member==1 else 'No'}"
            )

        else:

            st.info("Fill customer details and click Predict.")

        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# ABOUT PROJECT PAGE
# =====================================================

elif page == "About Project":

    st.title("About Project")

    st.markdown("""
### Customer Engagement & Product Utilization Analytics for Retention Strategy

This project predicts whether a customer will leave the bank using an Artificial Neural Network.

### Business Problem

Banks lose valuable customers because of low engagement, weak product adoption, and inactive relationships.

This application helps identify customers who are likely to churn so that proactive retention strategies can be applied.

### Business Objectives

- Reduce Customer Churn
- Improve Customer Engagement
- Increase Product Adoption
- Identify High-Risk Customers
- Support Data-Driven Decisions

### Dataset Features

- Credit Score
- Geography
- Gender
- Age
- Tenure
- Balance
- Number of Products
- Credit Card
- Active Member
- Estimated Salary

### Target Variable

Exited

0 → Customer Stays

1 → Customer Churns
""")

# =====================================================
# MODEL INFORMATION PAGE
# =====================================================

elif page == "Model Information":

    st.title("Model Information")

    st.subheader("Artificial Neural Network")

    st.write("Input Layer : 11 Features")

    st.write("Hidden Layer 1 : 11 Neurons")

    st.write("Hidden Layer 2 : 7 Neurons")

    st.write("Hidden Layer 3 : 6 Neurons")

    st.write("Output Layer : 1 Neuron")

    st.markdown("---")

    st.subheader("Activation Functions")

    st.write("Hidden Layers : ReLU")

    st.write("Output Layer : Sigmoid")

    st.markdown("---")

    st.subheader("Training Configuration")

    st.write("Optimizer : Adam")

    st.write("Loss Function : Binary Crossentropy")

    st.write("Task : Binary Classification")

    st.markdown("---")

    st.subheader("Model Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("Accuracy", "86%")

    col2.metric("Precision", "84%")

    col3.metric("Recall", "81%")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
"""
European Bank Customer Engagement & Product Utilization Analytics

Developed by Chidatma
"""
)