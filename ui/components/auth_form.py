import streamlit as st
from core.utils.text_parsers import fix_keyboard_layout


def render_login_form():
    """
    Отрисовывает форму логина по центру экрана и возвращает введенные данные.
    """
    # Используем колонки, чтобы отцентрировать форму
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("🔐 Вход в систему")
        st.markdown("Система контроля земельного банка (Land Bank Control System)")

        with st.form("login_form"):
            username = st.text_input("Пользователь")
            raw_password = st.text_input("Пароль", type="password")
            submitted = st.form_submit_button("Войти", use_container_width=True)

            if submitted:
                fixed_password = fix_keyboard_layout(raw_password)

                return username, fixed_password

    return None, None
