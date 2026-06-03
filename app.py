import sys
import os
# Make models/ importable regardless of working directory
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "models"))

import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import plotly.graph_objects as go
from models.fraud_detector import analyze_transaction

st.set_page_config(page_title="UniPay FraudX", layout="wide", initial_sidebar_state="expanded")

# ================== CSS THEME INJECTION ==================
def inject_custom_css(theme):
    """Inject theme-aware custom CSS into the Streamlit app.

    Args:
        theme (str): Active theme name. Expected values are "Dark" or "Light".

    Returns:
        None: This function writes CSS directly to the Streamlit app.
    """
    if theme == "Dark":
        app_bg = "#0b0f19"
        sidebar_bg = "#111827"
        text_color = "#f3f4f6"
        metric_title_color = "#f3f4f6"
        metric_title_opacity = "0.7"
        metric_value_color = "#ffffff"
        metric_subtitle_color = "#f3f4f6"
        metric_subtitle_opacity = "0.5"
        card_bg = "rgba(255,255,255,0.03)"
        input_bg = "rgba(255,255,255,0.05)"
    else:
        app_bg = "#f8fafc"
        sidebar_bg = "#ffffff"
        text_color = "#1e293b"
        metric_title_color = "#64748b"
        metric_title_opacity = "1"
        metric_value_color = "#0f172a"
        metric_subtitle_color = "#94a3b8"
        metric_subtitle_opacity = "1"
        card_bg = "#ffffff"
        input_bg = "#ffffff"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global font */
        * {{ font-family: 'Inter', sans-serif !important; }}

        /* App & sidebar backgrounds */
        [data-testid="stAppViewContainer"] {{ background-color: {app_bg}; }}
        [data-testid="stSidebar"] {{ background-color: {sidebar_bg}; }}

        /* Global text color */
        h1, h2, h3, h4, h5, h6, p, label {{ color: {text_color} !important; }}

        /* Glass card styling */
        .glass-card {{ 
            background: {card_bg}; 
            backdrop-filter: blur(10px); 
            border-radius: 16px; 
            padding: 24px; 
            margin-bottom: 24px; 
            border: 1px solid rgba(128,128,128,0.1); 
        }}

        /* Metric components */
        .metric-title {{ 
            font-size: 0.9rem; 
            font-weight: 500; 
            text-transform: uppercase; 
            margin-bottom: 4px; 
            color: {metric_title_color} !important;
            opacity: {metric_title_opacity};
        }}
        .metric-value {{ 
            font-size: 2.2rem; 
            font-weight: 700; 
            margin-bottom: 2px; 
            color: {metric_value_color} !important;
        }}
        .metric-subtitle {{ 
            font-size: 0.85rem; 
            color: {metric_subtitle_color} !important;
            opacity: {metric_subtitle_opacity};
        }}

        /* Button styling */
        .stButton > button {{ 
            background: linear-gradient(135deg, #ff4b8b 0%, #ff1e56 100%); 
            color: white !important; 
            border-radius: 8px; 
            padding: 0.5rem 1.5rem; 
            border: none; 
        }}

        /* Input fields */
        input, [data-baseweb="input"] {{ 
            background-color: {input_bg} !important; 
            color: {text_color} !important; 
        }}

        /* Progress bar */
        .progress-bg {{ 
            background: rgba(255,255,255,0.1); 
            border-radius: 8px; 
            height: 12px; 
            width: 100%; 
            overflow: hidden; 
            margin-top: 10px; 
        }}
        .progress-fill {{ 
            height: 100%; 
            border-radius: 8px; 
        }}

        /* Result boxes */
        .result-box {{ 
            padding: 24px; 
            border-radius: 16px; 
            margin-top: 20px; 
        }}
        .result-danger {{ 
            background: linear-gradient(145deg, rgba(255,30,86,0.1) 0%, rgba(255,75,139,0.05) 100%); 
            border-left: 6px solid #ff1e56; 
        }}
        .result-success {{ 
            background: linear-gradient(145deg, rgba(0,184,148,0.1) 0%, rgba(54,207,201,0.05) 100%); 
            border-left: 6px solid #00b894; 
        }}

        /* Block container */
        .block-container {{ padding-top: 2rem !important; }}

        /* Markdown container */
        div[data-testid="stMarkdownContainer"] p {{ color: {text_color} !important; }}

        </style>
    """, unsafe_allow_html=True)

# ================== DATA LOADING ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@st.cache_data
def load_data():
    """Load the transaction dataset from disk.

    Returns:
        pd.DataFrame: Loaded dataset if available and valid; otherwise an
        empty DataFrame.
    """
    dataset_path = os.path.join(BASE_DIR, "dataset", "data.xlsx")
    if not os.path.exists(dataset_path):
        return pd.DataFrame()
    try:
        df = pd.read_excel(dataset_path)
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_resource
def load_model():
    """Load the fraud detection model from disk.

    Returns:
        object | None: Deserialized model object if available and valid;
        otherwise None.
    """
    model_path = os.path.join(BASE_DIR, "models", "fraud_model.pkl")
    if not os.path.exists(model_path):
        return None
    try:
        model = pickle.load(open(model_path, "rb"))
        return model
    except Exception:
        return None


df = load_data()
model = load_model()

if df.empty or model is None:
    st.markdown("""
        <div style='
            background: linear-gradient(145deg, rgba(255,30,86,0.08), rgba(255,75,139,0.04));
            border-left: 6px solid #ff1e56;
            border-radius: 12px;
            padding: 28px 32px;
            margin: 40px auto;
            max-width: 720px;
        '>
            <h2 style='color:#ff1e56; margin-top:0;'>⚠️ Setup Required</h2>
            <p style='opacity:0.85; line-height:1.8;'>
                UniPay FraudX could not start because required files are missing.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ========== PRIMARY SETUP INSTRUCTION ==========
    st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(255, 107, 53, 0.15) 0%, rgba(255, 193, 7, 0.1) 100%);
            border: 2px solid #ff6b35;
            border-radius: 12px;
            padding: 24px;
            margin: 20px auto;
            max-width: 720px;
        '>
            <h3 style='color: #ff6b35; margin-top: 0; text-align: center;'>🚀 Quick Setup</h3>
            <p style='opacity: 0.9; text-align: center; font-weight: 600; margin-bottom: 16px;'>Run this command from the project root:</p>
            <div style='
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
                padding: 12px 16px;
                font-family: "Courier New", monospace;
                font-size: 1.05rem;
                text-align: center;
                color: #00ff88;
                margin-bottom: 12px;
                user-select: all;
            '><strong>python models/model.py</strong></div>
            <p style='opacity: 0.8; margin-bottom: 0; font-size: 0.9rem; text-align: center;'>This will generate both dataset and ML model automatically.</p>
        </div>
    """, unsafe_allow_html=True)

    # ========== DETAILED BREAKDOWN ==========
    st.markdown("### **What's Missing?**")

    missing_count = (1 if df.empty else 0) + (1 if model is None else 0)

    if missing_count > 0:
        columns = st.columns(missing_count)
        col_idx = 0

        if df.empty:
            with columns[col_idx]:
                st.error(
                    "❌ **Dataset Missing**\n\n"
                    "Expected: `dataset/data.xlsx`\n\n"
                    "This file will be auto-generated when you run:\n"
                    "```bash\npython models/model.py\n```"
                )
            col_idx += 1

        if model is None:
            with columns[col_idx]:
                st.error(
                    "❌ **Model Missing**\n\n"
                    "Expected: `models/fraud_model.pkl`\n\n"
                    "This file will be auto-generated when you run:\n"
                    "```bash\npython models/model.py\n```"
                )

    # ========== NEXT STEPS ==========
    st.markdown("""
        <div class='glass-card'>
            <h4>📋 Manual Steps (if auto-generation fails):</h4>
            <ol style='opacity: 0.85; line-height: 2;'>
                <li>Open terminal in project root: <code>c:\\Users\\HP\\UniPay-FraudX</code></li>
                <li>Run: <code style='background: rgba(0,0,0,0.1); padding: 2px 6px; border-radius: 4px;'>python models/model.py</code></li>
                <li>Wait for completion (1–2 minutes)</li>
                <li>Refresh this app in your browser</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

    st.info(
        "📖 For full setup instructions, refer to the "
        "[README](https://github.com/Aabhaaatomar/UniPay-FraudX#️-installation)."
    )
    st.stop()

