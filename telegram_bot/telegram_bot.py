import os
from dotenv import load_dotenv
from pyrogram import Client, filters


load_dotenv()

TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = Client(
        name='sergeant_bot',
        api_id=TELEGRAM_API_ID,
        api_hash=TELEGRAM_API_HASH,
        bot_token=TELEGRAM_BOT_TOKEN,
    )


@bot.on_message(filters.text & filters.private)
async def echo_message(client, message):
    """ Повторяет написанное пользователем сообщение. """
    await message.reply(message.text)


async def run():
    """ Запускает телеграм-бота. """
    print('SergeantBot на боевом дежурстве в Telegram!')
    await bot.start()


def stop():
    """ Останавливает телеграм-бота. """
    bot.stop()
