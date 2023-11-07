import asyncio
import os
from sys import exit

import discord
from dotenv import load_dotenv


load_dotenv()


ANNO_CHA = int(os.getenv('DISCORD_ANNOUNCEMENTS_CHANNEL_ID'))
BOT_TOKEN = str(os.getenv('DISCORD_BOT_TOKEN'))
MEDIA_PATH = str(os.getenv('MEDIA_PATH'))
ROLE_ID = int(os.getenv('DISCORD_ROLE_ID'))
SERVER_ID = int(os.getenv('DISCORD_SERVER_ID'))


intents = discord.Intents.all()
bot = discord.Client(intents=intents)


def check_dotenv_variables() -> None:
    """ Проверяет наличие необходимых переменных окружения. """
    dotenv_variables_names = [
        'ANNO_CHA',
        'BOT_TOKEN',
        'MEDIA_PATH',
        'ROLE_ID',
        'SERVER_ID',
    ]
    missing_vars = [name for name in dotenv_variables_names
                    if not globals()[name]]
    if missing_vars:
        exit(f'Отсутствуют необходимые переменные: {missing_vars}')

    print('Переменные окружения настроены. Запускаем бота...')


def build_message(message: discord.Message) -> str:
    """ Строим текст сообщения. """
    dummy_str = 'Сообщение не содержит текста.'
    text = (f'*Докладываю о новом оповещении от командования!*\n{"-" * 50}\n'
            f'**Сервер:** {message.guild}\n'
            f'**Канал:** {message.channel}\n'
            f'**Автор сообщения:**  {message.author}\n'
            f'**Ссылка на сообщение:**  {message.jump_url}\n\n'
            '**Содержание сообщения:**\n'
            f'{message.content if message.content else dummy_str}')
    if message.attachments:
        text += f'\n{"-" * 50}\n*Ниже прикреплены вложения. Доклад окончен!*'
    else:
        text += f'\n{"-" * 50}\n*Доклад окончен!*'
    return text


async def download_attachments(message: discord.Message) -> None:
    """Скачиваем прикреплённые файлы из сообщения. """
    for attachment in message.attachments:
        await attachment.save(attachment.filename)
        print(f'Файл {attachment.filename} загружен.')
        await asyncio.sleep(3)


def build_attachments(message: discord.Message) -> list[discord.File]:
    """ Собираем файлы для отправки в ЛС. """
    print('Начинаем билдить...')
    attcs_as_files = list()
    with attcs_as_files:
        for attc in message.attachments:
            print(attc)
            try:
                with discord.File(
                    MEDIA_PATH + attc.filename,
                    filename=attc.filename,
                ) as file:
                    attcs_as_files.append(file)
            except Exception as e:
                print(e)
    return attcs_as_files


def remove_files(message: discord.Message) -> None:
    """ Удаляем загруженные медиа-файлы. """
    for attachment in message.attachments:
        os.unlink(MEDIA_PATH + attachment.filename)
        print(f'Файл {attachment.filename} удалён.')


@bot.event
async def on_ready() -> None:
    """ Сообщает о рабочей готовности дискорд-бота. """
    print(f'{bot.user} на боевом дежурстве в Discord!')


@bot.event
async def on_message(message: discord.Message, attcs=None) -> None:

    if message.channel.id != ANNO_CHA:
        return

    print(f'Новое сообщение в #{message.channel.name} '
          f'от {message.author.name}')
    message_text = build_message(message)

    if message.attachments:
        print(f'Сообщение содержит вложения: {len(message.attachments)}')
        await download_attachments(message)
        attcs = build_attachments(message)

    guild = bot.get_guild(SERVER_ID)
    with attcs:
        for member in guild.members:
            member_roles_ids = [role.id for role in member.roles]
            if ROLE_ID in member_roles_ids:
                print(f'{ROLE_ID}: {member_roles_ids}')
                await asyncio.sleep(3)
                try:
                    await (
                        member.send(message_text, files=attcs) if attcs
                        else member.send(message_text)
                    )
                except Exception as e:
                    print(e)
                print(f'Сообщение отправлено для {member.name}')
    remove_files(message)


async def run() -> None:
    """ Запускает дискорд-бота. """
    check_dotenv_variables()
    await bot.start(BOT_TOKEN)
