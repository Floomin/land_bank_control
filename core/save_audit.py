import uuid
from core.database import get_connection

def save_audit_data(session_state_data):
    """
    Збирає дані з форми (st.session_state) та зберігає їх у базу даних.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Генеруємо унікальний ID для цього аудиту
    audit_id = str(uuid.uuid4())
    
    try:
        # 1. ЗБЕРЕЖЕННЯ ГОЛОВНОГО ДОГОВОРУ (Audit_Contracts)
        insert_contract_query = """
        INSERT INTO Audit_Contracts (
            id, cadastral_number, created_by, contract_type_1c, contract_type,
            organization, settlement, counterparty_type, is_multilateral, party_count,
            archive_folder_num, has_original, contract_number, rent_reg_number,
            end_date, sign_date, reg_date, end_date_audit, duration_years,
            duration_months, duration_days, area_paper, land_status_1c, area_legal,
            purpose_legal, has_lessee_sign, has_seals, auditor_note
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """
        
        # Витягуємо дані безпечно через .get()
        contract_values = (
            audit_id,
            session_state_data.get("last_selected_cadastre"),     # З пошуку
            "auditor_user",                                       # Тимчасовий хардкод користувача
            session_state_data.get("1c_contract_type"),           # Група 0
            session_state_data.get("contract_type"),              # Група 0
            session_state_data.get("organization"),               # Група 0
            session_state_data.get("settlement"),                 # Група 0
            session_state_data.get("counterparty_type"),          # Група 0
            1 if session_state_data.get("is_multilateral") == "Так" else 0, 
            int(session_state_data.get("party_count", 1)),
            session_state_data.get("archive_folder_num"),
            1 if session_state_data.get("has_original") else 0,   # Група 1
            session_state_data.get("contract_number"),            # Група 2
            session_state_data.get("rent_reg_number"),            
            session_state_data.get("end_date"),
            session_state_data.get("sign_date"),
            session_state_data.get("reg_date"),
            session_state_data.get("end_date_audit"),
            session_state_data.get("duration_years", 0),
            session_state_data.get("duration_months", 0),
            session_state_data.get("duration_days", 0),
            session_state_data.get("area_paper"),                 # Група 3
            session_state_data.get("purpose"),                    # Статус 1С
            session_state_data.get("area_legal"),                 
            session_state_data.get("purpose_legal"),
            1 if session_state_data.get("has_lessee_sign") else 0,# Група 5
            1 if session_state_data.get("has_seals") else 0,
            session_state_data.get("auditor_note")                # Примітка
        )
        
        cursor.execute(insert_contract_query, contract_values)
        
        # 2. ТУТ БУДЕ ЗБЕРЕЖЕННЯ СТОРІН (Audit_Parties)
        # ...
        
        # 3. ТУТ БУДЕ ЗБЕРЕЖЕННЯ ДОД. УГОД (Audit_Agreements_Simple)
        # ...
        
        # Фіксуємо транзакцію, якщо все пройшло без помилок
        conn.commit()
        return True, "Дані успішно збережено!"
        
    except Exception as e:
        # Якщо сталася помилка - скасовуємо всі зміни (Rollback)
        conn.rollback()
        return False, f"Помилка збереження: {e}"
    finally:
        conn.close()