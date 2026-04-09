import streamlit as st


def render_group_2(prefix=""):
    # ГРУПА 2: Реквізити договору
    with st.expander("Група 2: Реквізити договору", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Номер договору", key=f"{prefix}contract_number")
            st.text_input("Номер реєстрації оренди", key=f"{prefix}rent_reg_number")
            st.text_input("ПІБ Орендодавця", key=f"{prefix}landlord_name")
            st.text_input(
                "Частка права володіння (напр. 1/3)", key=f"{prefix}ownership_share"
            )
            st.date_input(
                "Дата закінчення (**:red[зігдно ДОГОВОРУ!!!]**)",
                value=None,
                key=f"{prefix}end_date",
            )
        with col2:
            st.date_input("Дата підписання", value=None, key=f"{prefix}sign_date")
            st.date_input(
                "Дата реєстрації договору", value=None, key=f"{prefix}reg_date"
            )
            st.text_input("ІПН (пайовика)", key=f"{prefix}landlord_ipn")
            # st.text_input("Паспортні дані")
            st.text_input(
                "Частка паю (картка земельної ділянки)", key=f"{prefix}part_share"
            )
            st.text_input("Частка орендної плати", key=f"{prefix}part_rent")
            st.date_input(
                "Дата закінчення (Аудит)", value=None, key=f"{prefix}end_date_audit"
            )

        st.write("**Строк дії**")
        sc1, sc2, sc3 = st.columns(3)
        sc1.number_input("Роки", min_value=0, step=1, key=f"{prefix}duration_years")
        sc2.number_input(
            "Місяці", min_value=0, max_value=11, key=f"{prefix}duration_months"
        )
        sc3.number_input("Дні", min_value=0, max_value=30, key=f"{prefix}duration_days")
