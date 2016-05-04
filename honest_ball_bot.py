#!/usr/bin/python
"""telegram bot to send a magic 8 ball answers"""

import sys
import json
from random import randint

import telegram
from telegram.ext import Updater, CommandHandler

with open('config.json', 'r') as f:
    config = json.load(f)

if 'telegram_bot' not in config:
    print('err: "telegram_bot" config section must be specified')
    sys.exit(1)

tg_bot = config['telegram_bot']

if 'token' not in tg_bot:
    print('err: telegram TOKEN must be specified')
    sys.exit(1)

if 'answers' not in config:
    print('err: "answers" config section must be specified')
    sys.exit(1)

ans = config['answers']
ans_max_idx = len(ans) - 1


def start(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text="Hi, %s!" % update.message.from_user.first_name
    )


def ask(bot, update):
    try:
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text='%s _%s_' % (
                telegram.Emoji.CRYSTAL_BALL,
                ans[randint(0, ans_max_idx)]
            ),
            parse_mode=telegram.ParseMode.MARKDOWN
        )
    except:
        print('error: ', sys.exc_info()[0])
        sys.exit(1)


updater = Updater(token=tg_bot['token'])
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.addHandler(start_handler)

word_handler = CommandHandler('ask', ask)
dispatcher.addHandler(word_handler)

updater.start_polling()
