import requests
import time
import logging
import datetime
import telegram
from common import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from models import EventDateTime, Event
from bs4 import BeautifulSoup, Tag

bot = telegram.Bot(token=TELEGRAM_TOKEN)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def get_time(event: Tag) -> EventDateTime:
    event_date_time = None

    detail_div = event.find("div", {"class": "detail"})
    if detail_div is not None:
        time_div = detail_div.find("div", {"class": "text"})
        if time_div is not None:
            parts = time_div.text.split("|")
            if len(parts) == 2:
                time_parts = parts[0].strip().split("-")

                event_date_time = EventDateTime(start_time=time_parts[0].strip(),
                                                end_time=time_parts[1].strip(),
                                                date=datetime.datetime.strptime(parts[1].strip(), "%d.%m.%Y"))

    return event_date_time


def has_tickets(event_name_part=None):
    url = "https://www.kotar-rishon-lezion.org.il/events-category/%D7%90%D7%99%D7%A8%D7%95%D7%A2%D7%99%D7%9D-%D7%95%D7%A4%D7%A2%D7%99%D7%9C%D7%99%D7%95%D7%AA/%D7%9B%D7%95%D7%AA%D7%A8-%D7%98%D7%A3-%D7%94%D7%A6%D7%92%D7%95%D7%AA/"
    headers = {
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    # while True:
    #     print("Checking")
    #
    #     events_h2 = soup.find_all("h2")
    #     for h2 in events_h2:
    #         if "אזלו"
    #         print(h2)
    #     print("Debugging")
    sold_out = True
    try:
        attempts = 1
        max_attempts = 200000
        while sold_out and attempts < max_attempts:
            print("Checking for tickets #{}".format(attempts))
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "lxml")
            events = [x for x in soup.find_all("div", class_="event") if
                      'class' in x.attrs and len(x.attrs['class']) == 1]
            print("Found {} events".format(len(events)))

            for event in events:
                event_name = None
                event_header = event.find("h2")
                if event_header:
                    event_name = event_header.text
                else:
                    print("Error! unable to get event header")

                if "אזלו" not in event_name:
                    print("Tickets available for {}".format(event_name))
                    if event_name_part is None or event_name_part in event_name:
                        event_data = Event(name=event_name, event_time=get_time(event), url=url)
                        sold_out = False
                        bot.send_message(chat_id=TELEGRAM_CHAT_ID,
                                         text="Available Tickets to \n{}".format(str(event_data)))
                        print("Event '{}' found".format(event_data.name))

            if sold_out:
                print("Waiting for 10 seconds")
                attempts = attempts + 1
                time.sleep(10)
        if not sold_out:
            time.sleep(30)
    except Exception as ex:
        print("Error! {}".format(str(ex)))
        time.sleep(5)
        raise ex
    return sold_out


# has_tickets("יואב")
has_tickets()
