import pandas as pd
import pyodbc
import numpy as np
import os
from dotenv import load_dotenv

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
        df = pd.read_excel(excel_path, sheet_name='data', dtype=str)
    except Exception as e:
        print(f"❌ Помилка читання Excel файлу: {e}")
        return
    
    df = df.dropna(subset=['Кадастровый номер'])
    
    # ---------------------------------------------------------
    # БРОНЕБІЙНІ ФУНКЦІЇ ОЧИЩЕННЯ ДАНИХ
    # ---------------------------------------------------------
    def clean_val(val):
        """Універсальна функція для очищення тексту від сміття."""
        if pd.isna(val) or val is None:
            return None
        val_str = str(val).strip()
        if val_str.lower() in ("", "nan", "none", "null", "<na>", "nat"):
            return None
        # Якщо Pandas додав .0 до номера договору чи ІНН, прибираємо його
        if val_str.endswith('.0'):
            val_str = val_str[:-2]
        return val_str

    def safe_date(date_val):
        val = clean_val(date_val)
        if not val:
            return None
        try:
            return pd.to_datetime(val, dayfirst=True).strftime('%Y-%m-%d')
        except Exception:
            return None

    def safe_decimal(val):
        """Перетворює на число і форматує як рядок з 4 знаками, щоб уникнути помилки масштабу в SQL."""
        v = clean_val(val)
        if not v:
            return None
        try:
            f_val = float(v.replace(',', '.'))
            return f"{f_val:.4f}"
        except ValueError:
            return None

    print("⚙️ Підключення до бази даних...")
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
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
            cadastral_number = clean_val(row['Кадастровый номер'])
            if not cadastral_number:
                continue
                
            # Очищуємо ключі словника від пробілів
            row_dict = {str(k).strip(): v for k, v in row.items()}
            
            # Обробка багатостороннього договору
            multi_raw = clean_val(row_dict.get('Багатосторонній договір'))
            is_multi_str = "Так" if multi_raw else "Ні"
            
            # Всі поля пропускаємо через clean_val, safe_date або safe_decimal
            values = (
                cadastral_number,                                         # 1
                clean_val(row_dict.get('Місцезнаходження оригіналів ДАЗ (договір)')), # 2
                clean_val(row_dict.get('Главная организация')),           # 3
                clean_val(row_dict.get('Село')),                          # 4
                safe_decimal(row_dict.get('Площадь')),                    # 5 (Ідеально відформатовано)
                clean_val(row_dict.get('Статус земельного участка')),     # 6
                is_multi_str,                                             # 7
                clean_val(row_dict.get('Номер')),                         # 8
                safe_date(row_dict.get('Дата')),                          # 9
                safe_decimal(row_dict.get('Термін із документа договір')),# 10
                safe_date(row_dict.get('Дата окончания действия')),       # 11
                clean_val(row_dict.get('Вид договора')),                  # 12
                clean_val(row_dict.get('Вид арендодателя')),              # 13
                clean_val(row_dict.get('№ дод. угоди')),                  # 14
                safe_date(row_dict.get('Дата дод. угоди')),               # 15
                safe_decimal(row_dict.get('Термін дод. угоди від дати основного договору')), # 16
                safe_date(row_dict.get('Дата закінчення дод. угоди')),    # 17
                clean_val(row_dict.get('Вид додаткової угоди')),          # 18
                clean_val(row_dict.get('Контрагент')),                    # 19
                clean_val(row_dict.get('ИНН')),                           # 20 (Без зайвих .0)
                clean_val(row_dict.get('Кво. паев')),                     # 21
                safe_date(row_dict.get('Дата регистрации договору')) or safe_date(row_dict.get('Дата регистрации договора')), # 22
                clean_val(row_dict.get('Регистрационный номер')) or clean_val(row_dict.get('№ реєстрації')) or clean_val(row_dict.get('Реєстраційний номер')), # 23
                clean_val(row_dict.get('Состояние'))                      # 24
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