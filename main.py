import logging
from time import sleep, time

import requests
from environs import Env
from telegram.ext import Updater

from lexicon import LEXICON


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


logger = logging.getLogger(__file__)


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
                             lesson_title))
    else:
        bot.send_message(chat_id=chat_id,
                         text=LEXICON['checked_errors_found'].format(
                             lesson_title=lesson_title,
                             lesson_url=lesson_url))


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
    env = Env()
    env.read_env()
    tg_token = env.str('TG_BOT_TOKEN')
    bot = Updater(token=tg_token).bot
    logging.basicConfig(
        format='%(asctime)s - %(pathname)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot=bot,
                                          chat_id=env.str('TG_ADMIN_CHAT_ID')))
    last_timestamp = time()

    logger.info('Bot started')
    while True:
        try:
            reviews = get_reviews(dvmn_token=f"Token {env('DVMN_API_TOKEN')}",
                                  timestamp=last_timestamp)
            if reviews['status'] == 'timeout':
                last_timestamp = reviews['timestamp_to_request']
                continue
            last_timestamp = reviews['last_attempt_timestamp']
            logger.info('Got a new review')
            notify_for_reviews(tg_token=tg_token,
                               chat_id=env.str('TG_CHAT_ID'),
                               new_attempts=reviews['new_attempts'][0])
            logger.info('Sent fetched review')
        except requests.exceptions.ConnectionError:
            logger.exception(
                'A connection error occurred, the script will try to'
                ' reconnect in 2 minutes.')
            sleep(120)
        except requests.exceptions.HTTPError as http_err:
            logger.exception(http_err)
            break
        except requests.exceptions.Timeout:
            last_timestamp = time()


if __name__ == '__main__':
    main()
