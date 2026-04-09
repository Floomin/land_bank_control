import streamlit as st
import uuid
from core.utils.data_cleaners import load_options

# Імпортуємо інші групи
from ui.components.audit_groups.group_1_docs import render_group_1
from ui.components.audit_groups.group_2_reqs import render_group_2
from ui.components.audit_groups.group_3_land import render_group_3
from ui.components.audit_groups.group_5_legal import render_group_5


def render_group_6():
    """Відображає Групу 6: Додаткові угоди з можливістю динамічного додавання"""
    if "agreements" not in st.session_state:
        st.session_state.agreements = []

    with st.expander("Група 6: Додаткові угоди", expanded=True):
        if st.button("➕ Додати додаткову угоду", width="stretch"):
            st.session_state.agreements.append(str(uuid.uuid4()))
            st.rerun()

        if not st.session_state.agreements:
            st.info("Немає доданих угод.")

        for index, agr_id in enumerate(st.session_state.agreements):
            with st.container(border=True):
                col_title, col_del = st.columns([4, 1])
                with col_title:
                    st.markdown(f"**Додаткова угода #{index + 1}**")
                with col_del:
                    if st.button("🗑️ Видалити", key=f"del_{agr_id}", width="stretch"):
                        st.session_state.agreements.remove(agr_id)
                        st.rerun()

                # 1. Власні атрибути додаткової угоди
                c1, c2 = st.columns(2)
                with c1:
                    st.selectbox(
                        "Тип Додаткової угоди",
                        options=load_options("agreements_type.txt"),
                        key=f"agr_type_{agr_id}",
                    )
                with c2:
                    st.selectbox(
                        "Багатостороння",
                        options=["Так", "Ні"],
                        key=f"agr_is_multilateral_{agr_id}",
                    )

                st.divider()

                # 2. Виклик стандартних груп із передачею префікса
                # Префікс гарантує, що ключі полів у різних угодах не співпадуть
                render_group_1(prefix=f"agr1_{agr_id}_")
                render_group_2(prefix=f"agr2_{agr_id}_")
                render_group_3(prefix=f"agr3_{agr_id}_")
                render_group_5(prefix=f"agr5_{agr_id}_")
