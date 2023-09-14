import argparse
import logging
from time import sleep, time
import requests
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler
from config import load_config
from lexicon import LEXICON


def start_process(update: Update, context: CallbackContext):
    '''Start handler'''
    update.message.reply_text(text=LEXICON['greeting'].format(
                    full_name=update.message.from_user.full_name))


def notify_for_reviews(tg_token: str, chat_id: str, new_attempts):
    '''Sends messages in telegram about recived from dwmn API reviews'''
    updater = Updater(token=tg_token)
    bot = updater.bot
    lesson_title = new_attempts['lesson_title']
    lesson_passed = not new_attempts['is_negative']
    lesson_url = new_attempts['lesson_url']
    if lesson_passed:
        bot.send_message(chat_id=chat_id,
                         text=LEXICON['checked_no_errors'].format(
                             lesson_title)
        )
    else:
        bot.send_message(chat_id=chat_id,
                         text=LEXICON['checked_errors_found'].format(
                             lesson_title=lesson_title,
                             lesson_url=lesson_url)
)


def get_reviews(dvmn_token: str, timestamp: float) -> dict | None:
    '''Uses dvmn api to get reviews with long polling'''
    headers = {'Authorization': dvmn_token}
    payload = {'timestamp': timestamp}
    url = 'https://dvmn.org/api/long_polling/'
    reviews_response = requests.get(url,
                                    headers=headers,
                                    params=payload,
                                    timeout=90)
    reviews_response.raise_for_status()
    return reviews_response.json()


def main():
    '''Main function'''
    parser = argparse.ArgumentParser(
        description='''This script helps to track and check for passed code
                       reviews on dvmn.org. If there are any, the telegram
                       bot sends a message about available code reviews for
                       a particular lesson.
                       To use this script you only need to specify your chat_id
                       for the telegram where you want to get messages.
                       To get your chat_id, send a message to @userinfobot in
                       telegram.'''
    )
    parser.add_argument('chat_id', help='Enter, your chat_id', type=str)
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    config = load_config()
    tg_token = config.tgbot.token
    updater = Updater(token=tg_token)
    start_handler = CommandHandler(command='start', callback=start_process)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(start_handler)
    updater.start_polling()
    last_timestamp = time()

    while True:
        try:
            reviews = get_reviews(dvmn_token=config.dvmn_api.token,
                                  timestamp=last_timestamp)
            last_timestamp = reviews.get('last_attempt_timestamp')
        except requests.exceptions.ConnectionError:
            print('A connection error occurred, the script will try to '
                  'reconnect in 2 minutes.')
            sleep(120)
        except requests.exceptions.HTTPError as http_err:
            print(http_err)
            break
        except requests.exceptions.Timeout:
            last_timestamp = time()
        else:
            notify_for_reviews(tg_token=tg_token,
                               chat_id=args.chat_id,
                               new_attempts=reviews['new_attempts'][0])


if __name__ == '__main__':
    main()
