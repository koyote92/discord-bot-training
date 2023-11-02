import os

import discord
from dotenv import load_dotenv

from . import responses


load_dotenv()

BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
SERVER_ID = int(os.getenv('DISCORD_SERVER_ID'))
SYS_CHA = int(os.getenv('DISCORD_SYS_CHANNEL'))

bot = discord.Client(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'{bot.user} на боевом дежурстве!')


@bot.event
async def on_message(message):
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


async def send_message(client, message, user_message, is_private):
    try:
        response = responses.handle_response(
            client,
            user_message,
            SERVER_ID,
        )
        await (message.author.send(response) if is_private
               else await message.channel.send(response))
    except TypeError:
        pass
    except Exception as e:
        print(e)


async def run():
    await bot.start(BOT_TOKEN)
