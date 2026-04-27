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
            is_multi = st.selectbox(
                "Багатосторонній", options=["Ні", "Так"], key="is_multilateral"
            )
            if is_multi == "Так":
                st.number_input(
                    "Кількість сторін",
                    min_value=2,
                    max_value=20,
                    value=2,
                    step=1,
                    key="party_count",
                )
            st.text_input("№ папки в Архіві", key="archive_folder_num")
            st.selectbox(
                "Вид Договору(облік в 1С)",
                options=load_options("oblik.txt"),
                key="oblik_type",
            )
