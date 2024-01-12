import streamlit as st
import pandas as pd


def slider(data: pd.DataFrame, label: str, col: str):
    return st.slider(
        label=label,
        min_value=data[col].min(),
        max_value=data[col].max(),
        value=(data[col].min(), data[col].max()),
        step=0.01,
    )


def multiselect(data: pd.DataFrame, label: str, col: str):
    return st.multiselect(
        label=label,
        options=data[col].sort_values().unique()
    )
