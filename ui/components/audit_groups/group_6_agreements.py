import streamlit as st
import uuid


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

                # Приклади полів додаткової угоди
                c1, c2 = st.columns(2)
                with c1:
                    st.text_input("Номер дод. угоди", key=f"num_{agr_id}")
                with c2:
                    st.date_input("Дата підписання", value=None, key=f"date_{agr_id}")
