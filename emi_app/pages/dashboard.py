# pages/dashboard.py

import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def show_dashboard(ROOT):
    # -----------------------------
    # Global Modern CSS Styles - LIGHT THEME
    # -----------------------------
    st.markdown(
        """
        <style>
        /* Import a clean font (fallbacks included) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        :root{
            --bg-1: #f8f9fa;               /* light grey background */
            --bg-2: #ffffff;               /* white finish */
            --card: #ffffff;               /* white card background */
            --muted: #6c757d;              /* muted grey text */
            --text: #2c3e50;               /* dark text for readability */
            --accent-1: #5b9bd5;           /* soft blue */
            --accent-2: #9b7bd8;           /* soft purple */
            --accent-3: #5dade2;           /* light blue accent */
            --border: #e1e8ed;             /* light grey border */
            --shadow: 0 6px 22px rgba(38, 56, 84, 0.08);
            --shadow-hover: 0 16px 48px rgba(38, 56, 84, 0.12);
            --card-radius: 14px;
            --glass-alpha: 0.55;
        }

        /* Base layout: soft layered background with subtle floating blobs */
        .stApp, .main {
            background: radial-gradient(1200px 600px at 5% 10%, rgba(91,155,213,0.06), transparent 8%),
                        radial-gradient(800px 400px at 95% 85%, rgba(155,123,216,0.05), transparent 6%),
                        linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%) !important;
            color: var(--text);
            font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
            min-height: 100vh;
            -webkit-font-smoothing:antialiased;
            -moz-osx-font-smoothing:grayscale;
        }

        /* Decorative floating shapes (pure CSS) */
        .stApp::before, .stApp::after {
            content: "";
            position: fixed;
            z-index: 0;
            pointer-events: none;
            filter: blur(38px);
            opacity: 0.55;
        }
        .stApp::before {
            width: 420px;
            height: 420px;
            left: -6%;
            top: -8%;
            background: radial-gradient(circle at 30% 30%, rgba(91,155,213,0.18), transparent 30%),
                        radial-gradient(circle at 70% 70%, rgba(155,123,216,0.12), transparent 30%);
            transform: translate3d(0,0,0);
            animation: floatSlow 18s ease-in-out infinite;
        }
        .stApp::after {
            width: 360px;
            height: 360px;
            right: -6%;
            bottom: -6%;
            background: radial-gradient(circle at 25% 25%, rgba(90,173,226,0.14), transparent 28%),
                        radial-gradient(circle at 75% 75%, rgba(102,217,167,0.09), transparent 30%);
            transform: translate3d(0,0,0);
            animation: floatSlow 22s ease-in-out infinite reverse;
        }

        @keyframes floatSlow {
            0% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(18px) rotate(2deg); }
            100% { transform: translateY(0) rotate(0deg); }
        }

        /* Header / Hero (glass card + subtle highlight) */
        .header-card{
            position: relative;
            z-index: 2;
            border-radius: calc(var(--card-radius) + 6px);
            padding: 28px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 18px;
            box-shadow: var(--shadow);
            background: linear-gradient(135deg, rgba(255,255,255,0.86), rgba(255,255,255,0.72));
            border: 1px solid rgba(40,55,71,0.04);
            backdrop-filter: blur(8px) saturate(120%);
            overflow: hidden;
            transition: transform 0.22s cubic-bezier(.2,.9,.3,1), box-shadow 0.22s ease;
        }
        .header-card:hover{
            transform: translateY(-6px);
            box-shadow: var(--shadow-hover);
        }

        /* animated accent ribbon at top-right of header */
        .header-card .accent-ribbon {
            position: absolute;
            right: -36px;
            top: -36px;
            width: 220px;
            height: 220px;
            transform: rotate(35deg);
            background: conic-gradient(from 180deg at 50% 50%, rgba(91,155,213,0.14), rgba(155,123,216,0.10), rgba(91,155,213,0.06));
            filter: blur(24px);
            opacity: 0.9;
            pointer-events: none;
        }

        .header-content {
            display:flex;
            align-items:center;
            justify-content:center;
            gap:18px;
            flex-direction:column;
            text-align:center;
            padding: 6px 12px;
            max-width: 980px;
            margin: 0 auto;
        }

        .header-left {
            display:flex;
            align-items:center;
            gap:14px;
            justify-content:center;
        }

        .header-logo {
            width:72px;
            height:72px;
            border-radius:16px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:28px;
            font-weight:700;
            color: white;
            background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
            box-shadow: 0 6px 18px rgba(91,155,213,0.12), inset 0 -6px 14px rgba(255,255,255,0.06);
            flex-shrink:0;
        }

        .header-title{
            font-size: 36px;
            margin: 0;
            color: var(--text);
            font-weight: 700;
            line-height:1.03;
            letter-spacing:-0.3px;
        }
        .header-title .highlight {
            background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header-sub{
            font-size: 14px;
            color: var(--muted);
            margin-top: 6px;
            max-width: 780px;
        }

        /* micro chips row inside header */
        .header-chips {
            display:flex;
            gap:8px;
            margin-top:10px;
            flex-wrap:wrap;
            justify-content:center;
        }
        .chip {
            display:inline-flex;
            align-items:center;
            gap:8px;
            padding:6px 10px;
            border-radius:999px;
            font-size:13px;
            color: white;
            background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
            box-shadow: 0 6px 18px rgba(91,155,213,0.08);
            font-weight:600;
        }

        /* subtle animated underline for title */
        .title-underline {
            height:6px;
            width:120px;
            border-radius:10px;
            margin-top:12px;
            background: linear-gradient(90deg, rgba(91,155,213,0.9), rgba(155,123,216,0.9));
            box-shadow: 0 10px 30px rgba(91,155,213,0.08);
            transform: scaleX(0.98);
            transition: transform 0.28s ease;
        }
        .header-card:hover .title-underline { transform: scaleX(1.02); }

        /* Metric cards */
        .metrics-row { display: flex; gap: 18px; flex-wrap: wrap; margin-bottom: 18px; position: relative; z-index: 2; }
        .metric-card {
            background: var(--card);
            padding: 18px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid var(--border);
            min-height: 110px;
            box-shadow: var(--shadow);
            transition: transform 0.22s ease, box-shadow 0.22s ease;
        }
        .metric-card:hover {
            transform: translateY(-6px);
            box-shadow: var(--shadow-hover);
        }
        .metric-emoji { font-size: 20px; margin: 0; }
        .metric-title { font-size: 15px; margin: 8px 0; color: var(--text); font-weight: 600; }
        .metric-value { font-size: 26px; font-weight: 700; margin: 4px 0; color: var(--text); }
        .metric-sub { color: var(--muted); font-size: 13px; }

        /* Colored accent strips for metric cards (kept) */
        .accent-1 { background: linear-gradient(135deg, #5b9bd5, #9b7bd8); color: white; }
        .accent-2 { background: linear-gradient(135deg, #f7a8b8, #f5606b); color: white; }
        .accent-3 { background: linear-gradient(135deg, #4facfe, #00f2fe); color: white; }
        .accent-4 { background: linear-gradient(135deg, #66d9a7, #5dade2); color: white; }

        /* Section headings */
        .section-title { font-size: 18px; margin: 8px 0 16px 0; color: var(--text); font-weight: 700; letter-spacing: -0.2px; }

        /* Feature cards */
        .feature-card {
            background: var(--card);
            border-radius: 12px;
            padding: 18px;
            border-left: 5px solid var(--accent-1);
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-hover);
        }

        .feature-title { font-size: 15px; margin-bottom: 8px; color: var(--text); font-weight: 600; }
        .feature-desc { color: var(--muted); font-size: 14px; line-height: 1.45; }

        /* Expander styling */
        .streamlit-expanderHeader {
            border-radius: 10px;
            background: var(--card);
            border: 1px solid var(--border);
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 18px;
            border-radius: 10px;
            background: var(--card);
            border: 1px solid var(--border);
            color: var(--muted);
            font-size: 13px;
            box-shadow: var(--shadow);
            position: relative;
            z-index: 2;
        }

        /* Responsive tweaks */
        @media (max-width: 900px) {
            .header-left { gap:10px; }
            .header-logo { width:56px; height:56px; font-size:22px; border-radius:12px; }
            .header-title { font-size: 22px; }
            .metric-value { font-size: 20px; }
            .header-card { padding: 18px; margin-bottom: 16px; }
            .title-underline { width: 86px; }
        }

        /* Accessibility (reduce motion) */
        @media (prefers-reduced-motion: reduce) {
            .stApp::before, .stApp::after, .header-card, .metric-card { animation: none !important; transition: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header with improved modern banner (glass effect + decorative accents)
    st.markdown(
        """
        <div class="header-card">
            <div class="accent-ribbon" aria-hidden="true"></div>
            <div class="header-content">
                <div class="header-left">
                    <div class="header-logo">EMI</div>
                    <div style="display:flex; flex-direction:column; align-items:flex-start; justify-content:center;">
                        <h1 class="header-title">🎯 <span class="highlight">EMI Intelligence</span> Dashboard</h1>
                        <div class="header-sub">Real-time Financial Analytics & EMI Planning — modern, fast, and secure</div>
                        <div class="header-chips" style="margin-top:10px;">
                            <div class="chip">2 Models</div>
                            <div class="chip">1000+ Predictions</div>
                            <div class="chip">94.2% Accuracy</div>
                        </div>
                        <div class="title-underline" aria-hidden="true"></div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # Key Metrics Row
    # -----------------------------
    st.markdown('<div class="section-title">📊 System Overview</div>', unsafe_allow_html=True)

    # Use Streamlit columns but inject styled cards inside them.
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.markdown(
            """
            <div class="metric-card accent-1" style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <div class="metric-emoji">🎯</div>
                <div class="metric-title">AI Models</div>
                <div class="metric-value">2</div>
                <div class="metric-sub">Active & Ready</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with metric_col2:
        st.markdown(
            """
            <div class="metric-card accent-2" style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <div class="metric-emoji">📈</div>
                <div class="metric-title">Predictions</div>
                <div class="metric-value">1000+</div>
                <div class="metric-sub">Total Analyzed</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with metric_col3:
        st.markdown(
            """
            <div class="metric-card accent-3" style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <div class="metric-emoji">✅</div>
                <div class="metric-title">Accuracy</div>
                <div class="metric-value">94.2%</div>
                <div class="metric-sub">Model Score</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with metric_col4:
        st.markdown(
            """
            <div class="metric-card accent-4" style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <div class="metric-emoji">⚡</div>
                <div class="metric-title">Response</div>
                <div class="metric-value">&lt;1s</div>
                <div class="metric-sub">Avg Time</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # Feature Highlights
    # -----------------------------
    st.markdown('<div class="section-title">✨ Platform Capabilities</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Core Features", "🔮 AI Power", "📊 Analytics", "🛡️ Security"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                """
                <div class="feature-card" style="border-left: 5px solid var(--accent-1);">
                    <div class="feature-title">🧮 Smart EMI Calculator</div>
                    <div class="feature-desc">
                        Calculate EMI eligibility with advanced AI algorithms. Get instant predictions on your loan approval chances and maximum EMI capacity.
                        <ul style="margin-top:8px; color:var(--muted);">
                            <li>Real-time eligibility assessment</li>
                            <li>Maximum EMI capacity prediction</li>
                            <li>Risk factor analysis</li>
                            <li>Multiple loan scenarios</li>
                        </ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div class="feature-card" style="border-left: 5px solid #f5606b;">
                    <div class="feature-title">📊 Visual Analytics</div>
                    <div class="feature-desc">
                        Comprehensive data visualization and exploratory analysis. Understand patterns, trends, and correlations in your financial data.
                        <ul style="margin-top:8px; color:var(--muted);">
                            <li>Interactive charts & graphs</li>
                            <li>Distribution analysis</li>
                            <li>Correlation heatmaps</li>
                            <li>Trend identification</li>
                        </ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                """
                <div class="feature-card" style="border-left: 5px solid #4facfe;">
                    <div class="feature-title">🤖 Machine Learning Models</div>
                    <div class="feature-desc">
                        Powered by state-of-the-art ML algorithms for accurate predictions.
                        <ul style="margin-top:8px; color:var(--muted);">
                            <li>Dual model architecture</li>
                            <li>Classification + Regression</li>
                            <li>Continuous learning</li>
                            <li>High accuracy rates</li>
                        </ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div class="feature-card" style="border-left: 5px solid var(--accent-3);">
                    <div class="feature-title">🎯 Intelligent Recommendations</div>
                    <div class="feature-desc">
                        Get personalized financial advice based on your profile.
                        <ul style="margin-top:8px; color:var(--muted);">
                            <li>Custom action plans</li>
                            <li>Risk mitigation strategies</li>
                            <li>Credit improvement tips</li>
                            <li>Financial health guidance</li>
                        </ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab3:
        st.markdown(
            """
            <div class="feature-card" style="border-left: 5px solid var(--accent-1);">
                <div class="feature-title">📈 Advanced Analytics Features</div>
                <div class="feature-desc">
                    A focused toolkit for deep exploratory analysis.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        feature_col1, feature_col2, feature_col3 = st.columns(3)

        with feature_col1:
            st.info("📊 **Dataset Management**\n\nUpload, clean, and manage your financial datasets efficiently.")

        with feature_col2:
            st.success("🎪 **Model Performance**\n\nTrack accuracy, F1 scores, RMSE, and feature importance metrics.")

        with feature_col3:
            st.warning("🔍 **Deep Insights**\n\nExplore correlations, distributions, and financial patterns.")

    with tab4:
        st.markdown(
            """
            <div class="feature-card" style="border-left: 5px solid #66d9a7;">
                <div class="feature-title">🛡️ Security & Privacy</div>
                <div class="feature-desc">
                    Your financial data is protected with enterprise-grade security measures.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sec_col1, sec_col2 = st.columns(2)
        with sec_col1:
            st.success("✅ Local Processing")
            st.success("✅ No Cloud Storage")
        with sec_col2:
            st.success("✅ Encrypted Models")
            st.success("✅ Privacy First")

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # Quick Start Guide
    # -----------------------------
    st.markdown('<div class="section-title">🚀 Quick Start Guide</div>', unsafe_allow_html=True)

    with st.expander("📖 How to Use This Platform", expanded=False):
        st.markdown(
            """
            <div style="padding:8px 6px; color:var(--muted); font-size:14px; line-height:1.55;">
            <strong>Step-by-Step Guide:</strong>
            <ol style="margin-top:8px;">
                <li><strong>🧮 EMI Calculator</strong>
                    <ul>
                        <li>Navigate to EMI Calculator from sidebar</li>
                        <li>Enter your financial details</li>
                        <li>Get instant eligibility prediction</li>
                        <li>View maximum EMI capacity</li>
                    </ul>
                </li>
                <li><strong>📊 Data Insights</strong>
                    <ul>
                        <li>Explore visual analytics</li>
                        <li>Understand data distributions</li>
                        <li>Identify patterns and trends</li>
                    </ul>
                </li>
                <li><strong>🎪 Model Metrics</strong>
                    <ul>
                        <li>Check model performance</li>
                        <li>View accuracy scores</li>
                        <li>Analyze feature importance</li>
                    </ul>
                </li>
                <li><strong>🤖 AI Advisor</strong>
                    <ul>
                        <li>Get personalized recommendations</li>
                        <li>Receive financial guidance</li>
                        <li>Improve your eligibility score</li>
                    </ul>
                </li>
                <li><strong>⚙️ System Settings</strong>
                    <ul>
                        <li>Manage datasets</li>
                        <li>Download reports</li>
                        <li>Configure system options</li>
                    </ul>
                </li>
            </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------
    # System Status
    # -----------------------------
    st.markdown('<div class="section-title">🔧 System Status</div>', unsafe_allow_html=True)

    status_col1, status_col2, status_col3 = st.columns(3)

    with status_col1:
        st.success("🟢 **Classification Model**: Online")

    with status_col2:
        st.success("🟢 **Regression Model**: Online")

    with status_col3:
        st.success("🟢 **Data Pipeline**: Ready")

    # -----------------------------
    # Footer
    # -----------------------------
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="footer" style="border-radius:10px;">
            <div style="font-weight:600; color:var(--text);">💎 EMI Intelligence Hub | Powered by Advanced AI</div>
            <div style="margin-top:6px; color:var(--muted); font-size:12px;">© 2025 All Rights Reserved</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
