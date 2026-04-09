import streamlit as st
from core.utils.data_cleaners import load_options


def render_group_1(prefix=""):
    # ГРУПА 1: Наявність документів
    with st.expander("Група 1: Наявність документів", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.checkbox("Оригінал договору", value=True, key=f"{prefix}has_original")
        with c2:
            st.checkbox("Копія паспорта", value=True, key=f"{prefix}has_passport_copy")
        with c3:
            st.checkbox(
                "Копія ІПН", value=True, help="text", key=f"{prefix}has_ipn_copy"
            )

        st.multiselect(
            "Копія правоустановчих документів",
            options=load_options("legal_docs.txt"),
            help="Можна обрати декілька варіантів",
            key=f"{prefix}legal_docs_copies",
        )
