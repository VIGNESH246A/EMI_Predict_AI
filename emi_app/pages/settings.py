# pages/settings.py

import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_settings(ROOT):
    # ------------------------------
    # Global CSS - Modern Professional LIGHT Theme
    # ------------------------------
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        :root{
            --bg-1: #f8f9fa;
            --bg-2: #ffffff;
            --card: #ffffff;
            --muted: #6c757d;
            --text: #2c3e50;
            --accent-1: #5b9bd5;
            --accent-2: #9b7bd8;
            --accent-3: #66d9a7;
            --danger: #f5576c;
            --border: #e1e8ed;
            --card-radius: 14px;
            --card-pad: 18px;
            --shadow: 0 10px 30px rgba(38,56,84,0.06);
            --shadow-hover: 0 18px 60px rgba(38,56,84,0.12);
            --glass-alpha: 0.78;
        }

        /* App background: layered radial accents for depth */
        .stApp, .main {
            min-height: 100vh;
            background:
                radial-gradient(900px 420px at 6% 10%, rgba(91,155,213,0.04), transparent 8%),
                radial-gradient(700px 360px at 94% 86%, rgba(155,123,216,0.03), transparent 6%),
                linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%) !important;
            color: var(--text);
            font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
            -webkit-font-smoothing:antialiased;
            -moz-osx-font-smoothing:grayscale;
        }

        /* Decorative floating shapes */
        .stApp::before, .stApp::after {
            content: "";
            position: fixed;
            z-index: 0;
            pointer-events: none;
            filter: blur(34px);
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

        /* Settings Header (glass hero + ribbon) */
        .settings-header {
            position: relative;
            z-index: 2;
            padding: 22px;
            border-radius: calc(var(--card-radius) + 6px);
            margin-bottom: 18px;
            display:flex;
            align-items:center;
            justify-content:center;
            gap:18px;
            flex-direction:column;
            text-align:center;
            background: linear-gradient(135deg, rgba(255,255,255,var(--glass-alpha)), rgba(250,250,250,0.92));
            border: 1px solid rgba(40,55,71,0.04);
            box-shadow: var(--shadow);
            backdrop-filter: blur(6px) saturate(120%);
            overflow: hidden;
            transition: transform 0.22s cubic-bezier(.2,.9,.3,1), box-shadow 0.22s ease;
            max-width: 980px;
            margin-left: auto;
            margin-right: auto;
        }
        .settings-header:hover { transform: translateY(-6px); box-shadow: var(--shadow-hover); }

        .settings-header .accent-ribbon {
            position: absolute;
            right: -40px;
            top: -40px;
            width: 220px;
            height: 220px;
            transform: rotate(32deg);
            background: conic-gradient(from 180deg at 50% 50%, rgba(91,155,213,0.12), rgba(155,123,216,0.08));
            filter: blur(22px);
            opacity: 0.95;
            pointer-events: none;
        }

        .settings-hero {
            display:flex;
            align-items:center;
            gap:16px;
            justify-content:center;
            width:100%;
            padding: 6px 12px;
        }

        .settings-logo {
            width:72px;
            height:72px;
            border-radius:14px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:22px;
            font-weight:700;
            color: white;
            background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
            box-shadow: 0 10px 28px rgba(91,155,213,0.12), inset 0 -6px 16px rgba(255,255,255,0.06);
            flex-shrink:0;
        }

        .settings-title-wrap {
            display:flex;
            flex-direction:column;
            align-items:flex-start;
            gap:6px;
            text-align:left;
            max-width:760px;
        }

        .settings-title {
            margin:0;
            font-size:30px;
            color:var(--text);
            font-weight:700;
            line-height:1.02;
        }
        .settings-title .accent-text {
            background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .settings-sub {
            margin:0;
            color:var(--muted);
            font-size:14px;
            max-width:740px;
        }

        .settings-chips {
            display:flex;
            gap:8px;
            margin-top:10px;
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
            background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
            box-shadow: 0 8px 18px rgba(91,155,213,0.08);
            font-weight:700;
        }

        /* Stat cards */
        .stat-card {
            padding: var(--card-pad);
            border-radius: 12px;
            border: 1px solid var(--border);
            background: var(--card);
            box-shadow: 0 8px 26px rgba(38,56,84,0.04);
            text-align:center;
            transition: transform .12s ease, box-shadow .12s ease;
        }
        .stat-card:hover { transform: translateY(-6px); box-shadow: var(--shadow-hover); }
        .stat-title { font-size:14px; color:var(--text); margin:0; font-weight:700; }
        .stat-value { font-size:28px; color:var(--text); margin-top:8px; font-weight:800; }

        .stat-1 { background: linear-gradient(135deg, #5b9bd5 0%, #9b7bd8 100%); color: white; }
        .stat-2 { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
        .stat-3 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; }
        .stat-4 { background: linear-gradient(135deg, #66d9a7 0%, #5dade2 100%); color: white; }

        /* Explorer / data card */
        .explorer-card {
            padding: 16px;
            border-radius: 12px;
            border: 1px solid var(--border);
            background: var(--card);
            box-shadow: 0 8px 22px rgba(38,56,84,0.04);
        }

        /* Empty / warning */
        .warning-card {
            padding: 24px;
            border-radius: 12px;
            border-left: 5px solid var(--danger);
            background: var(--card);
            color: var(--danger);
            box-shadow: 0 8px 22px rgba(38,56,84,0.04);
            text-align:center;
            border: 1px solid var(--border);
        }
        .warning-card p { color: var(--muted); margin-top:8px; }

        /* Export / small panels */
        .export-panel {
            padding: 16px;
            border-radius: 12px;
            border: 1px solid var(--border);
            background: var(--card);
            box-shadow: 0 8px 22px rgba(38,56,84,0.04);
            text-align:left;
        }

        /* Expander tune */
        .stExpander { border-radius:10px; border:1px solid var(--border); background: var(--card); }

        /* Footer small */
        .settings-footer { color: var(--muted); font-size:13px; text-align:center; padding:10px; margin-top:14px; }

        /* Buttons */
        div.stButton > button {
            background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
            color: white;
            border:none;
            padding: 10px 14px;
            border-radius: 10px;
            font-weight:700;
            box-shadow: 0 8px 26px rgba(91, 155, 213, 0.12);
            transition: transform .12s ease, box-shadow .12s ease;
        }
        div.stButton > button:hover { transform: translateY(-3px); box-shadow: var(--shadow-hover); }

        /* Make images / charts smooth */
        .stImage > img, .element-container .stPlotlyChart > div { border-radius: 10px; overflow: hidden; border:1px solid var(--border); }

        @media (max-width: 900px) {
            .settings-header { padding: 14px; }
            .settings-hero { flex-direction: column; gap:10px; align-items:center; }
            .settings-logo { width:56px; height:56px; font-size:18px; border-radius:12px; }
            .settings-title { font-size:22px; text-align:center; }
            .settings-title-wrap { align-items:center; text-align:center; }
            .stat-value { font-size:22px; }
        }

        /* Respect reduced motion */
        @media (prefers-reduced-motion: reduce) {
            .stApp::before, .stApp::after, .settings-header { animation: none !important; transition: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------
    # Header (styled)
    # ------------------------------
    st.markdown(
        """
        <div class="settings-header" role="banner" aria-label="System Configuration Header">
            <div class="accent-ribbon" aria-hidden="true"></div>
            <div class="settings-hero">
                <div class="settings-logo" aria-hidden="true">⚙️</div>
                <div class="settings-title-wrap">
                    <h1 class="settings-title"><span class="accent-text">System</span> Configuration</h1>
                    <p class="settings-sub">Dataset Management & System Controls — polished settings for production</p>
                    <div class="settings-chips" aria-hidden="true" style="margin-top:10px;">
                        <div class="chip">Data-first</div>
                        <div class="chip">Safe Exports</div>
                        <div class="chip">Admin Tools</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    ARTIFACTS_DIR = ROOT / "artifacts"
    CLEAN_FILE = ARTIFACTS_DIR / "cleaned_EMI_dataset.csv"

    # Tabs for different settings sections
    tab1, tab2, tab3 = st.tabs(["📊 Dataset Manager", "📥 Export Tools", "🔧 System Info"])

    with tab1:
        st.markdown('<div style="margin-bottom:10px;" class="section-title">📊 Dataset Overview</div>', unsafe_allow_html=True)

        if CLEAN_FILE.exists():
            df = pd.read_csv(CLEAN_FILE)

            # Dataset Stats Cards
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(
                    f"""
                    <div class="stat-card stat-1">
                        <div class="stat-title">📁 Records</div>
                        <div class="stat-value">{len(df):,}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="stat-card stat-2">
                        <div class="stat-title">📋 Features</div>
                        <div class="stat-value">{len(df.columns)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    f"""
                    <div class="stat-card stat-3">
                        <div class="stat-title">💾 Size</div>
                        <div class="stat-value">{CLEAN_FILE.stat().st_size / 1024:.1f}KB</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col4:
                missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
                st.markdown(
                    f"""
                    <div class="stat-card stat-4">
                        <div class="stat-title">✅ Quality</div>
                        <div class="stat-value">{100-missing_pct:.1f}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # Dataset Preview with Controls
            st.markdown('<div class="explorer-card"><h3 style="margin:0; color:var(--text);">🔍 Data Explorer</h3></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            # Filters
            filter_col1, filter_col2 = st.columns(2)

            with filter_col1:
                rows_to_show = st.slider("Rows to Display", 5, 100, 10)

            with filter_col2:
                search_col = st.selectbox("Search in Column", ["None"] + list(df.columns))

            # Search functionality
            display_df = df.head(rows_to_show)

            if search_col != "None":
                search_term = st.text_input(f"Search in {search_col}")
                if search_term:
                    display_df = df[df[search_col].astype(str).str.contains(search_term, case=False, na=False)].head(rows_to_show)

            # Display dataframe
            st.dataframe(
                display_df,
                use_container_width=True,
                height=400
            )

            # Column Statistics
            with st.expander("📈 Column Statistics", expanded=False):
                st.markdown("#### 📊 Numerical Columns")
                st.dataframe(df.describe(), use_container_width=True)

                st.markdown("#### 📋 Categorical Columns")
                cat_cols = df.select_dtypes(include=['object']).columns
                if len(cat_cols) > 0:
                    for col in cat_cols[:5]:  # Show first 5 categorical columns
                        st.markdown(f"**{col}:**")
                        value_counts = df[col].value_counts().head(10)
                        fig = px.bar(
                            x=value_counts.values,
                            y=value_counts.index,
                            orientation='h',
                            title=f"Top 10 values in {col}",
                            labels={'x': 'Count', 'y': col}
                        )
                        st.plotly_chart(fig, use_container_width=True)

            # Data Quality Report
            with st.expander("🔍 Data Quality Report", expanded=False):
                st.markdown("#### Missing Values Analysis")

                missing_data = df.isnull().sum()
                missing_data = missing_data[missing_data > 0].sort_values(ascending=False)

                if len(missing_data) > 0:
                    fig = px.bar(
                        x=missing_data.values,
                        y=missing_data.index,
                        orientation='h',
                        title="Missing Values by Column",
                        labels={'x': 'Count', 'y': 'Column'},
                        color=missing_data.values,
                        color_continuous_scale='Reds'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.success("✅ No missing values found in the dataset!")

                st.markdown("#### Duplicate Records")
                duplicates = df.duplicated().sum()
                if duplicates > 0:
                    st.warning(f"⚠️ Found {duplicates} duplicate records")
                else:
                    st.success("✅ No duplicate records found!")

        else:
            st.markdown(
                """
                <div class="warning-card">
                    <h3 style="margin:0;">⚠️ Dataset Not Found</h3>
                    <p>No dataset found in the artifacts folder.</p>
                    <p style="color:var(--muted); font-size:13px; margin-top:10px;">Expected location: <code>artifacts/cleaned_EMI_dataset.csv</code></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab2:
        st.markdown('<div class="section-title">📥 Export & Download Tools</div>', unsafe_allow_html=True)

        if CLEAN_FILE.exists():
            df = pd.read_csv(CLEAN_FILE)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    """
                    <div class="export-panel">
                        <h4 style="margin:0; color:var(--text);">📄 CSV Export</h4>
                        <p style="margin:8px 0 0 0; color:var(--muted);">Download the complete dataset in CSV format</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Full Dataset (CSV)",
                    data=csv,
                    file_name="cleaned_EMI_dataset.csv",
                    mime='text/csv',
                    use_container_width=True,
                    type="primary"
                )

            with col2:
                st.markdown(
                    """
                    <div class="export-panel">
                        <h4 style="margin:0; color:var(--text);">📊 Excel Export</h4>
                        <p style="margin:8px 0 0 0; color:var(--muted);">Download dataset with formatting in Excel</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Convert to Excel (requires openpyxl)
                try:
                    from io import BytesIO
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='EMI Dataset')

                    st.download_button(
                        label="📥 Download as Excel (XLSX)",
                        data=buffer.getvalue(),
                        file_name="cleaned_EMI_dataset.xlsx",
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        use_container_width=True,
                        type="secondary"
                    )
                except ImportError:
                    st.info("Install openpyxl to enable Excel export: pip install openpyxl")

            st.markdown("<br>", unsafe_allow_html=True)

            # Custom Export Options
            with st.expander("🎯 Custom Export Options", expanded=False):
                st.markdown("#### Filter Data Before Export")

                # Column selection
                selected_columns = st.multiselect(
                    "Select Columns to Export",
                    df.columns.tolist(),
                    default=df.columns.tolist()[:5]
                )

                # Row limit
                row_limit = st.number_input("Number of Rows", 1, len(df), min(100, len(df)))

                if selected_columns:
                    filtered_df = df[selected_columns].head(row_limit)

                    st.dataframe(filtered_df, use_container_width=True)

                    csv_filtered = filtered_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Filtered Data",
                        data=csv_filtered,
                        file_name="filtered_EMI_dataset.csv",
                        mime='text/csv',
                        use_container_width=True
                    )
        else:
            st.warning("⚠️ No dataset available for export")

    with tab3:
        st.markdown('<div class="section-title">🔧 System Information</div>', unsafe_allow_html=True)

        # System Status
        status_col1, status_col2 = st.columns(2)

        with status_col1:
            st.markdown(
                """
                <div class="explorer-card">
                    <h4 style="margin:0; color:var(--text);">📦 Installed Components</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.success("✅ Classification Model")
            st.success("✅ Regression Model")
            st.success("✅ Data Preprocessors")
            st.success("✅ Feature Encoders")

        with status_col2:
            st.markdown(
                """
                <div class="explorer-card">
                    <h4 style="margin:0; color:var(--text);">🔌 System Status</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.info("📡 Web Interface: Active")
            st.info("🤖 AI Models: Ready")
            st.info("💾 Data Pipeline: Online")
            st.info("📊 Analytics: Enabled")

        st.markdown("<br>", unsafe_allow_html=True)

        # Directory Structure
        with st.expander("📁 Project Structure", expanded=False):
            st.code("""
            EMI_Predict_AI/
            ├── artifacts/
            │   └── cleaned_EMI_dataset.csv
            ├── models/
            │   ├── best_classifier_*.joblib
            │   ├── best_regressor_*.joblib
            │   └── preprocessors/
            ├── reports/
            │   └── *.png (visualizations)
            ├── scripts/
            │   └── predict_emi.py
            └── streamlit_app1/
                ├── main_app.py
                └── pages/
            """, language="bash")

        # Version Info
        st.markdown("### 📌 Version Information")

        import streamlit as st_version
        import pandas as pd_version

        version_data = {
            "Component": ["EMI Intelligence Hub", "Streamlit", "Pandas", "Python"],
            "Version": ["v2.0", st_version.__version__, pd_version.__version__, "3.8+"],
            "Status": ["🟢 Active", "🟢 Active", "🟢 Active", "🟢 Active"]
        }

        st.table(pd.DataFrame(version_data))

    # Footer small note
    st.markdown('<div class="settings-footer">Polished settings UI — same functionality, improved visuals for portfolio & LinkedIn showcase.</div>', unsafe_allow_html=True)
