# !/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
from calculation_class import Calculations
from log_class import Logger as func_logger
from game.game import BossPuzzle

from setup import PROXY, TOKEN
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler,\
    Filters, MessageHandler, Updater

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s'
                           ' - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

log = func_logger()

# Define a few command handlers.
# These usually take the two arguments update and
# context. Error handlers also
# receive the raised TelegramError object in error.


@log.log_func
def corona_stats_dynamics(update: Update, context: CallbackContext):
    update.message.reply_text(
        Calculations.corona_stats_dynamics(update.message.text))


@log.log_func
def game(update: Update, context: CallbackContext):
    # TODO: переделать получение команд для игры
    puzzle.start_new_game()
    update.message.reply_text(puzzle.get_board()+'\n'
                              + 'Game has started' + '\n'

                              + 'Type:"game: *coordinates*'
                                ' *coordinates of free cell*" to play')


def gamesetup():
    global puzzle
    puzzle = BossPuzzle()
    global game_status
    game_status = False


@log.log_func
def corono_stats(update: Update, context: CallbackContext):
    update.message.reply_text(
        Calculations.get_msg_for_corona(update.message.text))


@log.log_func
def weather(update: Update, context: CallbackContext):
    update.message.reply_text(Calculations.get_weather())


@log.log_func
def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Привет, {update.effective_user.first_name}!')


@log.log_func
def horoscope(update: Update, context: CallbackContext):
    update.message.reply_text(
        Calculations.get_horoscope(update.message.text))

@log.log_func
def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    msg = 'Here is what you can do\n' \
          '/start to start\n' \
          '/weather to view weather\n' \
          '/game to play the 15-Puzzle\n' \
          '/horo *your zodiac sign* to view horoscope' \
          '/fact to get cat fact\n' \
          '/corona_stats *date* to view latest corona-virus' \
          ' statistic(for all the time)\n' \
          '/corona_dynamics *date* to view latest corona-virus dynamics\n'
    update.message.reply_text(msg)


@log.log_func
def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    if update.message.text[:6] == 'game: ':
        try:
            if puzzle.action(update.message.text[6:]):
                message = puzzle.get_board()
                update.message.reply_text(puzzle.get_board())
                if puzzle.board.check_for_solving():
                    message += '\n SOLVED!'
            else:
                update.message.reply_text('Wrong command format \nTry again')
        except BaseException:
            update.message.reply_text('First start a game')
    else:
        update.message.reply_text(
            Calculations.print_poem(update.message.text))


@log.log_func
def chat_history(update: Update, context: CallbackContext):
    update.message.reply_text(log.last_5_history(update))


@log.log_func
def fact(update: Update, context: CallbackContext):
    update.message.reply_text(Calculations.get_cat_fact())


@log.log_func
def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


def main():
    bot = Bot(
        token=TOKEN,
        base_url=PROXY,  # delete it if connection via VPN
    )
    updater = Updater(bot=bot, use_context=True)
    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))
    updater.dispatcher.add_handler(CommandHandler('history', chat_history))
    updater.dispatcher.add_handler(CommandHandler('fact', fact))
    updater.dispatcher.add_handler(CommandHandler
                                   ('corona_stats', corono_stats))
    updater.dispatcher.add_handler(CommandHandler('weather', weather))
    updater.dispatcher.add_handler(CommandHandler
                                   ('corona_dynamics', corona_stats_dynamics))
    updater.dispatcher.add_handler(CommandHandler('game', game))
    updater.dispatcher.add_handler(CommandHandler('horo', horoscope))
    gamesetup()
    # on noncommand i.e message - echo the message on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    updater.dispatcher.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()