# ================== NAVIGATION & SIDEBAR ==================
st.sidebar.markdown(
    """
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 1.8rem; font-weight: 700;">UniPay FraudX</h1>
        <p style="font-size: 0.8rem; opacity: 0.7; margin-top: 0;">AI Fraud Intelligence</p>
    </div>
    """, unsafe_allow_html=True
)

st.sidebar.markdown("### Navigation")
page = st.sidebar.radio(
    label="Navigation",
    options=["🏠 Home", "📊 Dashboard", "🔍 Analysis", "🔮 Prediction Engine", "⚙️ About"],
    label_visibility="collapsed"
)

st.sidebar.markdown("### Settings")
theme_choice = st.sidebar.radio("Theme Mode", ["🌙 Dark", "☀️ Light"], key="theme_choice")
theme = "Dark" if "Dark" in theme_choice else "Light"

inject_custom_css(theme)

chart_font_color = "#f3f4f6" if theme == "Dark" else "#1e293b"
chart_bg_color = "rgba(0,0,0,0)" if theme =="Dark" else "#ffffff"
grid_color = "rgba(255,255,255,0.1)" if theme == "Dark" else "rgba(0,0,0,0.08)"

# ================== GRAPH LAYOUTS ==================
def apply_plotly_layout(fig):
    """Apply a consistent theme-aware layout to a Plotly figure.

    Args:
        fig: Plotly figure object to update.

    Returns:
        The updated Plotly figure.
    """
    try:
        fig.update_layout(
            plot_bgcolor=chart_bg_color,
            paper_bgcolor=chart_bg_color,
            font=dict(family="Inter", color=chart_font_color),
            margin=dict(l=30, r=20, t=50, b=30),
            title=dict(font=dict(color=chart_font_color, size=16)),
            legend=dict(
                font=dict(color=chart_font_color),
                title=dict(font=dict(color=chart_font_color))
            ),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                title=dict(font=dict(color=chart_font_color)),
                tickfont=dict(color=chart_font_color)
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=grid_color,
                zeroline=False,
                title=dict(font=dict(color=chart_font_color)),
                tickfont=dict(color=chart_font_color)
            )
        )
    except Exception as e:
        msg = str(e).split("\n")[0][:120]
        st.error(f"Chart layout failed: {msg}")
    return fig


