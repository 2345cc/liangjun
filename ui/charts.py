import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import numpy as np

CHART_TYPES = ["折线图", "柱状图", "散点图", "饼图", "热力图", "箱线图", "直方图"]


def _setup_style():
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False


def create_line_chart(df, date_col, value_col, title=""):
    _setup_style()
    trend_data = df.groupby(date_col)[value_col].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(trend_data[date_col], trend_data[value_col],
            marker="o", linestyle="-", color="#FF6384", linewidth=2)
    ax.set_title(title or f"{value_col}趋势", fontsize=14, fontweight="bold")
    ax.set_xlabel(date_col, fontsize=11)
    ax.set_ylabel(value_col, fontsize=11)
    plt.xticks(rotation=45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    return fig


def create_bar_chart(df, category_col, value_col, title=""):
    _setup_style()
    group_data = df.groupby(category_col)[value_col].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = sns.color_palette("viridis", len(group_data))
    bars = ax.bar(group_data.index, group_data.values, color=colors, edgecolor="white")
    ax.set_title(title or f"各{category_col}{value_col}对比", fontsize=14, fontweight="bold")
    ax.set_xlabel(category_col, fontsize=11)
    ax.set_ylabel(value_col, fontsize=11)
    ax.bar_label(bars, fmt="%.0f", fontsize=9)
    plt.xticks(rotation=30, ha="right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    return fig


def create_scatter_chart(df, x_col, y_col, hue_col=None):
    _setup_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    if hue_col and hue_col in df.columns:
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue_col,
                        s=80, alpha=0.7, ax=ax)
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    else:
        ax.scatter(df[x_col], df[y_col], c="#FF6384", s=80, alpha=0.7)
    ax.set_title(f"{x_col}与{y_col}关系", fontsize=14, fontweight="bold")
    ax.set_xlabel(x_col, fontsize=11)
    ax.set_ylabel(y_col, fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    return fig


def create_pie_chart(df, category_col, value_col):
    _setup_style()
    group_data = df.groupby(category_col)[value_col].sum()
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = sns.color_palette("Set3", len(group_data))
    wedges, texts, autotexts = ax.pie(
        group_data.values, labels=group_data.index,
        autopct="%1.1f%%", startangle=90, colors=colors,
        textprops={"fontsize": 11}
    )
    ax.set_title(f"{category_col}{value_col}占比", fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig


def create_heatmap(df, index_col, columns_col, value_col):
    _setup_style()
    pivot_data = df.pivot_table(
        values=value_col, index=index_col, columns=columns_col, aggfunc="sum"
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot_data, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
    ax.set_title(f"{index_col}-{columns_col}{value_col}热力图",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig


def create_box_chart(df, category_col, value_col):
    _setup_style()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x=category_col, y=value_col, palette="Set2", ax=ax)
    ax.set_title(f"各{category_col}{value_col}分布", fontsize=14, fontweight="bold")
    ax.set_xlabel(category_col, fontsize=11)
    ax.set_ylabel(value_col, fontsize=11)
    plt.xticks(rotation=30, ha="right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    return fig


def create_histogram(df, column, bins=20):
    _setup_style()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df[column].dropna(), bins=bins, color="#4ECDC4",
            edgecolor="white", alpha=0.8)
    ax.set_title(f"{column}分布直方图", fontsize=14, fontweight="bold")
    ax.set_xlabel(column, fontsize=11)
    ax.set_ylabel("频数", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    return fig


CHART_FUNCTIONS = {
    "折线图": create_line_chart,
    "柱状图": create_bar_chart,
    "散点图": create_scatter_chart,
    "饼图": create_pie_chart,
    "热力图": create_heatmap,
    "箱线图": create_box_chart,
    "直方图": create_histogram
}

CHART_CONFIGS = {
    "折线图": {"requires_date": True, "num_cols": 1, "cat_cols": 0, "hue": False},
    "柱状图": {"requires_date": False, "num_cols": 1, "cat_cols": 1, "hue": False},
    "散点图": {"requires_date": False, "num_cols": 2, "cat_cols": 0, "hue": True},
    "饼图": {"requires_date": False, "num_cols": 1, "cat_cols": 1, "hue": False},
    "热力图": {"requires_date": False, "num_cols": 1, "cat_cols": 2, "hue": False},
    "箱线图": {"requires_date": False, "num_cols": 1, "cat_cols": 1, "hue": False},
    "直方图": {"requires_date": False, "num_cols": 1, "cat_cols": 0, "hue": False}
}