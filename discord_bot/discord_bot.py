import asyncio
import os

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


@bot.event
async def on_ready() -> None:
    """ Сообщает о рабочей готовности дискорд-бота. """
    print(f'{bot.user} на боевом дежурстве в Discord!')


def build_message(message: discord.Message) -> str:
    """ Строим текст сообщения. """
    text = (f'*Докладываю о новом оповещении от командования!*\n{"-" * 50}\n'
            f'**Сервер:** {message.guild}\n'
            f'**Автор сообщения:**  {message.author}\n'
            f'**Канал:** {message.channel}\n'
            f'**Ссылка на сообщение:**  {message.jump_url}\n\n'
            '**Содержание сообщения:**\n'
            f'{message.content}')
    if message.attachments:
        text += f'\n{"-" * 50}\n*Ниже прикреплены вложения. Доклад окончен!*'
    else:
        text += f'\n{"-" * 50}\n*Доклад окончен!*'
    return text


async def download_attachments(message: discord.Message) -> None:
    """Скачиваем прикреплённые файлы из сообщения. """
    for attachment in message.attachments:
        await attachment.save(attachment.filename)
        await asyncio.sleep(3)


def build_attachments(message: discord.Message) -> list[discord.File]:
    """ Собираем файлы для отправки в ЛС. """
    attcs_as_files = [
        discord.File(MEDIA_PATH + attc.filename, filename=attc.filename) for
        attc in message.attachments]
    return attcs_as_files


def remove_files(message: discord.Message) -> None:
    """ Удаляем загруженные медиа-файлы. """
    for attc in message.attachments:
        print(f'Удаляем {attc.filename} ...')
        os.unlink(MEDIA_PATH + attc.filename)
        print(f'Файл {MEDIA_PATH + attc.filename} удалён.')


@bot.event
async def on_message(message: discord.Message,
                     attcs: None | list[discord.File] = None) -> None:
    """ Реакция на событие - новое сообщение в дискорде. """
    if message.channel.id == ANNO_CHA:
        message_text = build_message(message)

        if message.attachments:
            await download_attachments(message)
            attcs = build_attachments(message)

        guild = bot.get_guild(SERVER_ID)
        for member in guild.members:
            member_roles_ids = [role.id for role in member.roles]
            if ROLE_ID in member_roles_ids:
                await asyncio.sleep(3)
                await (member.send(message_text, files=attcs) if attcs
                       else member.send(message_text))

    remove_files(message)


async def run() -> None:
    """ Запускает дискорд-бота. """
    await bot.start(BOT_TOKEN)
