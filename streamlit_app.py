import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
from models.prediction_engine import PredictionEngine

st.set_page_config(page_title="UniPay FraudX", layout="wide")

#  👉 NAVIGATION

nav_col1, nav_col2 = st.columns([6,2])

with nav_col1:
    page = st.radio(
        "Navigation",
        ["Home", "Analysis", "Dashboard", "Prediction", "About"],
        horizontal=True,
        label_visibility="collapsed"
    )

with nav_col2:
    theme = st.radio(
        "Theme",
        ["🌙", "☀️"],
        horizontal=True,
        label_visibility="collapsed"
    )

if theme == "🌙":
    theme = "Dark"
else:   
    theme = "Light"
# 🎨 DYNAMIC CSS
if theme == "Dark":
    st.markdown("""
    <style>

    /* Background */
    [data-testid="stAppViewContainer"] {
        background-color: #0e1117;
    }

    /* Text */
    h1, h2, h3, h4, h5, h6, p, label, div {
        color: white !important;
    }

    /* Navbar */
    div[data-testid="stRadio"] > div {
        flex-direction: row;
        justify-content: center;
        gap: 20px;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(90deg,#22c55e,#16a34a);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: 0.3s;
        font-weight: 600;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #16a34a, #22c55e);
    }

    </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <style>

    /* Background */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff;
    }

    /* Text */
    h1, h2, h3, h4, h5, h6, p, label, div {
        color: black !important;
    }

    /* Navbar */
    div[data-testid="stRadio"] > div {
        flex-direction: row;
        justify-content: center;
        gap: 20px;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(90deg,#22c55e,#16a34a);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: 0.3s;
        font-weight: 600;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #22c55e,#16a34a);
    }

    </style>
    """, unsafe_allow_html=True)


# ------------------ LOAD DATA ------------------
df=pd.read_excel("dataset/data.xlsx")
model = pickle.load(open("fraud_model.pkl", "rb"))
engine = PredictionEngine(model)

# ------------------ CUSTOM CSS ------------------

# 🎨 DYNAMIC CSS
if theme == "Dark":
    st.markdown("""
                <style>
                /* REMOVE SIDEBAR */
                section[data-testid="stSidebar"] {
                    display: none;
                    }
                /* BACKGROUND */
                [data-testid="stAppViewContainer"] {
                    background-color: #0e1117;
                    }
                /* HEADER */
                [data-testid="stHeader"] {
                    background: transparent;
                    }
                /* TEXT */
                h1, h2, h3, h4, h5, h6 {
                    color: white !important;
                    text-align: center;
                    }
                    p, label, div {
                        color: #e4e6eb !important;
                        }
                /* NAVBAR */
                div[data-testid="stRadio"] > div {
                    flex-direction: row;
                    justify-content: center;
                    gap: 20px;
                    }
                /* DATAFRAME */
                [data-testid="stDataFrame"] {
                    background-color: #1c1f26;
                    border-radius: 12px;
                    padding: 10px;
                    }
                 
                /* BUTTON */
                
                .stButton > button {
        background: linear-gradient(90deg,#22c55e,#16a34a);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: 0.3s;
        font-weight: 600;
    }
                .stButton > button:hover {
                    transform: scale(1.05);
                    background: linear-gradient(90deg,#22c55e,#16a34a);
                    }
                /* FULL WIDTH */
                .block-container {
                    padding-left: 2rem;
                    padding-right: 2rem;
                    }
                    </style>"""
                    , unsafe_allow_html=True)
else:
    st.markdown("""
    <style>

    section[data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #ffffff;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    h1, h2, h3, h4, h5, h6 {
        color: black !important;
        text-align: center;
    }

    p, label, div {
        color: #222 !important;
    }

    div[data-testid="stRadio"] > div {
        flex-direction: row;
        justify-content: center;
        gap: 20px;
    }

    [data-testid="stDataFrame"] {
        background-color: #f5f5f5;
        border-radius: 12px;
        padding: 10px;
    }

    .stButton > button {
        background: linear-gradient(90deg,#22c55e,#16a34a);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: 0.3s;
        font-weight: 600;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg,#22c55e,#16a34a);
    }

    .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
    }

    </style>
    """, unsafe_allow_html=True)

