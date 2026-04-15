import streamlit as st


def render_group_2(prefix=""):
    # ГРУПА 2: Реквізити договору
    with st.expander("Група 2: Реквізити договору", expanded=True):
        # 1. Загальні реквізити самого договору
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Номер договору", key=f"{prefix}contract_number")
            st.text_input("Номер реєстрації оренди", key=f"{prefix}rent_reg_number")
            st.date_input(
                "Дата закінчення (**:red[згідно ДОГОВОРУ!!!]**)",
                value=None,
                key=f"{prefix}end_date",
                format="DD/MM/YYYY",
            )
        with col2:
            st.date_input(
                "Дата підписання",
                value=None,
                key=f"{prefix}sign_date",
                format="DD/MM/YYYY",
            )
            st.date_input(
                "Дата реєстрації договору",
                value=None,
                key=f"{prefix}reg_date",
                format="DD/MM/YYYY",
            )
            st.date_input(
                "Дата закінчення (Аудит)",
                value=None,
                key=f"{prefix}end_date_audit",
                format="DD/MM/YYYY",
            )

        st.write("**Строк дії**")
        sc1, sc2, sc3 = st.columns(3)
        sc1.number_input("Роки", min_value=0, step=1, key=f"{prefix}duration_years")
        sc2.number_input(
            "Місяці", min_value=0, max_value=11, key=f"{prefix}duration_months"
        )
        sc3.number_input("Дні", min_value=0, max_value=30, key=f"{prefix}duration_days")

        st.divider()

        # 2. Реквізити Орендодавців
        is_multi = st.session_state.get(f"{prefix}is_multilateral", "Ні")
        count = (
            st.session_state.get(f"{prefix}party_count", 1) if is_multi == "Так" else 1
        )

        if count == 1:
            # СТАНДАРТНИЙ ВИГЛЯД (1 СТОРОНА)
            st.write("**Дані Орендодавця**")
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("ПІБ Орендодавця", key=f"{prefix}landlord_name")
                st.text_input(
                    "Частка права володіння (напр. 1/3)", key=f"{prefix}ownership_share"
                )
                st.text_input(
                    "Частка паю (картка земельної ділянки)", key=f"{prefix}part_share"
                )
            with c2:
                st.text_input("ІПН (пайовика)", key=f"{prefix}landlord_ipn")
                st.text_input("Частка орендної плати", key=f"{prefix}part_rent")
        else:
            # БАГАТОСТОРОННІЙ ВИГЛЯД
            st.write("**Дані Орендодавців:**")
            for i in range(1, count + 1):
                with st.container(border=True):
                    st.markdown(f"**Сторона {i}**")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.text_input(
                            "ПІБ Орендодавця", key=f"{prefix}landlord_name_{i}"
                        )
                        st.text_input(
                            "Частка права володіння (напр. 1/3)",
                            key=f"{prefix}ownership_share_{i}",
                        )
                        st.text_input(
                            "Частка паю (картка земельної ділянки)",
                            key=f"{prefix}part_share_{i}",
                        )
                    with c2:
                        st.text_input("ІПН (пайовика)", key=f"{prefix}landlord_ipn_{i}")
                        st.text_input(
                            "Частка орендної плати", key=f"{prefix}part_rent_{i}"
                        )
        # ---  ЗМІНА ВЛАСНИКА ---
        st.divider()
        st.write("**Зміна власника**")

        # Визначаємо ключ для чекбокса з урахуванням префікса
        owner_changed_key = f"{prefix}is_owner_changed"

        # Створюємо чекбокс. Його стан автоматично запишеться в st.session_state
        st.checkbox("Зміна власника", key=owner_changed_key)

        # Якщо чекбокс активний (True), відображаємо текстове поле
        if st.session_state.get(owner_changed_key, False):
            st.text_input("Новий власник (ПІБ / Назва)", key=f"{prefix}new_owner_name")
