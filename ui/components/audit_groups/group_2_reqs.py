import streamlit as st
import uuid
from core.utils.data_cleaners import load_options


def render_group_2(prefix=""):
    # ГРУПА 2: Реквізити договору
    with st.expander("Група 2: Реквізити договору", expanded=True):
        # 1. Загальні реквізити самого договору
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Номер договору", key=f"{prefix}contract_number")
            st.text_input("Номер реєстрації оренди", key=f"{prefix}rent_reg_number")
            st.date_input(
                "Дата закінчення (**:red[Згідно останього діючого документа]**)",
                value=None,
                key=f"{prefix}end_date",
                format="DD/MM/YYYY",
            )
        with col2:
            st.date_input(
                "Дата підписання (ДОЗ)",
                value=None,
                key=f"{prefix}sign_date",
                format="DD/MM/YYYY",
            )
            st.date_input(
                "Дата реєстрації договору / Дата реєстрації права оренди",
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

        st.write("**Строк дії (:red[Згідно останього діючого документа])**")
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
                st.text_input(
                    "ПІБ Орендодавця (**:red[Згідно останього діючого документа]**)",
                    key=f"{prefix}landlord_name",
                )
                st.text_input(
                    "Частка права володіння (напр. 1/3) (**:red[Згідно Право. документа]**)",
                    key=f"{prefix}ownership_share",
                )
                st.text_input(
                    "Частка паю (картка земельної ділянки)", key=f"{prefix}part_share"
                )
            with c2:
                st.text_input(
                    "ІПН (пайовика) (**:red[Згідно останього діючого документа]**)",
                    key=f"{prefix}landlord_ipn",
                )
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
                            "ПІБ Орендодавця (**:red[Згідно останього діючого документа]**)",
                            key=f"{prefix}landlord_name_{i}",
                        )
                        st.text_input(
                            "Частка права володіння (напр. 1/3) (**:red[Згідно Право. документа]**)",
                            key=f"{prefix}ownership_share_{i}",
                        )
                        st.text_input(
                            "Частка паю (картка земельної ділянки)",
                            key=f"{prefix}part_share_{i}",
                        )
                    with c2:
                        st.text_input(
                            "ІПН (пайовика) (**:red[Згідно останього діючого документа]**)",
                            key=f"{prefix}landlord_ipn_{i}",
                        )
                        st.text_input(
                            "Частка орендної плати", key=f"{prefix}part_rent_{i}"
                        )

        # --- НОВИЙ БЛОК: СПРОЩЕНІ ДОДАТКОВІ УГОДИ ---
        st.divider()
        st.write("**Додаткові угоди**")

        # Використовуємо унікальний ключ для списку угод у session_state
        agreements_key = f"{prefix}simple_agreements"
        if agreements_key not in st.session_state:
            st.session_state[agreements_key] = []

        if st.button("➕ Додати угоду", key=f"{prefix}add_simple_agr", width="stretch"):
            st.session_state[agreements_key].append(str(uuid.uuid4()))
            st.rerun()

        if not st.session_state[agreements_key]:
            st.info("Додаткові угоди відсутні")

        for idx, agr_id in enumerate(st.session_state[agreements_key]):
            with st.container(border=True):
                col_title, col_del = st.columns([4, 1])
                with col_title:
                    st.markdown(f"**Угода #{idx + 1}**")
                with col_del:
                    if st.button(
                        "🗑️ Видалити", key=f"{prefix}del_agr_{agr_id}", width="stretch"
                    ):
                        st.session_state[agreements_key].remove(agr_id)
                        st.rerun()

                c1, c2 = st.columns(2)
                with c1:
                    st.selectbox(
                        "Тип додаткової угоди",
                        options=load_options("agreements_type.txt"),
                        key=f"{prefix}agr_type_{agr_id}",
                    )
                with c2:
                    st.date_input(
                        "Дата підписання",
                        value=None,
                        format="DD/MM/YYYY",
                        key=f"{prefix}agr_date_{agr_id}",
                    )