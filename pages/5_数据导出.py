import streamlit as st
import pandas as pd
from datetime import datetime
from utils.helpers import setup_page, ensure_session_state
from ui.styles import apply_dashboard_style
from ui.components import render_section_title, render_data_source_info
from core.loader import ensure_data

setup_page("💾 数据导出 - 数据处理和看板")
apply_dashboard_style()
ensure_session_state()

df = ensure_data()

st.markdown("""
<div class="main-header">
    <h1>💾 数据导出</h1>
    <div class="subtitle">将数据导出为不同格式，便于分享和存档</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

render_data_source_info(st.session_state.get("data_source", "未知"))

export_df = df
if st.session_state.get("filtered_df") is not None:
    export_df = st.session_state["filtered_df"]
    st.info(f"当前将导出筛选后的数据 ({len(export_df)} 条记录)")
else:
    st.info(f"当前将导出全部数据 ({len(export_df)} 条记录)")

st.markdown('<div style="background: white; border-radius: 12px; padding: 20px; border: 1px solid #e8e8e8;">',
            unsafe_allow_html=True)

render_section_title("导出选项", "⚙️")

col1, col2 = st.columns(2)
with col1:
    export_format = st.selectbox("选择导出格式", ["CSV (逗号分隔)", "CSV (UTF-8 with BOM)", "JSON", "Excel (xlsx)"])
with col2:
    export_all = st.checkbox("导出全部列", value=True)
    if not export_all:
        export_columns = st.multiselect("选择要导出的列", df.columns.tolist(), default=df.columns.tolist())
    else:
        export_columns = df.columns.tolist()

include_index = st.checkbox("包含行索引", value=False)

st.markdown("---")
render_section_title("预览导出数据（前5条）", "👁️")
preview_df = export_df[export_columns].head(5) if export_columns else export_df.head(5)
st.dataframe(preview_df, use_container_width=True)

st.markdown("---")
render_section_title("下载数据", "📥")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_basename = f"export_{timestamp}"

export_data = export_df[export_columns] if export_columns else export_df

col1, col2 = st.columns(2)

with col1:
    if export_format in ["CSV (逗号分隔)", "CSV (UTF-8 with BOM)"]:
        is_bom = "BOM" in export_format
        encoding = "utf-8-sig" if is_bom else "utf-8"
        csv_data = export_data.to_csv(index=include_index, encoding=encoding)
        mime_type = "text/csv"
        ext = "csv"

        st.download_button(
            label=f"📥 下载 {export_format}",
            data=csv_data,
            file_name=f"{file_basename}.{ext}",
            mime=mime_type,
            use_container_width=True
        )

    elif export_format == "JSON":
        json_data = export_data.to_json(orient="records", force_ascii=False)
        st.download_button(
            label="📥 下载 JSON",
            data=json_data,
            file_name=f"{file_basename}.json",
            mime="application/json",
            use_container_width=True
        )

    elif export_format == "Excel (xlsx)":
        try:
            import openpyxl
            buffer = pd.ExcelWriter(f"{file_basename}.xlsx", engine="openpyxl")
            export_data.to_excel(buffer, index=include_index, sheet_name="Sheet1")
            buffer.close()
            with open(f"{file_basename}.xlsx", "rb") as f:
                excel_data = f.read()
            st.download_button(
                label="📥 下载 Excel",
                data=excel_data,
                file_name=f"{file_basename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except ImportError:
            st.error("导出Excel需要安装 openpyxl: pip install openpyxl")

with col2:
    st.markdown("""
    <div style="background: #f8f9fa; border-radius: 10px; padding: 16px; height: 100%;">
        <b>📋 导出摘要</b><br>
        记录数: {}<br>
        列数: {}<br>
        格式: {}<br>
    </div>
    """.format(len(export_data), len(export_columns), export_format), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)