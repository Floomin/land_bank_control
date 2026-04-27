import os
from typing import Tuple


def load_options(filename: str) -> list:
    """Завантажує список варіантів з текстового файлу в папці data/options."""
    path = os.path.join("data", "options", filename)
    if not os.path.exists(path):
        return ["Файл не знайдено"]
    with open(path, "r", encoding="utf-8") as f:
        # Читаємо рядки, прибираємо зайві пробіли та порожні рядки
        return [line.strip() for line in f.readlines() if line.strip()]


def convert_years_to_ymd(years_float: float) -> Tuple[int, int, int]:
    """
    Преобразует число лет с дробью (например 10.7427) в годы, месяцы и дни.
    Используется средняя длина месяца ≈ 30.436875 дней (учитывает високосные годы).
    Параметры:
    years_float (float): количество лет с дробной частью, например 10.7427
    Возвращает:
    (years, months, days)
    """
    if years_float < 0:
        raise ValueError("Число лет не может быть отрицательным")
    years = int(years_float)
    frac_year = years_float - years
    months = int(frac_year * 12)
    frac_month = frac_year * 12 - months
    days = round(frac_month * 30.436875)
    return years, months, days
