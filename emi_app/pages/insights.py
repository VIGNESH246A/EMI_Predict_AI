# pages/insights.py

import streamlit as st
from pathlib import Path
from PIL import Image
import plotly.express as px

def show_insights(REPORTS_DIR: Path):
    # ---------- Modern CSS/theme - LIGHT THEME ----------
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
            --accent-a: #9b7bd8;   /* soft purple */
            --accent-b: #5b9bd5;   /* soft blue */
            --accent-c: #f5576c;   /* coral */
            --border: #e1e8ed;
            --card-radius: 12px;
            --shadow-sm: 0 8px 26px rgba(38,56,84,0.06);
            --shadow-hover: 0 18px 48px rgba(38,56,84,0.10);
            --glass-alpha: 0.76;
        }

        /* App background: soft layered gradients + floating blobs */
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

        /* Decorative floating shapes for depth */
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

        /* Header - glass hero with ribbon and chips */
        .insights-header {
            position: relative;
            z-index: 2;
            border-radius: calc(var(--card-radius) + 6px);
            padding: 22px;
            margin-bottom: 18px;
            display:flex;
            align-items:center;
            justify-content:center;
            gap:18px;
            flex-direction:column;
            text-align:center;
            background: linear-gradient(135deg, rgba(255,255,255,var(--glass-alpha)), rgba(250,250,250,0.9));
            border: 1px solid rgba(40,55,71,0.04);
            box-shadow: var(--shadow-sm);
            backdrop-filter: blur(6px) saturate(120%);
            overflow: hidden;
            transition: transform 0.22s cubic-bezier(.2,.9,.3,1), box-shadow 0.22s ease;
            max-width: 980px;
            margin-left: auto;
            margin-right: auto;
        }
        .insights-header:hover { transform: translateY(-6px); box-shadow: var(--shadow-hover); }

        /* accent ribbon */
        .insights-header .accent-ribbon {
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

        .insights-hero {
            display:flex;
            gap:16px;
            align-items:center;
            justify-content:center;
            flex-direction:row;
            width:100%;
            padding: 6px 12px;
        }

        .insights-logo {
            width:70px;
            height:70px;
            border-radius:14px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:20px;
            font-weight:700;
            color: white;
            background: linear-gradient(135deg, var(--accent-b), var(--accent-a));
            box-shadow: 0 10px 28px rgba(91,155,213,0.12), inset 0 -6px 14px rgba(255,255,255,0.06);
            flex-shrink:0;
        }

        .insights-title-wrap {
            display:flex;
            flex-direction:column;
            align-items:flex-start;
            text-align:left;
            max-width:780px;
        }

        .insights-title {
            margin:0;
            font-size:30px;
            color:var(--text);
            font-weight:700;
            line-height:1.02;
        }
        .insights-title .accent-text {
            background: linear-gradient(90deg, var(--accent-b), var(--accent-a));
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .insights-sub {
            margin:6px 0 0 0;
            color:var(--muted);
            font-size:14px;
            max-width:740px;
        }

        .insights-chips {
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
            background: linear-gradient(90deg, var(--accent-b), var(--accent-a));
            box-shadow: 0 8px 18px rgba(91,155,213,0.08);
            font-weight:700;
        }

        /* Gallery controls */
        .controls-row { display:flex; gap:12px; align-items:center; margin-bottom:12px; }
        .control-box {
            padding:8px 12px;
            border-radius:10px;
            background: var(--card);
            border:1px solid var(--border);
            color:var(--muted);
        }

        /* Image card */
        .image-card {
            background: var(--card);
            padding:14px;
            border-radius:12px;
            border:1px solid var(--border);
            box-shadow: 0 8px 22px rgba(38,56,84,0.04);
            transition: transform .14s ease, box-shadow .14s ease;
            margin-bottom:18px;
        }
        .image-card:hover { transform: translateY(-6px); box-shadow: var(--shadow-hover); }
        .image-title { font-size:16px; margin:0 0 8px 0; color:var(--text); font-weight:600; }

        /* Empty state */
        .empty-state {
            background: var(--card);
            padding:28px;
            border-radius:14px;
            border-left:5px solid var(--accent-c);
            color: var(--accent-c);
            text-align:center;
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--border);
        }
        .empty-state p { color: var(--muted); margin-top:8px; }

        /* Slideshow header */
        .slide-header {
            text-align:center;
            padding:14px;
            border-radius:12px;
            background: var(--card);
            border:1px solid var(--border);
            margin: 18px 0;
            box-shadow: var(--shadow-sm);
        }
        .slide-count { color: var(--muted); font-size:13px; margin-top:6px; }

        /* Small insight cards */
        .insight-card {
            padding:16px;
            border-radius:12px;
            color:white;
            height:100%;
            box-shadow: var(--shadow-sm);
            border:1px solid var(--border);
        }
        .insight-a { background: linear-gradient(135deg, #5b9bd5 0%, #9b7bd8 100%); }
        .insight-b { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        .insight-c { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }

        /* Buttons (download/nav) */
        div.stButton > button {
            background: linear-gradient(90deg, var(--accent-b), var(--accent-a));
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 10px;
            font-weight: 700;
            box-shadow: 0 8px 22px rgba(91, 155, 213, 0.12);
            transition: transform .12s ease;
        }
        div.stButton > button:hover { transform: translateY(-3px); }

        /* Ensure images are nicely rounded */
        .stImage > img { border-radius: 10px; border:1px solid var(--border); }

        @media (max-width: 900px) {
            .insights-hero { flex-direction: column; gap:10px; align-items:center; }
            .insights-logo { width:56px; height:56px; font-size:18px; border-radius:12px; }
            .insights-title { font-size:22px; text-align:center; }
            .insights-title-wrap { align-items:center; text-align:center; }
            .insights-sub { font-size:13px; max-width:420px; }
            .chip { font-size:12px; padding:5px 8px; }
        }

        /* Accessibility (reduce motion) */
        @media (prefers-reduced-motion: reduce) {
            .stApp::before, .stApp::after, .insights-header, .image-card { animation: none !important; transition: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Header ----------
    st.markdown(
        """
        <div class="insights-header" role="banner" aria-label="Data Insights Explorer Header">
            <div class="accent-ribbon" aria-hidden="true"></div>
            <div class="insights-hero">
                <div class="insights-logo" aria-hidden="true">DI</div>
                <div class="insights-title-wrap">
                    <h1 class="insights-title">📊 <span class="accent-text">Data Insights</span> Explorer</h1>
                    <p class="insights-sub">Visual Analytics & Pattern Discovery — polished gallery for your reports</p>
                    <div class="insights-chips" aria-hidden="true" style="margin-top:10px;">
                        <div class="chip">Interactive</div>
                        <div class="chip">High-Res Exports</div>
                        <div class="chip">Mobile-ready</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Gather all images
    image_files = sorted(
        [f for f in REPORTS_DIR.glob("*") if f.suffix.lower() in [".png", ".jpg", ".jpeg"]]
    )

    if not image_files:
        st.markdown(
            """
            <div class="empty-state">
                <h3 style="margin:0;">⚠️ No Visualizations Found</h3>
                <p>Please run the data analysis pipeline first to generate visual reports.</p>
                <p style="color:var(--muted); font-size:13px; margin-top:10px;">Run: <code>python scripts/generate_plots.py</code></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown('<div style="font-size:18px; color:var(--text); font-weight:600; margin-bottom:8px;">🎨 Interactive Visual Gallery</div>', unsafe_allow_html=True)

    # Filter options (kept logic same)
    col1, col2 = st.columns([3, 1])
    with col1:
        view_mode = st.radio(
            "View Mode",
            ["Grid View", "Gallery View", "Slideshow"],
            horizontal=True,
            label_visibility="collapsed"
        )
    with col2:
        images_per_row = st.selectbox("Images per row", [1, 2, 3, 4], index=1)

    st.markdown("---")

    # Grid View
    if view_mode == "Grid View":
        for i in range(0, len(image_files), images_per_row):
            cols = st.columns(images_per_row)
            for j, img_path in enumerate(image_files[i:i+images_per_row]):
                with cols[j]:
                    with st.container():
                        st.markdown(
                            f"""
                            <div class="image-card">
                                <h4 class="image-title">📈 {img_path.stem.replace('_', ' ').title()}</h4>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        try:
                            st.image(str(img_path), use_container_width=True)

                            # Download button (kept same behavior)
                            with open(img_path, "rb") as file:
                                st.download_button(
                                    label="📥 Download",
                                    data=file,
                                    file_name=img_path.name,
                                    mime="image/png",
                                    key=f"download_{i}_{j}",
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"⚠️ Could not display: {e}")

    # Gallery View
    elif view_mode == "Gallery View":
        selected_image = st.selectbox(
            "Select Visualization",
            [f.stem.replace('_', ' ').title() for f in image_files]
        )

        selected_idx = [f.stem.replace('_', ' ').title() for f in image_files].index(selected_image)
        selected_path = image_files[selected_idx]

        st.markdown(
            f"""
            <div class="slide-header">
                <h2 style="margin:0; color:var(--text);">📊 {selected_image}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            try:
                st.image(str(selected_path), use_container_width=True)

                with open(selected_path, "rb") as file:
                    st.download_button(
                        label="📥 Download High Resolution",
                        data=file,
                        file_name=selected_path.name,
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"⚠️ Could not display: {e}")

    # Slideshow
    else:
        if 'slide_index' not in st.session_state:
            st.session_state.slide_index = 0

        current_img = image_files[st.session_state.slide_index]

        st.markdown(
            f"""
            <div class="slide-header">
                <h2 style="margin:0; color:var(--text);">📊 {current_img.stem.replace('_', ' ').title()}</h2>
                <div class="slide-count">Slide {st.session_state.slide_index + 1} of {len(image_files)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            st.image(str(current_img), use_container_width=True)
        except Exception as e:
            st.error(f"⚠️ Could not display: {e}")

        # Navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.slide_index = (st.session_state.slide_index - 1) % len(image_files)
                st.rerun()
        with col2:
            st.markdown(f"<div style='text-align: center; padding: 10px;'><p style='color:var(--muted); margin:0;'>Use navigation buttons to browse</p></div>", unsafe_allow_html=True)
        with col3:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.slide_index = (st.session_state.slide_index + 1) % len(image_files)
                st.rerun()

    # Insights Summary (kept content & layout)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 🔍 Key Insights")

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    with insight_col1:
        st.markdown(
            """
            <div class="insight-card insight-a">
                <h4 style="margin:0;">📈 Distributions</h4>
                <p style="color:rgba(255,255,255,0.9); margin-top:10px; font-size:14px;">
                    Analyze data distributions across various financial parameters
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with insight_col2:
        st.markdown(
            """
            <div class="insight-card insight-b">
                <h4 style="margin:0;">🔗 Correlations</h4>
                <p style="color:rgba(255,255,255,0.9); margin-top:10px; font-size:14px;">
                    Discover relationships between different financial features
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with insight_col3:
        st.markdown(
            """
            <div class="insight-card insight-c">
                <h4 style="margin:0;">📊 Trends</h4>
                <p style="color:rgba(255,255,255,0.9); margin-top:10px; font-size:14px;">
                    Identify patterns and trends in EMI eligibility data
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
