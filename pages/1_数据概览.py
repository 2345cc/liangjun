import streamlit as st
from utils.helpers import setup_page, ensure_session_state
from ui.styles import apply_dashboard_style
from ui.components import render_data_preview, render_section_title, render_data_source_info
from core.loader import ensure_data
from core.analyzer import DataAnalyzer

setup_page("📋 数据概览 - 数据处理和看板")
apply_dashboard_style()
ensure_session_state()

df = ensure_data()

st.markdown("""
<div class="main-header">
    <h1>📋 数据概览</h1>
    <div class="subtitle">快速了解数据全貌</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

render_data_source_info(st.session_state.get("data_source", "未知"))

col1, col2 = st.columns([1, 2])
analyzer = DataAnalyzer(df)

with col1:
    render_section_title("数据集基本信息", "📊")
    stats = analyzer.basic_stats()
    st.markdown(f"""
    <div style="background: white; border-radius: 12px; padding: 16px; border: 1px solid #e8e8e8;">
        <p>📝 记录数: <b>{stats['total_rows']:,}</b></p>
        <p>📋 列数: <b>{stats['total_cols']}</b></p>
        <p>🔢 数值列: <b>{stats['numeric_cols']}</b></p>
        <p>🏷️ 分类列: <b>{stats['category_cols']}</b></p>
        <p>⚠️ 缺失值: <b>{stats['missing_cells']:,}</b></p>
        <p>🔄 重复行: <b>{stats['duplicate_rows']:,}</b></p>
        <p>💾 内存占用: <b>{stats['memory_usage']}</b></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    render_section_title("数据预览（前10条）", "📄")
    render_data_preview(df, max_rows=10)

st.markdown("---")

render_section_title("列信息一览", "📋")
col_info = []
for col in df.columns:
    dtype = str(df[col].dtype)
    nunique = df[col].nunique()
    missing = int(df[col].isna().sum())
    col_info.append({
        "列名": col, "类型": dtype,
        "唯一值数": nunique, "缺失值": missing
    })
st.dataframe(col_info, use_container_width=True, hide_index=True)