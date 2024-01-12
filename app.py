import streamlit as st

from src.data import load_data, filter_data
from src.filter import slider, multiselect
from src.graph import Plot


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
        data=raw_data,
        label="Primary Elasticity  (Ep)",
        col="Ep",
    )

    selected_ec_ep = slider(
        data=raw_data,
        label="Linearity (Ec/Ep)",
        col="Ec/Ep",
    )

    selected_vibration = slider(
        data=raw_data,
        label="Primary Vibration (Vp)",
        col="Vp",
    )

    selected_vl_vp = slider(
        data=raw_data,
        label="Feedback Character (Vl/Vp)",
        col="Vl/Vp",
    )

    selected_brands = multiselect(
        data=raw_data,
        label="Brand",
        col="Brand",
    )

    selected_types = multiselect(
        data=raw_data,
        label="Blade Type",
        col="Type",
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

elasticity_plot = Plot(
    title="Comparison by Elasticity Indices",
    raw_data=raw_data,
    x_dim='Ep',
    y_dim="Ec/Ep",
    size_dim="Vp",
    marker_size_function=lambda x: 1 / x ** 7,
    legend_marker_size_function=lambda x: 10 / x,
)
st.plotly_chart(
    elasticity_plot.plot(filtered_data),
    use_container_width=True,
)

vibration_plot = Plot(
    title="Comparison by Vibration Indices",
    raw_data=raw_data,
    x_dim='Vp',
    y_dim="Vl/Vp",
    size_dim="Ep",
    marker_size_function=lambda x: x ** 3,
    legend_marker_size_function=lambda x: x ** 3,
)
st.plotly_chart(
    vibration_plot.plot(filtered_data),
    use_container_width=True,
)