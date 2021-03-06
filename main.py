import requests
import logging
import datetime
import telegram
import time
from argparse import ArgumentParser

import common
from database.models import EventDateTime, Event
from bs4 import BeautifulSoup, Tag
from database.base import create_all
from database import dal

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(common.APP_NAME)
url = "https://www.kotar-rishon-lezion.org.il/events-category/%D7%90%D7%99%D7%A8%D7%95%D7%A2%D7%99%D7%9D-%D7%95%D7%A4%D7%A2%D7%99%D7%9C%D7%99%D7%95%D7%AA/%D7%9B%D7%95%D7%AA%D7%A8-%D7%98%D7%A3-%D7%94%D7%A6%D7%92%D7%95%D7%AA/"
headers = {
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

create_all()

if common.TELEGRAM_TOKEN is None:
    bot = None
    logger.error("Telegram bot is unavailable, please make sure you set the TELEGRAM_TOKEN variable")
else:
    bot = telegram.Bot(token=common.TELEGRAM_TOKEN)


def send_bot(message):
    if bot is not None:
        bot.send_message(chat_id=common.TELEGRAM_CHAT_ID,
                         text=message, parse_mode=telegram.ParseMode.HTML)
    else:
        logger.warning("No Bot Available: {}".format(message))


def sleep(seconds):
    logger.debug("Waiting for {} seconds".format(seconds))
    time.sleep(seconds)


def get_time(event: Tag) -> EventDateTime:
    event_date_time = None

    detail_div = event.find("div", {"class": "detail"})
    if detail_div is not None:
        time_div = detail_div.find("div", {"class": "text"})
        if time_div is not None:
            parts = time_div.text.split("|")
            if len(parts) == 2:
                time_parts = parts[0].strip().split("-")
                start_time = datetime.datetime.strptime("{} {}".format(parts[1].strip(), time_parts[0].strip()),
                                                        "%d.%m.%Y %H:%M")
                end_time = datetime.datetime.strptime("{} {}".format(parts[1].strip(), time_parts[1].strip()),
                                                      "%d.%m.%Y %H:%M")
                event_date_time = EventDateTime(start_time=start_time, end_time=end_time)

    return event_date_time


def get_tickets(i_event_name=None):
    available_tickets = []
    try:
        logger.info("searching for tickets for {}".format(i_event_name if i_event_name is not None else "all events"))
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        events = [x for x in soup.find_all("div", class_="event") if
                  'class' in x.attrs and len(x.attrs['class']) == 1]
        logger.info("Found {} events".format(len(events)))

        for event in events:
            event_name = None
            event_header = event.find("h2")
            if event_header:
                event_name = event_header.text
            else:
                logger.error("Error! unable to get event header")

            if "????????" not in event_name:
                logger.info("Tickets available for {}".format(event_name))
                if i_event_name is None or i_event_name in event_name:
                    event_data = Event(name=event_name, url=url, time=get_time(event))
                    available_tickets.append(event_data)
                    if not dal.event_exists(event_data):
                        logger.info(str(event_data))
                        send_bot(str(event_data))
                        logger.info("Event '{}' found".format(event_data.name))
                        dal.add_event(event_data)
                    else:
                        logger.info("Event {} already notified".format(event_name))
            else:
                logger.info("No tickets: {}".format(event_name))
    except Exception as ex:
        logger.error("Error! {}".format(str(ex)))
        send_bot("Error! {}".format(str(ex)))
        raise ex
    return available_tickets


def app_loop(event_name=None, iterations=-1, wait_period=300):
    if iterations < 1:
        counter = 1
        while True:
            logger.info("Running iteration #{}".format(counter))
            get_tickets(event_name)
            counter += 1
            sleep(wait_period)
    else:
        for i in range(iterations):
            if i > 0:
                sleep(wait_period)
            logger.info("Running iteration #{}".format(i + 1))
            get_tickets(event_name)


def main():
    arg_parser = ArgumentParser(description="Kotar Events Checker")
    arg_parser.add_argument("--iterations", type=int, help="The number of iterations to run", default=1)
    arg_parser.add_argument("--wait_period", type=int, help="How many seconds to wait between attempts", default=300)
    arg_parser.add_argument("--event_name", type=str, help="The name of the event", default=None)
    parsed = arg_parser.parse_args()
    app_loop(**vars(parsed))


if __name__ == '__main__':
    main()
