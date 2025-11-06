import streamlit as st
import joblib
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import subprocess
import platform

def show_metrics(MODEL_DIR):
    # -------------------------
    # Global modern CSS theme - LIGHT THEME
    # -------------------------
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
            --border: #e1e8ed;
            --radius: 14px;
            --shadow: 0 10px 30px rgba(38,56,84,0.06);
            --shadow-hover: 0 18px 60px rgba(38,56,84,0.10);
            --glass-alpha: 0.78;
        }

        /* App background: layered gradients + soft floating forms */
        .stApp, .main {
            min-height: 100vh;
            background:
                radial-gradient(900px 420px at 6% 8%, rgba(91,155,213,0.05), transparent 8%),
                radial-gradient(700px 360px at 94% 86%, rgba(155,123,216,0.035), transparent 6%),
                linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%) !important;
            color: var(--text);
            font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
            -webkit-font-smoothing:antialiased;
            -moz-osx-font-smoothing:grayscale;
        }

        /* Decorative floating shapes for subtle depth */
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
            50% { transform: translateY(14px) rotate(1.6deg); }
            100% { transform: translateY(0) rotate(0deg); }
        }

        /* Metrics header - glass hero card */
        .metrics-header {
            position: relative;
            z-index: 2;
            padding: 20px;
            border-radius: calc(var(--radius) + 6px);
            background: linear-gradient(135deg, rgba(255,255,255,var(--glass-alpha)), rgba(250,250,250,0.92));
            border: 1px solid rgba(40,55,71,0.04);
            box-shadow: var(--shadow);
            text-align: center;
            transition: transform .22s cubic-bezier(.2,.9,.3,1), box-shadow .22s ease;
            margin-bottom: 18px;
            display:flex;
            align-items:center;
            justify-content:center;
            gap:18px;
            flex-direction:column;
            max-width: 980px;
            margin-left: auto;
            margin-right: auto;
            backdrop-filter: blur(6px) saturate(120%);
        }
        .metrics-header:hover { transform: translateY(-6px); box-shadow: var(--shadow-hover); }

        /* decorative accent ribbon */
        .metrics-header .accent-ribbon {
            position: absolute;
            right: -48px;
            top: -48px;
            width: 220px;
            height: 220px;
            transform: rotate(34deg);
            background: conic-gradient(from 180deg at 50% 50%, rgba(91,155,213,0.12), rgba(155,123,216,0.08));
            filter: blur(22px);
            opacity: 0.95;
            pointer-events: none;
        }

        .metrics-hero {
            display:flex;
            align-items:center;
            gap:16px;
            justify-content:center;
            width:100%;
            padding: 6px 12px;
        }

        .metrics-logo {
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

        .metrics-title-wrap {
            display:flex;
            flex-direction:column;
            align-items:flex-start;
            gap:6px;
            text-align:left;
            max-width:760px;
        }

        .metrics-title {
            margin:0;
            font-size:30px;
            color:var(--text);
            font-weight:700;
            line-height:1.02;
        }
        .metrics-title .accent-text {
            background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .metrics-sub {
            margin:0;
            color:var(--muted);
            font-size:14px;
            max-width:740px;
        }

        .metrics-chips {
            display:flex;
            gap:8px;
            margin-top:8px;
            flex-wrap:wrap;
            justify-content:flex-start;
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

        /* Metric cards improved visuals */
        .metric-card {
            padding:18px;
            border-radius:12px;
            text-align:center;
            color: white;
            border:1px solid var(--border);
            box-shadow: 0 8px 26px rgba(38,56,84,0.04);
            transition: transform .12s ease, box-shadow .12s ease;
        }
        .metric-card:hover { transform: translateY(-6px); box-shadow: var(--shadow-hover); }
        .metric-name { margin:0; font-size:13px; font-weight:600; opacity:0.95; }
        .metric-value { margin-top:10px; font-size:26px; font-weight:800; }

        .gradient-1 { background: linear-gradient(135deg, #5b9bd5 0%, #9b7bd8 100%); }
        .gradient-2 { background: linear-gradient(135deg, #9b7bd8 0%, #f093fb 100%); }
        .gradient-3 { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        .gradient-4 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }

        /* Section titles */
        .section-title { font-size:18px; color:var(--text); font-weight:700; margin: 10px 0 12px 0; }

        /* Sub headers & containers */
        .sub-header {
            padding:14px 16px;
            border-radius:10px;
            background: var(--card-bg);
            border:1px solid var(--border);
            color:var(--text);
            margin-bottom:12px;
            box-shadow: 0 8px 22px rgba(38,56,84,0.04);
        }

        /* Expander / plot styles */
        .stExpander { border-radius:10px; border:1px solid var(--border); background: var(--card-bg); }
        .element-container .stPlotlyChart > div { border-radius:12px; overflow:hidden; border:1px solid var(--border); }

        /* MLflow box */
        .mlflow-box {
            padding:16px;
            border-radius:12px;
            background: linear-gradient(135deg, rgba(227,242,253,0.9) 0%, rgba(243,229,245,0.9) 100%);
            border:1px solid var(--border);
            box-shadow: 0 8px 26px rgba(38,56,84,0.04);
        }

        /* Launch button refinement */
        div.stButton > button {
            background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
            color: white;
            border: none;
            padding: 10px 12px;
            border-radius: 10px;
            font-weight: 700;
            box-shadow: 0 10px 30px rgba(91, 155, 213, 0.14);
            transition: transform .12s ease, box-shadow .12s ease;
        }
        div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 18px 40px rgba(38,56,84,0.12); }

        @media (max-width: 900px) {
            .metrics-header { padding:14px; }
            .metrics-title { font-size:22px; text-align:center; }
            .metrics-logo { width:56px; height:56px; font-size:18px; border-radius:12px; }
            .metric-value { font-size:20px; }
        }

        /* Respect reduced motion */
        @media (prefers-reduced-motion: reduce) {
            .stApp::before, .stApp::after, .metrics-header { animation: none !important; transition: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------
    # Header (styled)
    # -------------------------
    st.markdown(
        """
        <div class="metrics-header" role="banner" aria-label="Model Performance Header">
            <div class="accent-ribbon" aria-hidden="true"></div>
            <div class="metrics-hero">
                <div class="metrics-logo" aria-hidden="true">ML</div>
                <div class="metrics-title-wrap">
                    <h1 class="metrics-title">🎪 <span class="accent-text">Model Performance</span> Metrics</h1>
                    <p class="metrics-sub">AI Model Analytics & Evaluation Dashboard — clear, actionable, and production-ready</p>
                    <div class="metrics-chips" aria-hidden="true" style="margin-top:8px;">
                        <div class="chip">Classification</div>
                        <div class="chip">Regression</div>
                        <div class="chip">Feature Analysis</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------
    # Load Models & Metrics (keep logic intact)
    # -------------------------
    clf_file = [f for f in os.listdir(MODEL_DIR) if f.startswith("best_classifier")][0]
    reg_file = [f for f in os.listdir(MODEL_DIR) if f.startswith("best_regressor")][0]

    clf = joblib.load(Path(MODEL_DIR) / clf_file)
    reg = joblib.load(Path(MODEL_DIR) / reg_file)

    metrics_dir = Path(MODEL_DIR) / "metrics"
    clf_metrics_file = metrics_dir / "classifier_metrics.joblib"
    reg_metrics_file = metrics_dir / "regressor_metrics.joblib"

    if clf_metrics_file.exists():
        clf_metrics = joblib.load(clf_metrics_file)
    else:
        clf_metrics = {"accuracy": "N/A", "f1": "N/A", "precision": "N/A", "recall": "N/A", "roc_auc": "N/A"}

    if reg_metrics_file.exists():
        reg_metrics = joblib.load(reg_metrics_file)
    else:
        reg_metrics = {"rmse": "N/A", "mae": "N/A", "r2": "N/A", "mape": "N/A"}

    # -------------------------
    # Tabs
    # -------------------------
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Classification", "📈 Regression", "🔬 Feature Analysis", "🚀 MLflow"])

    # -------------------------
    # Classification Tab
    # -------------------------
    with tab1:
        st.markdown('<div class="section-title">🎯 Classification Model Performance</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="sub-header">
                <h3 style="margin:0;color:var(--text);font-weight:700;">🤖 Model: {clf.__class__.__name__}</h3>
                <p style="margin:6px 0 0 0; color:var(--muted);">EMI Eligibility Classifier</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Metrics in cards (styled)
        metric_cols = st.columns(5)

        metrics_data = [
            ("🎯 Accuracy", clf_metrics.get("accuracy", "N/A"), "gradient-1"),
            ("⚡ F1 Score", clf_metrics.get("f1", "N/A"), "gradient-2"),
            ("🔍 Precision", clf_metrics.get("precision", "N/A"), "gradient-3"),
            ("📊 Recall", clf_metrics.get("recall", "N/A"), "gradient-3"),
            ("📈 ROC AUC", clf_metrics.get("roc_auc", "N/A"), "gradient-4")
        ]

        for col, (name, value, grad_class) in zip(metric_cols, metrics_data):
            with col:
                # Keep same displayed value/formatting while using new visual style
                try:
                    if value != "N/A":
                        val_numeric = float(value)
                        display_val = f"{val_numeric:.3f}"
                    else:
                        display_val = value
                except:
                    display_val = value

                st.markdown(
                    f"""
                    <div class="metric-card {grad_class}">
                        <div class="metric-name">{name}</div>
                        <div class="metric-value">{display_val}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # Gauge charts for metrics (logic preserved)
        if clf_metrics.get("accuracy") != "N/A":
            fig = go.Figure()

            metrics_to_plot = []
            if clf_metrics.get("accuracy") != "N/A":
                metrics_to_plot.append(("Accuracy", clf_metrics["accuracy"]))
            if clf_metrics.get("f1") != "N/A":
                metrics_to_plot.append(("F1 Score", clf_metrics["f1"]))
            if clf_metrics.get("precision") != "N/A":
                metrics_to_plot.append(("Precision", clf_metrics["precision"]))

            if metrics_to_plot:
                for i, (metric_name, metric_value) in enumerate(metrics_to_plot[:3]):
                    fig.add_trace(go.Indicator(
                        mode="gauge+number",
                        value=float(metric_value),
                        title={'text': metric_name, 'font': {'size': 20}},
                        domain={'row': 0, 'column': i},
                        gauge={
                            'axis': {'range': [0, 1]},
                            'bar': {'color': ["#5b9bd5", "#9b7bd8", "#f093fb"][i]},
                            'steps': [
                                {'range': [0, 0.5], 'color': "#e1e8ed"},
                                {'range': [0.5, 0.75], 'color': "#c8d6e5"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 0.9
                            }
                        }
                    ))

                fig.update_layout(
                    grid={'rows': 1, 'columns': len(metrics_to_plot), 'pattern': "independent"},
                    height=300,
                    margin=dict(l=20, r=20, t=60, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

        # Detailed Metrics
        with st.expander("📋 Detailed Metrics Breakdown", expanded=False):
            st.json(clf_metrics)

    # -------------------------
    # Regression Tab
    # -------------------------
    with tab2:
        st.markdown('<div class="section-title">📈 Regression Model Performance</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="sub-header">
                <h3 style="margin:0;color:var(--text);font-weight:700;">🤖 Model: {reg.__class__.__name__}</h3>
                <p style="margin:6px 0 0 0; color:var(--muted);">Maximum EMI Predictor</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Metrics in cards (styled)
        reg_metric_cols = st.columns(4)

        reg_metrics_data = [
            ("📉 RMSE", reg_metrics.get("rmse", "N/A"), "gradient-4"),
            ("📊 MAE", reg_metrics.get("mae", "N/A"), "gradient-4"),
            ("🎯 R² Score", reg_metrics.get("r2", "N/A"), "gradient-1"),
            ("📈 MAPE", reg_metrics.get("mape", "N/A"), "gradient-3")
        ]

        for col, (name, value, grad_class) in zip(reg_metric_cols, reg_metrics_data):
            with col:
                try:
                    display_val = value if value == "N/A" else f"{float(value):.2f}"
                except:
                    display_val = value

                st.markdown(
                    f"""
                    <div class="metric-card {grad_class}">
                        <div class="metric-name">{name}</div>
                        <div class="metric-value">{display_val}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # R² Score Gauge (logic preserved)
        if reg_metrics.get("r2") != "N/A":
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=float(reg_metrics["r2"]),
                title={'text': "R² Score", 'font': {'size': 24}},
                delta={'reference': 0.9},
                gauge={
                    'axis': {'range': [0, 1]},
                    'bar': {'color': "#4facfe"},
                    'steps': [
                        {'range': [0, 0.6], 'color': "#e1e8ed"},
                        {'range': [0.6, 0.8], 'color': "#c8d6e5"}
                    ],
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75,
                        'value': 0.95
                    }
                }
            ))
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=60, b=20))
            st.plotly_chart(fig, use_container_width=True)

        # Detailed Metrics
        with st.expander("📋 Detailed Metrics Breakdown", expanded=False):
            st.json(reg_metrics)

    # -------------------------
    # Feature Analysis Tab
    # -------------------------
    with tab3:
        st.markdown('<div class="section-title">🔬 Feature Importance Analysis</div>', unsafe_allow_html=True)

        def plot_feature_importance(model, title="Feature Importance", color_scale="Viridis"):
            try:
                if hasattr(model, "feature_importances_"):
                    importance = model.feature_importances_
                elif hasattr(model, "coef_"):
                    importance = np.abs(model.coef_)
                else:
                    st.info("Feature importance not available for this model.")
                    return

                if hasattr(model, "feature_names_in_"):
                    features = model.feature_names_in_
                else:
                    features = [f"Feature {i}" for i in range(len(importance))]

                fi_df = pd.DataFrame({"feature": features, "importance": importance})
                fi_df = fi_df.sort_values(by="importance", ascending=False).head(20)

                fig = px.bar(
                    fi_df,
                    x="importance",
                    y="feature",
                    orientation='h',
                    title=title,
                    color="importance",
                    color_continuous_scale=color_scale,
                    height=500
                )
                fig.update_layout(
                    xaxis_title="Importance Score",
                    yaxis_title="Features",
                    yaxis={'categoryorder': 'total ascending'},
                    margin=dict(l=20, r=20, t=60, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

                return fi_df
            except Exception as e:
                st.warning(f"Could not plot feature importance: {e}")
                return None

        # Classification Model Features
        st.markdown("#### 🎯 Classification Model Features")
        clf_fi = plot_feature_importance(clf, title="Top 20 Features - Classification", color_scale="Blues")

        if clf_fi is not None:
            with st.expander("📊 View Feature Importance Data"):
                st.dataframe(clf_fi, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Regression Model Features
        st.markdown("#### 📈 Regression Model Features")
        reg_fi = plot_feature_importance(reg, title="Top 20 Features - Regression", color_scale="Reds")

        if reg_fi is not None:
            with st.expander("📊 View Feature Importance Data"):
                st.dataframe(reg_fi, use_container_width=True)

    # -------------------------
    # MLflow Tab
    # -------------------------
    with tab4:
        st.markdown('<div class="section-title">🚀 MLflow Experiment Tracking</div>', unsafe_allow_html=True)

        mlruns_path = Path(MODEL_DIR).parent / "mlruns"

        if mlruns_path.exists():
            st.markdown(
                """
                <div class="mlflow-box">
                    <h3 style="margin:0;color:var(--text);font-weight:700;">🔗 MLflow Dashboard</h3>
                    <p style="margin:6px 0 0 0;color:var(--muted);">Track experiments, compare models, and analyze training runs</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)

            with col1:
                st.info(f"📁 **MLflow Path:** `{mlruns_path}`")

            with col2:
                st.success("✅ **Status:** MLflow tracking enabled")

            st.markdown("<br>", unsafe_allow_html=True)

            mlflow_ui_command = f"mlflow ui --backend-store-uri file:///{mlruns_path.as_posix()}"

            st.code(mlflow_ui_command, language="bash")

            st.markdown(
                """
                **🎯 To launch MLflow UI:**
                1. Copy the command above
                2. Run it in your terminal
                3. Visit [http://localhost:5000](http://localhost:5000)
                """
            )

            if st.button("🚀 Launch MLflow Dashboard", use_container_width=True, type="primary"):
                try:
                    if platform.system() == "Windows":
                        subprocess.Popen(["cmd", "/c", mlflow_ui_command], creationflags=subprocess.CREATE_NEW_CONSOLE)
                    else:
                        subprocess.Popen(["bash", "-c", mlflow_ui_command])
                    st.success("✅ MLflow Dashboard launching... Visit http://localhost:5000")
                except Exception as e:
                    st.error(f"❌ Failed to launch: {e}")
        else:
            st.warning("⚠️ MLflow folder not found. Ensure training was run with MLflow tracking.")
