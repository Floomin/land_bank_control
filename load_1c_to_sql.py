import pandas as pd
import pyodbc
import numpy as np
import os
from dotenv import load_dotenv

# Завантажуємо змінні середовища з файлу .env
load_dotenv()

# ==========================================
# 1. НАЛАШТУВАННЯ ПІДКЛЮЧЕННЯ ДО MS SQL
# ==========================================
SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")

if not SERVER or not DATABASE:
    raise ValueError("❌ Помилка: Впевніться, що DB_SERVER та DB_NAME вказані у файлі .env")

# Формуємо рядок підключення
if USER and PASSWORD:
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USER};"
        f"PWD={{{PASSWORD}}};"
    )
else:
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"

excel_path = os.path.join("data", "data.xlsx")

def process_and_load_data():
    print(f"📥 Завантаження файлу: {excel_path} (Лист: 'data')")
    
    try:
        df = pd.read_excel(excel_path, sheet_name='data')
    except Exception as e:
        print(f"❌ Помилка читання Excel файлу: {e}")
        return
    
    df = df.dropna(subset=['Кадастровый номер'])
    df = df.replace({np.nan: None})
    
    def safe_date(date_val):
        if pd.isna(date_val) or date_val is None:
            return None
        try:
            return pd.to_datetime(date_val, dayfirst=True).strftime('%Y-%m-%d')
        except Exception:
            return None

    print("⚙️ Підключення до бази даних...")
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # SQL-запит (тепер 24 параметри, вилучено term_agr_detailed_1c)
        insert_query = """
        IF NOT EXISTS (SELECT 1 FROM System1C_Contracts WHERE cadastral_number = ?)
        BEGIN
            INSERT INTO System1C_Contracts (
                cadastral_number, archive_folder_1c, organization_1c, settlement_1c,
                area_1c, land_status_1c, is_multilateral_1c, contract_number_1c,
                sign_date_1c, term_contract_1c, end_date_1c, contract_type_1c,
                landlord_type_1c, agr_number_1c, agr_date_1c, term_agr_from_main_1c,
                end_date_agr_1c, agr_type_1c, landlord_name_1c,
                landlord_ipn_1c, rent_share_1c, reg_date_1c, reg_number_1c, state_1c
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        END
        """
        
        records_inserted = 0
        records_skipped = 0

        print("🚀 Початок імпорту...")
        for index, row in df.iterrows():
            cadastral_number = str(row['Кадастровый номер']).strip()
            
            # --- ОБРОБКА БАГАТОСТОРОННЬОГО ДОГОВОРУ ---
            multi_raw = row.get('Багатосторонній договір')
            if multi_raw is not None and str(multi_raw).strip() != "":
                is_multi_str = "Так"
            else:
                is_multi_str = "Ні"
            
            # Підготовка значень для вставки (24 параметри)
            values = (
                cadastral_number,                                         # 1
                row.get('Місцезнаходження оригіналів ДАЗ (договір)'),     # 2
                row.get('Главная организация'),                           # 3
                row.get('Село'),                                          # 4
                row.get('Площадь'),                                       # 5
                row.get('Статус земельного участка'),                     # 6
                is_multi_str,                                             # 7 (Оброблене "Так"/"Ні")
                row.get('Номер'),                                         # 8
                safe_date(row.get('Дата')),                               # 9
                row.get('Термін із документа договір'),                   # 10
                safe_date(row.get('Дата окончания действия')),            # 11
                row.get('Вид договора'),                                  # 12
                row.get('Вид арендодателя'),                              # 13
                row.get('№ дод. угоди'),                                  # 14
                safe_date(row.get('Дата дод. угоди')),                    # 15
                row.get('Термін дод. угоди від дати основного договору'), # 16
                safe_date(row.get('Дата закінчення дод. угоди')),         # 17
                row.get('Вид додаткової угоди'),                          # 18
                # ВИЛУЧЕНО: Термін дод. угоди (років, міс.,днів)
                row.get('Контрагент'),                                    # 19
                str(row.get('ИНН')) if pd.notna(row.get('ИНН')) else None,# 20
                row.get('Кво. паев'),                                     # 21
                safe_date(row.get('Дата регистрации договора')),          # 22
                row.get('Регистрационный номер'),                         # 23
                row.get('Состояние')                                      # 24
            )
            
            cursor.execute(insert_query, (cadastral_number, *values))
            
            if cursor.rowcount > 0:
                records_inserted += 1
            else:
                records_skipped += 1

        conn.commit()
        print("✅ Імпорт завершено успішно!")
        print(f"➕ Додано нових записів: {records_inserted}")
        print(f"⏭️ Пропущено (вже існують): {records_skipped}")

    except pyodbc.Error as db_err:
        print(f"❌ Помилка бази даних: {db_err}")
    except Exception as e:
        print(f"❌ Неочікувана помилка: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    process_and_load_data()