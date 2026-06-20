import sqlite3
import pandas as pd
from pathlib import Path


class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / "data_samples" / "dashboard.db"
        self.db_path = str(db_path)
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def get_tables(self):
        if not self.conn:
            self.connect()
        cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in cursor.fetchall()]

    def load_table(self, table_name):
        if not self.conn:
            self.connect()
        return pd.read_sql(f"SELECT * FROM [{table_name}]", self.conn)

    def execute_query(self, query):
        if not self.conn:
            self.connect()
        return pd.read_sql(query, self.conn)

    def save_df_to_table(self, df, table_name, if_exists="replace"):
        if not self.conn:
            self.connect()
        df.to_sql(table_name, self.conn, if_exists=if_exists, index=False)
        return True

    def get_table_info(self, table_name):
        if not self.conn:
            self.connect()
        cursor = self.conn.execute(f"PRAGMA table_info([{table_name}])")
        columns = [{"name": row[1], "type": row[2]} for row in cursor.fetchall()]
        count = self.conn.execute(f"SELECT COUNT(*) FROM [{table_name}]").fetchone()[0]
        return {"columns": columns, "row_count": count}