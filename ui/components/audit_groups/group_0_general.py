import streamlit as st
from core.utils.data_cleaners import load_options


def render_group_0():
    # ГРУПА 0: Загальна інформація
    with st.expander("Група 0: Загальна інформація", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox(
                "Тип договору",
                options=load_options("contract_types.txt"),
                key="contract_type",
            )
            st.selectbox(
                "Організація", options=load_options("org_list.txt"), key="organization"
            )
            st.selectbox(
                "Населений пункт", options=load_options("vilage.txt"), key="settlement"
            )

        with col2:
            st.selectbox(
                "Тип Контрагенту",
                options=load_options("counterparty_types.txt"),
                key="counterparty_type",
            )
            st.selectbox(
                "Багатосторонній", options=["Так", "Ні"], key="is_multilateral"
            )
            st.text_input("№ папки в Архіві", key="archive_folder_num")
