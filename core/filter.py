import pandas as pd
import streamlit as st


def get_numeric_columns(df):
    return df.select_dtypes(include=["int64", "float64"]).columns.tolist()


def get_category_columns(df):
    return df.select_dtypes(include=["object", "category"]).columns.tolist()


def get_date_columns(df):
    return df.select_dtypes(include=["datetime64"]).columns.tolist()


def apply_filters(df, filters):
    filtered = df.copy()
    for col, values in filters.get("categorical", {}).items():
        if values:
            filtered = filtered[filtered[col].isin(values)]

    for col, (min_val, max_val) in filters.get("numeric", {}).items():
        if min_val is not None:
            filtered = filtered[filtered[col] >= min_val]
        if max_val is not None:
            filtered = filtered[filtered[col] <= max_val]

    for col, (start_date, end_date) in filters.get("date", {}).items():
        if start_date:
            filtered = filtered[filtered[col] >= pd.to_datetime(start_date)]
        if end_date:
            filtered = filtered[filtered[col] <= pd.to_datetime(end_date)]

    return filtered


def build_filter_ui(df):
    filters = {"categorical": {}, "numeric": {}, "date": {}}

    cat_cols = get_category_columns(df)
    num_cols = get_numeric_columns(df)
    date_cols = get_date_columns(df)

    st.markdown("**分类筛选**")
    for col in cat_cols[:4]:
        unique_vals = df[col].unique().tolist()
        selected = st.multiselect(f"选择{col}", unique_vals, default=unique_vals,
                                  key=f"filter_{col}")
        filters["categorical"][col] = selected

    st.markdown("**数值范围筛选**")
    for col in num_cols[:3]:
        min_v = float(df[col].min())
        max_v = float(df[col].max())
        if min_v != max_v:
            range_vals = st.slider(f"{col}范围", min_v, max_v,
                                   (min_v, max_v), key=f"range_{col}")
            filters["numeric"][col] = range_vals

    st.markdown("**日期筛选**")
    for col in date_cols[:1]:
        min_d = df[col].min().date()
        max_d = df[col].max().date()
        date_range = st.date_input(f"选择{col}范围", [min_d, max_d],
                                   key=f"date_{col}")
        if len(date_range) == 2:
            filters["date"][col] = (date_range[0], date_range[1])

    return filters