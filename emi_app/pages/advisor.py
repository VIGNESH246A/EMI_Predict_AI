# pages/advisor.py

import streamlit as st
import plotly.graph_objects as go

def show_advisor():
    # ---------- Global modern CSS - LIGHT THEME ----------
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        :root{
            --bg-1: #f8f9fa;
            --bg-2: #ffffff;
            --card-bg: #ffffff;
            --muted: #6c757d;
            --text: #2c3e50;
            --accent-blue: #5b9bd5;
            --accent-purple: #9b7bd8;
            --accent-teal: #66d9a7;
            --accent-coral: #f5576c;
            --gold: #ffd700;
            --border: #e1e8ed;
            --radius: 14px;
            --shadow: 0 8px 28px rgba(38,56,84,0.06);
            --shadow-hover: 0 18px 48px rgba(38,56,84,0.10);
            --glass-alpha: 0.72;
        }

        /* App background: soft layered gradients + subtle floating blobs */
        .stApp, .main {
            min-height: 100vh;
            background:
                radial-gradient(800px 400px at 5% 10%, rgba(91,155,213,0.05), transparent 8%),
                radial-gradient(700px 360px at 95% 85%, rgba(155,123,216,0.04), transparent 6%),
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
        .advisor-header {
            position: relative;
            z-index: 2;
            display: flex;
            align-items: center;
            gap: 18px;
            padding: 20px;
            border-radius: calc(var(--radius) + 6px);
            background: linear-gradient(135deg, rgba(255,255,255,var(--glass-alpha)), rgba(250,250,250,0.86));
            border: 1px solid rgba(40,55,71,0.04);
            box-shadow: var(--shadow);
            backdrop-filter: blur(6px) saturate(120%);
            transition: transform 0.22s cubic-bezier(.2,.9,.3,1), box-shadow 0.22s ease;
            margin-bottom: 18px;
            justify-content: center;
            text-align: center;
            flex-direction: column;
        }
        .advisor-header:hover { transform: translateY(-6px); box-shadow: var(--shadow-hover); }

        /* decorative ribbon */
        .advisor-header .accent-ribbon {
            position: absolute;
            right: -40px;
            top: -44px;
            width: 220px;
            height: 220px;
            transform: rotate(34deg);
            background: conic-gradient(from 180deg at 50% 50%, rgba(91,155,213,0.14), rgba(155,123,216,0.10), rgba(91,155,213,0.06));
            filter: blur(22px);
            opacity: 0.95;
            pointer-events: none;
        }

        .advisor-top {
            display:flex;
            align-items:center;
            gap:16px;
            justify-content:center;
            width:100%;
            max-width:980px;
        }

        .advisor-logo {
            width:72px;
            height:72px;
            border-radius:14px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:22px;
            font-weight:700;
            color: white;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            box-shadow: 0 10px 28px rgba(91,155,213,0.12), inset 0 -6px 16px rgba(255,255,255,0.06);
            flex-shrink:0;
        }

        .advisor-heading {
            display:flex;
            flex-direction:column;
            align-items:center;
            gap:6px;
            text-align:center;
        }

        .advisor-title {
            margin:0;
            font-size:28px;
            color:var(--text);
            font-weight:700;
            line-height:1.02;
        }
        .advisor-title .accent-text {
            background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .advisor-sub {
            margin:0;
            color:var(--muted);
            font-size:14px;
            max-width:820px;
        }

        /* micro chips row */
        .advisor-chips {
            display:flex;
            gap:8px;
            margin-top:10px;
            justify-content:center;
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
            background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
            box-shadow: 0 8px 18px rgba(91,155,213,0.08);
            font-weight:700;
        }

        /* existing classes reuse and improvements */
        .status-banner {
            padding:20px;
            border-radius:12px;
            color: white;
            text-align:center;
            font-weight:700;
            border:1px solid var(--border);
            box-shadow: var(--shadow);
            margin-bottom:14px;
        }
        .status-eligible { background: linear-gradient(135deg, var(--accent-teal) 0%, #5dade2 100%); }
        .status-risk { background: linear-gradient(135deg, #f093fb 0%, var(--accent-coral) 100%); }
        .status-not { background: linear-gradient(135deg, #ffa07a 0%, var(--gold) 100%); color:#2c3e50; }

        .info-panel {
            padding:16px;
            border-radius:12px;
            border-left:6px solid var(--accent-teal);
            background: var(--card-bg);
            border:1px solid var(--border);
            box-shadow: var(--shadow);
            margin-bottom:12px;
        }
        .info-panel.alt { border-left-width:6px; border-left-style:solid; margin-bottom:12px; }

        .info-title { font-size:15px; margin:0 0 8px 0; font-weight:700; }
        .info-desc { color:var(--muted); margin:0; font-size:14px; line-height:1.5; }

        .chart-card {
            padding:14px;
            border-radius:12px;
            background: var(--card-bg);
            border:1px solid var(--border);
            box-shadow: var(--shadow);
            margin-bottom:14px;
        }

        .cta-link { color: var(--accent-blue); text-decoration: none; font-weight:700; }

        .small-info { padding:10px 12px; border-radius:10px; background: var(--card-bg); border:1px solid var(--border); color:var(--muted); }

        /* Buttons - keep style but refine shadows */
        div.stButton > button {
            background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
            color: white;
            border: none;
            padding: 10px 14px;
            border-radius: 10px;
            font-weight: 700;
            box-shadow: 0 8px 26px rgba(91, 155, 213, 0.18);
            transition: transform .12s ease, box-shadow .12s ease;
        }
        div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 14px 36px rgba(38,56,84,0.12); }

        /* Plot rounding */
        .element-container .stPlotlyChart > div { border-radius:12px; overflow:hidden; border:1px solid var(--border); box-shadow: none; }

        @media (max-width: 900px) {
            .advisor-top { flex-direction: column; gap:12px; padding: 8px 6px; }
            .advisor-logo { width:56px; height:56px; font-size:18px; border-radius:12px; }
            .advisor-title { font-size:20px; }
            .advisor-sub { font-size:13px; max-width:420px; }
        }

        /* Respect reduced motion */
        @media (prefers-reduced-motion: reduce) {
            .stApp::before, .stApp::after, .advisor-header, .status-banner { animation: none !important; transition: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Header ----------
    st.markdown(
        """
        <div class="advisor-header" role="banner" aria-label="AI Financial Advisor Header">
            <div class="accent-ribbon" aria-hidden="true"></div>
            <div class="advisor-top">
                <div class="advisor-logo" aria-hidden="true">AI</div>
                <div class="advisor-heading">
                    <h1 class="advisor-title">🤖 <span class="accent-text">AI Financial Advisor</span></h1>
                    <p class="advisor-sub">Personalized Financial Guidance & Recommendations — practical, actionable, and easy to follow</p>
                    <div class="advisor-chips" aria-hidden="true">
                        <div class="chip">Personalized</div>
                        <div class="chip">Actionable</div>
                        <div class="chip">Privacy-first</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Check if prediction exists
    has_prediction = st.session_state.get('prediction_result') is not None

    # Tabs for different advice sections
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Personalized Advice", "📚 General Tips", "💡 Best Practices", "📊 Financial Health"])

    with tab1:
        st.markdown("### 🎯 Your Personalized Recommendations")

        if has_prediction:
            clf_pred = st.session_state.prediction_result['eligibility']
            reg_pred = st.session_state.prediction_result['max_emi']
            user_inputs = st.session_state.user_inputs

            # Status Banner
            if clf_pred == "Eligible":
                st.markdown(
                    """
                    <div class="status-banner status-eligible">
                        <div style="font-size:20px;">🎉 ELIGIBLE FOR EMI</div>
                        <div style="margin-top:8px; font-size:14px; font-weight:600;">Great! You qualify for loan approval</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(
                        """
                        <div class="info-panel" style="border-left:5px solid #66d9a7;">
                            <div class="info-title" style="color:#66d9a7;">✅ What You're Doing Right</div>
                            <div class="info-desc">
                                <ul style="margin:6px 0 0 18px; color:var(--text);">
                                    <li>Strong financial profile</li>
                                    <li>Good credit management</li>
                                    <li>Stable income source</li>
                                    <li>Manageable debt-to-income ratio</li>
                                </ul>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col2:
                    st.markdown(
                        f"""
                        <div class="info-panel" style="border-left:5px solid #5b9bd5;">
                            <div class="info-title" style="color:#5b9bd5;">💡 Optimization Tips</div>
                            <div class="info-desc">
                                <ul style="margin:6px 0 0 18px; color:var(--text);">
                                    <li>Maximum EMI: <strong>₹{reg_pred:,.2f}</strong></li>
                                    <li>Stay within 80% of max EMI for comfort</li>
                                    <li>Maintain emergency fund of 6+ months</li>
                                    <li>Consider longer tenure for lower EMI</li>
                                </ul>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                # EMI Planning Calculator
                st.markdown("#### 🧮 EMI Planning Calculator")

                recommended_emi = reg_pred * 0.8
                safe_emi = reg_pred * 0.6

                fig = go.Figure()

                fig.add_trace(go.Bar(
                    y=['Safe EMI\n(60%)', 'Recommended EMI\n(80%)', 'Maximum EMI\n(100%)'],
                    x=[safe_emi, recommended_emi, reg_pred],
                    orientation='h',
                    marker=dict(
                        color=['#66d9a7', '#5b9bd5', '#f5576c'],
                        line=dict(color='white', width=2)
                    ),
                    text=[f'₹{safe_emi:,.0f}', f'₹{recommended_emi:,.0f}', f'₹{reg_pred:,.0f}'],
                    textposition='auto',
                ))

                fig.update_layout(
                    title="EMI Planning Guide",
                    xaxis_title="Monthly EMI Amount (₹)",
                    height=300,
                    margin=dict(l=20, r=20, t=60, b=20)
                )

                st.plotly_chart(fig, use_container_width=True)

                st.info(f"💡 **Recommendation:** Aim for EMI around ₹{recommended_emi:,.2f} for comfortable repayment")

            elif clf_pred == "High_Risk":
                st.markdown(
                    """
                    <div class="status-banner status-risk">
                        <div style="font-size:20px;">⚠️ HIGH RISK PROFILE</div>
                        <div style="margin-top:8px; font-size:14px; font-weight:600;">Caution: Financial risk detected</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                    <div class="info-panel" style="border-left:5px solid #f5576c;">
                        <div class="info-title" style="color:#f5576c;">🎯 Priority Actions Required</div>
                        <div class="info-desc">
                            <ol style="margin:6px 0 0 18px; color:var(--text);">
                                <li><strong>Reduce Current EMIs:</strong> Pay off existing loans to lower your debt burden</li>
                                <li><strong>Increase Savings:</strong> Build emergency fund to at least ₹{user_inputs.get('monthly_salary', 0) * 3:,.0f}</li>
                                <li><strong>Improve Credit Score:</strong> Current: {user_inputs.get('credit_score', 'N/A')} - Target: 750+</li>
                                <li><strong>Reduce Expenses:</strong> Cut non-essential spending by 20-30%</li>
                                <li><strong>Lower Loan Request:</strong> Consider requesting {user_inputs.get('requested_amount', 0) * 0.6:,.0f} instead</li>
                            </ol>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Risk Factors Visualization
                risk_factors = {
                    'High Existing EMI': 85,
                    'Low Credit Score': 70,
                    'Insufficient Savings': 60,
                    'High Debt-to-Income': 75,
                    'Low Emergency Fund': 65
                }

                fig = go.Figure(go.Bar(
                    x=list(risk_factors.values()),
                    y=list(risk_factors.keys()),
                    orientation='h',
                    marker=dict(color='#f5576c')
                ))

                fig.update_layout(
                    title="Risk Factor Analysis",
                    xaxis_title="Risk Level (%)",
                    height=300,
                    margin=dict(l=20, r=20, t=60, b=20)
                )

                st.plotly_chart(fig, use_container_width=True)

            else:  # Not Eligible
                st.markdown(
                    """
                    <div class="status-banner status-not">
                        <div style="font-size:20px;">❌ NOT ELIGIBLE</div>
                        <div style="margin-top:8px; font-size:14px; font-weight:600;">Don't worry! Here's your improvement roadmap</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    """
                    <div class="info-panel" style="border-left:5px solid #ffd700;">
                        <div class="info-title" style="color:#ffa500;">📋 30-Day Improvement Plan</div>
                        <div class="info-desc" style="color:var(--text);">
                            <p style="margin:6px 0 4px 0;"><strong>Week 1-2: Stabilize</strong></p>
                            <ul style="margin:6px 0 8px 18px; color:var(--text);">
                                <li>Clear all overdue payments</li>
                                <li>Set up automatic bill payments</li>
                                <li>Create detailed expense tracker</li>
                            </ul>
                            <p style="margin:6px 0 4px 0;"><strong>Week 3-4: Build</strong></p>
                            <ul style="margin:6px 0 0 18px; color:var(--text);">
                                <li>Save 20% of income</li>
                                <li>Reduce discretionary spending</li>
                                <li>Start emergency fund</li>
                            </ul>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Timeline visualization
                timeline_data = {
                    'Month': ['Now', '1 Month', '3 Months', '6 Months'],
                    'Target Score': [user_inputs.get('credit_score', 600), 650, 700, 750]
                }

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=timeline_data['Month'],
                    y=timeline_data['Target Score'],
                    mode='lines+markers',
                    line=dict(color='#ffd700', width=3),
                    marker=dict(size=10),
                    fill='tozeroy',
                    fillcolor='rgba(255, 215, 0, 0.15)'
                ))

                fig.update_layout(
                    title="Credit Score Improvement Timeline",
                    xaxis_title="Timeline",
                    yaxis_title="Credit Score",
                    height=300,
                    margin=dict(l=20, r=20, t=60, b=20)
                )

                st.plotly_chart(fig, use_container_width=True)

        else:
            st.markdown(
                """
                <div class="chart-card" style="text-align:center; padding:28px;">
                    <h3 style="margin:0; color:var(--muted);">📊 No Prediction Data Available</h3>
                    <p style="color:var(--muted); margin-top: 12px;">Complete the EMI Calculator first to receive personalized recommendations</p>
                    <br>
                    <a href='#' class="cta-link">→ Go to EMI Calculator</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab2:
        st.markdown("### 📚 General Financial Wisdom")

        tips_col1, tips_col2 = st.columns(2)

        with tips_col1:
            st.markdown(
                """
                <div class="info-panel alt" style="border-left:5px solid #5b9bd5;">
                    <div class="info-title" style="color:#5b9bd5;">💰 EMI Management Rules</div>
                    <div class="info-desc" style="color:var(--text);">
                        <ul style="margin:6px 0 0 18px;">
                            <li><strong>50-30-20 Rule:</strong> 50% needs, 30% wants, 20% savings</li>
                            <li><strong>EMI Limit:</strong> Keep total EMIs below 40% of income</li>
                            <li><strong>Emergency Fund:</strong> Maintain 6-12 months expenses</li>
                            <li><strong>Credit Utilization:</strong> Keep below 30% of limit</li>
                            <li><strong>Diversification:</strong> Don't put all eggs in one basket</li>
                        </ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="info-panel alt" style="border-left:5px solid #66d9a7;">
                    <div class="info-title" style="color:#66d9a7;">✅ Loan Application Tips</div>
                    <div class="info-desc" style="color:var(--text);">
                        <ul style="margin:6px 0 0 18px;">
                            <li>Check credit score before applying</li>
                            <li>Compare interest rates across lenders</li>
                            <li>Read all terms and conditions</li>
                            <li>Calculate true cost including fees</li>
                            <li>Have all documents ready</li>
                        </ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with tips_col2:
            st.markdown(
                """
                <div class="info-panel alt" style="border-left:5px solid #f5576c;">
                    <div class="info-title" style="color:#f5576c;">⚠️ Red Flags to Avoid</div>
                    <div class="info-desc" style="color:var(--text);">
                        <ul style="margin:6px 0 0 18px;">
                            <li>Taking loans for daily expenses</li>
                            <li>Multiple loan applications simultaneously</li>
                            <li>Ignoring loan terms and fine print</li>
                            <li>Missing EMI payment deadlines</li>
                            <li>Using credit card cash advances</li>
                        </ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="info-panel alt" style="border-left:5px solid #4facfe;">
                    <div class="info-title" style="color:#4facfe;">📈 Credit Score Boosters</div>
                    <div class="info-desc" style="color:var(--text);">
                        <ul style="margin:6px 0 0 18px;">
                            <li>Pay all bills on time, every time</li>
                            <li>Keep old credit accounts active</li>
                            <li>Mix of credit types (secured + unsecured)</li>
                            <li>Dispute errors on credit report</li>
                            <li>Limit hard credit inquiries</li>
                        </ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab3:
        st.markdown("### 💡 Best Practices for Financial Health")

        # Accordion-style best practices
        practices = [
            {
                "title": "🎯 Debt-to-Income Ratio Management",
                "content": """
                - **Target:** Keep below 40% of gross monthly income
                - **Calculation:** (Total Monthly Debt Payments / Gross Monthly Income) × 100
                - **Action:** If above 40%, prioritize debt reduction before new loans
                - **Impact:** Lower ratio = better loan approval chances
                """
            },
            {
                "title": "💳 Credit Utilization Optimization",
                "content": """
                - **Target:** Use less than 30% of available credit
                - **Strategy:** Pay off balances multiple times per month
                - **Benefit:** Improves credit score quickly
                - **Monitoring:** Check credit reports quarterly
                """
            },
            {
                "title": "💰 Emergency Fund Building",
                "content": """
                - **Goal:** 6-12 months of expenses
                - **Priority:** Build this BEFORE taking new loans
                - **Storage:** Keep in liquid, easily accessible account
                - **Usage:** Only for true emergencies
                """
            },
            {
                "title": "📊 Expense Tracking",
                "content": """
                - **Method:** Use apps or spreadsheets
                - **Frequency:** Review weekly, analyze monthly
                - **Categories:** Housing, food, transport, entertainment, savings
                - **Optimization:** Cut 10% from top 3 expense categories
                """
            }
        ]

        for practice in practices:
            with st.expander(practice["title"], expanded=False):
                st.markdown(practice["content"])

    with tab4:
        st.markdown("### 📊 Financial Health Checklist")

        # Interactive checklist
        st.markdown("#### ✅ Rate Your Financial Health")

        health_score = 0
        max_score = 0

        checks = [
            ("Emergency fund covers 6+ months expenses", 20),
            ("Credit score above 750", 20),
            ("Total EMIs less than 40% of income", 15),
            ("Regular savings of 20%+ of income", 15),
            ("No missed payments in last 12 months", 15),
            ("Diversified income sources", 10),
            ("Insurance coverage adequate", 5)
        ]

        for check, points in checks:
            if st.checkbox(check, key=check):
                health_score += points
            max_score += points

        health_percentage = (health_score / max_score) * 100 if max_score > 0 else 0

        # Health meter
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=health_percentage,
            title={'text': "Financial Health Score", 'font': {'size': 24}},
            delta={'reference': 80},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#5b9bd5"},
                'steps': [
                    {'range': [0, 40], 'color': "rgba(245, 87, 108, 0.28)"},
                    {'range': [40, 70], 'color': "rgba(255, 215, 0, 0.28)"},
                    {'range': [70, 100], 'color': "rgba(102, 217, 167, 0.28)"}
                ],
                'threshold': {
                    'line': {'color': "green", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=60, b=20))
        st.plotly_chart(fig, use_container_width=True)

        if health_percentage >= 80:
            st.success("🎉 Excellent! Your financial health is strong!")
        elif health_percentage >= 60:
            st.info("👍 Good! A few improvements will make you even stronger.")
        elif health_percentage >= 40:
            st.warning("⚠️ Fair. Focus on building emergency fund and reducing debt.")
        else:
            st.error("🚨 Needs attention. Prioritize financial stability before new loans.")
