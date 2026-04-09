import streamlit as st
from ui.components.form_audit import render_audit_form

st.title("Аудит земельного банку")

# 1. Пошук кадастрового номера
col_search1, col_search2 = st.columns([2, 2])

with col_search1:
    search_input = st.text_input("Введіть кадастровий номер (або останні 4 цифри):")

# Тут буде логіка запиту до БД. Поки зробимо заглушку.
mock_db = ["3221483301:01:043:0001", "3221483301:01:043:0044", "0520885200:02:001:0123"]
filtered_options = (
    [cad for cad in mock_db if search_input in cad] if search_input else []
)

with col_search2:
    selected_cadastre = st.selectbox(
        "Оберіть кадастровий номер зі списку:", options=[""] + filtered_options, index=0
    )

# 2. Відображення блоків після вибору
if selected_cadastre:
    # col_left, col_right = st.columns([1, 2])

    # with col_left:
    st.info("ℹ️ Дані з 1С")
    st.write("Тут будуть дані для порівняння...")
    # st.json(data_from_1c) # Майбутня реалізація

    # with col_right:
    render_audit_form()
else:
    st.info("Будь ласка, введіть та оберіть кадастровий номер для початку роботи.")
