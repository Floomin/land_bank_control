import os
import pyodbc
from dotenv import load_dotenv

# Завантажуємо .env при імпорті модуля
load_dotenv()

def get_connection():
    """Створює та повертає підключення до бази даних MS SQL."""
    SERVER = os.getenv("DB_SERVER")
    DATABASE = os.getenv("DB_NAME")
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")

    if not SERVER or not DATABASE:
        raise ValueError("❌ Налаштування БД (DB_SERVER, DB_NAME) не знайдені в .env")

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
    
    return pyodbc.connect(conn_str)