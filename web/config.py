import os


class ConfigBase:
    # Определяет, включен ли режим отладки
    # В случае если включен, flask будет показывать
    # подробную отладочную информацию. Если выключен -
    # - 500 ошибку без какой либо дополнительной информации.
    DEBUG = True
    # Включение защиты против "Cross-site Request Forgery (CSRF)"
    CSRF_ENABLED = True
    # Случайный ключ, которые будет использоваться для подписи
    # данных, например cookies.
    SECRET_KEY = os.environ.get('FLASK_SECRET') or "PyQuest2"


class ProductionConfig(ConfigBase):
    DEBUG = False


class DevelopmentConfig(ConfigBase):
    DEVELOPMENT = True
    DEBUG = True
