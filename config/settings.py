import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

# Настройки БД
DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_NAME = os.getenv("DB_NAME", "LandBankControl")
DB_USER = os.getenv("DB_USER", "lbc_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Настройки авторизации
APP_ADMIN_USER = os.getenv("APP_ADMIN_USER", "admin")
APP_ADMIN_PASS = os.getenv("APP_ADMIN_PASS", "admin")
