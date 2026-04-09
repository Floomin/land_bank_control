import streamlit as st
from core.utils.data_cleaners import load_options


def render_group_3():
    # ГРУПА 3: Відомості про земельну ділянку
    with st.expander("Група 3: Відомості про земельну ділянку", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input(
                "Площа по паперовому примірнику", format="%.4f", min_value=0.0
            )
            st.text_input("Місце розташування")
            st.selectbox(
                "Цільове призначення", options=load_options("land_purposes.txt")
            )
            st.selectbox("Вид угідь", options=load_options("land_types.txt"))
        with col2:
            st.number_input(
                "Площа згідно правоустановчих документів", format="%.4f", min_value=0.0
            )
            st.text_input("Місце розташування (ПД)")
            st.selectbox(
                "Цільове призначення (ПД)",
                options=load_options("land_purposes.txt"),
                key="purpose_pd",
            )
            st.selectbox(
                "Вид угідь (ПД)", options=load_options("land_types.txt"), key="type_pd"
            )
