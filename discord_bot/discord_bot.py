import asyncio
import os

import discord
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = str(os.getenv('DISCORD_BOT_TOKEN'))
SERVER_ID = int(os.getenv('DISCORD_SERVER_ID'))
ANNO_CHA = int(os.getenv('DISCORD_ANNOUNCEMENTS_CHANNEL_ID'))
NF_ROLE_ID = int(os.getenv('DISCORD_NF_ROLE_ID'))
MEDIA_PATH = str(os.getenv('MEDIA_PATH'))

intents = discord.Intents.all()
bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    """ Сообщает о рабочей готовности дискорд-бота. """
    print(f'{bot.user} на боевом дежурстве в Discord!')


def build_message(message):
    text = (f'*Докладываю о новом оповещении от командования!*\n{"-" * 50}\n'
            f'**Сервер:** {message.guild}\n'
            f'**Автор сообщения:**  {message.author}\n'
            f'**Канал:** {message.channel}\n'
            f'**Ссылка на сообщение:**  {message.jump_url}\n\n'
            '**Содержание сообщения:**\n'
            f'{message.content}'
            f'\n{"-" * 50}\n*Ниже прикреплены вложения. Доклад окончен!*\n')
    return text


async def download_attachments(message):
    for attachment in message.attachments:
        await attachment.save(attachment.filename)
        await asyncio.sleep(3)


def build_attachments(message):
    attcs_as_files = [
        discord.File(MEDIA_PATH + attc.filename, filename=attc.filename) for
        attc in message.attachments]
    return attcs_as_files


async def remove_files(message):
    for attc in message.attachments:
        print(f'Removing {MEDIA_PATH + attc.filename}')
        try:
            os.unlink(MEDIA_PATH + attc.filename)
        except Exception as e:
            print(e)
        print(f'{MEDIA_PATH + attc.filename} removed')
        await asyncio.sleep(1)


@bot.event
async def on_message(message):
    """ Реакция на событие - новое сообщение в дискорде. """
    attcs = False
    if message.channel.id == ANNO_CHA:
        message_text = build_message(message)

        if message.attachments:
            await download_attachments(message)
            attcs = build_attachments(message)

        guild = bot.get_guild(SERVER_ID)
        for member in guild.members:
            member_roles_ids = [role.id for role in member.roles]
            if NF_ROLE_ID in member_roles_ids:
                print('Юзер найден')
                await asyncio.sleep(3)
                await (member.send(message_text, files=attcs) if attcs
                       else member.send(message_text))

    await remove_files(message)


async def run():
    """ Запускает дискорд-бота. """
    await bot.start(BOT_TOKEN)
