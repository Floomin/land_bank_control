import streamlit as st
import os
from core.utils.text_parsers import fix_keyboard_layout


def render_login_form():
    """
    Отрисовывает форму логина по центру экрана и возвращает введенные данные.
    """
    # Используем колонки, чтобы отцентрировать форму
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # --- БЛОК ДОБАВЛЕНИЯ ЛОГОТИПА ---
        # Путь к файлу логотипа (предполагаем, что он лежит в корне проекта)
        logo_path = os.path.join(os.getcwd(), "logo.png")

        # Проверяем, существует ли файл, прежде чем пытаться его отрисовать
        if os.path.exists(logo_path):
            # Отрисовываем логотип, растягиваем его по ширине колонки
            st.image(logo_path, width="stretch")
        else:
            st.warning(
                "⚠️ Файл логотипа 'logo.png' не найден в корневой папке проекта. Пожалуйста, добавьте его."
            )
        # --------------------------------

        st.title("Вхід в систему")
        st.markdown("Система контролю земельного банку")

        with st.form("login_form"):
            username = st.text_input("Користувач")
            raw_password = st.text_input("Пароль", type="password")
            submitted = st.form_submit_button("Увійти", width="stretch")

            if submitted:
                fixed_password = fix_keyboard_layout(raw_password)
                return username, fixed_password

    return None, None
