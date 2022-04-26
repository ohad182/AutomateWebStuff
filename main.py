import requests
import time
from bs4 import BeautifulSoup, Tag


def has_tickets(event_name_part):
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
                    if event_name_part in event_name:
                        sold_out = False
                        print("Event '{}' found".format(event_name_part))
                        break

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


has_tickets("יואב")
