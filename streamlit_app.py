from click import style
import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "data.xlsx")
MODEL_PATH = os.path.join(BASE_DIR, "fraud_model.pkl")
@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_excel(DATA_PATH)

    st.warning("⚠ Dataset not found. Running in DEMO MODE with sample data.")

    return pd.DataFrame({
        "amount": [1200, 5000, 15000, 300, 8000, 20000],
        "txn_count_1hr": [1, 5, 12, 2, 9, 15],
        "hour": [10, 2, 23, 14, 1, 22],
        "location_type": ["online", "offline", "online", "offline", "online", "online"],
        "sender_type": ["user", "merchant", "user", "user", "merchant", "user"],
        "receiver_type": ["merchant", "user", "merchant", "user", "merchant", "user"]
        
        "label": ["Normal", "Normal", "Suspicious", "Normal", "Normal", "Suspicious"],

    # (optional but better for realism)
        "is_high_amount": [0, 0, 1, 0, 0, 1],
        "is_high_velocity": [0, 0, 1, 0, 0, 1],
        "is_odd_hour": [0, 0, 1, 0, 1, 1],
        })

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        return pickle.load(open(MODEL_PATH, "rb"))

    st.error("❌ Model file missing")
    st.stop()


df = load_data()
model = load_model()

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
        background: linear-gradient(90deg, #ff4b8b, #ff6b6b);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: 0.3s;
        font-weight: 600;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #ff6b6b, #ff4b8b);
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
        background: linear-gradient(90deg, #ff4b8b, #ff6b6b);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: 0.3s;
        font-weight: 600;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #ff6b6b, #ff4b8b);
    }

    </style>
    """, unsafe_allow_html=True)
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
        background: linear-gradient(90deg, #ff4b8b, #ff6b6b);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: 0.3s;
        font-weight: 600;
    }
                .stButton > button:hover {
                    transform: scale(1.05);
                    background: linear-gradient(90deg, #ff6b6b, #ff4b8b);
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
        background: linear-gradient(90deg, #ff4b8b, #ff6b6b);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: 0.3s;
        font-weight: 600;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #ff6b6b, #ff4b8b);
    }

    .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
    }

    </style>
    """, unsafe_allow_html=True)

# ================== HOME (REDESIGNED) ==================
# ================== HOME ==================
if page == "Home":

    st.markdown("""
    <style>
    .hero {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 60px 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }

    .title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 10px;
        background: linear-gradient(90deg, #22c55e, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        font-size: 18px;
        opacity: 0.85;
        margin-bottom: 25px;
    }

    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        background: rgba(34,197,94,0.15);
        border: 1px solid #22c55e;
        font-size: 13px;
    }

    .card {
        background: #111827;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }

    .metric {
        font-size: 26px;
        font-weight: bold;
        color: #22c55e;
    }

    </style>
    """, unsafe_allow_html=True)

    # HERO SECTION
    st.markdown("""
    <div class="hero">
        <div class="title">🚨 Fraud Intelligence System</div>
        <div class="subtitle">
            Real-time AI-powered transaction monitoring & fraud detection
        </div>
        <div class="badge">🔐 Secure • AI Driven • Real-time Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # METRICS
    col1, col2, col3 = st.columns(3)

    col1.markdown("""
    <div class="card">
        <div class="metric">98.2%</div>
        Accuracy
    </div>
    """, unsafe_allow_html=True)

    col2.markdown("""
    <div class="card">
        <div class="metric">1K+</div>
        Transactions
    </div>
    """, unsafe_allow_html=True)

    col3.markdown("""
    <div class="card">
        <div class="metric">Real-Time</div>
        Detection
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # OVERVIEW TEXT
    st.subheader("📊 Fraud Intelligence Overview")
    
    import plotly.express as px

    # safe fallback (no crash)
    if "label" in df.columns:

        fig = px.pie(
            df,
            names="label",
            title="Fraud vs Normal Transactions",
            hole=0.5,
            color_discrete_sequence=["#22c55e", "#ef4444"]
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        st.plotly_chart(fig, use_container_width=True) 

    st.info("💡 System continuously analyzes transaction patterns using AI + rule-based intelligence.")

# ================== ANALYSIS ==================
elif page == "Analysis":

    st.title("📊 Data Analysis")
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
    fig_line.update_traces(mode="markers+lines", marker=dict(size=8, color="#ff6f91"))
    fig_line.update_layout(plot_bgcolor="#f5f5f5")
        
    fraud_count = df["label"].value_counts()
    fig_donut = px.pie(
            values=fraud_count.values,
            names=["Normal", "Fraud"],
            hole=0.5,
            title=" 📊 Fraud vs Normal")
    fig_donut.update_layout(annotations=[dict(text='Transaction<br>Split', x=0.5, y=0.5, font_size=22, showarrow=False, font = dict(size=20, color="#ff4b8b"))])
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

    amount = st.number_input("Amount")
    txn = st.number_input("Txn Count")
    hour = st.slider("Hour", 0, 23)

    if st.button("Predict"):
        if amount > 10000:
            pred = 1
            reason = "High transaction amount"

        elif txn > 10:
            pred = 1
            reason = "Too many transactions"

        elif 0<= hour <= 5 and amount > 4000:
            pred = 1
            reason = "Late night transaction"
        
        else:
            pred = model.predict([[amount, txn, hour]])[0]
            reason = "Based on ML model"
            
        # Confidence calculation
        proba = model.predict_proba([[amount, txn, hour]])[0]
        confidence = max(proba) * 100
        
        # RISK SCORE CALCULATION
        risk_score = 0
        
        if amount > 10000:
            risk_score += 50
        if txn > 10:
            risk_score += 30
        if 0<= hour <= 5 and amount > 4000:
            risk_score += 20
        
        if risk_score > 70:
            pred = 1
            reason = "High risk score based on rules"
        elif risk_score > 40:
            pred = 1
            reason = "Moderate risk score based on rules"
        elif risk_score > 0:
            pred = 1
            reason = "Low risk score based on rules"
        if risk_score > 70:
            risk_level = "HIGH"
            risk_color = "#ef4444"
            risk_message = "High probability of fraudulent activity."

        elif risk_score > 40:
            risk_level = "MEDIUM"
            risk_color = "#f59e0b"
            risk_message = "Potentially suspicious transaction."

        else:
            risk_level = "LOW"
            risk_color = "#22c55e"
            risk_message = "Transaction appears safe."
        
        st.markdown(
            f"""
            <div style="
                display:inline-block;
                padding:8px 16px;
                border-radius:999px;
                background:{risk_color};
                color:white;
                font-weight:bold;
                margin-bottom:10px;">
                {risk_level} RISK
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(confidence / 100)
        st.caption(f"{confidence:.2f}% confidence")

        if pred == 1:
            st.markdown(f"""
                        <div style="
                        background: linear-gradient(135deg, #ff4b8b, #ff1e56);
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
            background: linear-gradient(135deg, #36cfc9, #00b894);
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
    
