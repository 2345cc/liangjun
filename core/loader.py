import pandas as pd
import streamlit as st
from data.sample_generator import SAMPLE_DATASETS
from data.database import DatabaseManager


class DataLoader:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def load_sample_data(self, dataset_name):
        if dataset_name in SAMPLE_DATASETS:
            df = SAMPLE_DATASETS[dataset_name]["generator"]()
            return df
        return None

    def load_csv(self, uploaded_file):
        df = pd.read_csv(uploaded_file)
        return df

    def load_excel(self, uploaded_file, sheet_name=0):
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
        return df

    def get_db_tables(self):
        self.db_manager.connect()
        tables = self.db_manager.get_tables()
        return tables

    def load_db_table(self, table_name):
        return self.db_manager.load_table(table_name)

    def execute_sql(self, query):
        return self.db_manager.execute_query(query)


def save_data_to_session(df, source_desc):
    st.session_state["df"] = df
    st.session_state["data_source"] = source_desc
    st.session_state["data_loaded"] = True


def ensure_data():
    if "df" not in st.session_state or st.session_state.get("df") is None:
        st.warning("请先在首页加载数据")
        st.stop()
    return st.session_state["df"]