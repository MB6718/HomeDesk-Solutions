import os

class Config():
	""" получаем переменные окружения из .env файла проекта """
	PYTHONPATH = os.getenv('PYTHONPATH', 'src')
	DB_FILE = os.getenv('DB_FILE', 'database.db')
	SECRET_KEY = os.getenv('SECRET_KEY', 'topsecretkey').encode()
