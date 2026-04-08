import streamlit as st
from core.auth import authenticate
from ui.components.auth_form import render_login_form

# Настройка страницы должна быть первым вызовом Streamlit
st.set_page_config(
    page_title="Land Bank Control",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",  # Прячем боковое меню до авторизации
)

# Инициализация состояния сессии
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

# Роутинг
if not st.session_state.authenticated:
    # Если не авторизован - показываем форму
    user_input, pass_input = render_login_form()

    if user_input and pass_input:
        if authenticate(user_input, pass_input):
            st.session_state.authenticated = True
            st.session_state.username = user_input
            st.rerun()  # Перезапускаем приложение для обновления интерфейса
        else:
            st.error("Неверное имя пользователя или пароль.")
else:
    # Если авторизован - показываем основной интерфейс
    st.sidebar.success(f"👤 Вы вошли как: {st.session_state.username}")

    if st.sidebar.button("Выйти", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()

    st.title("Добро пожаловать!")
    st.info("👈 Раскройте боковое меню, чтобы перейти к Аудиту или Результатам.")
