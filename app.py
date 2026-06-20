import streamlit as st
from utils.helpers import setup_page, ensure_session_state
from ui.styles import apply_dashboard_style
from core.loader import DataLoader, save_data_to_session
from data.sample_generator import SAMPLE_DATASETS

setup_page("📊 数据处理和看板")
apply_dashboard_style()
ensure_session_state()

st.markdown("""
<div class="main-header">
    <h1>📊 数据处理和看板</h1>
    <div class="subtitle">数据加载 · 筛选分析 · 可视化 · 统计报表 · 导出</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

if st.session_state.get("data_loaded"):
    st.success(f"✅ 当前已加载数据: **{st.session_state['data_source']}**")
    st.info("💡 使用左侧侧边栏导航到不同功能页面进行数据处理和分析")
    if st.button("🔄 重新加载数据"):
        st.session_state["df"] = None
        st.session_state["data_loaded"] = False
        st.rerun()
    st.markdown("---")

st.markdown("""
<div style="text-align: center; padding: 10px 0 20px 0;">
    <h3 style="color: #1a1a2e;">📂 选择数据源开始分析</h3>
</div>
""", unsafe_allow_html=True)

loader = DataLoader()
tabs = st.tabs(["📦 示例数据", "📁 上传文件", "🗄️ 数据库"])

with tabs[0]:
    st.markdown("### 快速加载示例数据集")
    dataset_names = list(SAMPLE_DATASETS.keys())
    cols = st.columns(len(dataset_names))

    for i, name in enumerate(dataset_names):
        with cols[i]:
            info = SAMPLE_DATASETS[name]
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 16px;
                        border: 1px solid #e8e8e8; text-align: center; min-height: 160px;">
                <div style="font-size: 2rem; margin-bottom: 8px;">
                    {"📈" if "销售" in name else "🎓" if "学生" in name else "📦"}
                </div>
                <div style="font-weight: bold; font-size: 1.1rem; margin-bottom: 6px;">{name}</div>
                <div style="font-size: 0.85rem; color: #888; margin-bottom: 10px;">
                    {info['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"加载{name}", key=f"sample_{i}", use_container_width=True):
                df = loader.load_sample_data(name)
                save_data_to_session(df, f"示例数据 - {name}")
                st.success(f"✅ {name}加载成功！({len(df)}条记录)")
                st.rerun()

with tabs[1]:
    st.markdown("### 上传数据文件")
    col1, col2 = st.columns(2)
    with col1:
        uploaded_csv = st.file_uploader("上传 CSV 文件", type="csv")
        if uploaded_csv:
            try:
                df = loader.load_csv(uploaded_csv)
                save_data_to_session(df, f"CSV文件: {uploaded_csv.name}")
                st.success(f"✅ CSV上传成功！({len(df)}条记录)")
                st.rerun()
            except Exception as e:
                st.error(f"读取CSV失败: {e}")
    with col2:
        uploaded_excel = st.file_uploader("上传 Excel 文件", type=["xlsx", "xls"])
        if uploaded_excel:
            try:
                df = loader.load_excel(uploaded_excel)
                save_data_to_session(df, f"Excel文件: {uploaded_excel.name}")
                st.success(f"✅ Excel上传成功！({len(df)}条记录)")
                st.rerun()
            except Exception as e:
                st.error(f"读取Excel失败: {e}")

with tabs[2]:
    st.markdown("### 连接SQLite数据库")
    st.markdown("从已有的SQLite数据库文件中加载数据表")

    db_path = st.text_input("数据库文件路径",
                            value="data_samples/dashboard.db",
                            help="输入SQLite数据库文件的路径")

    if st.button("🔌 连接数据库", use_container_width=True):
        from data.database import DatabaseManager
        try:
            db = DatabaseManager(db_path)
            db.connect()
            tables = db.get_tables()
            if tables:
                st.session_state["db_manager"] = db
                st.session_state["db_tables"] = tables
                st.success(f"✅ 连接成功！发现 {len(tables)} 张表")
            else:
                st.warning("数据库连接成功，但未找到任何表")
        except Exception as e:
            st.error(f"连接失败: {e}")

    if st.session_state.get("db_tables"):
        st.markdown("**选择要加载的数据表:**")
        tables = st.session_state["db_tables"]
        for table in tables:
            if st.button(f"加载 {table}", key=f"db_{table}"):
                df = loader.load_db_table(table)
                save_data_to_session(df, f"数据库: {table}")
                st.success(f"✅ 表 {table} 加载成功！({len(df)}条记录)")
                st.rerun()

if not st.session_state.get("data_loaded"):
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <div style="font-size: 3rem; margin-bottom: 16px;">📊</div>
        <div style="color: #888;">
            请先在上方选择一个数据源开始<br>
            加载数据后即可使用筛选、可视化、分析、导出等功能
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div class="footer">
    📊 数据处理和看板 · 基于 Streamlit 构建
</div>
""", unsafe_allow_html=True)