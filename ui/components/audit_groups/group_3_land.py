import streamlit as st
from core.utils.data_cleaners import load_options


def render_group_3(prefix=""):
    # ГРУПА 3: Відомості про земельну ділянку
    with st.expander("Група 3: Відомості про земельну ділянку", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input(
                "Площа по паперовому примірнику",
                format="%.4f",
                min_value=0.0,
                key=f"{prefix}area_paper",
            )
            
            st.selectbox(
                "Статус ділянки (1С)",
                options=load_options("land_status.txt"),
                key=f"{prefix}purpose",
            )

        with col2:
            st.number_input(
                "Площа згідно правоустановчих документів",
                format="%.4f",
                min_value=0.0,
                key=f"{prefix}area_legal",
            )
            
            st.selectbox(
                "Цільове призначення згідно правоустановчих документів",
                options=load_options("land_purposes.txt"),
                key=f"{prefix}purpose_legal",
            )