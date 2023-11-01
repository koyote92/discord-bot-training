import os

import discord
from discord_bot import responses
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
SERVER_ID = int(os.getenv('MY_SERVER_ID'))
SYS_CHA = int(os.getenv('SYS_CHANNEL'))


async def send_message(client, message, user_message, is_private):
    try:
        response = responses.handle_response(client, user_message, SERVER_ID)
        await (message.author.send(response) if is_private
               else await message.channel.send(response))
    except TypeError:
        pass
    except Exception as e:
        print(e)


def run_discord_bot():
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f'{client.user} на боевом дежурстве!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        # message_id = int(message.id)
        # user_presence = str(message.author.status)
        # guild_id = int(message.guild.id)
        # guild_name = str(message.guild.name)

        print(f'{username} сказал: "{user_message}" ({channel})')
        # print(user_presence)
        # print(message.channel.id)
        # print(guild_id, guild_name)

        if message.channel.id == SYS_CHA:
            print('Это важное сообщение')

        if user_message.startswith('!'):
            user_message = user_message[1:]
            await send_message(client, message, user_message, is_private=False)
        elif user_message.startswith('?'):
            user_message = user_message[1:]
            await send_message(client, message, user_message, is_private=True)
            await message.delete()
        else:
            pass

    client.run(BOT_TOKEN)
