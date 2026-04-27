import streamlit as st
from core.database import get_connection

def get_all_cadastral_numbers():
    """Отримує список усіх кадастрових номерів для випадаючого списку."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT cadastral_number FROM System1C_Contracts ORDER BY cadastral_number")
        numbers = [row[0] for row in cursor.fetchall()]
        conn.close()
        return numbers
    except Exception as e:
        st.error(f"Помилка завантаження номерів: {e}")
        return []

def get_contract_details_by_cadastre(cadastral_number):
    """Отримує всі дані з 1С для конкретного кадастрового номера."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM System1C_Contracts WHERE cadastral_number = ?"
        cursor.execute(query, (cadastral_number,))
        
        # Отримуємо назви колонок
        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()
        conn.close()

        if row:
            # Повертаємо словник {назва_колонки: значення}
            return dict(zip(columns, row))
        return None
    except Exception as e:
        st.error(f"Помилка пошуку даних: {e}")
        return None

def get_audit_status(cadastral_number):
    """Перевіряє, чи вже є збережений аудит по цьому кадастру."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Шукаємо автора в головній таблиці аудитів (яку ми створимо на наступному кроці)
        cursor.execute("SELECT created_by FROM Audit_Contracts WHERE cadastral_number = ?", (cadastral_number,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {"is_audited": True, "created_by": row[0]}
        return {"is_audited": False}
    except Exception as e:
        # Поки таблиці Audit_Contracts немає, просто повертаємо False, щоб не ламався інтерфейс
        return {"is_audited": False}