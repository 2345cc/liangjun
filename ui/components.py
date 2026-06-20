import streamlit as st
import pandas as pd


def render_metric_row(metrics):
    cols = st.columns(len(metrics))
    for i, (label, value) in enumerate(metrics):
        with cols[i]:
            st.metric(label=label, value=value)


def render_data_preview(df, max_rows=10):
    st.dataframe(df.head(max_rows), use_container_width=True)
    st.caption(f"显示前 {min(max_rows, len(df))} 条，共 {len(df)} 条记录")


def render_section_title(text, icon="📊"):
    st.markdown(f"""
    <div style="margin: 16px 0 8px 0;">
        <h3 style="font-size: 1.25rem;">{icon} {text}</h3>
    </div>
    """, unsafe_allow_html=True)


def render_column_selector(df, label="选择分析列", key="col_selector"):
    all_cols = df.columns.tolist()
    return st.multiselect(label, all_cols, default=all_cols[:3], key=key)


def render_pagination(df, page_size=10, key="page"):
    total = len(df)
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = st.number_input("页码", min_value=1, max_value=total_pages,
                           value=1, key=key)
    start = (page - 1) * page_size
    end = min(start + page_size, total)
    st.dataframe(df.iloc[start:end], use_container_width=True)
    st.caption(f"第 {start + 1}-{end} 条，共 {total} 条")


def render_data_source_info(source_desc):
    st.info(f"📂 当前数据源: **{source_desc}**")