import streamlit as st
from core.auth import authenticate
from ui.components.auth_form import render_login_form

st.set_page_config(
    page_title="Land Bank Control",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

if not st.session_state.authenticated:
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)

    user_input, pass_input = render_login_form()

    if user_input and pass_input:
        if authenticate(user_input, pass_input):
            st.session_state.authenticated = True
            st.session_state.username = user_input
            st.rerun()
        else:
            st.error("Неверное имя пользователя или пароль.")

else:
    # Визначаємо доступні сторінки
    if st.session_state.get("username") == "admin":
        pages = [
            st.Page("pages/1_Аудит.py", title="Аудит", icon="📋"),
            st.Page("pages/2_Результати.py", title="Результати", icon="📈"),
        ]
    else:
        # Для звичайного аудитора
        pages = [
            st.Page("pages/1_Аудит.py", title="Аудит", icon="📋"),
        ]

    pg = st.navigation(pages)

    with st.sidebar:
        st.write(f"Пользователь: **{st.session_state.get('username', 'admin')}**")
        # Исправлено: используем width="stretch"
        if st.button("Выйти", width="stretch"):
            st.session_state.authenticated = False
            st.rerun()

    pg.run()