# ================== HOME ==================
if page == "Home":
    
    st.markdown("""
    <style>
    .hero {
        height: 90vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-image: url("https://elmeurope.com/wp-content/uploads/2024/10/elm-europe-high-demand-prediction-main.jpg");
        background-size: cover;
        background-position: center;
        color: white;
        text-align: center;
        border-radius: 20px;
    }

    .overlay {
        background: rgba(0,0,0,0.6);
        padding: 50px;
        border-radius: 20px;
    }

    .title {
        font-size: 50px;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    .subtitle {
        font-size: 18px;
        margin-top: 10px;
    }

    .btn {
        margin-top: 20px;
        padding: 12px 30px;
        background-color: #f5f5f5;
        color: #333;
        border-radius: 10px;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        background-color: #22c55e;
        color: white;
    }
    </style>

    <div class="hero">
        <div class="overlay">
            <div class="title">🚀 SMART TRANSACTION FRAUD DETECTION SYSTEM</div>
            <div class="subtitle">
            Detect fraudulent transactions in real-time with AI-powered insights
            </div>
            <div class="btn">🚀 UniPay FraudX</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Start Analysis"):
            st.info("Navigate to the Analysis page from the menu.")

    with col2:
        if st.button("📊 View Dashboard"):
            st.info("Navigate to the Dashboard page from the menu.")
        
    st.markdown("---")
    st.subheader("📊 Key Security Metrics")

    total_txn = len(df)
    fraud_txn = len(df[df["label"] == "Suspicious"])
    safe_txn = len(df[df["label"] == "Normal"])
    fraud_rate = round((fraud_txn / total_txn) * 100, 2) if total_txn else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Transactions", total_txn)

    with col2:
        st.metric("Fraud Cases", fraud_txn)

    with col3:
        st.metric("Safe Cases", safe_txn)

    with col4:
        st.metric("Fraud Rate", f"{fraud_rate}%")
        
    st.markdown("---")
    st.subheader("📈 Fraud Intelligence Analytics")    
    fraud_count = df["label"].value_counts().sort_index()
    fig_home = px.pie(
    values=fraud_count.values,
    names=["Normal", "Fraud"],
    hole=0.5,
    title="Fraud vs Normal Transactions"
    )
    fig_home.update_traces(
    marker=dict(colors=["#28a745", "#dc3545"])
    )
    risk_data = df["label"].value_counts().reset_index()
    risk_data.columns = ["Type", "Count"]
    
    fig_risk = px.bar(
    risk_data,
    x="Type",
    y="Count",
    title="Risk Distribution"
    )
    fig_risk.update_traces(
    marker_color="#22c55e"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig_home, use_container_width=True)
        
    with col2:
        st.plotly_chart(fig_risk, use_container_width=True)    
        
    st.markdown("---")
    st.subheader("🛡 Why UniPay FraudX?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("⚡ Real-Time Fraud Detection")
    with col2:
        st.warning("🤖 AI Risk Analysis")
    with col3:
        st.error("🚨 Fraud Intelligence Monitoring") 
        
    st.markdown("---")
    st.caption("© 2026 UniPay FraudX | AI-Powered Fraud Intelligence")

# ================== ANALYSIS ==================
elif page == "Analysis":

    st.title("📊 Data Analysis")

    df = pd.read_excel("dataset/data.xlsx")

    st.subheader("📁 Dataset Preview")
    st.dataframe(df)

    st.subheader("📌 Basic Info")
    st.write(df.describe())

    # Tabs
    tab1, tab2 = st.tabs(["Charts", "Insights"])

    with tab1:
        st.subheader("📊 Charts")

        fig1 = px.histogram(df, x="amount", color="label")
        fig1.update_traces(
            marker_line_width=1.5,
            marker_line_color="black")
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.scatter(df, x="amount", y="txn_count_1hr", color="label")
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("💡 Insights")
        
        st.markdown("""
                    🔍 **Key Observations:**
                    
                    • Transactions with **higher amounts and frequent activity** show a strong pattern of suspicious behavior.
                    
                    • **Late-night transactions (0–6 hours)** are more likely to be flagged as risky.
                    
                    • Users with **high transaction counts within short time** may indicate fraud attempts.
                    
                    • Normal transactions are generally **low frequency and moderate amount**.
                    
                    💡 **Conclusion:**  
                    
                    Combining transaction amount, frequency, and timing significantly improves fraud detection accuracy.
                    """)

# ================== DASHBOARD ==================
elif page == "Dashboard":

    st.title("📊 Transaction Analysis Dashboard")
    fig_bar = px.bar(
            df,
            x="hour",
            y="txn_count_1hr",
            color="label",
            title=" 🕒 Transactions by Hour"
            )
    fig_bar.update_traces(marker_line_color='black', marker_line_width=1)
    fig_bar.update_layout(plot_bgcolor="#f5f5f5")
    
    
    df_line = df.groupby("hour")["amount"].mean().reset_index()
    fig_line= px.line(df_line,
                      x="hour",
                      y="amount",
                      title=" 📈 Amount Trend Over Time")
    fig_line.update_traces(mode="markers+lines", marker=dict(size=8, color="#22c55e"))
    fig_line.update_layout(plot_bgcolor="#f5f5f5")
        
    fraud_count = df["label"].value_counts()
    fig_donut = px.pie(
            values=fraud_count.values,
            names=["Normal", "Fraud"],
            hole=0.5,
            title=" 📊 Fraud vs Normal")
    fig_donut.update_layout(annotations=[dict(text='Transaction<br>Split', x=0.5, y=0.5, font_size=22, showarrow=False, font = dict(size=20, color="#22c55e"))])
    fig_donut.update_layout(plot_bgcolor="#f5f5f5")
    
    fig_location = px.pie(df,
                     names="location_type",
                     title=" 📍 Transaction by Location")
    fig_location.update_layout(plot_bgcolor="#f5f5f5")
        
    fig_sender = px.bar(
            df,
            x="sender_type",
            color="receiver_type",
            title=" 📊 Sender vs Receiver Comparison",
            barmode="group")
    fig_sender.update_layout(plot_bgcolor="#f5f5f5")
        
    fig_box = px.box(
            df,
            x="label",
            y="amount",
            title=" 📈 Amount Distribution (Fraud vs Normal)")
    fig_box.update_layout(plot_bgcolor="#f5f5f5")
    
    # ------------------ LAYOUT ------------------

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_line, use_container_width=True)

    st.plotly_chart(fig_donut, use_container_width=True, key="donut chart")

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(fig_location, use_container_width=True)
    with col4:
        st.plotly_chart(fig_sender, use_container_width=True)

# ================== PREDICTION ==================
elif page == "Prediction":

    st.title("🔮 Predict Transaction")

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        value=1000.0
    )

    txn = st.number_input(
        "Txn Count",
        min_value=0,
        value=1
    )

    hour = st.slider(
        "Hour",
        0,
        23,
        12
    )

    if st.button("Predict"):

        result = engine.predict(
            amount,
            txn,
            hour
        )

        st.progress(confidence / 100)
        st.caption(f"{confidence:.2f}% confidence")

        if pred == 1:
            st.markdown(f"""
                        <div style="
                        background: linear-gradient(135deg, #dc2626, #ef4444);
                        padding: 25px;
                        border-radius: 15px;
                        color: white;
                        text-align: left;
                        font-size: 18px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                        ">
                        🚨 <b>Suspicious Transaction Detected</b><br><br>
                        💰 Amount: {amount}<br>
                        🔁 Transactions: {txn}<br>
                        ⏰ Hour: {hour}<br>
                        📊 Confidence: {confidence:.2f}%<br><br>
                        📈 Risk Score: {risk_score}<br><br>
                        ⚠️ Risk Level: {risk_level}<br>
                        📝 Risk Insight: {risk_message}<br>
                        📋 Reason: {reason}<br>
                        ⚠️ <b>Recommendation:</b><br>
                        • Verify transaction immediately<br>
                        • Enable OTP or 2FA authentication<br>
                        • Monitor account activity closely
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="
            background: linear-gradient(135deg, #22c55e, #16a34a);
            padding: 25px;
            border-radius: 15px;
            color: white;
            text-align: left;
            font-size: 18px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        ">
        ✅ <b>Normal Transaction</b><br><br>

        💰 Amount: {amount}<br>
        🔁 Transactions: {txn}<br>
        ⏰ Hour: {hour}<br>
        📊 Confidence: {confidence:.2f}%<br><br>
        📈 Risk Score: {risk_score}<br><br>
        ⚠️ Risk Level: {risk_level}<br>
        📝 Risk Insight: {risk_message}<br>
        📋 Reason: {reason}<br><br>

        👍 <b>Recommendation:</b><br>
        • Transaction appears safe<br>
        • No immediate action required<br>
        • Continue normal usage
        </div>
        """, unsafe_allow_html=True)
        if not result["success"]:

            for error in result["errors"]:
                st.error(error)

        else:

            confidence = result["confidence"]
            risk_score = result["risk_score"]
            risk_level = result["risk_level"]

            st.progress(confidence / 100)

            c1, c2 = st.columns(2)
            with c1:
                st.metric(
                    "Confidence",
                    f"{confidence:.2f}%"
                    )
                st.metric(
                    "Risk Score",
                    risk_score
                    )

            with c2:
                st.metric(
                    "Risk Level",
                    risk_level
                    )

                st.metric(
                    "Recommendation",
                    result["recommendation"]
                    )

            st.subheader("Reasons")

            for reason in result["reasons"]:
                st.write(f"• {reason}")

            if result["prediction"]:
                st.error(
                    "🚨 Suspicious Transaction"
                )
            else:
                st.success(
                    "✅ Normal Transaction"
                )
    

    
# ================== ABOUT ==================
elif page == "About":

    st.title("👨‍💻 About UniPay FraudX")

    st.markdown("""
    **UniPay FraudX** is an AI-powered fraud detection system designed to identify and prevent fraudulent transactions in real-time. Leveraging advanced machine learning algorithms, UniPay FraudX analyzes transaction patterns, user behavior, and contextual data to accurately flag suspicious activities.

    Key Features:
    - Real-time fraud detection with high accuracy
    - User-friendly dashboard for monitoring transactions
    - Customizable alerts and notifications
    - Comprehensive data analysis tools

    Developed by a passionate team of data scientists and engineers, UniPay FraudX aims to provide businesses with a robust solution to combat financial fraud and enhance security.
    """)
    
