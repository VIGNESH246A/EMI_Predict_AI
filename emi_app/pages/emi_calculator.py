# pages/emi_calculator.py

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path
import joblib
import plotly.graph_objects as go

def show_emi_calculator(MODEL_DIR="models"):
    ROOT = Path(__file__).resolve().parent.parent.parent
    sys.path.append(str(ROOT / "scripts"))
    MODEL_DIR = ROOT / "models"
    PREPROC_DIR = MODEL_DIR / "preprocessors"

    from predict_emi import predict_emi

    @st.cache_resource
    def load_label_encoder():
        return joblib.load(PREPROC_DIR / "eligibility_label_encoder.joblib")

    @st.cache_resource
    def load_clf_features():
        return joblib.load(MODEL_DIR / "clf_features.joblib")

    @st.cache_resource
    def load_reg_features():
        return joblib.load(MODEL_DIR / "reg_features.joblib")

    label_encoder = load_label_encoder()
    clf_features = load_clf_features()
    reg_features = load_reg_features()

    # ---------- Modern global CSS (LIGHT THEME) ----------
    st.markdown(
        """
        <style>
        /* Import clean font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        :root{
            --bg-1: #f8f9fa;         /* light grey */
            --bg-2: #ffffff;         /* white */
            --card: #ffffff;
            --muted: #6c757d;
            --text: #2c3e50;
            --accent-a: #5b9bd5;     /* soft blue */
            --accent-b: #9b7bd8;     /* soft purple */
            --accent-c: #66d9a7;     /* soft teal */
            --accent-coral: #f5576c;
            --border: #e1e8ed;
            --card-radius: 12px;
            --shadow-sm: 0 6px 22px rgba(38,56,84,0.06);
            --shadow-hover: 0 16px 48px rgba(38,56,84,0.10);
            --glass-alpha: 0.78;
        }

        /* App background: layered gradients + soft floating shapes */
        .stApp, .main {
            min-height: 100vh;
            background:
                radial-gradient(900px 420px at 4% 12%, rgba(91,155,213,0.06), transparent 8%),
                radial-gradient(700px 360px at 96% 86%, rgba(155,123,216,0.04), transparent 6%),
                linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%) !important;
            color: var(--text);
            font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
            -webkit-font-smoothing:antialiased;
            -moz-osx-font-smoothing:grayscale;
        }

        /* Decorative floating shapes for depth */
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
            background: radial-gradient(circle at 30% 30%, rgba(91,155,213,0.18), transparent 30%),
                        radial-gradient(circle at 70% 70%, rgba(155,123,216,0.12), transparent 30%);
            animation: floatSlow 18s ease-in-out infinite;
        }
        .stApp::after {
            width: 360px;
            height: 360px;
            right: -6%;
            bottom: -6%;
            background: radial-gradient(circle at 25% 25%, rgba(90,173,226,0.14), transparent 28%),
                        radial-gradient(circle at 75% 75%, rgba(102,217,167,0.09), transparent 30%);
            animation: floatSlow 22s ease-in-out infinite reverse;
        }

        @keyframes floatSlow {
            0% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(16px) rotate(1.8deg); }
            100% { transform: translateY(0) rotate(0deg); }
        }

        /* Header (glass-card hero) */
        .emi-header {
            position: relative;
            z-index: 2;
            display:flex;
            align-items:center;
            justify-content:center;
            gap:18px;
            padding:20px;
            border-radius: calc(var(--card-radius) + 6px);
            background: linear-gradient(135deg, rgba(255,255,255,var(--glass-alpha)), rgba(250,250,250,0.86));
            border: 1px solid rgba(40,55,71,0.04);
            box-shadow: var(--shadow-sm);
            backdrop-filter: blur(6px) saturate(120%);
            transition: transform 0.22s cubic-bezier(.2,.9,.3,1), box-shadow 0.22s ease;
            text-align:center;
            margin-bottom: 18px;
            flex-direction: column;
            max-width: 980px;
            margin-left: auto;
            margin-right: auto;
        }
        .emi-header:hover { transform: translateY(-6px); box-shadow: var(--shadow-hover); }

        /* Accent ribbon */
        .emi-header .accent-ribbon {
            position: absolute;
            right: -40px;
            top: -40px;
            width: 220px;
            height: 220px;
            transform: rotate(32deg);
            background: conic-gradient(from 180deg at 50% 50%, rgba(91,155,213,0.14), rgba(155,123,216,0.10), rgba(91,155,213,0.06));
            filter: blur(22px);
            opacity: 0.95;
            pointer-events: none;
        }

        .emi-top {
            display:flex;
            align-items:center;
            gap:14px;
            justify-content:center;
            flex-direction:row;
            width:100%;
        }

        .emi-logo {
            width:72px;
            height:72px;
            border-radius:14px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:22px;
            font-weight:700;
            color: white;
            background: linear-gradient(135deg, var(--accent-a), var(--accent-b));
            box-shadow: 0 10px 28px rgba(91,155,213,0.12), inset 0 -6px 16px rgba(255,255,255,0.06);
            flex-shrink:0;
        }

        .emi-heading {
            display:flex;
            flex-direction:column;
            align-items:flex-start;
            gap:6px;
            text-align:left;
            max-width: 760px;
        }

        .emi-title {
            margin:0;
            font-size:32px;
            color:var(--text);
            font-weight:700;
            line-height:1.02;
        }
        .emi-title .accent-text {
            background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .emi-sub {
            margin:0;
            color:var(--muted);
            font-size:14px;
            max-width:740px;
        }

        /* micro chips row */
        .emi-chips {
            display:flex;
            gap:8px;
            margin-top:10px;
            justify-content:flex-start;
            flex-wrap:wrap;
        }
        .chip {
            display:inline-flex;
            align-items:center;
            gap:8px;
            padding:6px 10px;
            border-radius:999px;
            font-size:13px;
            color: white;
            background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
            box-shadow: 0 8px 18px rgba(91,155,213,0.08);
            font-weight:700;
        }

        /* Progress step styles (preserve original classes) */
        .step-card {
            padding:10px;
            border-radius:10px;
            text-align:center;
            border:1px solid var(--border);
            background: var(--card);
            color:var(--muted);
            transition: transform .12s ease;
            box-shadow: 0 6px 18px rgba(38,56,84,0.04);
        }
        .step-card.current {
            background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
            color: white;
            font-weight:700;
            box-shadow: var(--shadow-sm);
        }
        .step-card.done {
            background: linear-gradient(90deg, #66d9a7, #5dade2);
            color: white;
            font-weight:700;
        }
        .step-card:hover { transform: translateY(-4px); }

        /* Section titles */
        .section-title { font-size:18px; margin: 10px 0 12px 0; color: var(--text); font-weight:600; }

        /* Feature / container cards */
        .form-card {
            padding:16px;
            border-radius: 12px;
            border: 1px solid var(--border);
            background: var(--card);
            box-shadow: 0 8px 26px rgba(38,56,84,0.04);
        }

        /* Result badges */
        .result-card {
            padding:20px;
            border-radius:14px;
            color: white;
            text-align:center;
            font-weight:700;
            border: 1px solid var(--border);
            box-shadow: var(--shadow-hover);
        }
        .result-eligible { background: linear-gradient(135deg, #66d9a7, #5dade2); }
        .result-risk { background: linear-gradient(135deg, #f093fb, #f5576c); }
        .result-not { background: linear-gradient(135deg, #ffa07a, #fee140); color:#2c3e50; }

        /* Result EMI box */
        .emi-box {
            padding:18px;
            border-radius:14px;
            text-align:center;
            background: linear-gradient(135deg, rgba(227,242,253,0.9), rgba(243,229,245,0.85));
            border:1px solid var(--border);
            color:var(--text);
            box-shadow: 0 8px 20px rgba(38,56,84,0.04);
        }
        .emi-value { font-size:28px; font-weight:800; margin-top:8px; }

        /* Button styling */
        div.stButton > button {
            background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
            color: white;
            border: none;
            padding: 12px 18px;
            border-radius: 10px;
            font-weight: 700;
            box-shadow: 0 8px 26px rgba(91, 155, 213, 0.18);
            transition: transform .12s ease, box-shadow .12s ease, opacity .12s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 14px 36px rgba(38,56,84,0.12);
            opacity: 0.98;
        }

        /* Expander / charts spacing */
        .stExpander { border-radius: 10px; border:1px solid var(--border); background: var(--card); }
        .footer-small { color: var(--muted); font-size:13px; text-align:center; padding:12px; margin-top:14px; }

        /* Plotly charts rounding */
        .element-container .stPlotlyChart > div { border-radius: 10px; overflow: hidden; border:1px solid var(--border); }

        @media (max-width: 900px) {
            .emi-header { padding:16px; }
            .emi-top { flex-direction:column; align-items:center; gap:10px; }
            .emi-heading { align-items:center; text-align:center; }
            .emi-title { font-size:22px; }
            .emi-sub { font-size:13px; max-width:420px; }
            .chip { font-size:12px; padding:5px 8px; }
        }

        /* Respect reduced motion */
        @media (prefers-reduced-motion: reduce) {
            .stApp::before, .stApp::after, .emi-header, .step-card { animation: none !important; transition: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Header ----------
    st.markdown(
        """
        <div class="emi-header" role="banner" aria-label="EMI Smart Calculator Header">
            <div class="accent-ribbon" aria-hidden="true"></div>
            <div class="emi-top">
                <div class="emi-logo" aria-hidden="true">EMI</div>
                <div class="emi-heading">
                    <h1 class="emi-title">🧮 <span class="accent-text">EMI Smart Calculator</span></h1>
                    <p class="emi-sub">AI-Powered EMI Eligibility & Prediction Engine — fast, private, and beginner-friendly</p>
                    <div class="emi-chips" aria-hidden="true">
                        <div class="chip">AI Driven</div>
                        <div class="chip">Instant Results</div>
                        <div class="chip">Privacy-first</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress indicator
    if 'step' not in st.session_state:
        st.session_state.step = 1

    # Step indicator
    progress_cols = st.columns(4)
    steps = ["👤 Personal", "💼 Employment", "💳 Financial", "📊 Results"]

    for i, (col, step_name) in enumerate(zip(progress_cols, steps), 1):
        with col:
            # Use class names but preserve original content & ordering
            if i < st.session_state.step:
                st.markdown(
                    f"""
                    <div class="step-card done">
                        <p style="margin:0;">✓ {step_name}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif i == st.session_state.step:
                st.markdown(
                    f"""
                    <div class="step-card current">
                        <p style="margin:0;">● {step_name}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="step-card">
                        <p style="margin:0; color:var(--muted);">○ {step_name}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<br>", unsafe_allow_html=True)

    # Form with tabs
    tab1, tab2, tab3 = st.tabs(["👤 Personal Info", "💼 Professional Details", "💰 Financial Profile"])

    with tab1:
        st.markdown('<div class="section-title">👤 Personal Information</div>', unsafe_allow_html=True)

        pcol1, pcol2 = st.columns(2)

        with pcol1:
            with st.container():
                st.markdown('<div class="form-card"><strong>🎂 Age & Demographics</strong>', unsafe_allow_html=True)
                age = st.slider("Age", 18, 75, 30, help="Your current age")
                gender = st.selectbox("Gender", ["Male", "Female"], help="Select your gender")
                marital_status = st.radio("Marital Status", ["Single", "Married"], horizontal=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with pcol2:
            with st.container():
                st.markdown('<div class="form-card"><strong>👨‍👩‍👧‍👦 Family Details</strong>', unsafe_allow_html=True)
                family_size = st.number_input("Family Size", 1, 20, 4, help="Total family members")
                dependents = st.number_input("Dependents", 0, 10, 2, help="Number of dependents")
                house_type = st.select_slider("House Type", options=["Rented", "Family", "Own"])
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("**🎓 Education Level**")
        education = st.selectbox(
            "Highest Qualification",
            ["High School", "Graduate", "Post Graduate", "Professional"],
            help="Your highest educational qualification"
        )

    with tab2:
        st.markdown('<div class="section-title">💼 Employment & Income</div>', unsafe_allow_html=True)

        ecol1, ecol2 = st.columns(2)

        with ecol1:
            with st.container():
                st.markdown('<div class="form-card"><strong>🏢 Employment Type</strong>', unsafe_allow_html=True)
                employment_type = st.selectbox(
                    "Sector",
                    ["Government", "Private", "Self-employed"],
                    help="Your employment sector"
                )
                company_type = st.selectbox(
                    "Company Category",
                    ["MNC", "Large Indian", "Mid-size", "Startup", "Small"],
                    help="Type of organization"
                )
                years_of_employment = st.number_input(
                    "Years of Experience",
                    0.0, 50.0, 3.0, 0.5,
                    help="Total professional experience"
                )
                st.markdown("</div>", unsafe_allow_html=True)

        with ecol2:
            with st.container():
                st.markdown('<div class="form-card"><strong>💰 Income Details</strong>', unsafe_allow_html=True)
                monthly_salary = st.number_input(
                    "Monthly Salary (₹)",
                    1000.0, 1_000_000.0, 40000.0, 1000.0,
                    help="Your gross monthly salary"
                )

                # Salary visualization (no change to logic)
                if monthly_salary > 0:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=monthly_salary,
                        title={'text': "Monthly Income"},
                        gauge={
                            'axis': {'range': [None, 100000]},
                            'bar': {'color': "#5b9bd5"},
                            'steps': [
                                {'range': [0, 30000], 'color': "#ffd700"},
                                {'range': [30000, 60000], 'color': "#90EE90"},
                                {'range': [60000, 100000], 'color': "#66d9a7"}
                            ]
                        }
                    ))
                    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="section-title">💳 Financial Profile</div>', unsafe_allow_html=True)

        # Financial Stability
        with st.expander("💎 Financial Stability", expanded=True):
            fcol1, fcol2, fcol3 = st.columns(3)

            with fcol1:
                credit_score = st.number_input("Credit Score", 300, 900, 650, 5)
                if credit_score >= 750:
                    st.success("✅ Excellent")
                elif credit_score >= 650:
                    st.info("ℹ️ Good")
                else:
                    st.warning("⚠️ Needs Improvement")

            with fcol2:
                bank_balance = st.number_input("Bank Balance (₹)", 0.0, 10_000_000.0, 100000.0, 5000.0)

            with fcol3:
                emergency_fund = st.number_input("Emergency Fund (₹)", 0.0, 10_000_000.0, 50000.0, 5000.0)

        # Loan Details
        with st.expander("🏦 Loan Requirements", expanded=True):
            lcol1, lcol2 = st.columns(2)

            with lcol1:
                requested_amount = st.number_input("Requested Amount (₹)", 10000.0, 5_000_000.0, 100000.0, 5000.0)
                requested_tenure = st.slider("Tenure (months)", 6, 120, 24, 6)

            with lcol2:
                existing_loans = st.radio("Existing Loans?", ["No", "Yes"], horizontal=True)
                current_emi_amount = st.number_input("Current EMI (₹)", 0.0, 500_000.0, 5000.0, 500.0)

        # EMI Scenario
        emi_scenario = st.selectbox(
            "📋 Loan Purpose",
            [
                "Personal Loan EMI",
                "E-commerce Shopping EMI",
                "Education EMI",
                "Vehicle EMI",
                "Home Appliances EMI"
            ]
        )

        # Monthly Expenses
        with st.expander("📊 Monthly Expenses Breakdown", expanded=True):
            exp_col1, exp_col2, exp_col3 = st.columns(3)

            with exp_col1:
                school_fees = st.number_input("School Fees (₹)", 0.0, 100_000.0, 2000.0, 500.0)
                college_fees = st.number_input("College Fees (₹)", 0.0, 500_000.0, 3000.0, 500.0)

            with exp_col2:
                travel_expenses = st.number_input("Travel (₹)", 0.0, 50_000.0, 1500.0, 500.0)
                groceries_utilities = st.number_input("Groceries & Utilities (₹)", 0.0, 50_000.0, 5000.0, 500.0)

            with exp_col3:
                monthly_rent = st.number_input("Rent (₹)", 0.0, 200_000.0, 8000.0, 500.0)
                other_monthly_expenses = st.number_input("Other Expenses (₹)", 0.0, 50_000.0, 1000.0, 500.0)

            # Expense Chart
            total_expenses = (school_fees + college_fees + travel_expenses +
                            groceries_utilities + monthly_rent + other_monthly_expenses)

            if total_expenses > 0:
                fig = go.Figure(data=[go.Pie(
                    labels=['School', 'College', 'Travel', 'Groceries', 'Rent', 'Other'],
                    values=[school_fees, college_fees, travel_expenses, groceries_utilities, monthly_rent, other_monthly_expenses],
                    hole=.4,
                    marker=dict(colors=['#5b9bd5', '#9b7bd8', '#f093fb', '#f5576c', '#4facfe', '#66d9a7'])
                )])
                fig.update_layout(
                    title="Expense Distribution",
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

    # Combine inputs (preserve variable names and structure)
    input_dict = {
        "age": age, "gender": gender, "marital_status": marital_status,
        "education": education, "employment_type": employment_type,
        "company_type": company_type, "years_of_employment": years_of_employment,
        "monthly_salary": monthly_salary, "family_size": family_size,
        "dependents": dependents, "house_type": house_type,
        "existing_loans": existing_loans, "current_emi_amount": current_emi_amount,
        "requested_amount": requested_amount, "requested_tenure": requested_tenure,
        "emi_scenario": emi_scenario, "credit_score": credit_score,
        "bank_balance": bank_balance, "emergency_fund": emergency_fund,
        "school_fees": school_fees, "college_fees": college_fees,
        "travel_expenses": travel_expenses, "groceries_utilities": groceries_utilities,
        "other_monthly_expenses": other_monthly_expenses, "monthly_rent": monthly_rent
    }

    # Predict button (centered using columns)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_btn = st.button("🔮 Calculate EMI Eligibility", use_container_width=True, type="primary")

    if predict_btn:
        with st.spinner("🤖 AI is analyzing your profile..."):
            try:
                clf_pred, reg_pred = predict_emi(input_dict, MODEL_DIR)

                st.balloons()

                # Results Section
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-title">📊 Prediction Results</div>', unsafe_allow_html=True)

                result_col1, result_col2 = st.columns(2)

                with result_col1:
                    # Styled result blocks but same logic and texts preserved
                    if clf_pred == "Eligible":
                        st.markdown(
                            """
                            <div class="result-card result-eligible">
                                <div style="font-size:22px;">🎉 ELIGIBLE</div>
                                <div style="margin-top:8px; font-size:14px;">Congratulations! You qualify for EMI</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    elif clf_pred == "High_Risk":
                        st.markdown(
                            """
                            <div class="result-card result-risk">
                                <div style="font-size:22px;">⚠️ HIGH RISK</div>
                                <div style="margin-top:8px; font-size:14px;">Caution: High risk profile</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            """
                            <div class="result-card result-not">
                                <div style="font-size:22px;">❌ NOT ELIGIBLE</div>
                                <div style="margin-top:8px; font-size:14px;">Currently not qualified</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                with result_col2:
                    st.markdown(
                        f"""
                        <div class="emi-box">
                            <div style="font-size:16px; font-weight:700;">💰 Maximum EMI</div>
                            <div class="emi-value">₹ {reg_pred:,.2f}</div>
                            <div style="margin-top:6px; color:var(--muted); font-size:13px;">Per Month</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # Store in session state
                st.session_state.prediction_result = {'eligibility': clf_pred, 'max_emi': reg_pred}
                st.session_state.user_inputs = input_dict

                # Gauge chart for EMI capacity (logic preserved)
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=reg_pred,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "EMI Capacity", 'font': {'size': 24}},
                    delta={'reference': monthly_salary * 0.4},
                    gauge={
                        'axis': {'range': [None, monthly_salary]},
                        'bar': {'color': "#5b9bd5"},
                        'steps': [
                            {'range': [0, monthly_salary * 0.3], 'color': "#e3f2fd"},
                            {'range': [monthly_salary * 0.3, monthly_salary * 0.5], 'color': "#90caf9"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': monthly_salary * 0.5
                        }
                    }
                ))
                fig.update_layout(height=400, margin=dict(l=20, r=20, t=60, b=20))
                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"⚠️ Error: {e}")

    # Small footer note
    st.markdown('<div class="footer-small">A modern EMI prediction platform — crafted for clarity, trust, and precision.</div>', unsafe_allow_html=True)
