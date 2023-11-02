import asyncio
import os
from sys import exit

from dotenv import load_dotenv

from discord_bot import discord_bot
from telegram_bot import telegram_bot


load_dotenv()

DISCORD_APPLICATION_ID = os.getenv('DISCORD_APPLICATION_ID')
DISCORD_PUBLIC_KEY = os.getenv('DISCORD_PUBLIC_KEY')
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_LINK = os.getenv('DISCORD_LINK')
DISCORD_SERVER_ID = os.getenv('DISCORD_SERVER_ID')
DISCORD_SYS_CHANNEL = os.getenv('DISCORD_SYS_CHANNEL')
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


def check_dotenv_variables():
    dotenv_variables_names = [
        'DISCORD_APPLICATION_ID',
        'DISCORD_PUBLIC_KEY',
        'DISCORD_CLIENT_SECRET',
        'DISCORD_BOT_TOKEN',
        'DISCORD_LINK',
        'DISCORD_SERVER_ID',
        'DISCORD_SYS_CHANNEL',
        'TELEGRAM_API_ID',
        'TELEGRAM_API_HASH',
        'TELEGRAM_BOT_TOKEN',
    ]
    missing_vars = [name for name in dotenv_variables_names
                    if not globals()[name]]
    if missing_vars:
        exit(f'Отсутствуют необходимые переменные: {missing_vars}')

    print('Переменные окружения настроены. Запускаем бота...')


if __name__ == '__main__':
    check_dotenv_variables()
    loop = asyncio.get_event_loop()
    loop.create_task(discord_bot.run())
    loop.create_task(telegram_bot.run())
    loop.run_forever()
