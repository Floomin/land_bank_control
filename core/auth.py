import streamlit as st
from core.database import get_connection

def authenticate(username, password):
    """Перевірка користувача через базу даних MS SQL."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Шукаємо активного користувача з відповідним паролем
        query = """
            SELECT username, full_name, role 
            FROM Users 
            WHERE username = ? AND password_hash = ? AND is_active = 1
        """
        cursor.execute(query, (username, password))
        row = cursor.fetchone()
        conn.close()

        if row:
            # Повертаємо об'єкт користувача
            return {
                "username": row.username,
                "full_name": row.full_name,
                "role": row.role
            }
        return None
    except Exception as e:
        st.error(f"Помилка авторизації: {e}")
        return None