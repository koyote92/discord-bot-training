import os

import discord
from dotenv import load_dotenv

from service import texts
from .responses import handle_response  # какая-то проблема с импортом


load_dotenv()

BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
SERVER_ID = int(os.getenv('DISCORD_SERVER_ID'))
SYS_CHA = int(os.getenv('DISCORD_SYS_CHANNEL'))

bot = discord.Client(intents=discord.Intents.all())


@bot.event
async def on_ready():
    """ Сообщает о рабочей готовности дискорд-бота. """
    print(f'{bot.user} на боевом дежурстве в Discord!')


@bot.event
async def on_message(message):
    """ Реакция на событие - новое сообщение в дискорде. """
    if message.author == bot.user:
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f'{username} сказал: "{user_message}" ({channel})')

    if message.channel.id == SYS_CHA:
        print('Это важное сообщение!')

    if user_message.startswith('!'):
        user_message = user_message[1:]
        await send_message(bot, message, user_message, is_private=False)
    elif user_message.startswith('?'):
        user_message = user_message[1:]
        await send_message(bot, message, user_message, is_private=True)
        await message.delete()
    elif user_message in texts.greetings:
        await send_message(bot, message, user_message, is_private=False)


async def send_message(client, message, user_message, is_private):
    """ Обрабатывает сообщение в зависимости от символа перед сообщением. """
    try:
        response = handle_response(
            client,
            user_message,
            SERVER_ID,
        )
        (await message.author.send(response) if is_private
         else await message.channel.send(response))
    except TypeError:
        pass
    except Exception as e:
        print(e)


async def run():
    """ Запускает дискорд-бота. """
    await bot.start(BOT_TOKEN)
