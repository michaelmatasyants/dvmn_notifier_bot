import logging
from telegram.ext import Updater
from handlers import start_handler, checked_handler
from config import load_config


def main():
    '''Main fucntion to run the bot'''
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    config = load_config()
    updater = Updater(token=config.tgbot.token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(checked_handler)
    updater.start_polling()


if __name__=='__main__':
    main()