# ================== PAGES ==================
if "Home" in page:
    st.markdown("""
        <div style='text-align:center; padding:40px;'>
            <h1 style='font-size:2.4rem; margin-bottom:8px;'>Next-Gen Fraud Defense</h1>
            <p style='opacity:0.8; max-width:700px; margin:0 auto;'>Protect your digital ecosystem with real-time AI analytics and robust machine learning predictions.</p>
        </div>
    """, unsafe_allow_html=True)

elif "Dashboard" in page:
    st.markdown("<h2>Analytics Dashboard</h2>", unsafe_allow_html=True)
    total_tx = len(df)
    fraud_tx = len(df[df["label"] == "Suspicious"])
    fraud_rate = (fraud_tx / total_tx) * 100 if total_tx > 0 else 0
    total_vol = df["amount"].sum()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.markdown(f"""
        <div class='glass-card'><div class='metric-title'>Total Volume</div><div class='metric-value'>₹{total_vol/1000000:.2f}M</div><div class='metric-subtitle'>Processed Transactions</div></div>
    """, unsafe_allow_html=True)
    kpi2.markdown(f"""
        <div class='glass-card'><div class='metric-title'>Total Transactions</div><div class='metric-value'>{total_tx:,}</div><div class='metric-subtitle'>Last 30 Days</div></div>
    """, unsafe_allow_html=True)
    kpi3.markdown(f"""
        <div class='glass-card'><div class='metric-title'>Fraud Flags</div><div class='metric-value'>{fraud_tx:,}</div><div class='metric-subtitle'>Suspicious Activities</div></div>
    """, unsafe_allow_html=True)
    kpi4.markdown(f"""
        <div class='glass-card'><div class='metric-title'>Fraud Rate</div><div class='metric-value'>{fraud_rate:.2f}%</div><div class='metric-subtitle'>Of total volume</div></div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.05); margin: 2rem 0;'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        fig_bar = px.bar(
            df.groupby(["hour", "label"]) ["txn_count_1hr"].sum().reset_index(),
            x="hour", y="txn_count_1hr", color="label",
            title="Activity Volume by Hour",
            color_discrete_sequence=["#00b894", "#ff4b8b"]
        )
        st.plotly_chart(apply_plotly_layout(fig_bar), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        df_line = df.groupby("hour")["amount"].mean().reset_index()
        fig_line = px.line(df_line, x="hour", y="amount", title="Average Transaction Value Trend")
        fig_line.update_traces(line_color="#ff4b8b", line_width=3, fill='tozeroy', fillcolor='rgba(255,75,139,0.1)')
        st.plotly_chart(apply_plotly_layout(fig_line), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1.5])
    with col3:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        fig_donut = px.pie(df, names="label", hole=0.6, title="Risk Distribution", color_discrete_sequence=["#00b894", "#ff4b8b"])
        fig_donut.update_layout(annotations=[dict(text=f'{fraud_rate:.1f}%<br>Fraud', x=0.5, y=0.5, font_size=20, showarrow=False, font=dict(color=chart_font_color))])
        st.plotly_chart(apply_plotly_layout(fig_donut), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        fig_sender = px.bar(df, x="sender_type", color="receiver_type", title="Entity Type Correlation Matrix", barmode="stack", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(apply_plotly_layout(fig_sender), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)


elif "Analysis" in page:
    st.markdown("<h2>Data Intelligence Explorer</h2>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("#### Transaction Registry")
    st.dataframe(df, width="stretch", height=400, )
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        fig_hist = px.histogram(df, x="amount", color="label", nbins=40, title="Amount Distribution Density", color_discrete_sequence=["#00b894", "#ff4b8b"])
        st.plotly_chart(apply_plotly_layout(fig_hist), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        fig_scatter = px.scatter(df, x="amount", y="txn_count_1hr", color="label", size="amount", hover_data=["hour"], title="Velocity vs Value Analysis", color_discrete_sequence=["#00b894", "#ff4b8b"])
        st.plotly_chart(apply_plotly_layout(fig_scatter), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)


elif "Prediction" in page or "Prediction Engine" in page:
    st.markdown("<h2>Real-time Fraud Prediction Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p style='opacity:0.8;'>Submit transaction telemetry for instant ML inference.</p>", unsafe_allow_html=True)

    form_col, result_col = st.columns([1, 1.2])
    with form_col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### Input Telemetry")
        amount = st.number_input("Transaction Value (₹)", min_value=0.0, value=1500.0, step=100.0)
        txn = st.number_input("Txn Velocity (Last 1hr)", min_value=0, value=2, step=1)
        hour = st.slider("Hour of Day", 0, 23, 14)
        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("Initialize Inference", width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with result_col:
        if predict_btn:
            result = analyze_transaction(amount=amount, txn_count=txn, hour=hour, model=model)

            final_pred  = 1 if result["is_fraud"] else 0
            risk_score  = result["fraud_score"]
            reason      = result["reason"]
            risk_level  = result["risk_label"]
            confidence  = result["ml_proba"] * 100
            rules_fired = result["triggered_rules"]

            card_class  = "result-danger" if final_pred == 1 else "result-success"
            icon        = "🚨" if final_pred == 1 else "✅"
            color       = "#ff0000" if final_pred == 1 else "#10B981"
            display_verdict = "SUSPICIOUS" if final_pred == 1 else "SAFE"


            st.markdown(f"""
                <div class="{card_class} style="padding-bottom:16px">
                    <h3 style="margin-top:0; color: {color} !important;">{icon} {display_verdict} — {risk_level} RISK</h3>
                    <p style="opacity:0.8; margin-bottom: 30px;">{reason}</p>
                    <div style="display:flex; justify-content:space-between; margin-bottom: 18px;">
                        <span style="font-size:0.9rem; font-weight:600; color: {chart_font_color};">ML Fraud Probability</span>
                        <span style="font-size:0.9rem; font-weight:600; color:{color};">{confidence:.1f}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
                    <div class="progress-bg"><div class="progress-fill" style="width: {min(confidence, 100):.1f}%; background: {color};"></div></div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px;">
                    <div>
                        <div style="font-size:0.8rem; opacity:0.7; color: {chart_font_color};">Risk Score (Calculated)</div>
                        <div style="font-size:1.5rem; font-weight:700; color: {chart_font_color};"">{risk_score}/100</div>
                    </div>
                    <div>
                        <div style="font-size:0.8rem; opacity:0.7; color: {chart_font_color};">Recommendation</div>
                        <div style="font-size:1.1rem; font-weight:600; color: {chart_font_color};">{result['recommendation'].replace('_', ' ')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if rules_fired:
                rules_items = "".join(f"<li style='margin-bottom:4px; font-size:0.85rem; opacity:0.85;'>{r}</li>" for r in rules_fired)
                st.markdown(f"""
                <div style="font-size:0.8rem; font-weight:600; opacity:0.7; margin-bottom:8px; margin-top:20px;">TRIGGERED RULES</div>
                <ul style='margin:0; padding-left:18px; list-style:disc;'>{rules_items}</ul>
                """, unsafe_allow_html=True)


        else:
            st.markdown(f"<div style='height: 100%; display: flex; align-items: center; justify-content: center; opacity: 0.3; border: 2px dashed rgba(128,128,128,0.2); border-radius: 16px; padding: 50px; text-align: center; color: {chart_font_color};'>Waiting for telemetry input... Enter parameters and click Initialize Inference.</div>", unsafe_allow_html=True)


elif "About" in page:
    st.markdown("<h2>System Architecture & Intelligence</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <h4>UniPay FraudX</h4>
            <p style="opacity: 0.8; line-height: 1.6;">An enterprise-grade fraud detection platform engineered to process digital transactions in real-time.</p>
        </div>
    """, unsafe_allow_html=True)
