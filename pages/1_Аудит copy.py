import streamlit as st
from core.queries.queries import get_all_cadastral_numbers, get_contract_details_by_cadastre, get_audit_status
from core.auth import authenticate
from ui.components.form_audit import render_audit_form

st.title("Аудит земельного банку")

if "cadastral_list" not in st.session_state:
    st.session_state.cadastral_list = get_all_cadastral_numbers()

col_search1, col_search2 = st.columns([2, 2])

with col_search1:
    search_input = st.text_input("Введіть кадастровий номер (або останні 4 цифри):", key="search_field")
    filtered_options = (
        [cad for cad in st.session_state.cadastral_list if search_input in cad] if search_input else []
    )

with col_search2:
    # ПУНКТ 1: Динамічна зміна заголовка
    if search_input:
        label_text = f"Знайдено ділянок: **{len(filtered_options)}**"
    else:
        label_text = "Оберіть кадастровий номер зі списку:"
    
    selected_cadastre = st.selectbox(label_text, options=[""] + filtered_options, index=0)

# Функція заповнення (ПУНКТ 3: Додано примусове скидання значень перед заповненням)
def fill_form_from_1c(data):
    if data:
        # Очищуємо старі ключі, щоб уникнути конфліктів
        fields_to_update = {
            "archive_folder_num": data.get("archive_folder_1c"),
            "organization": data.get("organization_1c"),
            "settlement": data.get("settlement_1c"),
            "is_multilateral": data.get("is_multilateral_1c") or "Ні",
            "counterparty_type": data.get("landlord_type_1c"),
            "1c_contract_type": data.get("contract_type_1c"),
            "contract_number": data.get("contract_number_1c"),
            "rent_reg_number": data.get("reg_number_1c"), # ПУНКТ 2: Перевірка зв'язку
            "landlord_name": data.get("landlord_name_1c"),
            "landlord_ipn": data.get("landlord_ipn_1c"),
            "part_rent": data.get("rent_share_1c"),
            "purpose": data.get("land_status_1c"),
            "duration_years": int(data.get("term_contract_1c") or 0),
            "area_legal": float(data.get("area_1c") or 0.0),
            "area_paper": float(data.get("area_1c") or 0.0),
            # ПУНКТ 4: Дати тепер обробляються без ризику порожніх значень
            "sign_date": data.get("sign_date_1c"),
            "reg_date": data.get("reg_date_1c"),
            "end_date": data.get("end_date_1c")
        }
        for key, val in fields_to_update.items():
            st.session_state[key] = val if val is not None else ""

# Обробка вибору (Перенесено ВГОРУ, до рендеру форми)
if selected_cadastre and selected_cadastre != st.session_state.get("last_selected_cadastre"):
    data_1c = get_contract_details_by_cadastre(selected_cadastre)
    if data_1c:
        fill_form_from_1c(data_1c)
        st.session_state["last_selected_cadastre"] = selected_cadastre
        st.rerun() # ПУНКТ 3: Примусовий перезапуск гарантує, що віджети побачать дані

if selected_cadastre:
    audit_status = get_audit_status(selected_cadastre)
    is_unlocked = st.session_state.get(f"unlocked_{selected_cadastre}", False)

    if audit_status["is_audited"] and not is_unlocked:
        st.error(f"🔒 Ця кадастрова ділянка вже опрацьована користувачем **{audit_status['created_by']}**.")
        if st.session_state.user.get("role") == "admin":
            admin_pass = st.text_input("Підтвердіть пароль адміністратора:", type="password")
            if st.button("🔓 Розблокувати"):
                if authenticate(st.session_state.user["username"], admin_pass):
                    st.session_state[f"unlocked_{selected_cadastre}"] = True
                    st.rerun()
    else:
        render_audit_form()