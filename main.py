import asyncio
import os
from sys import exit

from dotenv import load_dotenv

from discord_bot import discord_bot


load_dotenv()


DISCORD_ANNOUNCEMENTS_CHANNEL_ID = os.getenv(
    'DISCORD_ANNOUNCEMENTS_CHANNEL_ID'
)
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_ROLE_ID = os.getenv('DISCORD_ROLE_ID')
DISCORD_SERVER_ID = os.getenv('DISCORD_SERVER_ID')
MEDIA_PATH = str(os.getenv('MEDIA_PATH'))


def check_dotenv_variables() -> None:
    """ Проверяет наличие необходимых переменных окружения. """
    dotenv_variables_names = [
        'DISCORD_BOT_TOKEN',
        'DISCORD_SERVER_ID',
        'DISCORD_ANNOUNCEMENTS_CHANNEL_ID',
        'DISCORD_ROLE_ID',
        'MEDIA_PATH',
    ]
    missing_vars = [name for name in dotenv_variables_names
                    if not globals()[name]]
    if missing_vars:
        exit(f'Отсутствуют необходимые переменные: {missing_vars}')

    print('Переменные окружения настроены. Запускаем бота...')


if __name__ == '__main__':
    try:
        check_dotenv_variables()
        loop = asyncio.get_event_loop()
        loop.create_task(discord_bot.run())
        loop.run_forever()
    except KeyboardInterrupt:
        print('Бот остановлен принудительно.')
    except Exception as e:
        print(e)
