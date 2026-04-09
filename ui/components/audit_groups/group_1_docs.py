import streamlit as st
from core.utils.data_cleaners import load_options


def render_group_1():
    # ГРУПА 1: Наявність документів
    with st.expander("Група 1: Наявність документів", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.checkbox("Оригінал договору", value=True)
        with c2:
            st.checkbox("Копія паспорта", value=True)
        with c3:
            st.checkbox("Копія ІПН", value=True, help="text")

        st.multiselect(
            "Копія правоустановчих документів",
            options=load_options("legal_docs.txt"),
            help="Можна обрати декілька варіантів",
        )
