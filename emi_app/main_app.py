# main_app.py

import streamlit as st
from pathlib import Path
import sys

# -----------------------------
# Project Setup
# -----------------------------
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "scripts"))

from predict_emi import predict_emi

# -----------------------------
# Page Imports
# -----------------------------
from pages.dashboard import show_dashboard
from pages.emi_calculator import show_emi_calculator
from pages.insights import show_insights
from pages.metrics import show_metrics
from pages.settings import show_settings
from pages.advisor import show_advisor

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="💎 EMI Intelligence Hub",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS for Modern LIGHT THEME Look
# -----------------------------
st.markdown(
    """
    <style>
    /* Import a clean, professional font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    :root{
        --bg-start: #f8f9fa;        /* light grey */
        --bg-end:   #ffffff;        /* white */
        --panel: #ffffff;
        --muted: #6c757d;
        --text: #2c3e50;
        --accent-1: #5b9bd5;        /* primary blue */
        --accent-2: #9b7bd8;        /* purple */
        --accent-3: #66d9a7;        /* teal */
        --border: #e1e8ed;
        --radius: 12px;
        --shadow-sm: 0 6px 22px rgba(38,56,84,0.06);
        --shadow-hover: 0 18px 48px rgba(38,56,84,0.10);
        --glass-alpha: 0.78;
    }

    /* App background: layered gradients + soft floating shapes for depth */
    .stApp {
        min-height: 100vh;
        background:
            radial-gradient(900px 420px at 6% 10%, rgba(91,155,213,0.04), transparent 8%),
            radial-gradient(700px 360px at 96% 86%, rgba(155,123,216,0.03), transparent 6%),
            linear-gradient(180deg, var(--bg-start) 0%, var(--bg-end) 100%) !important;
        color: var(--text);
        font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
        -webkit-font-smoothing:antialiased;
        -moz-osx-font-smoothing:grayscale;
    }

    /* Floating decorative shapes for subtle motion (reduced motion respected below) */
    .stApp::before, .stApp::after {
        content: "";
        position: fixed;
        z-index: 0;
        pointer-events: none;
        filter: blur(36px);
        opacity: 0.55;
    }
    .stApp::before {
        width: 420px;
        height: 420px;
        left: -6%;
        top: -8%;
        background: radial-gradient(circle at 30% 30%, rgba(91,155,213,0.16), transparent 30%),
                    radial-gradient(circle at 70% 70%, rgba(155,123,216,0.10), transparent 30%);
        animation: floatSlow 18s ease-in-out infinite;
    }
    .stApp::after {
        width: 360px;
        height: 360px;
        right: -6%;
        bottom: -6%;
        background: radial-gradient(circle at 25% 25%, rgba(90,173,226,0.12), transparent 28%),
                    radial-gradient(circle at 75% 75%, rgba(102,217,167,0.08), transparent 30%);
        animation: floatSlow 22s ease-in-out infinite reverse;
    }

    @keyframes floatSlow {
        0% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(16px) rotate(1.8deg); }
        100% { transform: translateY(0) rotate(0deg); }
    }

    /* Top-level content area padding and card look */
    .main .block-container {
        padding-top: 20px;
        padding-left: 28px;
        padding-right: 28px;
        padding-bottom: 28px;
    }

    /* Sidebar: glass card with subtle gradient + softened edges */
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(250,250,250,0.98));
        border-right: 1px solid var(--border);
        padding-top: 18px;
        box-shadow: 0 10px 30px rgba(38,56,84,0.03);
        backdrop-filter: blur(6px) saturate(120%);
    }

    /* Sidebar hero card (enhanced banner) */
    .sidebar-hero {
        padding: 14px;
        margin: 8px 10px 14px 10px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(227,242,253,0.9), rgba(243,229,245,0.88));
        border: 1px solid rgba(40,55,71,0.04);
        box-shadow: var(--shadow-sm);
        text-align: left;
        display:flex;
        gap:12px;
        align-items:center;
    }
    .sidebar-hero .logo {
        width:56px;
        height:56px;
        border-radius: 12px;
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:800;
        font-size:18px;
        color: white;
        background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
        box-shadow: 0 10px 22px rgba(91,155,213,0.12), inset 0 -6px 10px rgba(255,255,255,0.06);
        flex-shrink:0;
    }
    .sidebar-hero .meta {
        display:flex;
        flex-direction:column;
        gap:4px;
    }
    .sidebar-hero .meta .title { font-size:16px; font-weight:700; color:var(--text); margin:0; }
    .sidebar-hero .meta .subtitle { font-size:12px; color:var(--muted); margin:0; }

    /* Sidebar chips */
    .sidebar-chips { display:flex; gap:8px; margin-top:8px; flex-wrap:wrap; }
    .chip {
        display:inline-flex;
        align-items:center;
        gap:8px;
        padding:6px 10px;
        border-radius:999px;
        font-size:12px;
        color: white;
        background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
        box-shadow: 0 8px 18px rgba(91,155,213,0.06);
        font-weight:700;
    }

    /* Sidebar header card fallback (older markup) */
    .sidebar .sidebar-content .stMarkdown > div {
        padding: 10px 12px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    /* Sidebar quick stats layout smoothing */
    [data-testid="stSidebar"] .stMetric {
        background: transparent;
        padding: 6px 4px;
        border-radius: 8px;
    }

    /* Primary buttons */
    div.stButton > button, button.streamlit-expanderHeader {
        background: linear-gradient(90deg, var(--accent-1) 0%, var(--accent-2) 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 14px;
        font-weight: 700;
        box-shadow: 0 10px 30px rgba(91, 155, 213, 0.14);
        transition: transform .14s ease, box-shadow .14s ease, opacity .12s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 18px 40px rgba(38,56,84,0.12);
        opacity: 0.98;
    }

    /* Secondary / subtle buttons (kept visually consistent) */
    .stButton button[kind="secondary"], button[title="secondary"] {
        background: var(--panel);
        color: var(--text);
        border: 1px solid var(--border);
    }

    /* Make inputs look modern (only styling; behavior unchanged) */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, textarea {
        background: var(--panel);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 8px 10px;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        padding-bottom: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: var(--panel);
        border-radius: 10px;
        padding: 8px 16px;
        color: var(--muted);
        font-weight: 600;
        border: 1px solid var(--border);
        transition: transform .12s ease, background .12s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
        color: white !important;
        transform: translateY(-4px);
        box-shadow: var(--shadow-hover);
        border: 1px solid transparent;
    }

    /* Expander header tuning */
    .streamlit-expanderHeader {
        background: var(--panel);
        border-radius: 10px;
        padding: 8px 12px;
        font-weight: 700;
        color: var(--text);
        border: 1px solid var(--border);
    }

    /* Card / section look used across pages */
    .card {
        padding: 16px;
        border-radius: 12px;
        background: var(--panel);
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
    }

    /* Footer small */
    .app-footer { color: var(--muted); font-size:13px; text-align:center; padding:10px; margin-top:8px; }

    /* Plotly chart container rounding */
    .element-container .stPlotlyChart > div { border-radius: 12px; overflow: hidden; border:1px solid var(--border); }

    /* Make tables slightly elevated */
    .stDataFrame [role="table"] { border-radius: 8px; overflow: hidden; box-shadow: var(--shadow-sm); }

    /* Responsive tweaks for smaller screens */
    @media (max-width: 900px) {
        .stApp .main .block-container { padding-left: 14px; padding-right: 14px; }
        div.stButton > button { width: 100%; }
        .sidebar-hero { padding: 12px; margin: 8px; }
        .sidebar-hero .meta .title { font-size:14px; }
    }

    /* Respect reduced motion preferences */
    @media (prefers-reduced-motion: reduce) {
        .stApp::before, .stApp::after { animation: none !important; transition: none !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

MODEL_DIR = ROOT / "models"
REPORTS_DIR = ROOT / "reports"

# -----------------------------
# Session State Initialization
# -----------------------------
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None
if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = None

# -----------------------------
# Animated Sidebar with Icons (structure unchanged; markup improved)
# -----------------------------
with st.sidebar:
    # Sidebar top card (modernized hero but same textual content)
    st.markdown(
        """
        <div class="sidebar-hero" role="banner" aria-label="EMI Intelligence Sidebar">
            <div class="logo" aria-hidden="true">EMI</div>
            <div class="meta">
                <div class="title">💎 EMI Intelligence</div>
                <div class="subtitle">Your Smart Finance Partner</div>
                <div class="sidebar-chips" aria-hidden="true" style="margin-top:8px;">
                    <div class="chip">AI-Powered</div>
                    <div class="chip">Privacy-first</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Navigation (keeps the same options and behavior)
    selected = st.radio(
        "Navigation Menu",
        [
            "🎯 Dashboard",
            "🧮 EMI Calculator",
            "📊 Data Insights",
            "🎪 Model Metrics",
            "⚙️ System Settings",
            "🤖 AI Advisor"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Quick Stats in Sidebar (keeps values unchanged)
    st.markdown("### 📈 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Models", "2", delta="Active")
    with col2:
        st.metric("Accuracy", "94%", delta="+2%")

    st.markdown("---")
    st.markdown("### 🔔 Status")
    st.success("✅ System Online")
    st.info("📡 Models Loaded")

    st.markdown("---")
    st.caption("© 2025 EMI Intelligence Hub")

# -----------------------------
# Route to Pages (logic unchanged)
# -----------------------------
if selected == "🎯 Dashboard":
    show_dashboard(ROOT)
elif selected == "🧮 EMI Calculator":
    show_emi_calculator(MODEL_DIR)
elif selected == "📊 Data Insights":
    show_insights(REPORTS_DIR)
elif selected == "🎪 Model Metrics":
    show_metrics(MODEL_DIR)
elif selected == "⚙️ System Settings":
    show_settings(ROOT)
elif selected == "🤖 AI Advisor":
    show_advisor()
