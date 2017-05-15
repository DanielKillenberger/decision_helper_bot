import json
import os
import random
from telegram.ext import Updater
from telegram.ext import CommandHandler

DIR = os.path.dirname(os.path.abspath(__file__))

config = open(os.path.join(DIR, "telegram_config.json")).read()
config = json.loads(config)
telegram_token = config['telegram_api_token']
updater = Updater(token=telegram_token)
dispatcher = updater.dispatcher


def answer(bot, update, message):
    bot.send_message(chat_id=update.message.chat_id, text=message)


def roll_error_response(bot, update):
    answer(bot, update, 'Without parameters: Ask for a roll between 1-10 \n'
                        'With integer n > 1 as a parameter:\n'
                        'Roll between 1-n')


def roll_response(bot, update, n):
    number = random_roll(1, n)
    answer(bot, update, 'Roll between 1-{n}: {number}'.format(**locals()))


def random_roll(s, n):
    return random.randint(s, n)


def start(bot, update):
    answer(bot, update, 'You can roll random numbers with /roll n where n is an optional integer parameter'
                        ' that has to be larger than 1.\n'
                        'You can choose between N options by entering /choose option1, option2, ... optionN\n')


def roll(bot, update):
    message = update.message.text.replace("/roll", "").strip()
    if len(message) > 0:
        try:
            n = int(message)
        except ValueError as err:
            roll_error_response(bot, update)
        if n < 2:
            roll_error_response(bot, update)
        else:
            roll_response(bot, update, n)
    else:
        roll_response(bot, update, 10)


def choose(bot, update):
    message = update.message.text.replace("/choose", "").replace(" ", "").strip()

    if len(message) > 0:
        choices = message.split(',')
        i = random_roll(0, len(choices)-1)
        response = "Choices: \n"
        for choice in choices:
            response += '{choice} \n'.format(**locals())

        choice = choices[i]
        response += '\nI have chosen the following: {choice}'.format(**locals())
        answer(bot, update, response)
    else:
        answer(bot, update, 'You need to add choices separated by commas')


start_handler = CommandHandler('start', start)
roll_handler = CommandHandler('roll', roll)
choose_handler = CommandHandler('choose', choose)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(roll_handler)
dispatcher.add_handler(choose_handler)

updater.start_polling()
