import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection


def load_data(from_local: bool = False) -> pd.DataFrame:
    if from_local:
        df = pd.read_csv("lab/blades.csv")
    else:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl="15m")
    df['Ec/Ep'] = df['Ec'] / df['Ep']
    df['Vl/Vp'] = df['Vl'] / df['Vp']
    return df


def filter_data(
        data,
        selected_elasticity,
        selected_ec_ep,
        selected_vibration,
        selected_vl_vp,
        selected_brands,
        selected_types
) -> pd.DataFrame:
    data = data[data['Ep'].between(selected_elasticity[0], selected_elasticity[1])]
    data = data[data['Ec/Ep'].between(selected_ec_ep[0], selected_ec_ep[1])]
    data = data[data['Vp'].between(selected_vibration[0], selected_vibration[1])]
    data = data[data['Vl/Vp'].between(selected_vl_vp[0], selected_vl_vp[1])]
    if selected_types:
        data = data[data["Type"].isin(selected_types)]
    if selected_brands:
        data = data[data["Brand"].isin(selected_brands)]
    return data
