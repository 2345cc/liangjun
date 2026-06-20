import streamlit as st
from utils.helpers import setup_page, ensure_session_state
from ui.styles import apply_dashboard_style
from ui.components import render_section_title, render_data_source_info
from core.loader import ensure_data
from core.filter import build_filter_ui, apply_filters

setup_page("🔍 数据筛选 - 数据处理和看板")
apply_dashboard_style()
ensure_session_state()

df = ensure_data()

st.markdown("""
<div class="main-header">
    <h1>🔍 数据筛选</h1>
    <div class="subtitle">按条件筛选你需要的数据子集</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

render_data_source_info(st.session_state.get("data_source", "未知"))

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div style="background: white; border-radius: 12px; padding: 16px; border: 1px solid #e8e8e8;">',
                unsafe_allow_html=True)
    render_section_title("筛选条件", "🎯")
    filters = build_filter_ui(df)
    st.markdown('</div>', unsafe_allow_html=True)

    apply_btn = st.button("✅ 应用筛选", use_container_width=True)

with col2:
    render_section_title("筛选结果", "📊")

    if apply_btn:
        filtered_df = apply_filters(df, filters)
        st.session_state["filtered_df"] = filtered_df
        st.success(f"筛选完成！共 {len(filtered_df)} 条记录（原始: {len(df)} 条）")
    elif st.session_state.get("filtered_df") is not None:
        filtered_df = st.session_state["filtered_df"]
        st.info(f"当前显示筛选结果（共 {len(filtered_df)} 条）")
    else:
        filtered_df = df
        st.info(f"未应用筛选，显示全部数据（共 {len(df)} 条）")

    st.dataframe(filtered_df, use_container_width=True)

    if st.session_state.get("filtered_df") is not None:
        if st.button("🔄 清除筛选"):
            st.session_state["filtered_df"] = None
            st.rerun()