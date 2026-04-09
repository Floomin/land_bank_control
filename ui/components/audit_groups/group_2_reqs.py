import streamlit as st


def render_group_2():
    # ГРУПА 2: Реквізити договору
    with st.expander("Група 2: Реквізити договору", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Номер договору")
            st.text_input("Номер реєстрації оренди")
            st.text_input("ПІБ Орендодавця")
            st.text_input("Частка права володіння (напр. 1/3)")
            st.date_input("Дата закінчення (зігдно ДОГОВОРУ!!!)", value=None)
        with col2:
            st.date_input("Дата підписання", value=None)
            st.date_input("Дата реєстрації договору", value=None)
            st.text_input("ІПН (пайовика)")
            # st.text_input("Паспортні дані")
            st.text_input("Частка паю (картка земельної ділянки)")
            st.text_input("Частка орендної плати")
            st.date_input("Дата закінчення (Аудит)", value=None)

        st.write("**Строк дії**")
        sc1, sc2, sc3 = st.columns(3)
        sc1.number_input("Роки", min_value=0, step=1)
        sc2.number_input("Місяці", min_value=0, max_value=11)
        sc3.number_input("Дні", min_value=0, max_value=30)
