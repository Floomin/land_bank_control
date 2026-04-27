import streamlit as st
from core.auth import authenticate
from ui.components.auth_form import render_login_form

# Налаштування сторінки
st.set_page_config(
    page_title="Land Bank Control",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Стиль для приховування сайдбару та навігації на екрані логіна
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
"""

# Ініціалізація станів сесії
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.authenticated:
    # Відображення екрана входу
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)

    user_input, pass_input = render_login_form()

    if user_input and pass_input:
        # Виклик функції автентифікації, яка перевіряє дані в БД
        user_data = authenticate(user_input, pass_input)
        if user_data:
            st.session_state.authenticated = True
            st.session_state.user = user_data
            st.rerun()
        else:
            st.error("Неправильне ім'я користувача або пароль.")

else:
    # Визначення доступних сторінок на основі ролі користувача
    role = st.session_state.user.get("role")
    pages = []

    if role == "admin":
        pages = [
            st.Page("pages/1_Аудит.py", title="Аудит", icon="📋"),
            st.Page("pages/2_Результати.py", title="Результати", icon="📈"),
            st.Page("pages/3_Користувачі.py", title="Користувачі", icon="👤"),
        ]
    elif role == "auditor":
        pages = [
            st.Page("pages/1_Аудит.py", title="Аудит", icon="📋"),
        ]
    elif role == "management":
        pages = [
            st.Page("pages/2_Результати.py", title="Результати", icon="📈"),
        ]

    # Налаштування навігації
    pg = st.navigation(pages)

    # Бічна панель з інформацією про користувача та кнопкою виходу
    with st.sidebar:
        st.write(f"Користувач: **{st.session_state.user.get('full_name', 'Користувач')}**")
        st.caption(f"Роль: {role}")
        
        if st.button("Вийти", width="stretch"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()

    # Запуск обраної сторінки
    pg.run()