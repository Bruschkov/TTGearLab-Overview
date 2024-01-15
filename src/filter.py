import streamlit as st
import pandas as pd


def slider(data: pd.Series, label: str):
    return st.slider(
        label=label,
        min_value=data.min(),
        max_value=data.max(),
        value=(data.min(), data.max()),
        step=0.01,
    )


