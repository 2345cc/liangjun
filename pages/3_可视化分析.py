import streamlit as st
from utils.helpers import setup_page, ensure_session_state
from ui.styles import apply_dashboard_style
from ui.components import render_section_title, render_column_selector, render_data_source_info
from ui.charts import CHART_TYPES, CHART_FUNCTIONS, CHART_CONFIGS
from core.loader import ensure_data
from core.filter import get_date_columns, get_numeric_columns, get_category_columns

setup_page("📈 可视化分析 - 数据处理和看板")
apply_dashboard_style()
ensure_session_state()

df = ensure_data()

st.markdown("""
<div class="main-header">
    <h1>📈 可视化分析</h1>
    <div class="subtitle">通过图表探索数据中的模式和趋势</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

render_data_source_info(st.session_state.get("data_source", "未知"))

if st.session_state.get("filtered_df") is not None:
    df = st.session_state["filtered_df"]
    st.info(f"当前使用筛选后的数据 ({len(df)} 条记录)")

st.markdown('<div style="background: white; border-radius: 12px; padding: 20px; border: 1px solid #e8e8e8;">',
            unsafe_allow_html=True)

render_section_title("图表配置", "⚙️")

col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    chart_type = st.selectbox("选择图表类型", CHART_TYPES)
with col2:
    num_cols = get_numeric_columns(df)
    if not num_cols:
        st.error("数据集中没有数值列，无法生成图表")
        st.stop()
    value_col = st.selectbox("选择数值列", num_cols)
with col3:
    cat_cols = get_category_columns(df)
    has_category = bool(cat_cols)
    category_col = st.selectbox("选择分类列", cat_cols) if has_category else None

st.markdown("---")

render_section_title("图表预览", "📊")

fig = None
config = CHART_CONFIGS.get(chart_type, {})

try:
    if chart_type == "折线图":
        date_cols = get_date_columns(df)
        if date_cols:
            date_col = st.selectbox("选择日期列", date_cols)
            fig = CHART_FUNCTIONS[chart_type](df, date_col, value_col)
        else:
            st.warning("折线图需要日期列，请检查数据中是否有日期类型列")

    elif chart_type == "柱状图":
        if category_col:
            fig = CHART_FUNCTIONS[chart_type](df, category_col, value_col)
        else:
            st.warning("柱状图需要选择一个分类列")

    elif chart_type == "散点图":
        x_col = st.selectbox("选择X轴", num_cols, index=0)
        y_col = st.selectbox("选择Y轴", num_cols, index=min(1, len(num_cols) - 1))
        hue_col = st.selectbox("选择分类着色（可选）", ["无"] + cat_cols) if has_category else "无"
        hue = hue_col if hue_col != "无" else None
        fig = CHART_FUNCTIONS[chart_type](df, x_col, y_col, hue)

    elif chart_type == "饼图":
        if category_col:
            fig = CHART_FUNCTIONS[chart_type](df, category_col, value_col)
        else:
            st.warning("饼图需要选择一个分类列")

    elif chart_type == "热力图":
        if len(cat_cols) >= 2:
            row_col = st.selectbox("选择行分类", cat_cols, index=0)
            col_col = st.selectbox("选择列分类", cat_cols, index=min(1, len(cat_cols) - 1))
            fig = CHART_FUNCTIONS[chart_type](df, row_col, col_col, value_col)
        else:
            st.warning("热力图需要至少两个分类列")

    elif chart_type == "箱线图":
        if category_col:
            fig = CHART_FUNCTIONS[chart_type](df, category_col, value_col)
        else:
            st.warning("箱线图需要选择一个分类列")

    elif chart_type == "直方图":
        fig = CHART_FUNCTIONS[chart_type](df, value_col)

except Exception as e:
    st.error(f"生成图表时出错: {e}")

if fig:
    st.pyplot(fig)
    st.caption(f"图表类型: {chart_type} · 数值列: {value_col}")

st.markdown('</div>', unsafe_allow_html=True)