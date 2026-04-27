import streamlit as st

from ui.components.audit_groups.group_0_general import render_group_0
from ui.components.audit_groups.group_1_docs import render_group_1
from ui.components.audit_groups.group_2_reqs import render_group_2
from ui.components.audit_groups.group_3_land import render_group_3
from ui.components.audit_groups.group_5_legal import render_group_5
#from ui.components.audit_groups.group_6_agreements import render_group_6

def render_audit_form():
    """Відображає форму аудиту, розділену на групи."""

    st.subheader("Форма аудиту")

    render_group_0()
    render_group_1()
    render_group_2()
    render_group_3()
    render_group_5()
    
    st.text_area(
        "Примітка Аудитора",
        placeholder="Заповніть усі не зазначені у формі помилки в договорі. \nКожну помилку починайте з цифри по порядку.\nНаприклад:\n1. У паперовому примірнику помилка у ПІБ орендодавця ",
        height=200,
        key="auditor_note",
    )

    # КНОПКА ЗБЕРЕЖЕННЯ
    st.divider()
    
    # Вирівнюємо кнопку по центру
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Зберегти результати аудиту", width="stretch", type="primary"):
            st.session_state.show_confirm = True

    # Модальне вікно підтвердження
    if st.session_state.get("show_confirm"):
        st.warning("Ви впевнені, що хочете зберегти дані?")
        cb1, cb2 = st.columns(2)
        if cb1.button("Так, зберегти", width="stretch"):
            # ТУТ ми пізніше викличемо функцію save_audit_data()
            st.success("Дані збережено!")
            st.session_state.show_confirm = False
        if cb2.button("Скасувати", width="stretch"):
            st.session_state.show_confirm = False