import os
import time
import logging.config
import requests
import telegram
from dotenv import load_dotenv

load_dotenv()
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('apiLogger')

PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
API_URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
bot = telegram.Bot(token=TELEGRAM_TOKEN)


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    status = homework.get('status')
    if homework_name is None or status is None:
        logger.error(f'Invalid server response: {homework}')
        return 'Invalid server response'
    if status == 'rejected':
        verdict = ('Unfortunately, homework was not accepted this time.'
                   'Not great, not terrible.')
    else:
        verdict = ('Everything all right, '
                   'good job, switch to the next task!')
    return f'Homework "{homework_name}" was checked!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    current_timestamp = current_timestamp or int(time.time())
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    params = {'from_date': current_timestamp}
    try:
        homework_statuses = requests.get(API_URL, headers=headers,
                                         params=params)
        return homework_statuses.json()
    except Exception as err:
        logger.error(err)
        return {}


def send_message(message):
    return bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    current_timestamp = int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(new_homework.get
                                                   ('homeworks')[0]))
            current_timestamp = new_homework.get('current_date')
            time.sleep(1200)

        except Exception as err:
            print(f'Bot failed with error: {err}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
