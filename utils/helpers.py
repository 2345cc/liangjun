import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path


def setup_page(title, icon="📊", layout="wide"):
    st.set_page_config(page_title=title, page_icon=icon, layout=layout)
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False


def get_project_root():
    return Path(__file__).parent.parent


def ensure_session_state():
    defaults = {
        "df": None,
        "data_source": None,
        "data_loaded": False,
        "filtered_df": None,
        "chart_type": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def format_number(num):
    if abs(num) >= 1e8:
        return f"{num / 1e8:.2f}亿"
    elif abs(num) >= 1e4:
        return f"{num / 1e4:.2f}万"
    return f"{num:,.2f}"