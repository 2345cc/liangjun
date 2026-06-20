import streamlit as st


def apply_dashboard_style():
    st.markdown("""
    <style>
        .stApp {
            background: #f8f9fa;
        }
        .main-header {
            text-align: center;
            padding: 1.2rem 0;
        }
        .main-header h1 {
            font-size: 2.4rem;
            color: #1a1a2e;
            margin-bottom: 0.3rem;
        }
        .main-header .subtitle {
            font-size: 1rem;
            color: #666;
        }
        .dashboard-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #e8e8e8;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            margin: 8px 0;
            transition: all 0.2s ease;
        }
        .dashboard-card:hover {
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        }
        .stat-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #1a1a2e;
        }
        .stat-label {
            font-size: 0.85rem;
            color: #888;
        }
        .nav-card {
            background: white;
            border: 1px solid #e8e8e8;
            border-radius: 14px;
            padding: 24px;
            text-align: center;
            height: 100%;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .nav-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
            border-color: #4ECDC4;
        }
        .nav-card .icon {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .nav-card .title {
            font-size: 1.1rem;
            font-weight: bold;
            color: #1a1a2e;
            margin-bottom: 6px;
        }
        .nav-card .desc {
            font-size: 0.85rem;
            color: #888;
            line-height: 1.4;
        }
        .stButton button {
            border-radius: 8px;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.6rem !important;
        }
        .footer {
            text-align: center;
            color: #aaa;
            padding: 20px;
            font-size: 0.8rem;
        }
        hr {
            border-color: #eee !important;
        }
        .stDataFrame {
            border: 1px solid #eee;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)