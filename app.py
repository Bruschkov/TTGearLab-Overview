import streamlit as st

from src.data import load_data, filter_data
from src.filter import slider
from src.graph import TrendLinePlot, SizeDimPlot
from src.util import sort_unique


raw_data = load_data()

st.title("TTGearLab Blade Metrics Overview")
st.markdown(
    '''
    Complete Overview of all TTGearlabs blade lab result. See [here](https://ttgearlab.com/about-ttgearlab/) a detailed explanation of metrics and how they can be interpreted.  
    '''
)

with st.sidebar:
    st.title("Filters")

    selected_elasticity = slider(
        data=raw_data['Ep'],
        label="Primary Elasticity  (Ep)",
    )

    selected_ec_ep = slider(
        data=raw_data["Ec/Ep"],
        label="Linearity (Ec/Ep)",
    )

    selected_vibration = slider(
        data=raw_data["Vp"],
        label="Primary Vibration (Vp)",
    )

    selected_vl_vp = slider(
        data=raw_data["Vl/Vp"],
        label="Feedback Character (Vl/Vp)",
    )

    selected_brands = st.multiselect(
        label="Brand",
        options=sort_unique(raw_data["Brand"])
    )

    selected_types = st.multiselect(
        label="Blade Type",
        options=sort_unique(raw_data["Type"])
    )


filtered_data = filter_data(
    data=raw_data,
    selected_elasticity=selected_elasticity,
    selected_ec_ep=selected_ec_ep,
    selected_vibration=selected_vibration,
    selected_vl_vp=selected_vl_vp,
    selected_brands=selected_brands,
    selected_types=selected_types,
)

elasticity_plot = SizeDimPlot(
    title="Comparison by Elasticity Indices",
    raw_data=raw_data,
    x_dim='Ep',
    y_dim="Ec/Ep",
    size_dim="Vp",
    marker_size_function=lambda x: 1 / x ** 8,
    legend_marker_size_function=lambda x: 10 / x,
)
st.plotly_chart(
    elasticity_plot.plot(filtered_data),
    use_container_width=True,
)

vibration_plot = SizeDimPlot(
    title="Comparison by Vibration Indices",
    raw_data=raw_data,
    x_dim='Vp',
    y_dim="Vl/Vp",
    size_dim="Ep",
    marker_size_function=lambda x: x ** 3.8,
    legend_marker_size_function=lambda x: x ** 3,
)
st.plotly_chart(
    vibration_plot.plot(filtered_data),
    use_container_width=True,
)

ep_vs_vp_plot = TrendLinePlot(
    title="Primary Elasticity vs. Primary Vibration",
    raw_data=raw_data,
    x_dim='Ep',
    y_dim="Vp",
)
st.plotly_chart(
    ep_vs_vp_plot.plot(filtered_data),
    use_container_width=True,
)