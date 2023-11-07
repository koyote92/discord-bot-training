import asyncio

from discord_bot import discord_bot


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(discord_bot.run())
        loop.run_forever()
    except KeyboardInterrupt:
        print('Бот остановлен принудительно.')
    except Exception as e:
        print(e)
