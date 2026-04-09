import os


def load_options(filename: str) -> list:
    """Завантажує список варіантів з текстового файлу в папці data/options."""
    path = os.path.join("data", "options", filename)
    if not os.path.exists(path):
        return ["Файл не знайдено"]
    with open(path, "r", encoding="utf-8") as f:
        # Читаємо рядки, прибираємо зайві пробіли та порожні рядки
        return [line.strip() for line in f.readlines() if line.strip()]
