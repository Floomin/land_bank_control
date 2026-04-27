import streamlit as st
from core.database import get_connection

st.title("⚙️ Керування користувачами")

# Перевірка прав доступу (на всякий випадок)
if st.session_state.user.get("role") != "admin":
    st.error("Доступ заборонено!")
    st.stop()

tabs = st.tabs(["➕ Додати користувача", "📋 Список користувачів"])

with tabs[0]:
    st.subheader("Створити новий акаунт")
    with st.form("add_user_form", clear_on_submit=True):
        new_username = st.text_input("Логін (username)")
        new_fullname = st.text_input("Повне ім'я (ПІБ)")
        new_password = st.text_input("Пароль", type="password")
        new_role = st.selectbox("Роль", ["auditor", "management", "admin"])
        
        if st.form_submit_button("Зберегти користувача"):
            if new_username and new_password:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO Users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                        (new_username, new_password, new_fullname, new_role)
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"Користувача {new_username} успішно створено!")
                except Exception as e:
                    st.error(f"Помилка: {e}")
            else:
                st.warning("Заповніть логін та пароль")

with tabs[1]:
    st.subheader("Поточні користувачі")
    try:
        conn = get_connection()
        import pandas as pd
        df = pd.read_sql("SELECT username, full_name, role, is_active FROM Users", conn)
        conn.close()
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Не вдалося завантажити список: {e}")