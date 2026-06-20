import streamlit as st
import pandas as pd
from utils.helpers import setup_page, ensure_session_state, format_number
from ui.styles import apply_dashboard_style
from ui.components import render_section_title, render_data_source_info
from ui.charts import create_histogram
from core.loader import ensure_data
from core.analyzer import DataAnalyzer
from core.filter import get_numeric_columns, get_category_columns

setup_page("📊 统计分析 - 数据处理和看板")
apply_dashboard_style()
ensure_session_state()

df = ensure_data()

st.markdown("""
<div class="main-header">
    <h1>📊 统计分析</h1>
    <div class="subtitle">深入分析数据的统计特征和趋势</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

render_data_source_info(st.session_state.get("data_source", "未知"))

if st.session_state.get("filtered_df") is not None:
    df = st.session_state["filtered_df"]
    st.info(f"当前使用筛选后的数据 ({len(df)} 条记录)")

analyzer = DataAnalyzer(df)
num_cols = get_numeric_columns(df)
cat_cols = get_category_columns(df)

st.markdown('<div style="background: white; border-radius: 12px; padding: 20px; border: 1px solid #e8e8e8;">',
            unsafe_allow_html=True)

render_section_title("描述性统计", "📋")
st.dataframe(analyzer.numeric_summary(num_cols[:6]), use_container_width=True)

st.markdown("---")

render_section_title("分组分析", "📊")
col1, col2 = st.columns(2)
with col1:
    group_col = st.selectbox("选择分组列", cat_cols if cat_cols else ["无"])
with col2:
    agg_col = st.selectbox("选择聚合列", num_cols)
agg_func = st.selectbox("选择聚合函数", ["sum", "mean", "count", "max", "min"])

if group_col != "无" and agg_col:
    result = analyzer.group_analysis(group_col, agg_col, agg_func)
    if result is not None:
        st.dataframe(result.reset_index(), use_container_width=True, hide_index=True)

st.markdown("---")

render_section_title("相关性分析", "🔗")
corr_cols = st.multiselect("选择参与相关性分析的列", num_cols, default=num_cols[:4])
corr = analyzer.correlation_analysis(corr_cols if corr_cols else None)
if corr is not None:
    import matplotlib.pyplot as plt
    import seaborn as sns
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r",
                vmin=-1, vmax=1, center=0, ax=ax)
    ax.set_title("相关性热力图", fontsize=14, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

render_section_title("异常值检测", "⚠️")
outlier_col = st.selectbox("选择检测列", num_cols, key="outlier")
outlier_result = analyzer.detect_outliers(outlier_col)
if outlier_result and outlier_result["count"] > 0:
    st.warning(f"发现 {outlier_result['count']} 个异常值 "
               f"(下界: {outlier_result['lower']:.2f}, 上界: {outlier_result['upper']:.2f})")
    with st.expander("查看异常值详情"):
        st.dataframe(outlier_result["data"], use_container_width=True)
else:
    st.success("未发现明显异常值")

st.markdown('</div>', unsafe_allow_html=True)