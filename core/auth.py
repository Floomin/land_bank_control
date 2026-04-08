from config import settings


def authenticate(username, password):
    """
    Проверяет связку логин/пароль.
    Пока используем простую проверку из .env.
    """
    if username == settings.APP_ADMIN_USER and password == settings.APP_ADMIN_PASS:
        return True
    return False
