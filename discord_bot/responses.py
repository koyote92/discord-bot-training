import random

from service import texts


def handle_response(client, message, server_id) -> str:
    p_message = message.lower()

    if p_message in texts.greetings:
        return 'Здорова, боец!'

    elif p_message == 'кубы':
        dices = str(random.randint(1, 6))
        return f'На кубиках выпало {dices}, солдат.'

    elif p_message == 'помощь':
        return texts.help_text

    elif p_message == 'перекличка':
        guild = client.get_guild(server_id)
        playing_members = dict()

        for member in guild.members:
            if member.activity:
                playing_members[member.name] = member.activity.name

        if playing_members:
            separator = '-' * 50
            roll_call = 'Начинаю перекличку!\n'
            roll_call += separator
            roll_call += '\nБойцы играют в:\n\n'
            players_count_by_game = dict()
            for k, v in sorted(playing_members.items()):
                roll_call += f'{k}: {v}\n'
                players_count_by_game[v] = players_count_by_game.get(v, 0) + 1
            roll_call += separator
            roll_call += '\nКоличество игроков в играх:\n\n'
            for k, v in sorted(players_count_by_game.items()):
                roll_call += f'{k}: {v}\n'
            roll_call += separator
            roll_call += '\nПерекличка окончена, старшой!'
            return roll_call

        return 'Никакой активности, старшой.'

    else:
        pass
