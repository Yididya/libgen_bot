'''
Command handlers, MessageHandlers here

'''

from libgen import api
from emoji import emojize
from telegram.parsemode import ParseMode
from telegram import ChatAction


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                    text='Hola amigo, We\'re glad you\'re here\
                    <b>Commands</b> \
                    \n/search -keyword- -- Search books by title', parse_mode=ParseMode.HTML)


def search_or_fetch(bot, update, **args):
    if update.effective_message.text.startswith('/get'): return fetch(bot, update, args)

    search(bot, update, args)

def fetch(bot, update, args):
    md5 = update.effective_message.text[4:]
    url = api.fetch(md5)
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text=url)

def emojize_book_list(books):
    return '\n'.join(map(lambda book: emojize(':blue_book:' + book['title'] + book['author'] + '<a href="/get' + book['md5'] + '">[/get'+ book['md5'] +']</a>') , books))

def search(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    results = api.search(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text=(emojize_book_list(results) if results  else 'Oops, no results found!!'), parse_mode=ParseMode.HTML)

def search_with_out_command(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    results = api.search(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text=(emojize_book_list(results) if results  else 'Oops, no results found!!'), parse_mode=ParseMode.HTML)
