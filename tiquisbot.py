#!/usr/bin/env python3
import requests
import json
import datetime
import logging
import time, sys
import os
import re
import telegram
from threading import Thread
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def hola(update, context):
    """Send a message when the command /start is issued."""
    #update.message.reply_text('Hi!')
    bot_welcome = """Hola, {} sóc en <b> Tiquismiquis Bot</b>,
    I em faré càrrec de traduïr els missatges que interpreto d'aquest grup.
    """.format(update.message.from_user.first_name)
    xatid = update.message.chat.id
    context.bot.send_message(chat_id=xatid,text=bot_welcome,parse_mode='html')
    #update.message.reply_html(bot_welcome)

def start(update, context):
    """Send a message when the command /start is issued."""
    #update.message.reply_text('Hi!')
    bot_welcome = """Benvingut sóc el <b> Bot Tiquismiquis </b>,
    creat per XXXX.
    Aquest bot es farà càrrec de traduïr-vos els missatges que interpreta d'aquest grup.
    """
    xatid = update.message.chat.id
    context.bot.send_message(chat_id=xatid,text=bot_welcome,parse_mode='html')
    #update.message.reply_html(bot_welcome)

def options(update, context):
    """Send a message when the command /start is issued."""
    #update.message.reply_text('Hi!')
    keyboard = [[InlineKeyboardButton("Estat del sistema", callback_data='3')],
                [InlineKeyboardButton("Temps en marxa", callback_data='1')],
                 [InlineKeyboardButton("Usuaris actius", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Aquestes són les opcions disponibles, trieu una si us plau:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    logger.warning('Opció escollida: "%s" ', query.data)
    logger.warning(update)
    logger.warning(query)

    query.edit_message_text(text="Opció triada: {}".format(query.data))

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    if update.message.chat.type == "group":
        update.message.reply_text(str(update.message.from_user.first_name) + " : ... " + re.sub("[aeiouAEIOUàáèéìíòóùúïäëöü]", "i", update.message.text) + " ... ")
    else:
        update.message.reply_text(str(update.message.chat.first_name) + " : ... " + re.sub("[aeiouAEIOUàáèéìíòóùúïäëöü]", "i", update.message.text) + " ... ")
    #update.message.reply_text(str(update.message.chat.first_name) + " : ... " + str(update.message.text) + " ... ")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def envia_msg(update, context):
    logger.warning('Enviarem un missatge?')
    logger.warning(update)
    try:
        xatid = context.args[0]
        missatge = str(context.args[1])
        context.bot.send_message(chat_id=xatid, text=missatge)
    except (IndexError, ValueError):
        context.bot.send_message('Alguna cosa falla') 

def sum(update, context):
    try:
        number1 = int(context.args[0])
        number2 = int(context.args[1])
        result = number1+number2
        update.message.reply_text('La suma és: '+str(result))
    except (IndexError, ValueError):
        update.message.reply_text('Falten nombres')    

#Variables para el Token y la URL del chatbot

TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"   #Aquí va el token del bot creat
URL = "https://api.telegram.org/bot" + TOKEN + "/"

def main():

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        updater.stop()
        #os.execl(sys.executable, sys.executable, *sys.argv)
        #os.execl('/bin/bash', 'bash','bot_start.sh')

    def restart(update, context):
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()

    def myid(update, context):
        update.message.reply_text(' El teu nom és: ' + update.message.from_user.first_name)
        update.message.reply_text(' El teu id és: ' + str(update.message.from_user.id))
    
    def chatid(update, context):
        update.message.reply_text(' El id és: ' + str(update.message.chat.id))
        update.message.reply_text(' El nom del grup és: ' + update.message.chat.title)

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("hola", hola))
    #dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("echo", echo))
    #dp.add_handler(CommandHandler("options", options))
    dp.add_handler(CommandHandler("myid", myid))
    dp.add_handler(CommandHandler("chatid", chatid))
    dp.add_handler(CommandHandler("envia_msg", envia_msg))
    dp.add_handler(CommandHandler("sum", sum))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('r', restart, filters=Filters.user(username='@usuari')))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        bot = telegram.Bot(token=TOKEN)
        bot.sendMessage(chat_id=sys.argv[1], text=sys.argv[2])
        #r=requests.post(URL+'sendMessage', data={'chat_id': , 'text': })
        #data = json.loads(r.text)
        #print(data)
    else:
        main()


 
 
