import os

PROJECT_NAME = os.environ.get('PROJECT_NAME')
DB_URL = os.environ.get('DATABASE_URL')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMINS = os.environ.get('ADMINS').split(',')

WEBHOOK_HOST = f"https://{PROJECT_NAME}.herokuapp.com"
WEBHOOK_PATH = '/webhook/' + BOT_TOKEN
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'


