import pandas as pd
import numpy as np


class DataAnalyzer:
    def __init__(self, df):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        self.category_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    def basic_stats(self):
        stats = {}
        stats["total_rows"] = len(self.df)
        stats["total_cols"] = len(self.df.columns)
        stats["numeric_cols"] = len(self.numeric_cols)
        stats["category_cols"] = len(self.category_cols)
        stats["missing_cells"] = int(self.df.isna().sum().sum())
        stats["duplicate_rows"] = int(self.df.duplicated().sum())
        stats["memory_usage"] = f"{self.df.memory_usage(deep=True).sum() / 1024:.1f} KB"
        return stats

    def numeric_summary(self, columns=None):
        if columns is None:
            columns = self.numeric_cols[:6]
        return self.df[columns].describe().T

    def category_summary(self, columns=None):
        if columns is None:
            columns = self.category_cols[:4]
        result = {}
        for col in columns:
            result[col] = {
                "unique_count": self.df[col].nunique(),
                "top_values": self.df[col].value_counts().head(5).to_dict()
            }
        return result

    def group_analysis(self, group_col, agg_col, agg_func="sum"):
        if group_col in self.category_cols and agg_col in self.numeric_cols:
            return self.df.groupby(group_col)[agg_col].agg(agg_func).sort_values(ascending=False)
        return None

    def correlation_analysis(self, columns=None):
        if columns is None:
            columns = self.numeric_cols
        if len(columns) >= 2:
            return self.df[columns].corr()
        return None

    def trend_analysis(self, date_col, value_col, freq="D"):
        if date_col in self.df.columns and value_col in self.numeric_cols:
            return self.df.set_index(date_col).resample(freq)[value_col].sum()
        return None

    def detect_outliers(self, column, method="iqr"):
        if column not in self.numeric_cols:
            return None
        data = self.df[column].dropna()
        if method == "iqr":
            q1, q3 = data.quantile(0.25), data.quantile(0.75)
            iqr = q3 - q1
            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            outliers = self.df[(self.df[column] < lower) | (self.df[column] > upper)]
            return {"count": len(outliers), "lower": lower, "upper": upper, "data": outliers}
        return None